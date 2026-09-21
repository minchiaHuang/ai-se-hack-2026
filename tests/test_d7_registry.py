"""Reference data must be real. A fabricated unit code is caught on stage."""
import unittest

from skeleton.core import registry


class ReferenceData(unittest.TestCase):
    def test_three_occupations_are_seeded(self):
        self.assertEqual(
            set(registry.load_occupations()), {"aged_care", "welding", "cookery"}
        )

    def test_each_occupation_carries_both_classifications(self):
        """ANZSCO 2022 still runs migration; OSCA 2024 runs ABS statistics."""
        for key in registry.load_occupations():
            with self.subTest(key=key):
                occ = registry.occupation(key)
                self.assertRegex(occ["anzsco"]["code"], r"^\d{6}$")
                self.assertRegex(occ["osca"]["code"], r"^\d{6}$")
                self.assertTrue(occ["anzsco"]["title"])
                self.assertTrue(occ["osca"]["title"])

    def test_welding_points_at_the_current_qualification(self):
        """MEM31922 was superseded by MEM31925 on 2025-09-04."""
        qual = registry.occupation("welding")["qualification"]
        self.assertEqual(qual["code"], "MEM31925")
        self.assertEqual(qual["superseded_code"], "MEM31922")

    def test_every_unit_has_a_code_and_a_title(self):
        for key in registry.load_occupations():
            for unit in registry.all_units(key):
                with self.subTest(key=key, unit=unit.get("code")):
                    self.assertRegex(unit["code"], r"^[A-Z]{3,7}\d{3,6}$")
                    self.assertTrue(unit["title"].strip())

    def test_cookery_carries_the_nsw_food_safety_supervisor_units(self):
        """SITXFSA005 + SITXFSA006 are the NSW statutory certificate."""
        codes = {u["code"] for u in registry.all_units("cookery")}
        self.assertIn("SITXFSA005", codes)
        self.assertIn("SITXFSA006", codes)


class SourceCheck(unittest.TestCase):
    def test_offline_reports_the_seeded_record_unchecked(self):
        checked = registry.source_check("cookery")
        self.assertEqual(checked["code"], "SIT30821")
        self.assertEqual(checked["status"], "Current")
        self.assertFalse(checked["reachable"])

    def test_the_seeded_record_names_what_was_superseded(self):
        checked = registry.source_check("welding")
        self.assertEqual(checked["code"], "MEM31925")
        self.assertEqual(checked["superseded_code"], "MEM31922")

    def test_a_pdf_response_marks_the_source_reachable(self):
        def fake_fetch(url):
            self.assertTrue(url.endswith("MEM31925_R1.pdf"))
            return b"%PDF-1.4"

        self.assertTrue(registry.source_check("welding", fetch=fake_fetch)["reachable"])

    def test_a_non_pdf_response_is_not_reachable(self):
        """An error page served with 200 must not count."""
        checked = registry.source_check("welding", fetch=lambda url: b"<html>")
        self.assertFalse(checked["reachable"])

    def test_a_failed_fetch_degrades_instead_of_raising(self):
        def broken_fetch(url):
            raise OSError("no network at the venue")

        checked = registry.source_check("welding", fetch=broken_fetch)
        self.assertFalse(checked["reachable"])
        self.assertEqual(checked["code"], "MEM31925")


if __name__ == "__main__":
    unittest.main()
