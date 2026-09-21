"""Job matching counts evidence; it never scores the person.

The board is a committed snapshot of real Adzuna ads, refetched by hand, so
nothing here pins a job id or a count from today's file. Every expectation is
derived from whatever the snapshot currently holds.
"""
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


def _required(job):
    """The codes an ad asks for, whatever shape the snapshot is in."""
    return [u["code"] for u in (job.get("required_units") or ())]


def _mapped(jobs):
    """The ads that name at least one unit: the only ones with a count to make."""
    return [j for j in jobs if j["units_status"] == d7_match.MAPPED]


def _fake(job_id, occupation, required, **rest):
    """One ad in snapshot shape. The two empty cases have to be testable even
    when the committed snapshot happens to hold neither."""
    job = {"id": job_id, "occupation": occupation, "title": "Cook", "company": "A Kitchen",
           "location": "Sydney, Sydney Region", "contract_type": "permanent",
           "contract_time": "full_time", "created": "2026-09-17T14:18:08Z",
           "redirect_url": "https://www.adzuna.com.au/land/ad/" + job_id,
           "snippet": "A short ad.", "required_units": required, "mapped_by": None}
    job.update(rest)
    return job


class Matching(unittest.TestCase):
    def test_matched_is_required_and_evidenced_missing_is_the_rest(self):
        evidenced = {u["code"] for u in EVIDENCED}
        ads = {j["id"]: j for j in d7_match.load_jobs()}
        counted = _mapped(d7_match.match_jobs("cookery", EVIDENCED))

        self.assertTrue(counted, "the snapshot holds no mapped cookery ad")
        for job in counted:
            required = _required(ads[job["id"]])
            with self.subTest(job=job["id"]):
                self.assertEqual([u["code"] for u in job["matched"]],
                                 [c for c in required if c in evidenced])
                self.assertEqual([u["code"] for u in job["missing"]],
                                 [c for c in required if c not in evidenced])
                self.assertEqual(job["fit"], f"{len(job['matched'])} of {len(required)} "
                                             "required units evidenced")

    def test_only_jobs_for_the_occupation_come_back_best_fit_first(self):
        jobs = d7_match.match_jobs("cookery", EVIDENCED)

        self.assertEqual({j["id"] for j in jobs},
                         {j["id"] for j in d7_match.load_jobs() if j["occupation"] == "cookery"})
        counts = [len(j["matched"]) for j in jobs]
        self.assertEqual(counts, sorted(counts, reverse=True))

    def test_a_unit_without_sources_never_counts(self):
        claimed = [{"code": "SITHCCC043", "sources": []}, {"code": "SITHCCC036"}]

        for job in d7_match.match_jobs("cookery", claimed):
            with self.subTest(job=job["id"]):
                self.assertEqual(job["matched"], [])
                if job["units_status"] == d7_match.MAPPED:
                    self.assertTrue(job["fit"].startswith("0 of "))

    def test_every_matched_unit_carries_its_sources_and_the_words_it_came_from(self):
        for job in d7_match.match_jobs("cookery", EVIDENCED):
            for unit in job["matched"]:
                with self.subTest(job=job["id"], unit=unit["code"]):
                    self.assertTrue(unit["sources"])
                    self.assertTrue(unit["title"])
                    # The ad's own words travel with the unit, and say which of
                    # the ad and the job title they were read from.
                    self.assertTrue(unit["quote"])
                    self.assertIn(unit["basis"], {"stated", "title"})

    def test_a_missing_unit_carries_its_quote_and_basis_too(self):
        """A unit is no less quoted for not being evidenced yet."""
        for job in d7_match.match_jobs("cookery", EVIDENCED):
            for unit in job["missing"]:
                with self.subTest(job=job["id"], unit=unit["code"]):
                    self.assertTrue(unit["quote"])
                    self.assertIn(unit["basis"], {"stated", "title"})
                    self.assertNotIn("sources", unit)

    def test_the_fit_is_a_count_never_a_percentage_or_score(self):
        for occupation in ("cookery", "welding", "aged_care"):
            for job in d7_match.match_jobs(occupation, EVIDENCED):
                with self.subTest(job=job["id"]):
                    self.assertNotIn("%", job["fit"])
                    if job["units_status"] == d7_match.MAPPED:
                        self.assertRegex(job["fit"], r"^\d+ of \d+ required units evidenced$")
                    else:
                        self.assertIn(job["fit"], {d7_match.NONE_NAMED_FIT, d7_match.NOT_MAPPED_FIT})
                    self.assertFalse({"score", "rank", "percent", "rating"} & set(job))

    def test_an_unknown_occupation_is_refused(self):
        with self.assertRaises(KeyError):
            d7_match.match_jobs("plumbing", EVIDENCED)


