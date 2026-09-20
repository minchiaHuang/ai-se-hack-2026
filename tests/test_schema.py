"""Shared pipeline guarantees: nothing is shown without a source or enough confidence."""
import unittest

from skeleton.core.schema import Source, Suggestion, sort_by_confidence


class SuggestionRules(unittest.TestCase):
    def test_a_suggestion_without_a_source_is_rejected(self):
        with self.assertRaises(ValueError):
            Suggestion(field="destination", value="repair", reason="looks mendable",
                       confidence=0.9, sources=())

    def test_confidence_outside_zero_to_one_is_rejected(self):
        with self.assertRaises(ValueError):
            Suggestion(field="destination", value="repair", reason="r", confidence=1.4,
                       sources=(Source("route list", "row 3"),))

    def test_low_confidence_suggestions_are_separated_from_confident_ones(self):
        src = (Source("route list", "row 3"),)
        confident = Suggestion("destination", "repair", "r", 0.82, src)
        unsure = Suggestion("condition", "unknown", "r", 0.20, src)

        shown, needs_human = sort_by_confidence([confident, unsure], threshold=0.6)

        self.assertEqual([s.field for s in shown], ["destination"])
        self.assertEqual([s.field for s in needs_human], ["condition"])
        self.assertEqual(shown[0].displayed_value(), "repair")

    def test_a_low_confidence_suggestion_never_carries_its_value_forward(self):
        src = (Source("route list", "row 3"),)
        unsure = Suggestion("destination", "landfill", "r", 0.1, src)

        _, needs_human = sort_by_confidence([unsure], threshold=0.6)

        self.assertIsNone(needs_human[0].displayed_value())


if __name__ == "__main__":
    unittest.main()
