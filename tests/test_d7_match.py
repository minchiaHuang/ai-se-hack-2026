"""Job matching counts evidence; it never scores the person."""
import json
import re
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from skeleton.directions import d7_match

ROOT = Path(__file__).resolve().parent.parent
PLAN = ROOT / "docs" / "superpowers" / "plans" / "2026-09-21-direction-7-implementation.md"
_patch = None


def setUpModule():
    """occupations.json is created by another package. Until it lands, read the
    verified seed from the plan's Task 1, which is where that file comes from."""
    global _patch
    if d7_match.OCCUPATIONS.exists():
        return
    seed = re.search(r"```json\n(.*?)```", PLAN.read_text(encoding="utf-8"), re.S).group(1)
    tmp = Path(tempfile.mkdtemp()) / "occupations.json"
    tmp.write_text(seed, encoding="utf-8")
    _patch = mock.patch.object(d7_match, "OCCUPATIONS", tmp)
    _patch.start()


def tearDownModule():
    if _patch:
        _patch.stop()


TRANSCRIPT = [
    {"t": "00:12", "text": "我在營區廚房做了三年飯。", "en": "I cooked in the camp kitchen for three years."},
    {"t": "01:05", "text": "我們每天做湯和醬汁。", "en": "We made soups and sauces every day."},
    {"t": "02:41", "text": "每次都先洗手、分開生熟食。", "en": "I always washed my hands and kept raw and cooked food apart."},
    {"t": "03:30", "text": "我逃離時一路走到邊境。", "en": "When I fled I walked to the border."},
]

EVIDENCED = [
    {"code": "SITXFSA005", "sources": [["transcript", "t=02:41"]]},
    {"code": "SITXFSA006", "sources": [["transcript", "t=02:41"]]},
    {"code": "SITHCCC027", "sources": [["transcript", "t=00:12"]]},
    {"code": "SITHCCC029", "sources": [["transcript", "t=01:05"]]},
]


def _job(jobs, job_id):
    return next(j for j in jobs if j["id"] == job_id)


class Matching(unittest.TestCase):
    def test_matched_is_required_and_evidenced_missing_is_the_rest(self):
        job = _job(d7_match.match_jobs("cookery", EVIDENCED), "cookery-1")

        self.assertEqual([u["code"] for u in job["matched"]],
                         ["SITHCCC027", "SITXFSA005", "SITXFSA006"])
        self.assertEqual([u["code"] for u in job["missing"]], ["SITHCCC043"])
        self.assertEqual(job["fit"], "3 of 4 required units evidenced")
        self.assertEqual(job["note"], "Representative sample, not a real listing")

    def test_only_jobs_for_the_occupation_come_back_best_fit_first(self):
        jobs = d7_match.match_jobs("cookery", EVIDENCED)

        self.assertEqual([j["id"] for j in jobs],
                         ["cookery-5", "cookery-1", "cookery-3", "cookery-6", "cookery-7",
                          "cookery-8", "cookery-2", "cookery-4", "cookery-9"])
        counts = [len(j["matched"]) for j in jobs]
        self.assertEqual(counts, sorted(counts, reverse=True))

    def test_a_unit_without_sources_never_counts(self):
        claimed = [{"code": "SITHCCC043", "sources": []}, {"code": "SITHCCC036"}]

        for job in d7_match.match_jobs("cookery", claimed):
            with self.subTest(job=job["id"]):
                self.assertEqual(job["matched"], [])
                self.assertTrue(job["fit"].startswith("0 of "))

    def test_every_matched_unit_carries_its_sources(self):
        for job in d7_match.match_jobs("cookery", EVIDENCED):
            for unit in job["matched"]:
                with self.subTest(job=job["id"], unit=unit["code"]):
                    self.assertTrue(unit["sources"])
                    self.assertTrue(unit["title"])

    def test_the_fit_is_a_count_never_a_percentage_or_score(self):
        for occupation in ("cookery", "welding", "aged_care"):
            for job in d7_match.match_jobs(occupation, EVIDENCED):
                with self.subTest(job=job["id"]):
                    self.assertNotIn("%", job["fit"])
                    self.assertRegex(job["fit"], r"^\d+ of \d+ required units evidenced$")
                    self.assertFalse({"score", "rank", "percent", "rating"} & set(job))

    def test_an_unknown_occupation_is_refused(self):
        with self.assertRaises(KeyError):
            d7_match.match_jobs("plumbing", EVIDENCED)


