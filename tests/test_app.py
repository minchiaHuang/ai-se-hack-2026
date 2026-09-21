"""The demo shell must render every scenario, including the refusals."""
import os
import unittest
from unittest import mock

from skeleton.app import SCENARIOS, render_index, render_result

# extract() goes live when ANTHROPIC_API_KEY is set, and these tests pin the
# stub's canned answers; without this a developer's key makes them network calls.
_offline = mock.patch.dict(os.environ)


def setUpModule():
    _offline.start()
    os.environ.pop("ANTHROPIC_API_KEY", None)
    os.environ.pop("ELEVENLABS_API_KEY", None)


def tearDownModule():
    _offline.stop()


class DemoShell(unittest.TestCase):
    def test_every_scenario_renders(self):
        for key in SCENARIOS:
            with self.subTest(scenario=key):
                self.assertIn("<h1>", render_result(key))

    def test_the_small_group_scenario_renders_a_refusal(self):
        page = render_result("d6_small_group")
        self.assertIn("Refused", page)
        self.assertNotIn("Suggested", page)

    def test_the_low_confidence_scenario_withholds_the_value(self):
        page = render_result("d2_lowconfidence")
        self.assertIn("a person decides", page)
        self.assertIn("value withheld", page)
        # the suggested value itself must not reach the page
        self.assertNotIn("unclear", page)

    def test_index_lists_every_scenario(self):
        page = render_index()
        for key in SCENARIOS:
            self.assertIn(f"/run?s={key}", page)


class IntakeEndpoint(unittest.TestCase):
    def test_extract_returns_a_sourced_evidence_pack(self):
        from skeleton.app import extract
        body = extract({
            "occupation": "cookery", "language": "zh", "consent": True,
            "transcript": [{"t": "00:12", "text": "我每天要做两百个人的饭。",
                            "en": "I cooked for two hundred people a day."}],
        })
        self.assertIn("suggestions", body)
        self.assertTrue(all(s["sources"] for s in body["suggestions"]))

    def test_extract_attaches_the_gate_from_the_registry(self):
        """The strongest demo line must never render as a blank."""
        from skeleton.app import extract
        body = extract({"occupation": "cookery", "language": "zh", "consent": True,
                        "transcript": [{"t": "00:12", "text": "x", "en": "x"}]})
        self.assertIn("Food Safety Supervisor", body["gate"]["text"])

    def test_extract_reports_a_refusal_as_data_not_an_exception(self):
        from skeleton.app import extract
        body = extract({"occupation": "cookery", "language": "ti",
                        "consent": True, "transcript": []})
        self.assertIn("refused", body)
        self.assertIn("ti", body["refused"])

    def test_extract_answers_for_the_occupation_that_was_asked(self):
        """A welder must not get the cook's evidence pack back."""
        from skeleton.app import extract
        body = extract({"occupation": "welding", "language": "zh", "consent": True,
                        "transcript": [{"t": "00:05", "text": "x", "en": "x"}]})
        values = {s["field"]: s["value"] for s in body["suggestions"]}
        self.assertEqual(values["anzsco_code"], "322313 Welder (First Class)")

    def test_an_occupation_without_canned_evidence_gets_gaps_not_another_trade(self):
        from skeleton.app import extract
        body = extract({"occupation": "aged_care", "language": "zh", "consent": True,
                        "transcript": [{"t": "00:05", "text": "x", "en": "x"}]})
        self.assertEqual(body["suggestions"], [])
        self.assertIn("anzsco_code", body["gaps"])

    def test_extract_carries_the_seeded_qualification_record(self):
        """The supersession comes from the record checked on 2026-09-21, offline."""
        from skeleton.app import extract
        body = extract({"occupation": "welding", "language": "zh", "consent": True,
                        "transcript": [{"t": "00:05", "text": "x", "en": "x"}]})
        self.assertEqual(body["qualification_source"]["code"], "MEM31925")
        self.assertEqual(body["qualification_source"]["superseded_code"], "MEM31922")
        self.assertFalse(body["qualification_source"]["reachable"])


    def test_the_live_model_answers_only_when_a_key_is_set(self):
        """With a key the stub becomes the fallback; without one nothing changes."""
        from skeleton.app import model_for_occupation
        from skeleton.core.live import LiveModel
        from skeleton.core.model import StubModel
        self.assertIsInstance(model_for_occupation("cookery"), StubModel)
        with mock.patch.dict(os.environ, {"ANTHROPIC_API_KEY": "k"}):
            self.assertIsInstance(model_for_occupation("cookery"), LiveModel)


if __name__ == "__main__":
    unittest.main()
