"""Live calls degrade to offline rather than breaking the demo."""
import io
import json
import os
import unittest
import urllib.error
from unittest import mock

from skeleton.core import live


class Transcribe(unittest.TestCase):
    def test_without_an_api_key_it_reports_offline(self):
        result = live.transcribe(b"audio", "ar", post=None, api_key="")
        self.assertTrue(result["offline"])
        self.assertTrue(result["text"])

    def test_with_a_key_it_posts_and_returns_the_text(self):
        def fake_post(url, headers, fields, files):
            self.assertIn("elevenlabs", url)
            self.assertEqual(headers["xi-api-key"], "k")
            self.assertEqual(fields["language_code"], "ar")
            return {"text": "I cooked for two hundred people a day."}

        result = live.transcribe(b"audio", "ar", post=fake_post, api_key="k")
        self.assertFalse(result["offline"])
        self.assertIn("two hundred", result["text"])

    def test_a_network_failure_degrades_to_offline(self):
        def broken_post(*args, **kwargs):
            raise OSError("venue wifi")

        result = live.transcribe(b"audio", "ar", post=broken_post, api_key="k")
        self.assertTrue(result["offline"])

    def test_mandarin_is_sent_as_the_code_scribe_lists(self):
        """The demo language; Scribe's language list names it zho."""
        sent = {}

        def fake_post(url, headers, fields, files):
            sent.update(fields)
            return {"text": "我在营地厨房做饭。"}

        live.transcribe(b"audio", "zh", post=fake_post, api_key="k")
        self.assertEqual(sent["language_code"], "zho")


PREPARED = {
    "transcript": [
        {"t": "00:12", "text": "我在营地厨房做了三年饭。", "en": "I cooked in the camp kitchen for three years."},
        {"t": "02:41", "text": "生的和熟的要分开放。", "en": "Raw and cooked food must be kept apart."},
    ],
    "candidate_units": [
        {"code": "SITXFSA005", "title": "Use hygienic practices for food safety", "role": "core"},
        {"code": "SITXFSA006", "title": "Participate in safe food handling practices", "role": "core"},
    ],
    "anzsco": {"code": "351411", "title": "Cook"},
    "osca": {"code": "351411", "title": "Cook"},
}

GOOD = {"field": "anzsco_code", "value": "351411 Cook",
        "reason": "Cooked daily in a camp kitchen for three years.",
        "confidence": 0.86, "sources": [["transcript", "t=00:12"]]}


class Fallback:
    CANNED = [{"field": "canned", "value": "x", "reason": "x",
               "confidence": 1.0, "sources": [["canned", "x"]]}]

    def suggest(self, direction_key, prepared):
        return self.CANNED


def answering(items):
    """A fake post that answers as the Messages API does."""
    def fake_post(url, headers, payload):
        return {"content": [{"type": "text", "text": json.dumps(items)}]}
    return fake_post


class LiveModelSuggest(unittest.TestCase):
    def test_without_an_api_key_it_uses_the_fallback(self):
        model = live.LiveModel(Fallback(), api_key="", post=answering([GOOD]))
        self.assertEqual(model.suggest("d7", PREPARED), Fallback.CANNED)

    def test_a_valid_response_is_parsed(self):
        units = {"field": "units_evidenced", "value": "SITXFSA005; SITXFSA006",
                 "reason": "Keeps raw and cooked food apart.",
                 "confidence": 0.78, "sources": [["transcript", "t=02:41"]]}
        model = live.LiveModel(Fallback(), api_key="k", post=answering([GOOD, units]))
        self.assertEqual(model.suggest("d7", PREPARED), [GOOD, units])

    def test_an_item_without_sources_is_dropped_and_the_rest_kept(self):
        bare = dict(GOOD, field="osca_code", sources=[])
        model = live.LiveModel(Fallback(), api_key="k", post=answering([GOOD, bare]))
        self.assertEqual(model.suggest("d7", PREPARED), [GOOD])

    def test_an_unknown_field_or_bad_confidence_is_dropped(self):
        items = [GOOD, dict(GOOD, field="candidate_score"), dict(GOOD, confidence=1.4)]
        model = live.LiveModel(Fallback(), api_key="k", post=answering(items))
        self.assertEqual(model.suggest("d7", PREPARED), [GOOD])

    def test_a_code_not_among_the_candidates_is_dropped(self):
        """Never invent a code: a fabricated one is caught on stage."""
        invented = dict(GOOD, field="units_evidenced", value="SITXFSA005; SITHCCC999")
        model = live.LiveModel(Fallback(), api_key="k", post=answering([GOOD, invented]))
        self.assertEqual(model.suggest("d7", PREPARED), [GOOD])

    def test_a_locator_not_in_the_transcript_is_dropped(self):
        """No source, no suggestion: a made-up timestamp is no source."""
        fabricated = dict(GOOD, field="osca_code", sources=[["transcript", "t=09:59"]])
        model = live.LiveModel(Fallback(), api_key="k", post=answering([GOOD, fabricated]))
        self.assertEqual(model.suggest("d7", PREPARED), [GOOD])

    def test_malformed_json_uses_the_fallback(self):
        def fake_post(url, headers, payload):
            return {"content": [{"type": "text", "text": "[{not json"}]}

        model = live.LiveModel(Fallback(), api_key="k", post=fake_post)
        self.assertEqual(model.suggest("d7", PREPARED), Fallback.CANNED)

    def test_an_http_error_uses_the_fallback(self):
        def fake_post(url, headers, payload):
            raise urllib.error.HTTPError(url, 529, "overloaded", {}, io.BytesIO())

        model = live.LiveModel(Fallback(), api_key="k", post=fake_post)
        self.assertEqual(model.suggest("d7", PREPARED), Fallback.CANNED)

    def test_the_request_carries_the_headers_and_the_scope_instruction(self):
        sent = {}

        def fake_post(url, headers, payload):
            sent.update(url=url, headers=headers, payload=payload)
            return {"content": [{"type": "text", "text": "[]"}]}

        with mock.patch.dict(os.environ, {"ANTHROPIC_MODEL": ""}):
            live.LiveModel(Fallback(), api_key="k", post=fake_post).suggest("d7", PREPARED)
        self.assertEqual(sent["url"], "https://api.anthropic.com/v1/messages")
        self.assertEqual(sent["headers"]["x-api-key"], "k")
        self.assertEqual(sent["headers"]["anthropic-version"], "2023-06-01")
        self.assertEqual(sent["payload"]["model"], "claude-sonnet-5")
        prompt = sent["payload"]["system"]
        # Whether the model obeys cannot be unit-tested; that it was told can.
        for phrase in ("journey", "how they came to Australia", "detention",
                       "persecution", "why they fled", "never put it in any field"):
            self.assertIn(phrase, prompt)
        self.assertIn('["transcript", "t=MM:SS"]', prompt)
        self.assertIn("If there is no supporting line, omit the item.", prompt)
        self.assertIn("Never output a score", prompt)
        self.assertIn("营地厨房", sent["payload"]["messages"][0]["content"])


