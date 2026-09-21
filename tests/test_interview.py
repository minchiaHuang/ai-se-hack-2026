"""The interview backend degrades to offline, never to a fake answer."""
import io
import json
import os
import unittest
import urllib.error
from unittest import mock

from skeleton.core import interview

ANSWER = "我在营地厨房做了三年饭。"


def answering(text):
    """A fake post that answers as the Messages API does."""
    def fake_post(url, headers, payload):
        return {"content": [{"type": "text", "text": text}]}
    return fake_post


def broken(*args, **kwargs):
    raise OSError("venue wifi")


class Questions(unittest.TestCase):
    def test_the_seven_fixed_questions_in_file_order(self):
        ids = [q["id"] for q in interview.questions()["questions"]]
        self.assertEqual(ids, ["profile", "contacts", "education", "employment",
                               "volunteer", "skills", "certificates"])

    def test_each_question_carries_exactly_the_contract_fields(self):
        for q in interview.questions()["questions"]:
            self.assertEqual(set(q), {"id", "section", "en", "zh"})
            self.assertTrue(q["en"] and q["zh"])

    def test_no_question_asks_how_the_person_came_to_australia(self):
        for q in interview.questions()["questions"]:
            for phrase in ("journey", "came to Australia", "arrive", "flee", "fled", "visa"):
                self.assertNotIn(phrase, q["en"])

    def test_the_file_keeps_its_unreviewed_note(self):
        data = json.loads(interview.QUESTIONS.read_text(encoding="utf-8"))
        self.assertIn("not yet been checked", data["_note"])


class Translate(unittest.TestCase):
    def test_without_a_key_it_is_offline_with_a_reason(self):
        result = interview.translate(ANSWER, "zh", post=broken, api_key="")
        self.assertEqual(set(result), {"offline", "reason"})
        self.assertTrue(result["offline"])

    def test_with_a_key_it_returns_the_english(self):
        result = interview.translate(
            ANSWER, "zh", post=answering(" I cooked in the camp kitchen for three years.\n"),
            api_key="k")
        self.assertEqual(result, {"en": "I cooked in the camp kitchen for three years."})

    def test_the_request_carries_the_answer_and_the_no_additions_rule(self):
        sent = {}

        def fake_post(url, headers, payload):
            sent.update(url=url, headers=headers, payload=payload)
            return {"content": [{"type": "text", "text": "x"}]}

        with mock.patch.dict(os.environ, {"ANTHROPIC_MODEL": ""}):
            interview.translate(ANSWER, "zh", post=fake_post, api_key="k")
        self.assertEqual(sent["url"], "https://api.anthropic.com/v1/messages")
        self.assertEqual(sent["headers"]["x-api-key"], "k")
        self.assertEqual(sent["payload"]["model"], "claude-sonnet-5")
        self.assertEqual(sent["payload"]["messages"], [{"role": "user", "content": ANSWER}])
        system = sent["payload"]["system"]
        for phrase in ("Mandarin Chinese", "Australian English", "Do not add",
                       "Never add a score"):
            self.assertIn(phrase, system)

    def test_a_network_failure_is_offline(self):
        self.assertTrue(interview.translate(ANSWER, "zh", post=broken, api_key="k")["offline"])

    def test_an_http_error_is_offline(self):
        def fake_post(url, headers, payload):
            raise urllib.error.HTTPError(url, 529, "overloaded", {}, io.BytesIO())

        self.assertTrue(interview.translate(ANSWER, "zh", post=fake_post, api_key="k")["offline"])

    def test_an_empty_or_malformed_answer_is_offline_not_blank(self):
        for post in (answering("  "), lambda *a: {"content": []}, lambda *a: {}):
            with self.subTest(post=post):
                self.assertTrue(interview.translate(ANSWER, "zh", post=post, api_key="k")["offline"])


class Speak(unittest.TestCase):
    def test_without_a_key_it_is_offline_with_a_reason(self):
        result = interview.speak("你好", post=broken, api_key="")
        self.assertEqual(set(result), {"offline", "reason"})

    def test_with_a_key_it_returns_the_audio_bytes(self):
        sent = {}

        def fake_post(url, headers, payload):
            sent.update(url=url, headers=headers, payload=payload)
            return b"ID3 mp3 bytes"

        with mock.patch.dict(os.environ, {"ELEVENLABS_VOICE_ID": ""}):
            audio = interview.speak("你好", post=fake_post, api_key="k")
        self.assertEqual(audio, b"ID3 mp3 bytes")
        self.assertTrue(sent["url"].startswith(
            "https://api.elevenlabs.io/v1/text-to-speech/" + interview.DEFAULT_VOICE_ID + "?"))
        self.assertEqual(sent["headers"]["xi-api-key"], "k")
        self.assertEqual(sent["payload"], {"text": "你好", "model_id": "eleven_multilingual_v2"})

    def test_the_voice_comes_from_the_environment(self):
        sent = {}

        def fake_post(url, headers, payload):
            sent["url"] = url
            return b"mp3"

        with mock.patch.dict(os.environ, {"ELEVENLABS_VOICE_ID": "voice123"}):
            interview.speak("你好", post=fake_post, api_key="k")
        self.assertIn("/text-to-speech/voice123?", sent["url"])

    def test_a_failure_or_empty_audio_is_offline(self):
        for post in (broken, lambda *a: b"", lambda *a: {"detail": "quota"}):
            with self.subTest(post=post):
                self.assertTrue(interview.speak("你好", post=post, api_key="k")["offline"])


if __name__ == "__main__":
    unittest.main()
