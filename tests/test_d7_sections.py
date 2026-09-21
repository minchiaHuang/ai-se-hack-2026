"""The interview's answers drafted into resume sections: POST /api/resume-sections.

No test here touches the network: the model is a fake post, and the HTTP round
trip clears the key so the endpoint answers offline.
"""
import json
import os
import threading
import unittest
from http.server import ThreadingHTTPServer
from unittest import mock
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from skeleton import app
from skeleton.app import Handler
from skeleton.directions import d7_sections

ANSWERS = [
    {"id": "employment", "section": "Employment",
     "question_en": "What was your most recent job?", "question_zh": "你最近一份工作是什么？",
     "answer_zh": "我在成都一家餐厅当主厨。",
     "answer_en": "I was head cook at a restaurant in Chengdu."},
]

GOOD = {
    "profile": "Head cook.",
    "contacts": {"phone": "0400 000 000", "email": ""},
    "education": [],
    "employment": [{"position": "Head cook", "company": "", "location": "Chengdu",
                    "dates": "", "description": "Cooked."}],
    "volunteer": [],
    "skills": ["Woks"],
    "certificates": [],
}


def answering(obj, sent=None):
    """A fake post that answers as the Messages API does, wrapped in prose."""
    def fake_post(url, headers, payload):
        if sent is not None:
            sent.update(url=url, headers=headers, payload=payload)
        return {"content": [{"type": "text", "text": "Here it is:\n" + json.dumps(obj)}]}
    return fake_post


class Draft(unittest.TestCase):
    def test_a_valid_answer_comes_back_as_the_contract(self):
        body = d7_sections.draft({"answers": ANSWERS}, post=answering(GOOD), api_key="k")
        self.assertEqual(body, {"sections": GOOD})

    def test_the_request_carries_the_key_the_answers_and_the_no_invention_rule(self):
        sent = {}
        d7_sections.draft({"answers": ANSWERS}, post=answering(GOOD, sent), api_key="k")
        self.assertIn("anthropic", sent["url"])
        self.assertEqual(sent["headers"]["x-api-key"], "k")
        self.assertIn("Never invent", sent["payload"]["system"])
        self.assertIn("how the person came to Australia", sent["payload"]["system"])
        self.assertIn("head cook at a restaurant in Chengdu",
                      sent["payload"]["messages"][0]["content"])

    def test_only_the_question_and_answer_reach_the_model(self):
        sent = {}
        extra = dict(ANSWERS[0], visa_status="x")
        d7_sections.draft({"answers": [extra]}, post=answering(GOOD, sent), api_key="k")
        self.assertNotIn("visa_status", sent["payload"]["messages"][0]["content"])

    def test_missing_sections_become_empty_never_invented(self):
        body = d7_sections.draft({"answers": ANSWERS}, post=answering({"profile": "Cook."}),
                                 api_key="k")
        sections = body["sections"]
        self.assertEqual(sections["profile"], "Cook.")
        self.assertEqual(sections["contacts"], {"phone": "", "email": ""})
        for name in ("education", "employment", "volunteer", "skills", "certificates"):
            self.assertEqual(sections[name], [], name)

    def test_wrong_types_and_empty_entries_are_dropped(self):
        raw = dict(GOOD, profile=3, skills=["Woks", 7, "  "],
                   employment=[{"position": "Cook", "company": None}, {}, "text"])
        sections = d7_sections.draft({"answers": ANSWERS}, post=answering(raw),
                                     api_key="k")["sections"]
        self.assertEqual(sections["profile"], "")
        self.assertEqual(sections["skills"], ["Woks"])
        self.assertEqual(sections["employment"], [{"position": "Cook", "company": "",
                                                   "location": "", "dates": "",
                                                   "description": ""}])

    def test_without_a_key_it_reports_offline_and_drafts_nothing(self):
        body = d7_sections.draft({"answers": ANSWERS}, post=answering(GOOD), api_key="")
        self.assertTrue(body["offline"])
        self.assertTrue(body["reason"])
        self.assertNotIn("sections", body)

    def test_a_network_failure_reports_offline(self):
        def broken(*args):
            raise OSError("venue wifi")
        body = d7_sections.draft({"answers": ANSWERS}, post=broken, api_key="k")
        self.assertTrue(body["offline"])

    def test_output_that_does_not_parse_reports_offline(self):
        def prose(*args):
            return {"content": [{"type": "text", "text": "I cannot help with that."}]}
        body = d7_sections.draft({"answers": ANSWERS}, post=prose, api_key="k")
        self.assertTrue(body["offline"])

    def test_no_english_answer_is_not_sent(self):
        def must_not_post(*args):
            raise AssertionError("posted with nothing to draft from")
        blank = [dict(ANSWERS[0], answer_en=" ")]
        body = d7_sections.draft({"answers": blank}, post=must_not_post, api_key="k")
        self.assertTrue(body["offline"])

    def test_answers_that_are_not_a_list_of_objects_are_refused(self):
        with self.assertRaises(ValueError):
            d7_sections.draft({"answers": "text"}, post=answering(GOOD), api_key="k")