class Courses(unittest.TestCase):
    def test_courses_are_exactly_the_missing_units_never_an_evidenced_one(self):
        jobs = d7_match.match_jobs("cookery", EVIDENCED)
        courses = d7_match.courses_for(jobs)

        missing = {u["code"] for j in jobs for u in j["missing"]}
        self.assertEqual({c["code"] for c in courses}, missing)
        self.assertFalse({c["code"] for c in courses} & {u["code"] for u in EVIDENCED})

    def test_a_course_names_its_qualification_and_the_jobs_it_opens(self):
        jobs = d7_match.match_jobs("cookery", EVIDENCED)
        courses = {c["code"]: c for c in d7_match.courses_for(jobs)}

        self.assertEqual(courses["SITHCCC043"]["for_jobs"],
                         ["cookery-1", "cookery-7", "cookery-2", "cookery-9"])
        self.assertEqual(courses["SITHCCC036"]["for_jobs"],
                         ["cookery-7", "cookery-8", "cookery-2", "cookery-9"])
        self.assertEqual(courses["SITHCCC036"]["qualification"],
                         "SIT30821 Certificate III in Commercial Cookery")
        self.assertEqual(courses["SITHCCC036"]["note"],
                         "Gap training through a Registered Training Organisation")

    def test_courses_opening_more_jobs_come_first(self):
        courses = d7_match.courses_for(d7_match.match_jobs("cookery", EVIDENCED))
        counts = [len(c["for_jobs"]) for c in courses]
        self.assertEqual(counts, sorted(counts, reverse=True))


class Resume(unittest.TestCase):
    def setUp(self):
        self.jobs = d7_match.match_jobs("cookery", EVIDENCED)
        self.text = d7_match.resume_for(self.jobs[0], EVIDENCED, TRANSCRIPT)

    def test_it_holds_no_unit_the_person_did_not_evidence(self):
        seeded = {u["code"] for occ in d7_match._occupations().values() for u in occ["units"]}
        evidenced = {u["code"] for u in EVIDENCED}
        for code in seeded - evidenced:
            with self.subTest(code=code):
                self.assertNotIn(code, self.text)

    def test_every_experience_line_traces_to_a_timestamp(self):
        section = self.text.split("WORK EXPERIENCE")[1].split("\n\n")[0]
        experience = [l for l in section.splitlines() if l.startswith("- ")]
        self.assertEqual(len(experience), 3)
        for line in experience:
            with self.subTest(line=line):
                self.assertRegex(line, r"\[transcript \d\d:\d\d\]$")

    def test_a_line_no_unit_cites_stays_out(self):
        """What the person volunteers about their journey is never extracted."""
        self.assertNotIn("border", self.text)

    def test_it_claims_recognition_in_progress_not_a_held_qualification(self):
        self.assertIn("Recognition of Prior Learning in progress", self.text)
        self.assertNotIn("holder", self.text.lower())

    def test_it_never_carries_the_fit(self):
        self.assertNotIn("required units evidenced", self.text)
        self.assertNotIn("%", self.text)


def _skill_codes(text):
    section = text.split("SKILLS MAPPED")[1].split("\n\n")[0]
    return [l.split()[1] for l in section.splitlines() if l.startswith("- ")]


def _experience_stamps(text):
    section = text.split("WORK EXPERIENCE")[1].split("\n\n")[0]
    return re.findall(r"\[transcript (\d\d:\d\d)\]$", section, re.M)


