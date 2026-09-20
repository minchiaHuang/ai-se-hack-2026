"""The one pipeline all three directions share."""
import unittest

from skeleton.core.pipeline import run
from skeleton.core.model import StubModel
from skeleton.core.schema import AggregationError
from skeleton.directions import d2_triage, d3_evidence, d6_outcomes


class SharedPipeline(unittest.TestCase):
    def test_a_target_field_the_model_says_nothing_about_becomes_a_gap(self):
        model = StubModel({"d2": [
            {"field": "destination", "value": "repair", "reason": "mendable",
             "confidence": 0.82, "sources": [["route list", "row 3"]]},
        ]})

        result = run(d2_triage, {"item": "kettle"}, model, threshold=0.6)

        self.assertIn("condition", result.gaps)
        self.assertNotIn("destination", result.gaps)

    def test_low_confidence_lands_in_needs_human_and_withholds_the_value(self):
        model = StubModel({"d2": [
            {"field": "destination", "value": "landfill", "reason": "unsure",
             "confidence": 0.2, "sources": [["route list", "row 3"]]},
        ]})

        result = run(d2_triage, {"item": "kettle"}, model, threshold=0.6)

        self.assertEqual(result.suggestions, ())
        self.assertEqual(result.needs_human[0].field, "destination")
        self.assertIsNone(result.needs_human[0].displayed_value())

    def test_the_metric_counts_only_what_a_human_could_accept(self):
        model = StubModel({"d2": [
            {"field": "destination", "value": "repair", "reason": "r",
             "confidence": 0.9, "sources": [["route list", "row 3"]]},
            {"field": "condition", "value": "worn", "reason": "r",
             "confidence": 0.1, "sources": [["route list", "row 4"]]},
        ]})

        result = run(d2_triage, {"item": "kettle", "landfill_cost": 2.0}, model, threshold=0.6)

        self.assertEqual(result.metric_name, d2_triage.METRIC)
        self.assertEqual(result.metric_value, 2.0)


class DirectionThree(unittest.TestCase):
    def test_a_field_without_evidence_is_reported_as_a_gap_not_invented(self):
        model = StubModel({"d3": []})

        result = run(d3_evidence, {"target_fields": ["beneficiaries"]}, model, threshold=0.6)

        self.assertEqual(result.gaps, ("beneficiaries",))
        self.assertEqual(result.suggestions, ())


class DirectionSix(unittest.TestCase):
    def test_an_individual_level_payload_is_refused_before_any_model_call(self):
        model = StubModel({"d6": []})

        with self.assertRaises(AggregationError):
            run(d6_outcomes, {"employee_name": "…", "group_size": 40}, model, threshold=0.6)

    def test_a_group_that_is_too_small_is_refused(self):
        model = StubModel({"d6": []})

        with self.assertRaises(AggregationError):
            run(d6_outcomes, {"placements": 3, "group_size": 3}, model, threshold=0.6)

    def test_a_large_enough_aggregate_runs(self):
        model = StubModel({"d6": [
            {"field": "retention_6m", "value": "0.75", "reason": "retained / placed",
             "confidence": 0.9, "sources": [["attendance summary", "Q3"]]},
        ]})

        result = run(d6_outcomes, {"placements": 12, "group_size": 40,
                                   "prep_hours": 9.0}, model, threshold=0.6)

        self.assertEqual(result.suggestions[0].field, "retention_6m")
        self.assertEqual(result.metric_value, 9.0)


if __name__ == "__main__":
    unittest.main()
