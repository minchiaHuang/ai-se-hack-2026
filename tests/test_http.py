"""One real round trip, so the handler wiring is proven and not just the rendering.

No test here may touch the network: both API keys are cleared for the whole
class, so transcription and the model run on their offline paths.
"""
import base64
import json
import re
import os
import threading
import unittest
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer
from unittest import mock
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from pathlib import Path

from skeleton import app
from skeleton.app import Handler

COOK_TRANSCRIPT = [
    {"t": "00:12", "text": "我在营地厨房做了三年饭，每天给两百个人做饭。",
     "en": "I cooked in the camp kitchen for three years, for two hundred people a day."},
    {"t": "02:41", "text": "生肉和煮好的食物要分开放。",
     "en": "Raw meat and cooked food had to be kept apart."},
]

# The Mandarin lines "Use demo transcript" sends, copied from intake.html.
DEMO_TRANSCRIPT = [
    {"t": "00:12", "text": "我在營區的廚房做了三年，每天煮兩百個人的飯。",
     "en": "I worked in the camp kitchen for three years, cooking for two hundred people every day."},
    {"t": "00:47", "text": "早上四點就開始準備，主要做米飯、燉菜和湯。",
     "en": "We started preparing at four in the morning, mostly rice, stews and soup."},
    {"t": "01:30", "text": "我負責排班，也教新來的人怎麼切菜。",
     "en": "I did the roster and taught new people how to cut vegetables."},
    {"t": "02:41", "text": "生肉和煮好的食物要分開放，冰箱的溫度我每天都記在本子上。",
     "en": "Raw meat and cooked food had to be kept apart, and I wrote the fridge temperature in a notebook every day."},
    {"t": "03:20", "text": "我沒有證書，那裡沒有人發這種東西。",
     "en": "I have no certificate; nobody there issued one."},
]


SAMPLE_RESUME = json.loads(
    (app.CANNED / "d7_resume.json").read_text(encoding="utf-8"))["resume"]
# What the page sends for the sample: numbered lines, English as its own gloss.
SAMPLE_LINES = [{"line": i + 1, "text": text, "en": text} for i, text in enumerate(SAMPLE_RESUME)]
PDF_FIXTURES = Path(__file__).parent / "fixtures"


def resume(**over):
    body = {"source": "resume", "occupation": "cookery", "language": "en", "consent": True,
            "resume": SAMPLE_LINES}
    body.update(over)
    return body


def cook(**over):
    body = {"occupation": "cookery", "language": "zh", "consent": True,
            "transcript": COOK_TRANSCRIPT}
    body.update(over)
    return body


def pdf_resume(name="resume_text.pdf", **over):
    body = {"source": "resume", "language": "en", "consent": True,
            "filename": name,
            "pdf_base64": base64.b64encode((PDF_FIXTURES / name).read_bytes()).decode("ascii")}
    body.update(over)
    return body


class Server(unittest.TestCase):
    """One server per test class, on an ephemeral port, with no API keys."""

    @classmethod
    def setUpClass(cls):
        cls.env = mock.patch.dict(os.environ)
        cls.env.start()
        os.environ.pop("ELEVENLABS_API_KEY", None)
        os.environ.pop("ANTHROPIC_API_KEY", None)
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=5)
        cls.env.stop()

    def get(self, path):
        with urlopen(f"http://127.0.0.1:{self.port}{path}", timeout=5) as response:
            return response.status, response.read().decode("utf-8")

    def post(self, path, data, content_type="application/json"):
        """Returns (status, raw text); a 4xx/5xx is returned, not raised."""
        if not isinstance(data, bytes):
            data = json.dumps(data).encode("utf-8")
        request = Request(f"http://127.0.0.1:{self.port}{path}", data=data, method="POST",
                          headers={"Content-Type": content_type})
        try:
            with urlopen(request, timeout=5) as response:
                return response.status, response.read().decode("utf-8")
        except HTTPError as error:
            return error.code, error.read().decode("utf-8")