RESUME_PREPARED = dict(
    {k: v for k, v in PREPARED.items() if k != "transcript"},
    resume=[{"line": 1, "text": "Head cook, hotel restaurant"},
            {"line": 2, "text": "Kept raw and cooked food apart."}])

FROM_RESUME = dict(GOOD, sources=[["resume", "line=1"]])


class LiveModelResume(unittest.TestCase):
    def test_a_cited_resume_line_is_kept(self):
        model = live.LiveModel(Fallback(), api_key="k", post=answering([FROM_RESUME]))
        self.assertEqual(model.suggest("d7", RESUME_PREPARED), [FROM_RESUME])

    def test_a_line_the_resume_does_not_have_is_dropped(self):
        """A fabricated line number is no source, exactly as a made-up timestamp."""
        fabricated = dict(FROM_RESUME, field="osca_code", sources=[["resume", "line=99"]])
        model = live.LiveModel(Fallback(), api_key="k", post=answering([FROM_RESUME, fabricated]))
        self.assertEqual(model.suggest("d7", RESUME_PREPARED), [FROM_RESUME])

    def test_a_timestamp_cannot_stand_in_for_a_resume_line_or_back(self):
        on_resume = dict(GOOD, sources=[["transcript", "t=00:12"]])
        model = live.LiveModel(Fallback(), api_key="k", post=answering([on_resume]))
        self.assertEqual(model.suggest("d7", RESUME_PREPARED), [])
        on_transcript = dict(GOOD, sources=[["resume", "line=1"]])
        model = live.LiveModel(Fallback(), api_key="k", post=answering([on_transcript]))
        self.assertEqual(model.suggest("d7", PREPARED), [])

    def test_the_request_carries_the_resume_lines_and_how_to_cite_them(self):
        sent = {}

        def fake_post(url, headers, payload):
            sent.update(payload=payload)
            return {"content": [{"type": "text", "text": "[]"}]}

        live.LiveModel(Fallback(), api_key="k", post=fake_post).suggest("d7", RESUME_PREPARED)
        content = json.loads(sent["payload"]["messages"][0]["content"])
        self.assertEqual(content["resume"], RESUME_PREPARED["resume"])
        self.assertNotIn("transcript", content)
        self.assertNotIn("resume", content["candidates"])
        self.assertIn('["resume", "line=N"]', sent["payload"]["system"])
        self.assertIn("If the transcript or resume mentions", sent["payload"]["system"])


class Offline(unittest.TestCase):
    def test_with_no_keys_in_the_environment_nothing_raises(self):
        env = {k: v for k, v in os.environ.items()
               if k not in ("ELEVENLABS_API_KEY", "ANTHROPIC_API_KEY")}
        with mock.patch.dict(os.environ, env, clear=True):
            self.assertTrue(live.transcribe(b"audio", "zh")["offline"])
            self.assertEqual(live.LiveModel(Fallback()).suggest("d7", PREPARED),
                             Fallback.CANNED)


if __name__ == "__main__":
    unittest.main()