class AllJobs(unittest.TestCase):
    """The board lists every job; other occupations' jobs are counted, not hidden."""

    def test_every_job_once_the_occupation_first_in_match_order(self):
        board = d7_match.all_jobs("cookery", EVIDENCED)
        ours = d7_match.match_jobs("cookery", EVIDENCED)

        self.assertEqual(sorted(j["id"] for j in board),
                         sorted(j["id"] for j in d7_match.load_jobs()))
        self.assertEqual([j["id"] for j in board[:len(ours)]], [j["id"] for j in ours])
        self.assertTrue(all(j["for_occupation"] for j in board[:len(ours)]))
        self.assertFalse(any(j["for_occupation"] for j in board[len(ours):]))

    def test_a_job_counts_the_same_as_match_jobs(self):
        ours = {j["id"]: j for j in d7_match.match_jobs("cookery", EVIDENCED)}
        for job in d7_match.all_jobs("cookery", EVIDENCED):
            if job["id"] in ours:
                with self.subTest(job=job["id"]):
                    same = {k: v for k, v in job.items()
                            if k not in ("occupation", "occupation_label", "for_occupation")}
                    self.assertEqual(same, ours[job["id"]])

    def test_other_occupations_show_zero_of_their_required_units(self):
        required = {j["id"]: len(_required(j)) for j in d7_match.load_jobs()}
        others = [j for j in d7_match.all_jobs("cookery", EVIDENCED) if not j["for_occupation"]]

        self.assertEqual({j["id"] for j in others},
                         {j["id"] for j in d7_match.load_jobs() if j["occupation"] != "cookery"})
        for job in others:
            with self.subTest(job=job["id"]):
                self.assertEqual(job["matched"], [])
                self.assertEqual(len(job["missing"]), required[job["id"]])
                if job["units_status"] == d7_match.MAPPED:
                    self.assertEqual(job["fit"],
                                     f"0 of {required[job['id']]} required units evidenced")
                self.assertTrue(job["occupation_label"])

    def test_the_board_never_carries_a_percentage_or_score(self):
        """Only what this module writes is checked. A "%" inside an ad's own
        words is the employer's shift loading, not a score we invented, and
        passing it through verbatim is the point of quoting the ad."""
        written = ("id", "employment_type", "salary", "fit", "units_status",
                   "occupation_label")
        for job in d7_match.all_jobs("welding", EVIDENCED):
            with self.subTest(job=job["id"]):
                self.assertNotIn("%", json.dumps({k: job[k] for k in written}))
                if job["units_status"] == d7_match.MAPPED:
                    self.assertRegex(job["fit"], r"^\d+ of \d+ required units evidenced$")
                self.assertFalse({"score", "rank", "percent", "rating"} & set(job))

    def test_the_board_never_carries_the_posting_date(self):
        """Adzuna sends "created" and the snapshot keeps it; showing how long an
        ad has been up is one of the things this board does not do."""
        for job in d7_match.all_jobs("cookery", EVIDENCED):
            with self.subTest(job=job["id"]):
                self.assertNotIn("created", job)
                self.assertNotIn("applicants", job)

    def test_an_unknown_occupation_is_refused(self):
        with self.assertRaises(KeyError):
            d7_match.all_jobs("plumbing", EVIDENCED)


