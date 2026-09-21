"""Direction 6 red line, enforced in code: aggregate only, never an individual."""
import unittest

from skeleton.core.schema import AggregationError, check_aggregate


class AggregationGuard(unittest.TestCase):
    def test_individual_level_field_is_refused(self):
        with self.assertRaises(AggregationError) as caught:
            check_aggregate({"employee_name": "…", "placements": 12}, group_size=40)
        self.assertIn("employee_name", str(caught.exception))

    def test_group_smaller_than_minimum_is_refused(self):
        with self.assertRaises(AggregationError) as caught:
            check_aggregate({"placements": 3}, group_size=3)
        self.assertIn("group", str(caught.exception).lower())

    def test_plain_aggregate_over_a_large_enough_group_passes(self):
        check_aggregate({"placements": 12, "retained_6m": 9}, group_size=40)

    def test_every_individual_marker_is_caught(self):
        for field in ("name", "employee_id", "dob", "email", "address", "phone"):
            with self.subTest(field=field):
                with self.assertRaises(AggregationError):
                    check_aggregate({field: "x", "placements": 12}, group_size=40)


if __name__ == "__main__":
    unittest.main()
