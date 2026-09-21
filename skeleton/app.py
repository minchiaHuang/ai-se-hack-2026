"""Demo shell. Standard library only: python3 skeleton/app.py

One page per scenario: run the pipeline, show what it suggests, what it
withholds, what it cannot answer, and what it refuses outright. A human
confirms every row before anything counts.
"""
import base64
import html
import json
import os
import sys
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

# Run by path (python3 skeleton/app.py) and sys.path holds skeleton/, not the
# repo root, so the package imports below fail. Put the root back.
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from skeleton.core import interview, live, pdf_text, registry
from skeleton.core.model import CANNED, StubModel
from skeleton.core.pipeline import run
from skeleton.core.schema import AggregationError
from skeleton.directions import d2_triage, d3_evidence, d6_outcomes, d7_credentials, d7_match
from skeleton.directions import d7_sections
from skeleton.directions.d7_credentials import RedLineError, UnsupportedLanguageError

DIRECTIONS = {"d2": d2_triage, "d3": d3_evidence,
              "d6": d6_outcomes, "d7": d7_credentials}

REFUSALS = (AggregationError, RedLineError, UnsupportedLanguageError)
SCENARIOS = json.loads(
    (Path(__file__).resolve().parent / "demo_data" / "payloads.json").read_text(encoding="utf-8")
)
WEB = Path(__file__).resolve().parent / "web"
INTAKE_PAGE = WEB / "intake.html"
# The board the intake hands over to, carrying the pack in sessionStorage.
JOBS_PAGE = WEB / "jobs.html"
# Where the caseworker edits the resume drafted from the interview.
REVIEW_PAGE = WEB / "review.html"
# The spoken interview that hands its answers to /review.
INTERVIEW_PAGE = WEB / "interview.html"
# The other way into /review: a resume the person already has, translated.
UPLOAD_PAGE = WEB / "upload.html"
# The product's entry: the homepage, the client's details, then the choice
# between the spoken interview and an uploaded resume.
HOME_PAGE = WEB / "home.html"
START_PAGE = WEB / "start.html"
PATH_PAGE = WEB / "path.html"
LOGO = WEB / "logo.svg"
# The Figma resume template, drawn the same way on /review and /jobs.
RESUME_CSS = WEB / "resume-template.css"
RESUME_JS = WEB / "resume-template.js"

# A request past these is refused before it is read: a few minutes of webm
# speech is well under 25 MB, and no JSON the page sends comes near 1 MB.
MAX_AUDIO_BYTES = 25 * 1024 * 1024
MAX_JSON_BYTES = 1024 * 1024
# A resume is decoded only in memory. The JSON envelope is larger because the
# browser sends its local PDF as base64, so both limits are explicit.
MAX_PDF_BYTES = 2 * 1024 * 1024
MAX_PDF_JSON_BYTES = 3 * 1024 * 1024


class BadRequest(Exception):
    """Answered as HTTP 400 with this message and nothing else."""


def direction_for(scenario_key):
    return DIRECTIONS[scenario_key.split("_")[0]]


def model_for(scenario_key):
    """Canned output lives next to the scenario, so a scenario can show a
    different model response for the same direction."""
    direction = direction_for(scenario_key)
    path = CANNED / f"{scenario_key}.json"
    if not path.exists():
        path = CANNED / f"{direction.KEY}.json"
    canned = json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
    return StubModel({direction.KEY: canned})


def render_index():
    rows = "".join(
        f'<li><a href="/run?s={key}">{html.escape(payload["label"])}</a>'
        f' <span class="k">{html.escape(direction_for(key).NAME)}</span></li>'
        for key, payload in SCENARIOS.items()
    )
    return f"""<h1>Direction skeleton</h1>
<p class="note">Stub model, no network. Every scenario below runs offline.</p>
<ul class="scenarios">{rows}</ul>"""