class TailoredResume(unittest.TestCase):
    """One resume per job, tailored by ordering alone: never a new claim."""

    def setUp(self):
        self.jobs = d7_match.match_jobs("cookery", EVIDENCED)
        self.texts = {job["id"]: d7_match.resume_for(job, EVIDENCED, TRANSCRIPT)
                      for job in self.jobs}

    def test_each_job_lists_its_required_and_evidenced_units_first(self):
        self.assertEqual(_skill_codes(self.texts["cookery-1"]),
                         ["SITXFSA005", "SITXFSA006", "SITHCCC027", "SITHCCC029"])
        self.assertEqual(_skill_codes(self.texts["cookery-2"]),
                         ["SITHCCC027", "SITHCCC029", "SITXFSA005", "SITXFSA006"])
        for job in self.jobs:
            matched = [u["code"] for u in job["matched"]]
            with self.subTest(job=job["id"]):
                codes = _skill_codes(self.texts[job["id"]])
                self.assertEqual(set(codes[:len(matched)]), set(matched))

    def test_the_lines_that_evidence_the_job_come_first(self):
        self.assertEqual(_experience_stamps(self.texts["cookery-1"]), ["00:12", "02:41", "01:05"])
        self.assertEqual(_experience_stamps(self.texts["cookery-2"]), ["00:12", "01:05", "02:41"])

    def test_tailoring_only_reorders_the_same_claims(self):
        def claims(text):
            return sorted(l for l in text.splitlines()[1:] if l.strip())
        first, *others = self.texts.values()
        for other in others:
            self.assertEqual(claims(other), claims(first))

    def test_no_resume_holds_an_unevidenced_unit_a_percentage_or_an_uncited_line(self):
        seeded = {u["code"] for occ in d7_match._occupations().values() for u in occ["units"]}
        unevidenced = seeded - {u["code"] for u in EVIDENCED}
        for job_id, text in self.texts.items():
            with self.subTest(job=job_id):
                self.assertFalse({code for code in unevidenced if code in text})
                self.assertNotIn("%", text)
                self.assertNotIn("required units evidenced", text)
                self.assertNotIn("border", text)
                self.assertNotIn("03:30", text)

    def test_the_text_is_rendered_from_the_sections(self):
        for job in self.jobs:
            sections = d7_match.resume_sections(job, EVIDENCED, TRANSCRIPT)
            with self.subTest(job=job["id"]):
                self.assertEqual(d7_match.resume_text(sections), self.texts[job["id"]])
                self.assertEqual(sections["job"]["id"], job["id"])
                self.assertFalse({"fit", "missing", "matched", "score"} & set(sections))
                for q in sections["qualifications"]:
                    self.assertEqual(q["status"],
                                     "Recognition of Prior Learning in progress, not yet assessed")


RESUME = [
    {"line": 1, "text": "Head cook, hotel restaurant", "en": "Head cook, hotel restaurant"},
    {"line": 2, "text": "Made soups and sauces every day.", "en": "Made soups and sauces every day."},
    {"line": 9, "text": "Kept raw and cooked food apart.", "en": "Kept raw and cooked food apart."},
    {"line": 10, "text": "Cooked for 150 guests a day.", "en": "Cooked for 150 guests a day."},
    {"line": 11, "text": "In 2019 I fled and walked to the border.", "en": "In 2019 I fled and walked to the border."},
]

RESUME_EVIDENCED = [
    {"code": "SITXFSA005", "sources": [["resume", "line=9"]]},
    {"code": "SITHCCC027", "sources": [["resume", "line=10"]]},
    {"code": "SITHCCC029", "sources": [["resume", "line=2"]]},
]


