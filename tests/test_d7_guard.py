"""Direction 7 red lines, enforced in code before the model is called."""
import json
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

    def test_english_is_still_refused_for_the_interview(self):
        """Only a written resume gains English; spoken input is not loosened."""
        for over in ({}, {"source": "interview"}, {"source": "something else"}):
            with self.subTest(**over):
                with self.assertRaises(d7.UnsupportedLanguageError):
                    d7.guard(payload(language="en", **over))


def resume_payload(**over):
    base = {"source": "resume", "occupation": "cookery", "language": "en", "consent": True,
            "resume": [{"line": 1, "text": "Head cook, hotel restaurant"}]}
    base.update(over)
    return base


class ResumeRedLines(unittest.TestCase):
    """The resume path: the language rule widens to what can be read; nothing else moves."""

    def test_a_written_resume_may_be_english_mandarin_or_arabic(self):
        for code in ("en", "zh", "ar"):
            with self.subTest(code=code):
                d7.guard(resume_payload(language=code))

    def test_any_other_written_language_is_refused(self):
        for code in ("ti", "fa", "sw", "fr", None):
            with self.subTest(code=code):
                with self.assertRaises(d7.UnsupportedLanguageError) as caught:
                    d7.guard(resume_payload(language=code))
                self.assertIn("written resume", str(caught.exception))

    def test_consent_is_still_required(self):
        with self.assertRaises(d7.RedLineError):
            d7.guard(resume_payload(consent=False))

    def test_identifying_fields_and_person_scores_are_still_refused(self):
        for field in ("visa_status", "country_of_origin", "employability_score"):
            with self.subTest(field=field):
                with self.assertRaises(d7.RedLineError):
                    d7.guard(resume_payload(**{field: "x"}))

    def test_prepare_sends_the_resume_lines_not_a_transcript(self):
        prepared = d7.prepare(resume_payload())
        self.assertEqual(set(prepared),
                         {"resume", "candidate_units", "anzsco", "osca", "qualification"})
        self.assertEqual(prepared["resume"], [{"line": 1, "text": "Head cook, hotel restaurant"}])


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
        self.assertEqual(set(prepared),
                         {"transcript", "candidate_units", "anzsco", "osca", "qualification"})

    def test_prepare_carries_the_seeded_qualification_code_and_title_only(self):
        """The live model checks a cited qualification against this; the rest of
        the registry record (status, PDF, packaging) is not the model's business."""
        prepared = d7.prepare(payload())
        self.assertEqual(prepared["qualification"],
                         {"code": "SIT30821", "title": "Certificate III in Commercial Cookery"})

    def test_the_live_model_keeps_a_qualification_prepare_offers(self):
        """The seam: before prepare() carried it, every qualification was dropped."""
        from skeleton.core import live
        item = {"field": "qualification", "value": "SIT30821 Certificate III in Commercial Cookery",
                "reason": "Both food safety units sit in its core.", "confidence": 0.5,
                "sources": [["transcript", "t=00:12"]]}

        def answer(url, headers, body):
            return {"content": [{"type": "text", "text": json.dumps([item])}]}

        model = live.LiveModel(fallback=None, api_key="k", post=answer)
        self.assertEqual(model.suggest(d7.KEY, d7.prepare(payload())), [item])


if __name__ == "__main__":
    unittest.main()