def render_result(scenario_key):
    direction = direction_for(scenario_key)
    payload = SCENARIOS[scenario_key]
    back = '<p><a href="/scenarios">&larr; back</a></p>'
    head = f'<h1>{html.escape(direction.NAME)}</h1><p class="note">{html.escape(payload["label"])}</p>'

    try:
        result = run(direction, payload, model_for(scenario_key))
    except REFUSALS as refused:
        return (head + '<div class="refused"><strong>Refused</strong><p>'
                + html.escape(str(refused)) + "</p></div>" + back)

    parts = [head]
    if result.suggestions:
        parts.append("<h2>Suggested &mdash; confirm each</h2><table>")
        for s in result.suggestions:
            sources = "; ".join(f"{x.label}: {x.locator}" for x in s.sources)
            parts.append(
                f"<tr><td><input type=checkbox></td><td><b>{html.escape(s.field)}</b></td>"
                f"<td>{html.escape(str(s.displayed_value()))}</td>"
                f"<td>{s.confidence:.2f}</td>"
                f"<td class=src>{html.escape(s.reason)}<br><i>{html.escape(sources)}</i></td></tr>"
            )
        parts.append("</table>")
    if result.needs_human:
        parts.append("<h2>Not confident enough &mdash; a person decides</h2><ul>")
        for s in result.needs_human:
            parts.append(
                f"<li><b>{html.escape(s.field)}</b>: value withheld "
                f"(confidence {s.confidence:.2f}) &mdash; {html.escape(s.reason)}</li>"
            )
        parts.append("</ul>")
    if result.gaps:
        parts.append("<h2>No evidence &mdash; left blank on purpose</h2><ul>"
                     + "".join(f"<li>{html.escape(g)}</li>" for g in result.gaps) + "</ul>")
    value = "not supplied" if result.metric_value is None else result.metric_value
    parts.append(f'<div class="metric">{html.escape(result.metric_name)}: <b>{html.escape(str(value))}</b></div>')
    parts.append(back)
    return "".join(parts)


def resume_lines(payload):
    """The resume the page sends: numbered lines, checked before anything reads them."""
    lines = payload.get("resume")
    if not isinstance(lines, list) or not all(
            isinstance(line, dict) and type(line.get("line")) is int
            and isinstance(line.get("text"), str) for line in lines):
        raise BadRequest("resume must be a list of {line: integer, text: string} objects")
    return lines