class HttpRoundTrip(Server):
    def raw_get(self, path):
        """(status, headers) without following a redirect."""
        conn = HTTPConnection("127.0.0.1", self.port, timeout=5)
        try:
            conn.request("GET", path)
            response = conn.getresponse()
            response.read()
            return response.status, response.headers
        finally:
            conn.close()

    def test_the_root_serves_the_homepage(self):
        status, headers = self.raw_get("/")
        self.assertEqual(status, 200)
        self.assertEqual(headers["Content-Type"], "text/html; charset=utf-8")
        _, body = self.get("/")
        self.assertIn("Work experience should not be lost in translation.", body)
        self.assertIn('href="/start"', body)

    def test_the_homepage_offers_the_demo_in_mock_mode(self):
        # The demo button carries ?mock=1 itself, so it must not be rewritten
        # by the data-route script, which would drop mock mode on a live page.
        _, body = self.get("/")
        self.assertIn(
            '<a class="btn ghost-light" href="/start?mock=1&amp;quiet=1">Live demo</a>', body)

    def test_every_homepage_photo_serves_as_jpeg(self):
        _, body = self.get("/")
        photos = sorted(set(re.findall(r"/img/([\w-]+\.jpg)", body)))
        self.assertEqual(len(photos), 9)
        for name in photos:
            with self.subTest(photo=name):
                status, headers = self.raw_get("/img/" + name)
                self.assertEqual(status, 200)
                self.assertEqual(headers["Content-Type"], "image/jpeg")

    def test_the_photo_route_serves_only_the_photo_folder(self):
        # Anything not in the folder falls through to the developer index page.
        _, headers = self.raw_get("/img/../app.py")
        self.assertEqual(headers["Content-Type"], "text/html; charset=utf-8")
        _, body = self.get("/img/../app.py")
        self.assertNotIn("class Handler", body)

    def test_the_homepage_keeps_mock_mode_on_its_own(self):
        # No redirect any more: the page carries ?mock=1 onto its links itself.
        status, body = self.get("/?mock=1")
        self.assertEqual(status, 200)
        self.assertIn('carried.set("mock", "1")', body)

    def test_the_homepage_quotes_no_caseworker(self):
        """Figma's "Impact stories" quotes a caseworker no one interviewed;
        AI_CONTEXT.md forbids presenting unvalidated testimony."""
        _, body = self.get("/")
        self.assertNotIn("Impact stories", body)
        self.assertNotIn("I didn’t have to write anything", body)

    def test_the_employer_card_leads_nowhere(self):
        # There is no employer side, so its button is disabled rather than a link.
        _, body = self.get("/")
        self.assertIn("<button class=\"button\" type=\"button\" disabled>Coming soon</button>", body)

    def test_the_personal_information_page_serves(self):
        status, body = self.get("/start")
        self.assertEqual(status, 200)
        self.assertIn("Personal Information", body)
        self.assertIn('"d7.person"', body)
        self.assertIn("/start/path", body)

    def test_the_personal_information_page_offers_only_supported_languages(self):
        _, body = self.get("/start")
        offered = [v for v in body.split('<option value="')[1:]]
        self.assertEqual([v.split('"')[0] for v in offered],
                         ["", *app.d7_credentials.SUPPORTED_LANGUAGES])

    def test_the_mock_person_is_the_interviews_cook(self):
        _, body = self.get("/start")
        person = json.loads(body.split("const MOCK_PERSON = ")[1].split(";\n")[0])
        self.assertEqual(person, {"name": "Li Wei", "phone": "0400 000 000",
                                  "email": "liwei.cook@example.com", "language": "zh"})
        # The interview does not ask for either any more: /review takes them from
        # what was typed here, so the mock resume is where they have to show up.
        interview = app.INTERVIEW_PAGE.read_text(encoding="utf-8")
        self.assertNotIn(person["phone"], interview)
        self.assertNotIn(person["email"], interview)
        review = app.REVIEW_PAGE.read_text(encoding="utf-8")
        self.assertIn(person["phone"], review)
        self.assertIn(person["email"], review)

    def test_the_choose_path_page_serves(self):
        status, body = self.get("/start/path")
        self.assertEqual(status, 200)
        self.assertIn("How would you like to build this Resume?", body)
        for href in ('href="/interview"', 'href="/upload"', 'href="/start"'):
            with self.subTest(href=href):
                self.assertIn(href, body)

    def test_quiet_hides_only_the_mock_banner_on_the_entry_pages(self):
        # &quiet=1 is for the demo video: the banner goes, mock mode stays.
        for path in ("/", "/start", "/start/path"):
            with self.subTest(path=path):
                _, body = self.get(path)
                self.assertIn('id="mock-banner"', body)
                self.assertIn('.hidden = !MOCK || params.get("quiet") === "1"', body)

    def test_the_logo_serves_as_svg(self):
        status, headers = self.raw_get("/logo.svg")
        self.assertEqual(status, 200)
        self.assertEqual(headers["Content-Type"], "image/svg+xml")
        with urlopen(f"http://127.0.0.1:{self.port}/logo.svg", timeout=5) as response:
            self.assertTrue(response.read().startswith(b"<svg"))

    def test_the_scenario_list_serves_at_scenarios(self):
        status, body = self.get("/scenarios")
        self.assertEqual(status, 200)
        self.assertIn("Direction skeleton", body)
        self.assertIn("/run?s=d2", body)

    def test_a_scenario_links_back_to_the_list(self):
        status, body = self.get("/run?s=d2")
        self.assertEqual(status, 200)
        self.assertIn('href="/scenarios"', body)

    def test_a_scenario_serves(self):
        status, body = self.get("/run?s=d2")
        self.assertEqual(status, 200)
        self.assertIn("Intake triage", body)

    def test_the_refusal_serves(self):
        status, body = self.get("/run?s=d6_small_group")
        self.assertEqual(status, 200)
        self.assertIn("Refused", body)

    def test_an_unknown_scenario_falls_back_to_the_index(self):
        status, body = self.get("/run?s=nope")
        self.assertEqual(status, 200)
        self.assertIn("Direction skeleton", body)


    def test_the_intake_page_serves(self):
        with urlopen(f"http://127.0.0.1:{self.port}/intake", timeout=5) as response:
            self.assertEqual(response.status, 200)
            self.assertEqual(response.headers["Content-Type"], "text/html; charset=utf-8")
            self.assertIn("/api/extract", response.read().decode("utf-8"))

    def test_the_jobs_page_serves(self):
        status, body = self.get("/jobs")
        self.assertEqual(status, 200)
        # It reads the pack the intake left in sessionStorage; it calls no endpoint.
        self.assertIn("d7-session", body)
        self.assertNotIn("/api/extract", body)

    def test_the_jobs_page_grades_no_one_and_borrows_no_branding(self):
        """The ring is unit coverage of the job. Nothing on the page grades the
        match or the person, and nothing carries another product's wording.
        A plain "Apply" button is allowed since the one-click apply flow; an
        automated apply ("Autofill", "Auto apply") is still another product's."""
        _, body = self.get("/jobs")
        for word in ("GOOD MATCH", "STRONG MATCH", "Jobright", "jobright", "Orion",
                     "Turbo", "Autofill", "Auto apply", "Auto-apply", "applicants"):
            with self.subTest(word=word):
                self.assertNotIn(word, body)

    def test_applying_on_the_jobs_page_sends_nothing(self):
        """Save and apply are recorded in this tab only. The page opens no
        connection of any kind, so a confirmed application cannot leave it,
        and the panel says who sends it and that this is a demo."""
        _, body = self.get("/jobs")
        self.assertIn("The caseworker sends this with the jobseeker's agreement.", body)
        self.assertIn("Demo: recorded in this browser tab only", body)
        self.assertIn('const APPLY_KEY = "d7-apply"', body)
        for call in ("fetch(", "XMLHttpRequest", "sendBeacon", "WebSocket", "mailto:", "/api/",
                     "window.confirm", "alert("):
            with self.subTest(call=call):
                self.assertNotIn(call, body)

    def test_the_jobs_page_carries_the_adzuna_mark_at_the_size_the_licence_asks(self):
        """Adzuna's terms: the mark links to the ad and is drawn at no less
        than 116x23 px. Both numbers are pinned here so a later tidy-up of the
        stylesheet cannot quietly shrink them."""
        _, body = self.get("/jobs")
        self.assertIn("Jobs by Adzuna", body)
        self.assertIn("min-width: 116px", body)
        self.assertIn("min-height: 23px", body)
        self.assertIn('rel: "noopener"', body)
        self.assertIn('target: "_blank"', body)

    def test_the_jobs_page_tells_the_two_empty_cases_apart(self):
        """An ad that named nothing and an ad that was never mapped read
        differently, and neither shows a percentage."""
        _, body = self.get("/jobs")
        self.assertIn("Ad too short to name units", body)
        self.assertIn("Ad not mapped to units", body)
        self.assertIn("The ad says it needs this", body)
        self.assertIn("Jobs with this title normally need this", body)


