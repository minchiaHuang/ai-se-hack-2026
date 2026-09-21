"""Direction 7 red lines, enforced in code before the model is called."""
import unittest

from skeleton.directions import d7_credentials as d7


def payload(**over):
    base = {
        "occupation": "cookery",
        "language": "zh",
        "consent": True,
        "transcript": [{"t": "00:12", "text": "我在营地厨房做了三年饭。"}],
    }
    base.update(over)
    return base


class RedLines(unittest.TestCase):
    def test_identifying_refugee_fields_are_refused(self):
        for field in ("country_of_origin", "visa_status", "protection_claim", "biometric_id"):
            with self.subTest(field=field):
                with self.assertRaises(d7.RedLineError) as caught:
                    d7.guard(payload(**{field: "x"}))
                self.assertIn(field, str(caught.exception))

    def test_missing_consent_is_refused(self):
        with self.assertRaises(d7.RedLineError) as caught:
            d7.guard(payload(consent=False))
        self.assertIn("consent", str(caught.exception).lower())

    def test_unsupported_language_is_refused_not_silently_englished(self):
        """Every language other than Mandarin and Arabic is refused, Farsi and
        Swahili included: nobody on the team can verify them."""
        for code in ("ti", "prs", "rhg", "haz", "fa", "sw"):
            with self.subTest(code=code):
                with self.assertRaises(d7.UnsupportedLanguageError) as caught:
                    d7.guard(payload(language=code))
                self.assertIn(code, str(caught.exception))

    def test_scoring_the_person_is_refused(self):
        """A job-fit score is allowed. A score on the human being is not."""
        with self.assertRaises(d7.RedLineError):
            d7.guard(payload(candidate_score=0.8))

    def test_a_clean_payload_passes(self):
        d7.guard(payload())

    def test_supported_languages_are_only_the_ones_we_can_actually_do(self):
        self.assertEqual(set(d7.SUPPORTED_LANGUAGES), {"zh", "ar"})


class Shape(unittest.TestCase):
    def test_target_fields_cover_both_classifications(self):
        fields = d7.target_fields(payload())
        for expected in ("anzsco_code", "osca_code", "qualification", "units_evidenced"):
            self.assertIn(expected, fields)

    def test_the_gate_is_never_asked_of_the_model(self):
        """It is reference data. Asking the model would render it as a guess."""
        self.assertNotIn("gate", d7.target_fields(payload()))

    def test_prepare_sends_exactly_the_transcript_and_the_occupational_frame(self):
        prepared = d7.prepare(payload(label="demo"))
        self.assertEqual(set(prepared), {"transcript", "candidate_units", "anzsco", "osca"})


if __name__ == "__main__":
    unittest.main()
