"""Direction 7 through the shared pipeline: golden path and the failures."""
import json
import unittest

from skeleton.app import SCENARIOS
from skeleton.core import registry
from skeleton.core.model import CANNED as CANNED_DIR, StubModel
from skeleton.core.pipeline import run
from skeleton.directions import d7_credentials as d7

CANNED = [
    {"field": "anzsco_code", "value": "351411 Cook",
     "reason": "Three years cooking for 200 people a day in a camp kitchen.",
     "confidence": 0.86, "sources": [["transcript", "t=00:12"]]},
    {"field": "osca_code", "value": "322331 Cook",
     "reason": "Same testimony; OSCA 2024 code for the same occupation.",
     "confidence": 0.84, "sources": [["transcript", "t=00:12"]]},
    {"field": "units_evidenced", "value": "SITXFSA005; SITXFSA006",
     "reason": "Describes separating raw and cooked food and logging fridge temperatures.",
     "confidence": 0.78, "sources": [["transcript", "t=02:41"]]},
    {"field": "qualification", "value": "SIT30821 Certificate III in Commercial Cookery",
     "reason": "Both food safety units sit in the core of this qualification.",
     "confidence": 0.44, "sources": [["transcript", "t=02:41"]]},
]

PAYLOAD = {
    "occupation": "cookery",
    "language": "zh",
    "consent": True,
    "transcript": [{"t": "00:12", "text": "我每天要做两百个人的饭。",
                    "en": "I cooked for two hundred people a day."}],
}


class GoldenPath(unittest.TestCase):
    def setUp(self):
        self.model = StubModel({d7.KEY: CANNED})

    def test_confident_suggestions_are_shown_and_cite_the_transcript(self):
        result = run(d7, PAYLOAD, self.model)
        self.assertEqual(len(result.suggestions), 3)
        for suggestion in result.suggestions:
            self.assertTrue(suggestion.sources)
            self.assertEqual(suggestion.sources[0].label, "transcript")

    def test_low_confidence_is_withheld_for_a_person_to_decide(self):
        result = run(d7, PAYLOAD, self.model)
        withheld = {s.field for s in result.needs_human}
        self.assertIn("qualification", withheld)
        for suggestion in result.needs_human:
            self.assertIsNone(suggestion.displayed_value())

    def test_a_complete_answer_leaves_no_gaps(self):
        self.assertEqual(run(d7, PAYLOAD, self.model).gaps, ())

    def test_a_field_the_model_did_not_answer_is_reported_as_a_gap(self):
        partial = [item for item in CANNED if item["field"] != "osca_code"]
        result = run(d7, PAYLOAD, StubModel({d7.KEY: partial}))
        self.assertEqual(result.gaps, ("osca_code",))

    def test_metric_counts_only_sourced_items(self):
        result = run(d7, PAYLOAD, self.model)
        self.assertEqual(result.metric_value, 3)
        self.assertEqual(result.metric_name, d7.METRIC)


class FailurePaths(unittest.TestCase):
    def test_unsupported_language_stops_before_the_model(self):
        model = StubModel({d7.KEY: CANNED})
        with self.assertRaises(d7.UnsupportedLanguageError):
            run(d7, dict(PAYLOAD, language="ti"), model)

    def test_missing_consent_stops_before_the_model(self):
        model = StubModel({d7.KEY: CANNED})
        with self.assertRaises(d7.RedLineError):
            run(d7, dict(PAYLOAD, consent=False), model)


class DemoScenarios(unittest.TestCase):
    """The canned files are what the recorded demo shows, so they must hold together."""

    def test_every_canned_locator_points_at_a_line_in_its_transcript(self):
        """A citation to a timestamp nobody spoke at would be caught on stage."""
        for key in ("d7", "d7_lowconfidence", "d7_welding"):
            with self.subTest(scenario=key):
                spoken = {f"t={line['t']}" for line in SCENARIOS[key]["transcript"]}
                for item in json.loads((CANNED_DIR / f"{key}.json").read_text(encoding="utf-8")):
                    for label, locator in item["sources"]:
                        self.assertEqual(label, "transcript")
                        self.assertIn(locator, spoken)

    def test_transcript_lines_carry_the_spoken_text_and_an_english_gloss(self):
        for key, scenario in SCENARIOS.items():
            if not key.startswith("d7"):
                continue
            for line in scenario["transcript"]:
                with self.subTest(scenario=key, t=line.get("t")):
                    self.assertEqual(set(line), {"t", "text", "en"})

    def test_welding_units_come_only_from_the_reference_data(self):
        """Never invent a unit code: every one cited must be seeded."""
        seeded = {u["code"] for u in registry.all_units("welding")}
        canned = json.loads((CANNED_DIR / "d7_welding.json").read_text(encoding="utf-8"))
        units = next(item for item in canned if item["field"] == "units_evidenced")
        cited = {code.strip() for code in units["value"].split(";")}
        self.assertTrue(cited)
        self.assertLessEqual(cited, seeded)


if __name__ == "__main__":
    unittest.main()