class AdWithNoUnits(unittest.TestCase):
    """[] and None are different facts about an ad and are reported apart.

    Both are built here rather than read from the snapshot: a refetch may leave
    the file with neither, and the rule holds regardless of what it holds today.
    """

    def board(self, jobs):
        with mock.patch.object(d7_match, "load_jobs", return_value=jobs):
            return d7_match.all_jobs("cookery", EVIDENCED)

    def test_an_ad_that_names_no_unit_is_not_a_zero_of_zero(self):
        job, = self.board([_fake("empty", "cookery", [])])

        self.assertEqual(job["units_status"], d7_match.NONE_NAMED)
        self.assertEqual(job["fit"], d7_match.NONE_NAMED_FIT)
        self.assertEqual((job["matched"], job["missing"]), ([], []))
        self.assertNotIn("0 of 0", job["fit"])

    def test_an_unmapped_ad_says_so_in_its_own_words(self):
        job, = self.board([_fake("unmapped", "cookery", None)])

        self.assertEqual(job["units_status"], d7_match.NOT_MAPPED)
        self.assertEqual(job["fit"], d7_match.NOT_MAPPED_FIT)
        self.assertNotEqual(job["fit"], d7_match.NONE_NAMED_FIT)

    def test_neither_is_dropped_from_the_board_or_from_the_occupation(self):
        jobs = [_fake("empty", "cookery", []), _fake("unmapped", "cookery", None),
                _fake("welder", "welding", [])]
        self.assertEqual({j["id"] for j in self.board(jobs)},
                         {"empty", "unmapped", "welder"})
        with mock.patch.object(d7_match, "load_jobs", return_value=jobs):
            self.assertEqual({j["id"] for j in d7_match.match_jobs("cookery", EVIDENCED)},
                             {"empty", "unmapped"})

    def test_neither_carries_a_percentage_and_courses_ask_nothing_of_them(self):
        board = self.board([_fake("empty", "cookery", []), _fake("unmapped", "cookery", None)])

        self.assertNotIn("%", json.dumps(board))
        self.assertEqual(d7_match.courses_for(board), [])