def read_pdf_resume(payload):
    """Turn an opted-in PDF text layer into the numbered lines the model cites.

    The raw file never reaches disk. Guarding consent and language before base64
    decoding means an unconsented or unsupported resume is not read at all.
    """
    guard_payload = {"source": d7_credentials.RESUME, "consent": payload.get("consent"),
                     "language": payload.get("language")}
    try:
        d7_credentials.guard(guard_payload)
    except REFUSALS as refused:
        return {"refused": str(refused)}
    encoded = payload.get("pdf_base64")
    if not isinstance(encoded, str):
        raise BadRequest("pdf_base64 must be a base64 string")
    max_encoded = ((MAX_PDF_BYTES + 2) // 3) * 4
    if len(encoded) > max_encoded:
        return {"refused": "This PDF is larger than 2 MB, so it was not read."}
    try:
        data = base64.b64decode(encoded, validate=True)
    except (ValueError, UnicodeEncodeError):
        raise BadRequest("pdf_base64 is not valid base64") from None
    if len(data) > MAX_PDF_BYTES:
        return {"refused": "This PDF is larger than 2 MB, so it was not read."}
    try:
        lines = pdf_text.extract_lines(data)
    except pdf_text.PdfTextError as unreadable:
        return {"refused": str(unreadable)}
    return {"lines": [{"line": index, "text": text}
                      for index, text in enumerate(lines, 1)]}


def extract(payload):
    """Run the pipeline and return JSON-safe data. Refusals come back as data."""
    occupation_key = payload.get("occupation")
    from_resume = payload.get("source") == d7_credentials.RESUME
    if from_resume:
        model = model_for_resume(occupation_key, resume_lines(payload))
    else:
        model = model_for_occupation(occupation_key)
    try:
        result = run(d7_credentials, payload, model)
    except REFUSALS as refused:
        return {"refused": str(refused)}
    return {
        "suggestions": [
            {"field": s.field, "value": s.displayed_value(), "reason": s.reason,
             "confidence": s.confidence,
             "sources": [[x.label, x.locator] for x in s.sources]}
            for s in result.suggestions
        ],
        "needs_human": [
            {"field": s.field, "reason": s.reason, "confidence": s.confidence,
             "sources": [[x.label, x.locator] for x in s.sources]}
            for s in result.needs_human
        ],
        "gaps": list(result.gaps),
        # The gate is reference data about the occupation, looked up here and
        # never asked of the model, so it cannot render as a guess or a blank.
        "gate": registry.occupation(occupation_key)["gate"],
        # NEEDS DECISION: not in the locked /api/extract contract; added so the
        # page can show "superseded MEM31922" beside the qualification. Offline
        # on purpose: reachable stays False and never claims currency.
        "qualification_source": registry.source_check(occupation_key),
        # The pipeline names the transcript metric; a resume's items cite lines
        # of the resume, and the label must not claim otherwise.
        "metric_name": d7_credentials.RESUME_METRIC if from_resume else result.metric_name,
        "metric_value": result.metric_value,
    }


def model_for_occupation(occupation_key):
    """Pick the stub's canned answer by occupation, so a welder is not handed
    the cook's evidence pack. An occupation with no canned file gets nothing,
    which the pipeline reports as gaps rather than borrowing another trade's
    evidence. With ANTHROPIC_API_KEY set the live model answers, and this
    stub is what it falls back to when the call fails."""
    if occupation_key == "cookery":
        stub = model_for("d7")
    elif (CANNED / f"d7_{occupation_key}.json").exists():
        stub = model_for(f"d7_{occupation_key}")
    else:
        stub = StubModel({d7_credentials.KEY: []})
    if os.environ.get("ANTHROPIC_API_KEY"):
        return live.LiveModel(fallback=stub)
    return stub


def model_for_resume(occupation_key, lines):
    """Offline, the canned answer is given only for the built-in sample resume,
    whose lines it cites. Any other resume gets nothing, reported as gaps: the
    sample's reasons pinned to someone else's line numbers would be evidence
    in name only. NEEDS DECISION: the interview's offline stub answers any
    transcript; this path is stricter on purpose."""
    canned = json.loads((CANNED / "d7_resume.json").read_text(encoding="utf-8"))
    is_sample = [line["text"] for line in lines] == canned["resume"]
    answer = canned["answer"] if occupation_key == "cookery" and is_sample else []
    stub = StubModel({d7_credentials.KEY: answer})
    if os.environ.get("ANTHROPIC_API_KEY"):
        return live.LiveModel(fallback=stub)
    return stub


def transcribe(audio, language):
    """Refused before ElevenLabs is called: audio in a language we cannot
    verify is never sent anywhere, and never transcribed as English."""
    if language not in d7_credentials.SUPPORTED_LANGUAGES:
        return {"refused": f"{language}: not supported. This demo runs in "
                           f"{', '.join(d7_credentials.SUPPORTED_LANGUAGES)}. "
                           "We will not fake a language we cannot verify."}
    return live.transcribe(audio, language)


def _interview_text(payload, language_field):
    """The text and language of a translate or speak request, checked the way
    transcribe checks its language: nothing unsupported is sent anywhere."""
    text, language = payload.get("text"), payload.get(language_field)
    if not isinstance(text, str) or not text.strip():
        raise BadRequest("text must be a non-empty string")
    if language not in d7_credentials.SUPPORTED_LANGUAGES:
        return None, {"refused": f"{language}: not supported. This demo runs in "
                                 f"{', '.join(d7_credentials.SUPPORTED_LANGUAGES)}."}
    return text.strip(), None


def translate(payload):
    text, refused = _interview_text(payload, "source")
    return refused or interview.translate(text, payload["source"])


def speak(payload):
    text, refused = _interview_text(payload, "language")
    if refused:
        return refused
    if len(text) > interview.MAX_SPEAK_CHARS:
        raise BadRequest(f"text must be at most {interview.MAX_SPEAK_CHARS} characters")
    return interview.speak(text)


def match(payload):
    """Real job ads, gap courses and a draft resume tailored to each job.

    Without a transcript the resume's experience lines are empty; units and
    qualifications are still listed. Lines without an English gloss are left
    out because the resume is written in English. "resume" stays the best-fit
    job's draft so callers written before "resumes" existed keep working.

    With "source": "resume" the lines come from the resume the person brought
    ("resume": [{line, text, en}]) and the drafts cite resume lines.

    "all_jobs" lists every job, the occupation's first, for the page's board.
    "jobs_source" names the Adzuna snapshot the board was read from.
    """
    evidenced = payload.get("evidenced_units", [])
    if not isinstance(evidenced, list) or not all(isinstance(u, dict) for u in evidenced):
        raise BadRequest("evidenced_units must be a list of objects")
    source = "interview"
    if payload.get("source") == d7_credentials.RESUME:
        source = "resume"
        lines = [line for line in resume_lines(payload) if isinstance(line.get("en"), str)]
    else:
        lines = [line for line in payload.get("transcript") or []
                 if isinstance(line, dict) and "t" in line and "en" in line]
    jobs = d7_match.match_jobs(payload.get("occupation"), evidenced)
    resumes = {}
    for job in jobs:
        sections = d7_match.resume_sections(job, evidenced, lines, source)
        resumes[job["id"]] = {"job_id": job["id"], "text": d7_match.resume_text(sections),
                              "sections": sections}
    resume = resumes[jobs[0]["id"]] if jobs else None
    # "all_jobs" is the whole board, other occupations included; "all_courses"
    # is the gap training for every one of them. "resumes" stays keyed to the
    # occupation's jobs: a draft for another occupation's job would cite none
    # of the units that job asks for.
    board = d7_match.all_jobs(payload.get("occupation"), evidenced)
    # Where the ads came from and when. Adzuna's licence asks for the mark, and
    # a snapshot has to say how old it is, so the page is given both.
    return {"jobs": jobs, "courses": d7_match.courses_for(jobs),
            "resume": resume, "resumes": resumes,
            "all_jobs": board, "all_courses": d7_match.courses_for(board),
            "jobs_source": d7_match.snapshot_meta()}


def resume_sections(payload):
    try:
        return d7_sections.draft(payload)
    except ValueError as bad:
        raise BadRequest(str(bad)) from None


def resume_polish(payload):
    try:
        return d7_sections.polish(payload)
    except ValueError as bad:
        raise BadRequest(str(bad)) from None


PAGE = """<!doctype html><meta charset=utf-8><title>Direction skeleton</title>
<style>
body{{font:15px/1.5 system-ui,sans-serif;max-width:760px;margin:2rem auto;padding:0 1rem}}
h1{{font-size:1.3rem}} h2{{font-size:1rem;margin-top:1.5rem}}
.note{{color:#666}} .k{{color:#888;font-size:.85em}}
table{{border-collapse:collapse;width:100%}} td{{border-top:1px solid #ddd;padding:.4rem;vertical-align:top}}
.src{{color:#555;font-size:.85em}}
.metric{{margin-top:1.5rem;padding:.6rem;background:#f4f4f4}}
.refused{{margin-top:1rem;padding:.8rem;border-left:4px solid #b00;background:#fff4f4}}
.scenarios li{{margin:.3rem 0}}
</style>{body}"""


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        # The root opens the product; the scenario list is a developer page at
        # /scenarios. The pages read ?mock=1 themselves, so no redirect is needed.
        if parsed.path == "/":
            return self._send(200, "text/html; charset=utf-8", HOME_PAGE.read_bytes())
        if parsed.path == "/start":
            return self._send(200, "text/html; charset=utf-8", START_PAGE.read_bytes())
        if parsed.path == "/start/path":
            return self._send(200, "text/html; charset=utf-8", PATH_PAGE.read_bytes())
        if parsed.path == "/logo.svg":
            return self._send(200, "image/svg+xml", LOGO.read_bytes())
        if parsed.path == "/resume-template.css":
            return self._send(200, "text/css; charset=utf-8", RESUME_CSS.read_bytes())
        if parsed.path == "/resume-template.js":
            return self._send(200, "text/javascript; charset=utf-8", RESUME_JS.read_bytes())
        if parsed.path == "/intake":
            return self._send(200, "text/html; charset=utf-8", INTAKE_PAGE.read_bytes())
        if parsed.path == "/jobs":
            return self._send(200, "text/html; charset=utf-8", JOBS_PAGE.read_bytes())
        if parsed.path == "/review":
            return self._send(200, "text/html; charset=utf-8", REVIEW_PAGE.read_bytes())
        if parsed.path == "/interview":
            return self._send(200, "text/html; charset=utf-8", INTERVIEW_PAGE.read_bytes())
        if parsed.path == "/upload":
            return self._send(200, "text/html; charset=utf-8", UPLOAD_PAGE.read_bytes())
        if parsed.path == "/api/interview/questions":
            return self._json(200, interview.questions())
        scenario = parse_qs(parsed.query).get("s", [None])[0]
        if parsed.path == "/run" and scenario in SCENARIOS:
            body = render_result(scenario)
        else:
            body = render_index()
        self._send(200, "text/html; charset=utf-8", PAGE.format(body=body).encode("utf-8"))

    def do_POST(self):
        parsed = urlparse(self.path)
        # Every refusal is a 200 {"refused": ...}: the page shows its refusal
        # panel only on a 200, and a non-200 reads as a generic error.
        try:
            if parsed.path == "/api/transcribe":
                language = parse_qs(parsed.query).get("language", [""])[0]
                body = transcribe(self._read(MAX_AUDIO_BYTES), language)
            elif parsed.path == "/api/resume-text":
                body = read_pdf_resume(self._read_json(MAX_PDF_JSON_BYTES))
            elif parsed.path == "/api/extract":
                body = extract(self._read_json())
            elif parsed.path == "/api/match":
                body = match(self._read_json())
            elif parsed.path == "/api/resume-sections":
                body = resume_sections(self._read_json())
            elif parsed.path == "/api/resume-polish":
                body = resume_polish(self._read_json())
            elif parsed.path == "/api/translate":
                body = translate(self._read_json())
            elif parsed.path == "/api/speak":
                body = speak(self._read_json())
                if isinstance(body, bytes):
                    return self._send(200, "audio/mpeg", body)
            else:
                return self._json(404, {"error": f"{parsed.path}: no such endpoint"})
        except BadRequest as bad:
            return self._json(400, {"error": str(bad)})
        except KeyError as unknown:
            # An unknown occupation, or a missing field the pipeline needs.
            return self._json(400, {"error": f"unknown or missing: {unknown.args[0]}"})
        except Exception:
            # The traceback stays in the server's terminal, never in the response.
            traceback.print_exc()
            return self._json(500, {"error": "internal error"})
        self._json(200, body)

    def _read(self, limit):
        try:
            length = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            length = -1
        if not 0 <= length <= limit:
            # The body is left unread, so this connection cannot be reused.
            self.close_connection = True
            raise BadRequest(f"body must be between 0 and {limit} bytes")
        return self.rfile.read(length)

    def _read_json(self, limit=MAX_JSON_BYTES):
        try:
            payload = json.loads(self._read(limit))
        except (UnicodeDecodeError, json.JSONDecodeError):
            raise BadRequest("body is not valid JSON") from None
        if not isinstance(payload, dict):
            raise BadRequest("body must be a JSON object")
        return payload

    def _json(self, status, body):
        self._send(status, "application/json", json.dumps(body).encode("utf-8"))

    def _send(self, status, content_type, encoded):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def log_message(self, *args):
        pass


def check():
    """Offline smoke check: render every scenario, print nothing on success."""
    for key in SCENARIOS:
        render_result(key)


if __name__ == "__main__":
    if "--check" in sys.argv:
        check()
    else:
        print("http://127.0.0.1:8000  (scenarios: http://127.0.0.1:8000/scenarios)")
        ThreadingHTTPServer(("127.0.0.1", 8000), Handler).serve_forever()
