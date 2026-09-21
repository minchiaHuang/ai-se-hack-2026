"""The /interview page: served, and its mock fixtures agree with the files they copy."""
import json
import unittest

from skeleton import app
from skeleton.core import interview
from tests.test_http import Server


def constant(page, name):
    return json.loads(page.read_text(encoding="utf-8").split(f"const {name} = ")[1].split(";\n")[0])


class InterviewPage(Server):
    def test_the_interview_page_is_served(self):
        status, text = self.get("/interview")
        self.assertEqual(status, 200)
        self.assertIn("Translated contents", text)


class MockFixtures(unittest.TestCase):
    """?mock=1 is the demo video; it must say what the live page would."""

    def test_the_questions_are_the_ones_the_server_serves(self):
        self.assertEqual(constant(app.INTERVIEW_PAGE, "FIXTURE_QUESTIONS"), interview.questions())

    def test_the_mock_hand_over_is_the_one_review_expects(self):
        # /interview?mock=1 writes this into sessionStorage and /review?mock=1 drafts
        # from it, so the transcript on video and the resume must be the same answers.
        questions = constant(app.INTERVIEW_PAGE, "FIXTURE_QUESTIONS")["questions"]
        answers = {a["id"]: a for a in constant(app.INTERVIEW_PAGE, "MOCK_ANSWERS")}
        handed = {"language": "zh", "answers": [
            {"id": q["id"], "section": q["section"], "question_en": q["en"], "question_zh": q["zh"],
             "answer_zh": answers[q["id"]]["answer_zh"], "answer_en": answers[q["id"]]["answer_en"]}
            for q in questions]}
        self.assertEqual(handed, constant(app.REVIEW_PAGE, "MOCK_INTERVIEW"))


if __name__ == "__main__":
    unittest.main()
