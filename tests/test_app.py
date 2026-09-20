"""The demo shell must render every scenario, including the refusals."""
import unittest

from skeleton.app import SCENARIOS, render_index, render_result


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


if __name__ == "__main__":
    unittest.main()
