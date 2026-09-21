"""Demo shell. Standard library only: python3 skeleton/app.py

One page per scenario: run the pipeline, show what it suggests, what it
withholds, what it cannot answer, and what it refuses outright. A human
confirms every row before anything counts.
"""
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

from skeleton.core import live, registry
from skeleton.core.model import CANNED, StubModel
from skeleton.core.pipeline import run
from skeleton.core.schema import AggregationError
from skeleton.directions import d2_triage, d3_evidence, d6_outcomes, d7_credentials, d7_match
from skeleton.directions.d7_credentials import RedLineError, UnsupportedLanguageError

DIRECTIONS = {"d2": d2_triage, "d3": d3_evidence,
              "d6": d6_outcomes, "d7": d7_credentials}

REFUSALS = (AggregationError, RedLineError, UnsupportedLanguageError)
SCENARIOS = json.loads(
    (Path(__file__).resolve().parent / "demo_data" / "payloads.json").read_text(encoding="utf-8")
)
INTAKE_PAGE = Path(__file__).resolve().parent / "web" / "intake.html"

# A request past these is refused before it is read: a few minutes of webm
# speech is well under 25 MB, and no JSON the page sends comes near 1 MB.
MAX_AUDIO_BYTES = 25 * 1024 * 1024
MAX_JSON_BYTES = 1024 * 1024


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
    back = '<p><a href="/">&larr; back</a></p>'
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


def extract(payload):
    """Run the pipeline and return JSON-safe data. Refusals come back as data."""
    occupation_key = payload.get("occupation")
    try:
        result = run(d7_credentials, payload, model_for_occupation(occupation_key))
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
        "metric_name": result.metric_name,
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


def transcribe(audio, language):
    """Refused before ElevenLabs is called: audio in a language we cannot
    verify is never sent anywhere, and never transcribed as English."""
    if language not in d7_credentials.SUPPORTED_LANGUAGES:
        return {"refused": f"{language}: not supported. This demo runs in "
                           f"{', '.join(d7_credentials.SUPPORTED_LANGUAGES)}. "
                           "We will not fake a language we cannot verify."}
    return live.transcribe(audio, language)


def match(payload):
    """Jobs, gap courses and a draft resume tailored to each job.

    Without a transcript the resume's experience lines are empty; units and
    qualifications are still listed. Lines without an English gloss are left
    out because the resume is written in English. "resume" stays the best-fit
    job's draft so callers written before "resumes" existed keep working.
    """
    evidenced = payload.get("evidenced_units", [])
    if not isinstance(evidenced, list) or not all(isinstance(u, dict) for u in evidenced):
        raise BadRequest("evidenced_units must be a list of objects")
    transcript = [line for line in payload.get("transcript") or []
                  if isinstance(line, dict) and "t" in line and "en" in line]
    jobs = d7_match.match_jobs(payload.get("occupation"), evidenced)
    resumes = {}
    for job in jobs:
        sections = d7_match.resume_sections(job, evidenced, transcript)
        resumes[job["id"]] = {"job_id": job["id"], "text": d7_match.resume_text(sections),
                              "sections": sections}
    resume = resumes[jobs[0]["id"]] if jobs else None
    return {"jobs": jobs, "courses": d7_match.courses_for(jobs),
            "resume": resume, "resumes": resumes}


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
        if parsed.path == "/intake":
            return self._send(200, "text/html; charset=utf-8", INTAKE_PAGE.read_bytes())
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
            elif parsed.path == "/api/extract":
                body = extract(self._read_json())
            elif parsed.path == "/api/match":
                body = match(self._read_json())
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

    def _read_json(self):
        try:
            payload = json.loads(self._read(MAX_JSON_BYTES))
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
        print("http://127.0.0.1:8000  (intake page: http://127.0.0.1:8000/intake)")
        ThreadingHTTPServer(("127.0.0.1", 8000), Handler).serve_forever()
