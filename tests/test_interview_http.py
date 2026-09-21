"""The interview routes over real HTTP, with no API keys, so nothing leaves the machine."""
import json
import unittest
from http.client import HTTPConnection
from unittest import mock
from urllib.request import Request, urlopen

from skeleton import app
from tests.test_http import Server


class InterviewRoutes(Server):
    def test_questions_are_served_in_file_order(self):
        status, text = self.get("/api/interview/questions")
        self.assertEqual(status, 200)
        questions = json.loads(text)["questions"]
        self.assertEqual(len(questions), 7)
        self.assertEqual(questions[0]["id"], "profile")
        self.assertEqual(set(questions[0]), {"id", "section", "en", "zh"})

    def test_translate_without_a_key_is_a_200_offline(self):
        status, text = self.post("/api/translate", {"text": "我是厨师。", "source": "zh"})
        self.assertEqual(status, 200)
        body = json.loads(text)
        self.assertTrue(body["offline"])
        self.assertTrue(body["reason"])
        self.assertNotIn("en", body)

    def test_translate_returns_the_models_english(self):
        with mock.patch.object(app.interview, "translate", return_value={"en": "I am a cook."}) as sent:
            status, text = self.post("/api/translate", {"text": " 我是厨师。 ", "source": "zh"})
        self.assertEqual((status, json.loads(text)), (200, {"en": "I am a cook."}))
        sent.assert_called_once_with("我是厨师。", "zh")

    def test_speak_without_a_key_is_a_200_offline(self):
        status, text = self.post("/api/speak", {"text": "你好", "language": "zh"})
        self.assertEqual(status, 200)
        self.assertTrue(json.loads(text)["offline"])

    def test_speak_returns_mpeg_audio(self):
        with mock.patch.object(app.interview, "speak", return_value=b"ID3 mp3") as sent:
            request = json.dumps({"text": "你好", "language": "zh"}).encode("utf-8")
            with urlopen(Request(f"http://127.0.0.1:{self.port}/api/speak", data=request,
                                 method="POST"), timeout=5) as response:
                self.assertEqual(response.headers["Content-Type"], "audio/mpeg")
                self.assertEqual(response.read(), b"ID3 mp3")
        sent.assert_called_once_with("你好")

    def test_an_unsupported_language_is_refused_before_anything_is_sent(self):
        for path, body in (("/api/translate", {"text": "hola", "source": "es"}),
                           ("/api/speak", {"text": "hola", "language": "es"})):
            with self.subTest(path=path), \
                    mock.patch.object(app.interview, "translate") as translate, \
                    mock.patch.object(app.interview, "speak") as speak:
                status, text = self.post(path, body)
                self.assertEqual(status, 200)
                self.assertIn("refused", json.loads(text))
                translate.assert_not_called()
                speak.assert_not_called()

    def test_missing_or_blank_text_is_a_400(self):
        for path, body in (("/api/translate", {"source": "zh"}),
                           ("/api/translate", {"text": "  ", "source": "zh"}),
                           ("/api/speak", {"text": 3, "language": "zh"})):
            with self.subTest(path=path, body=body):
                status, text = self.post(path, body)
                self.assertEqual(status, 400)
                self.assertIn("error", json.loads(text))

    def test_speak_refuses_text_past_the_cap(self):
        with mock.patch.object(app.interview, "speak") as speak:
            status, _ = self.post("/api/speak", {"text": "字" * (app.interview.MAX_SPEAK_CHARS + 1),
                                                 "language": "zh"})
        self.assertEqual(status, 400)
        speak.assert_not_called()

    def test_an_oversized_body_is_refused_unread(self):
        for path in ("/api/translate", "/api/speak"):
            connection = HTTPConnection("127.0.0.1", self.port, timeout=5)
            try:
                connection.putrequest("POST", path)
                connection.putheader("Content-Type", "application/json")
                connection.putheader("Content-Length", str(app.MAX_JSON_BYTES + 1))
                connection.endheaders()
                self.assertEqual(connection.getresponse().status, 400)
            finally:
                connection.close()


if __name__ == "__main__":
    unittest.main()