class AdzunaFields(unittest.TestCase):
    """What a card shows comes from the ad, or is left out."""

    def board(self, job):
        with mock.patch.object(d7_match, "load_jobs", return_value=[job]):
            return d7_match.all_jobs("cookery", EVIDENCED)[0]

    def test_employment_type_joins_whichever_halves_the_ad_stated(self):
        cases = {("full_time", "permanent"): "Full-time · Permanent",
                 ("part_time", None): "Part-time",
                 (None, "contract"): "Contract",
                 (None, None): ""}
        for (time, kind), expected in cases.items():
            with self.subTest(contract_time=time, contract_type=kind):
                job = self.board(_fake("x", "cookery", [], contract_time=time, contract_type=kind))
                self.assertEqual(job["employment_type"], expected)

    def test_a_salary_shows_only_when_the_employer_stated_one(self):
        self.assertEqual(self.board(_fake("x", "cookery", []))["salary"], "")
        self.assertEqual(
            self.board(_fake("x", "cookery", [], salary_min=80000, salary_max=90000))["salary"],
            "$80,000 - $90,000")
        # One figure, not a range invented from it.
        self.assertEqual(
            self.board(_fake("x", "cookery", [], salary_min=124800, salary_max=124800))["salary"],
            "$124,800")

    def test_the_employer_and_the_link_travel_to_the_page(self):
        job = self.board(_fake("5887149079", "cookery", []))
        self.assertEqual(job["company"], "A Kitchen")
        self.assertIn("adzuna.com.au", job["redirect_url"])
        self.assertTrue(job["snippet"])


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

        self.assertTrue(courses, "no cookery ad in the snapshot has a gap unit")
        for code, course in courses.items():
            with self.subTest(code=code):
                # The jobs a unit would open, in the order the board lists them.
                self.assertEqual(course["for_jobs"],
                                 [j["id"] for j in jobs
                                  if code in {u["code"] for u in j["missing"]}])
                self.assertRegex(course["qualification"], r"^[A-Z]{3}\d{5} ")
                self.assertEqual(course["note"],
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
        """The units this job asks for move up; the rest keep the pack's order."""
        pack = [u["code"] for u in EVIDENCED]
        for job in self.jobs:
            matched = {u["code"] for u in job["matched"]}
            with self.subTest(job=job["id"]):
                self.assertEqual(_skill_codes(self.texts[job["id"]]),
                                 [c for c in pack if c in matched]
                                 + [c for c in pack if c not in matched])

    def test_the_lines_that_evidence_the_job_come_first(self):
        """Then by timestamp within each group, so a draft still reads in order."""
        cited = {u["code"]: [s[1][2:] for s in u["sources"]] for u in EVIDENCED}
        for job in self.jobs:
            for_job = {t for u in job["matched"] for t in cited[u["code"]]}
            rest = {t for stamps in cited.values() for t in stamps} - for_job
            with self.subTest(job=job["id"]):
                self.assertEqual(_experience_stamps(self.texts[job["id"]]),
                                 sorted(for_job) + sorted(rest))

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
        for job_id, sections in self.sections.items():
            with self.subTest(job=job_id):
                self.assertEqual({s["code"]: s["described_at"] for s in sections["skills"]},
                                 {"SITXFSA005": ["9"], "SITHCCC027": ["10"], "SITHCCC029": ["2"]})
                self.assertIn("SITXFSA005 Use hygienic practices for food safety (resume line 9)",
                              self.texts[job_id])

    def test_lines_sort_by_number_not_as_text(self):
        """Line 10 comes after line 9, not before line 2, in every draft."""
        for job_id, sections in self.sections.items():
            for_job = {t for s in sections["skills"] if s["for_this_job"] for t in s["described_at"]}
            rest = {"2", "9", "10"} - for_job
            with self.subTest(job=job_id):
                self.assertEqual([e["line"] for e in sections["experience"]],
                                 sorted(for_job, key=int) + sorted(rest, key=int))

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
    """The committed snapshot of real Adzuna ads, as the page will read it."""

    def test_the_snapshot_says_where_it_came_from_and_when(self):
        meta = d7_match.snapshot_meta()
        self.assertEqual(meta["source"], "Adzuna")
        self.assertEqual(meta["attribution"], "Jobs by Adzuna")
        # Licensing and honesty both rest on the date: the board is a snapshot.
        self.assertRegex(meta["fetched_at"], r"^\d{4}-\d{2}-\d{2}T")

    def test_every_ad_carries_what_a_card_needs_and_a_link_back_to_adzuna(self):
        jobs = d7_match.load_jobs()
        self.assertTrue(jobs)
        self.assertEqual(len({j["id"] for j in jobs}), len(jobs))
        for job in jobs:
            with self.subTest(job=job["id"]):
                self.assertTrue(job["title"])
                self.assertIn(job["occupation"], d7_match._occupations())
                self.assertRegex(job["redirect_url"], r"^https://www\.adzuna\.com\.au/")
                self.assertIn(job.get("contract_time"), {None, "full_time", "part_time"})
                self.assertIn(job.get("contract_type"), {None, "permanent", "contract"})

    def test_no_ad_carries_a_predicted_salary_or_an_applicant_count(self):
        """Adzuna's terms require a predicted salary to be labelled as such, so
        fetch_jobs.py keeps only employer-stated ones and the page shows those."""
        for job in d7_match.load_jobs():
            with self.subTest(job=job["id"]):
                self.assertNotIn("salary_is_predicted", job)
                self.assertNotIn("applicants", job)

    def test_every_required_unit_is_a_seeded_unit_of_its_occupation_and_is_quoted(self):
        occupations = d7_match._occupations()
        for job in d7_match.load_jobs():
            codes = {u["code"] for u in occupations[job["occupation"]]["units"]}
            for unit in (job["required_units"] or ()):
                with self.subTest(job=job["id"], code=unit["code"]):
                    self.assertIn(unit["code"], codes)
                    self.assertIn(unit["basis"], {"stated", "title"})
                    # A single word cannot stand as the citation for a unit.
                    self.assertGreaterEqual(len(unit["quote"].strip()), 12)

    def test_an_unmapped_ad_is_null_and_an_ad_that_named_nothing_is_empty(self):
        """The two are never collapsed into one another in the file either."""
        for job in d7_match.load_jobs():
            required = job["required_units"]
            with self.subTest(job=job["id"]):
                self.assertTrue(required is None or isinstance(required, list))
                if required is None:
                    self.assertIsNone(job["mapped_by"])

    def test_the_invented_sample_board_is_still_on_disk_and_is_no_longer_read(self):
        """Deciding jobs.json's fate is not this module's job, but the product
        reads real ads now, so nothing here may fall back to it."""
        self.assertTrue(d7_match.SAMPLE_JOBS.exists())
        self.assertEqual(d7_match.JOBS.name, "jobs_adzuna.json")


if __name__ == "__main__":
    unittest.main()