RESUME_ZH = "李伟\n工作经历\n主厨｜蓉香楼｜成都｜2016年–2022年"


class Polish(unittest.TestCase):
    """A resume the person already has, in any language: POST /api/resume-polish."""

    def test_a_valid_answer_comes_back_as_the_contract(self):
        body = d7_sections.polish({"text": RESUME_ZH, "language": "zh"},
                                  post=answering(GOOD), api_key="k")
        self.assertEqual(body, {"sections": GOOD})

    def test_the_request_carries_the_text_the_language_and_the_rules(self):
        sent = {}
        d7_sections.polish({"text": RESUME_ZH, "language": "zh"},
                           post=answering(GOOD, sent), api_key="k")
        self.assertEqual(sent["headers"]["x-api-key"], "k")
        system = sent["payload"]["system"]
        self.assertIn("Translate into plain Australian English", system)
        self.assertIn("Never invent", system)
        self.assertIn("Do not add praise", system)
        self.assertIn("how the person came to Australia", system)
        content = sent["payload"]["messages"][0]["content"]
        self.assertIn("Language: zh", content)
        self.assertIn("蓉香楼", content)

    def test_missing_and_wrong_typed_sections_are_cleaned_like_draft(self):
        body = d7_sections.polish({"text": RESUME_ZH, "language": "zh"},
                                  post=answering({"profile": "Cook.", "skills": ["Woks", 3]}),
                                  api_key="k")
        sections = body["sections"]
        self.assertEqual(sections["skills"], ["Woks"])
        self.assertEqual(sections["contacts"], {"phone": "", "email": ""})
        for name in ("education", "employment", "volunteer", "certificates"):
            self.assertEqual(sections[name], [], name)

    def test_without_a_key_it_reports_offline_and_writes_nothing(self):
        body = d7_sections.polish({"text": RESUME_ZH, "language": "zh"},
                                  post=answering(GOOD), api_key="")
        self.assertTrue(body["offline"])
        self.assertTrue(body["reason"])
        self.assertNotIn("sections", body)

    def test_a_network_failure_reports_offline(self):
        def broken(*args):
            raise OSError("venue wifi")
        body = d7_sections.polish({"text": RESUME_ZH, "language": "zh"}, post=broken, api_key="k")
        self.assertTrue(body["offline"])

    def test_an_unsupported_language_is_refused_before_anything_is_sent(self):
        def must_not_post(*args):
            raise AssertionError("posted a language nobody can check")
        body = d7_sections.polish({"text": "رزومه", "language": "fa"},
                                  post=must_not_post, api_key="k")
        self.assertIn("fa", body["refused"])

    def test_empty_or_oversized_text_is_refused(self):
        for text in ("", "  ", None, "x" * (d7_sections.MAX_POLISH_CHARS + 1)):
            with self.subTest(text=str(text)[:5]), self.assertRaises(ValueError):
                d7_sections.polish({"text": text, "language": "zh"}, post=answering(GOOD),
                                   api_key="k")