class ResumeSource(unittest.TestCase):
    """A draft built from the resume the person brought cites that resume's lines."""

    def setUp(self):
        self.jobs = d7_match.match_jobs("cookery", RESUME_EVIDENCED)
        self.sections = {job["id"]: d7_match.resume_sections(job, RESUME_EVIDENCED, RESUME, "resume")
                         for job in self.jobs}
        self.texts = {k: d7_match.resume_text(v) for k, v in self.sections.items()}

    def test_every_experience_line_cites_a_resume_line(self):
        for job_id, text in self.texts.items():
            section = text.split("WORK EXPERIENCE")[1].split("\n\n")[0]
            experience = [l for l in section.splitlines() if l.startswith("- ")]
            with self.subTest(job=job_id):
                self.assertEqual(len(experience), 3)
                for line in experience:
                    self.assertRegex(line, r"\[resume line \d+\]$")
                self.assertNotIn("transcript", text)

    def test_skills_name_the_resume_lines_they_come_from(self):
        skills = self.sections["cookery-1"]["skills"]
        self.assertEqual({s["code"]: s["described_at"] for s in skills},
                         {"SITXFSA005": ["9"], "SITHCCC027": ["10"], "SITHCCC029": ["2"]})
        self.assertIn("SITXFSA005 Use hygienic practices for food safety (resume line 9)",
                      self.texts["cookery-1"])

    def test_lines_sort_by_number_not_as_text(self):
        """Line 10 comes after line 9, not before line 2."""
        lines = [e["line"] for e in self.sections["cookery-2"]["experience"]]
        self.assertEqual(lines, ["2", "10", "9"])

    def test_a_journey_line_no_unit_cites_never_reaches_a_draft(self):
        for job_id, text in self.texts.items():
            with self.subTest(job=job_id):
                self.assertNotIn("border", text)
                self.assertNotIn("resume line 11", text)

    def test_the_interview_output_carries_no_source_key(self):
        """The interview's draft is exactly what it was before resumes came in."""
        sections = d7_match.resume_sections(self.jobs[0], EVIDENCED, TRANSCRIPT)
        self.assertNotIn("source", sections)
        self.assertEqual(self.sections[self.jobs[0]["id"]]["source"], "resume")


class JobData(unittest.TestCase):
    def test_nine_cookery_four_welding_four_aged_care_all_marked_as_samples(self):
        jobs = d7_match.load_jobs()
        self.assertEqual(len(jobs), 17)
        for occupation, count in (("cookery", 9), ("welding", 4), ("aged_care", 4)):
            self.assertEqual(sum(j["occupation"] == occupation for j in jobs), count)
        for job in jobs:
            with self.subTest(job=job["id"]):
                self.assertEqual(job["note"], "Representative sample, not a real listing")

    def test_every_job_has_a_board_row_and_nothing_a_sample_cannot_honestly_carry(self):
        """Salaries, posted dates and applicant counts would read as a real
        listing, so a sample never carries them."""
        jobs = d7_match.load_jobs()
        self.assertEqual(len({j["id"] for j in jobs}), len(jobs))
        for job in jobs:
            with self.subTest(job=job["id"]):
                self.assertIn(job["employment_type"], {"Full-time", "Part-time", "Casual"})
                self.assertRegex(job["location"], r" NSW$")
                self.assertTrue(job["level"] and job["shift"] and job["setting"])
                self.assertFalse({"salary", "pay", "posted", "applicants", "employer", "company"} & set(job))
                self.assertNotRegex(json.dumps(job), r"\$|\d+ ?(days?|hours?) ago|applicant")

    def test_every_required_unit_is_a_seeded_unit_of_its_occupation(self):
        occupations = d7_match._occupations()
        for job in d7_match.load_jobs():
            codes = {u["code"] for u in occupations[job["occupation"]]["units"]}
            for code in job["required_units"]:
                with self.subTest(job=job["id"], code=code):
                    self.assertIn(code, codes)

    def test_one_cookery_job_needs_the_nsw_food_safety_supervisor_pair(self):
        self.assertTrue(any({"SITXFSA005", "SITXFSA006"} <= set(j["required_units"])
                            for j in d7_match.load_jobs() if j["occupation"] == "cookery"))


if __name__ == "__main__":
    unittest.main()