class IntakeApi(Server):
    """The routes the intake page calls, against the real handler."""

    def post_json(self, path, data, content_type="application/json"):
        status, text = self.post(path, data, content_type)
        return status, json.loads(text)

    def test_pdf_resume_text_is_numbered_before_the_evidence_pipeline(self):
        status, body = self.post_json("/api/resume-text", pdf_resume())
        self.assertEqual(status, 200)
        self.assertEqual(body["lines"], [
            {"line": 1, "text": "Leah Example"},
            {"line": 2, "text": "Commercial cook"},
            {"line": 3, "text": "Food safety and kitchen work"},
        ])

    def test_pdf_resume_needs_consent_before_its_bytes_are_read(self):
        with mock.patch.object(app.pdf_text, "extract_lines") as extracted:
            status, body = self.post_json("/api/resume-text", pdf_resume(consent=False))
        self.assertEqual(status, 200)
        self.assertIn("consent", body["refused"])
        extracted.assert_not_called()

    def test_scanned_and_encrypted_pdfs_are_refused_as_non_evidence(self):
        for name, words in (("scanned.pdf", "scan or a photo"),
                            ("encrypted.pdf", "encrypted")):
            with self.subTest(name=name):
                status, body = self.post_json("/api/resume-text", pdf_resume(name))
                self.assertEqual(status, 200)
                self.assertIn(words, body["refused"])

    def test_pdf_upload_body_limit_is_checked_before_reading(self):
        connection = HTTPConnection("127.0.0.1", self.port, timeout=5)
        try:
            connection.putrequest("POST", "/api/resume-text")
            connection.putheader("Content-Type", "application/json")
            connection.putheader("Content-Length", str(app.MAX_PDF_JSON_BYTES + 1))
            connection.endheaders()
            response = connection.getresponse()
            self.assertEqual(response.status, 400)
            self.assertIn("error", json.loads(response.read()))
        finally:
            connection.close()

    def test_extract_golden_path(self):
        status, body = self.post_json("/api/extract", cook())
        self.assertEqual(status, 200)
        values = {s["field"]: s["value"] for s in body["suggestions"]}
        self.assertEqual(values["anzsco_code"], "351411 Cook")
        self.assertTrue(all(s["sources"] for s in body["suggestions"]))
        self.assertIn("Food Safety Supervisor", body["gate"]["text"])

    def test_extract_withholds_a_low_confidence_value(self):
        status, body = self.post_json("/api/extract", cook())
        self.assertEqual(status, 200)
        withheld = [s for s in body["needs_human"] if s["field"] == "qualification"]
        self.assertTrue(withheld)
        self.assertNotIn("value", withheld[0])

    def test_an_unsupported_language_is_a_200_refusal(self):
        status, body = self.post_json("/api/extract", cook(language="ti"))
        self.assertEqual(status, 200)
        self.assertIn("ti", body["refused"])

    def test_no_consent_is_a_200_refusal(self):
        status, body = self.post_json("/api/extract", cook(consent=False))
        self.assertEqual(status, 200)
        self.assertIn("consent", body["refused"])

    def test_transcribe_without_a_key_is_offline(self):
        status, body = self.post_json("/api/transcribe?language=zh", b"webm bytes", "audio/webm")
        self.assertEqual(status, 200)
        self.assertTrue(body["offline"])
        self.assertTrue(body["text"])

    def test_transcribe_refuses_an_unsupported_language_without_sending_audio(self):
        with mock.patch.object(app.live, "transcribe") as sent:
            status, body = self.post_json("/api/transcribe?language=ti", b"webm bytes", "audio/webm")
        self.assertEqual(status, 200)
        self.assertIn("ti", body["refused"])
        sent.assert_not_called()

    def test_match_returns_jobs_courses_and_a_resume_for_the_best_fit(self):
        units = [{"code": "SITXFSA005", "sources": [["transcript", "t=02:41"]]},
                 {"code": "SITXFSA006", "sources": [["transcript", "t=02:41"]]}]
        status, body = self.post_json("/api/match", {"occupation": "cookery",
                                                     "evidenced_units": units})
        self.assertEqual(status, 200)
        self.assertTrue(body["jobs"])
        self.assertTrue(body["courses"])
        self.assertEqual(body["resume"]["job_id"], body["jobs"][0]["id"])
        self.assertIn("SITXFSA005", body["resume"]["text"])

    def test_match_lists_every_job_with_other_occupations_at_zero(self):
        """The page's board: every ad in the snapshot, the occupation's first as
        in "jobs", the rest counted honestly at 0. Counts come from the file, so
        a refetched snapshot does not need this test rewritten."""
        units = [{"code": "SITXFSA005", "sources": [["transcript", "t=02:41"]]},
                 {"code": "SITXFSA006", "sources": [["transcript", "t=02:41"]]}]
        status, body = self.post_json("/api/match", {"occupation": "cookery",
                                                     "evidenced_units": units,
                                                     "transcript": DEMO_TRANSCRIPT})
        self.assertEqual(status, 200)
        board = body["all_jobs"]
        required = {j["id"]: len(j["required_units"] or ())
                    for j in app.d7_match.load_jobs()}
        self.assertEqual({j["id"] for j in board}, set(required))
        self.assertEqual([j["id"] for j in board[:len(body["jobs"])]],
                         [j["id"] for j in body["jobs"]])
        for job in board:
            with self.subTest(job=job["id"]):
                self.assertEqual(job["for_occupation"], job["occupation"] == "cookery")
                self.assertEqual(len(job["matched"]) + len(job["missing"]), required[job["id"]])
                # The posting date is read from the ad and never passed on.
                self.assertNotIn("created", job)
                if not job["for_occupation"] and job["units_status"] == "mapped":
                    self.assertEqual(job["fit"], f"0 of {required[job['id']]} required units evidenced")
        self.assertEqual({c["code"] for c in body["all_courses"]},
                         {u["code"] for j in board for u in j["missing"]})
        # Only what the server writes; a "%" inside an ad's own words is the
        # employer's shift loading, and quoting it verbatim is the point.
        self.assertNotIn("%", json.dumps([j["fit"] for j in board]))

    def test_match_says_which_snapshot_the_board_came_from(self):
        """Adzuna's mark and the snapshot date both need this."""
        status, body = self.post_json("/api/match", {"occupation": "cookery",
                                                     "evidenced_units": []})
        self.assertEqual(status, 200)
        self.assertEqual(body["jobs_source"]["source"], "Adzuna")
        self.assertEqual(body["jobs_source"]["attribution"], "Jobs by Adzuna")
        self.assertRegex(body["jobs_source"]["fetched_at"], r"^\d{4}-\d{2}-\d{2}T")

    def test_an_ad_with_no_units_is_listed_and_never_counted_as_zero_of_zero(self):
        """Both empty cases reach the page whole, with their own wording, and
        no division by zero on the way."""
        status, body = self.post_json("/api/match", {"occupation": "cookery",
                                                     "evidenced_units": []})
        self.assertEqual(status, 200)
        by_status = {}
        for job in body["all_jobs"]:
            by_status.setdefault(job["units_status"], []).append(job)
        self.assertTrue(by_status.get("mapped"))
        for job in by_status.get("none_named", []):
            with self.subTest(job=job["id"]):
                self.assertEqual(job["fit"], app.d7_match.NONE_NAMED_FIT)
                self.assertEqual((job["matched"], job["missing"]), ([], []))
        for job in by_status.get("not_mapped", []):
            with self.subTest(job=job["id"]):
                self.assertEqual(job["fit"], app.d7_match.NOT_MAPPED_FIT)
        for job in by_status.get("mapped", []):
            with self.subTest(job=job["id"]):
                self.assertRegex(job["fit"], r"^\d+ of [1-9]\d* required units evidenced$")

    def test_match_uses_a_transcript_when_one_is_sent(self):
        units = [{"code": "SITXFSA005", "sources": [["transcript", "t=02:41"]]}]
        status, body = self.post_json("/api/match", {"occupation": "cookery",
                                                     "evidenced_units": units,
                                                     "transcript": COOK_TRANSCRIPT})
        self.assertEqual(status, 200)
        self.assertIn("Raw meat and cooked food", body["resume"]["text"])

    def test_the_demo_transcript_gives_the_resume_experience_lines(self):
        """What the page does: extract, then match with the same transcript and
        the units the pack evidences. The experience lines are what a viewer reads."""
        status, pack = self.post_json("/api/extract", cook(transcript=DEMO_TRANSCRIPT))
        self.assertEqual(status, 200)
        units = [{"code": code, "sources": item["sources"]}
                 for item in pack["suggestions"] if item["field"] == "units_evidenced"
                 for code in item["value"].split("; ")]
        status, body = self.post_json("/api/match", {"occupation": "cookery",
                                                     "evidenced_units": units,
                                                     "transcript": DEMO_TRANSCRIPT})
        self.assertEqual(status, 200)
        self.assertRegex(body["resume"]["text"], r"(?m)^- .+ \[transcript \d\d:\d\d\]$")

    def test_match_returns_a_resume_tailored_to_every_job(self):
        units = [{"code": "SITXFSA005", "sources": [["transcript", "t=02:41"]]},
                 {"code": "SITHCCC027", "sources": [["transcript", "t=00:12"]]},
                 {"code": "SITHCCC029", "sources": [["transcript", "t=00:47"]]}]
        status, body = self.post_json("/api/match", {"occupation": "cookery",
                                                     "evidenced_units": units,
                                                     "transcript": DEMO_TRANSCRIPT})
        self.assertEqual(status, 200)
        self.assertEqual(set(body["resumes"]), {job["id"] for job in body["jobs"]})
        self.assertEqual(body["resume"], body["resumes"][body["jobs"][0]["id"]])
        for job in body["jobs"]:
            resume = body["resumes"][job["id"]]
            with self.subTest(job=job["id"]):
                self.assertEqual(resume["job_id"], job["id"])
                self.assertIn(job["title"], resume["text"])
                skills = [s["code"] for s in resume["sections"]["skills"]]
                matched = [u["code"] for u in job["matched"]]
                self.assertEqual(set(skills[:len(matched)]), set(matched))
                self.assertEqual(set(skills), {u["code"] for u in units})
                self.assertNotIn("%", resume["text"])
                self.assertNotIn(job["fit"], resume["text"])
                # 01:30 and 03:20 are cited by no unit, so neither may appear.
                self.assertNotIn("roster", resume["text"])
                self.assertNotIn("nobody there issued", resume["text"])

    def fixture_match(self):
        page = app.INTAKE_PAGE.read_text(encoding="utf-8")
        block = page.split("const FIXTURE_MATCH = {")[1].split("\n};")[0]
        def rows(name, closer):
            body = block.split(f"  {name}: {closer[0]}\n")[1].split(f"\n  {closer[1]},")[0]
            return [line.strip().rstrip(",") for line in body.splitlines()]
        return {"jobs": [json.loads(r) for r in rows("jobs", "[]")],
                "courses": [json.loads(r) for r in rows("courses", "[]")],
                "resumes": json.loads("{" + ",".join(rows("resumes", "{}")) + "}"),
                "all_jobs": [json.loads(r) for r in rows("all_jobs", "[]")],
                "all_courses": [json.loads(r) for r in rows("all_courses", "[]")],
                "jobs_source": json.loads(block.split("  jobs_source: ")[1].splitlines()[0].rstrip(","))}

    def test_the_mock_fixture_is_what_the_server_returns_for_the_demo(self):
        """?mock=1 must show the same board and resumes as the real server,
        the real Adzuna snapshot included, since the demo is recorded in mock mode."""
        fixture = self.fixture_match()
        units = [{"code": c, "sources": [["transcript", "t=02:41"]]} for c in ("SITXFSA005", "SITXFSA006")]
        status, body = self.post_json("/api/match", {"occupation": "cookery", "evidenced_units": units,
                                                     "transcript": DEMO_TRANSCRIPT})
        self.assertEqual(status, 200)
        for key in ("jobs", "courses", "resumes", "all_jobs", "all_courses", "jobs_source"):
            with self.subTest(key=key):
                self.assertEqual(fixture[key], body[key])

    def units_of(self, pack):
        return [{"code": code, "sources": item["sources"]}
                for item in pack["suggestions"] if item["field"] == "units_evidenced"
                for code in item["value"].split("; ")]

    def test_resume_golden_path(self):
        """Same pipeline, same pack; every item cites a line of the sample resume."""
        status, pack = self.post_json("/api/extract", resume())
        self.assertEqual(status, 200)
        values = {s["field"]: s["value"] for s in pack["suggestions"]}
        self.assertEqual(values["anzsco_code"], "351411 Cook")
        self.assertIn("Food Safety Supervisor", pack["gate"]["text"])
        self.assertEqual(pack["metric_name"], "evidence items mapped to a resume line")
        written = {f"line={line['line']}" for line in SAMPLE_LINES}
        for item in pack["suggestions"] + pack["needs_human"]:
            for label, locator in item["sources"]:
                with self.subTest(field=item["field"], locator=locator):
                    self.assertEqual(label, "resume")
                    self.assertIn(locator, written)

        status, body = self.post_json("/api/match", {
            "source": "resume", "occupation": "cookery",
            "evidenced_units": self.units_of(pack), "resume": SAMPLE_LINES})
        self.assertEqual(status, 200)
        self.assertEqual(set(body["resumes"]), {job["id"] for job in body["jobs"]})
        for job_id, draft in body["resumes"].items():
            with self.subTest(job=job_id):
                self.assertRegex(draft["text"], r"(?m)^- .+ \[resume line \d+\]$")
                self.assertNotIn("transcript", draft["text"])
                self.assertNotIn("%", draft["text"])

    def test_an_unsupported_written_language_is_a_200_refusal(self):
        status, body = self.post_json("/api/extract", resume(language="ti"))
        self.assertEqual(status, 200)
        self.assertIn("ti: not supported for a written resume", body["refused"])

    def test_the_resume_path_still_needs_consent(self):
        status, body = self.post_json("/api/extract", resume(consent=False))
        self.assertEqual(status, 200)
        self.assertIn("consent", body["refused"])

    def test_offline_another_resume_gets_gaps_not_the_samples_evidence(self):
        mine = [{"line": 1, "text": "Welder, seven years", "en": "Welder, seven years"}]
        status, body = self.post_json("/api/extract", resume(resume=mine))
        self.assertEqual(status, 200)
        self.assertEqual(body["suggestions"], [])
        self.assertIn("units_evidenced", body["gaps"])

    def test_malformed_resume_lines_are_a_400(self):
        for lines in ("a resume", [{"t": "00:12", "text": "x"}], [{"line": "1", "text": "x"}]):
            with self.subTest(lines=lines):
                status, text = self.post("/api/extract", resume(resume=lines))
                self.assertEqual(status, 400)
                self.assertIn("resume", json.loads(text)["error"])

    def test_a_journey_line_is_never_extracted_or_in_any_tailored_resume(self):
        """Live path: the resume sent to the model holds a line about the
        journey, the model answers from the work lines, and neither the pack nor
        any draft carries the journey line."""
        journey = "2019  Fled with my family and crossed the border on foot"
        lines = SAMPLE_LINES + [{"line": len(SAMPLE_LINES) + 1, "text": journey, "en": journey}]
        canned = json.loads((app.CANNED / "d7_resume.json").read_text(encoding="utf-8"))["answer"]
        sent = {}

        def model(url, headers, payload):
            sent.update(payload)
            return {"content": [{"type": "text", "text": json.dumps(canned)}]}

        with mock.patch.dict(os.environ, {"ANTHROPIC_API_KEY": "k"}), \
                mock.patch.object(app.live, "_post_json", model):
            status, pack = self.post_json("/api/extract", resume(resume=lines))
        self.assertEqual(status, 200)
        self.assertIn("border", sent["messages"][0]["content"])
        journey_locator = f"line={len(lines)}"
        for item in pack["suggestions"] + pack["needs_human"]:
            self.assertNotIn(["resume", journey_locator], item["sources"])
            self.assertNotIn("border", item["reason"])
        status, body = self.post_json("/api/match", {
            "source": "resume", "occupation": "cookery",
            "evidenced_units": self.units_of(pack), "resume": lines})
        self.assertEqual(status, 200)
        for job_id, draft in body["resumes"].items():
            with self.subTest(job=job_id):
                self.assertNotIn("border", draft["text"])
                self.assertNotIn(f"resume line {len(lines)}", draft["text"])

    def constant(self, name):
        page = app.INTAKE_PAGE.read_text(encoding="utf-8")
        return json.loads(page.split(f"const {name} = ")[1].split(";\n")[0])

    def test_the_resume_mock_pack_is_what_the_server_returns(self):
        """?mock=1 on the resume path must show the same pack as the server.
        The pack is unchanged by real jobs: it is built from the resume alone."""
        self.assertEqual(self.constant("SAMPLE_RESUME"), SAMPLE_RESUME)
        status, pack = self.post_json("/api/extract", resume())
        self.assertEqual(status, 200)
        self.assertEqual(self.constant("FIXTURE_RESUME_EXTRACT"), pack)

    def test_the_resume_mock_board_is_what_the_server_returns(self):
        """?mock=1 on the resume path must show the same board as the server."""
        status, pack = self.post_json("/api/extract", resume())
        self.assertEqual(status, 200)
        status, body = self.post_json("/api/match", {
            "source": "resume", "occupation": "cookery",
            "evidenced_units": self.units_of(pack), "resume": SAMPLE_LINES})
        self.assertEqual(status, 200)
        body.pop("resume")
        self.assertEqual(self.constant("FIXTURE_RESUME_MATCH"), body)

    def test_an_unknown_occupation_is_a_400_without_a_traceback(self):
        for path, data in (("/api/extract", cook(occupation="astronaut")),
                           ("/api/match", {"occupation": "astronaut", "evidenced_units": []})):
            with self.subTest(path=path):
                status, text = self.post(path, data)
                self.assertEqual(status, 400)
                self.assertNotIn("Traceback", text)
                self.assertIn("astronaut", json.loads(text)["error"])

    def test_malformed_json_is_a_400(self):
        status, text = self.post("/api/extract", b"{not json")
        self.assertEqual(status, 400)
        self.assertNotIn("Traceback", text)
        self.assertIn("error", json.loads(text))

    def test_an_oversized_body_is_refused_unread(self):
        # Only the header is sent: the server answers before reading a body, so
        # actually streaming one would race its closing of the connection.
        connection = HTTPConnection("127.0.0.1", self.port, timeout=5)
        try:
            connection.putrequest("POST", "/api/extract")
            connection.putheader("Content-Type", "application/json")
            connection.putheader("Content-Length", str(app.MAX_JSON_BYTES + 1))
            connection.endheaders()
            response = connection.getresponse()
            self.assertEqual(response.status, 400)
            self.assertIn("error", json.loads(response.read()))
        finally:
            connection.close()


if __name__ == "__main__":
    unittest.main()