class Route(unittest.TestCase):
    """The page's two requests, over real HTTP, with no API key."""

    @classmethod
    def setUpClass(cls):
        cls.env = mock.patch.dict(os.environ)
        cls.env.start()
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

    def post(self, data, path="/api/resume-sections"):
        request = Request(f"http://127.0.0.1:{self.port}{path}",
                          data=json.dumps(data).encode("utf-8"), method="POST",
                          headers={"Content-Type": "application/json"})
        try:
            with urlopen(request, timeout=5) as response:
                return response.status, json.loads(response.read())
        except HTTPError as error:
            return error.code, json.loads(error.read())

    def test_the_review_page_is_served(self):
        with urlopen(f"http://127.0.0.1:{self.port}/review", timeout=5) as response:
            self.assertEqual(response.status, 200)
            self.assertIn("Caseworker Review", response.read().decode("utf-8"))

    def test_offline_is_a_200_with_a_reason(self):
        status, body = self.post({"answers": ANSWERS})
        self.assertEqual(status, 200)
        self.assertTrue(body["offline"])

    def test_the_upload_page_is_served(self):
        with urlopen(f"http://127.0.0.1:{self.port}/upload", timeout=5) as response:
            self.assertEqual(response.status, 200)
            self.assertIn("Add the client's resume", response.read().decode("utf-8"))

    def test_polish_offline_is_a_200_with_a_reason(self):
        status, body = self.post({"text": RESUME_ZH, "language": "zh"}, "/api/resume-polish")
        self.assertEqual(status, 200)
        self.assertTrue(body["offline"])

    def test_polish_without_text_is_a_400(self):
        status, body = self.post({"language": "zh"}, "/api/resume-polish")
        self.assertEqual(status, 400)
        self.assertIn("text", body["error"])

    def test_bad_answers_are_a_400(self):
        status, body = self.post({"answers": [1, 2]})
        self.assertEqual(status, 400)
        self.assertIn("answers", body["error"])


def constant(name, page=app.REVIEW_PAGE):
    page = page.read_text(encoding="utf-8")
    return json.loads(page.split(f"const {name} = ")[1].split(";\n")[0])


def join(*parts):
    return ", ".join(p.strip() for p in parts if p and p.strip())


def resume_lines(s):
    """Python copy of resumeLines() in review.html, only to pin the fixture layout."""
    out = []

    def block(title, rows):
        rows = [r.strip() for r in rows if r and r.strip()]
        if rows:
            out.extend([title] + rows)
    block("PROFILE", [s["profile"]])
    block("WORK EXPERIENCE", [x for e in s["employment"] for x in
                              (join(e["position"], e["company"], e["location"], e["dates"]), e["description"])])
    block("VOLUNTEER EXPERIENCE", [x for e in s["volunteer"] for x in
                                   (join(e["role"], e["location"], e["dates"]), e["description"])])
    block("EDUCATION", [x for e in s["education"] for x in
                        (join(e["major"], e["school"], e["location"], e["dates"]), e["description"])])
    block("SKILLS", s["skills"])
    block("CERTIFICATES", s["certificates"])
    return out


class MockFixtures(unittest.TestCase):
    """?mock=1 on /review is the demo video; its fixtures must agree with the server."""

    def test_the_mock_questions_are_the_teams(self):
        path = app.Path(app.__file__).parent / "demo_data" / "reference" / "interview_questions.json"
        questions = {q["id"]: q for q in json.loads(path.read_text(encoding="utf-8"))["questions"]}
        for answer in constant("MOCK_INTERVIEW")["answers"]:
            with self.subTest(id=answer["id"]):
                self.assertEqual(answer["question_en"], questions[answer["id"]]["en"])
                self.assertEqual(answer["question_zh"], questions[answer["id"]]["zh"])

    def test_the_upload_mock_lands_on_the_same_sections_as_the_interview_mock(self):
        # Same sections, same lines, so the /jobs match fixtures stay valid for both paths.
        self.assertEqual(constant("FIXTURE_SECTIONS", app.UPLOAD_PAGE), constant("FIXTURE_SECTIONS"))

    def test_the_mock_lines_are_built_from_the_mock_sections(self):
        self.assertEqual(resume_lines(constant("FIXTURE_SECTIONS")), constant("FIXTURE_REVIEW_LINES"))

    def test_the_mock_board_is_what_the_server_returns(self):
        texts = constant("FIXTURE_REVIEW_LINES")
        lines = [{"line": i + 1, "text": t, "en": t} for i, t in enumerate(texts)]
        units = [{"code": code, "sources": item["sources"]}
                 for item in constant("FIXTURE_REVIEW_EXTRACT")["suggestions"]
                 if item["field"] == "units_evidenced"
                 for code in item["value"].replace(",", ";").split(";") if code.strip()]
        body = app.match({"source": "resume", "occupation": "cookery",
                          "evidenced_units": units, "resume": lines})
        body.pop("resume")
        self.assertEqual(constant("FIXTURE_REVIEW_MATCH"), body)


if __name__ == "__main__":
    unittest.main()
