"""The Adzuna snapshot tool, fully offline: recorded responses, no keys."""
import contextlib
import io
import json
import os
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock

from skeleton.tools import fetch_jobs

# Shaped like an Adzuna search result (developer.adzuna.com, 2026-09-21).
COOK = {
    "id": "4821", "title": "<strong>Cook</strong> - Cafe",
    "description": "Busy Parramatta cafe needs a cook. You will prepare dishes "
                   "for a la carte service and follow food safety &amp; hygiene rules.",
    "company": {"display_name": "Harbour Cafe Pty Ltd"},
    "location": {"display_name": "Parramatta, Sydney", "area": ["Australia", "New South Wales"]},
    "category": {"label": "Hospitality & Catering Jobs"},
    "salary_min": 65000, "salary_max": 70000, "salary_is_predicted": "0",
    "contract_type": "permanent", "contract_time": "full_time",
    "created": "2026-09-18T03:12:44Z", "redirect_url": "https://www.adzuna.com.au/land/ad/4821",
    "latitude": -33.8, "longitude": 151.0,
}
PREDICTED = dict(COOK, id="4822", salary_is_predicted="1")
WELDER = dict(COOK, id="9001", title="Welder", description="MIG welder wanted.")

CLEAR = {"ADZUNA_APP_ID": "", "ADZUNA_APP_KEY": "", "ANTHROPIC_API_KEY": "",
         "ANTHROPIC_MODEL": ""}
KEYS = dict(CLEAR, ADZUNA_APP_ID="id-123", ADZUNA_APP_KEY="key-456")


def searching(by_term):
    """A fake get that answers each search term with its recorded results."""
    calls = []

    def fake_get(url):
        calls.append(url)
        what = fetch_jobs.urllib.parse.parse_qs(url.split("?", 1)[1])["what"][0]
        return {"results": by_term.get(what, [])}
    fake_get.calls = calls
    return fake_get


def answering(items):
    def fake_post(url, headers, payload):
        return {"content": [{"type": "text", "text": json.dumps(items)}]}
    return fake_post


def run(get=None, post=None, env=CLEAR):
    """main() with the environment replaced, output captured, file in a temp dir."""
    out, err = io.StringIO(), io.StringIO()
    with tempfile.TemporaryDirectory() as tmp, \
            mock.patch.dict(os.environ, env), \
            contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        path = Path(tmp) / "jobs_adzuna.json"
        code = fetch_jobs.main(get=get, post=post, out=path,
                               now=datetime(2026, 9, 21, tzinfo=timezone.utc),
                               sleep=lambda _seconds: None)
        saved = json.loads(path.read_text()) if path.exists() else None
    return code, saved, out.getvalue(), err.getvalue()


class Fetch(unittest.TestCase):
    def test_only_the_needed_fields_are_kept_and_markup_is_stripped(self):
        job = fetch_jobs.keep(COOK, "cookery")
        self.assertEqual(set(job), {
            "id", "occupation", "title", "company", "location", "contract_type",
            "contract_time", "created", "redirect_url", "snippet",
            "salary_min", "salary_max"})
        self.assertEqual(job["title"], "Cook - Cafe")
        self.assertEqual(job["company"], "Harbour Cafe Pty Ltd")
        self.assertIn("food safety & hygiene", job["snippet"])
        self.assertEqual((job["salary_min"], job["salary_max"]), (65000, 70000))

    def test_a_predicted_salary_is_dropped(self):
        """Kept, it would need Adzuna's Jobsworth label on the page."""
        job = fetch_jobs.keep(PREDICTED, "cookery")
        self.assertNotIn("salary_min", job)
        self.assertNotIn("salary_max", job)

    def test_a_job_found_by_two_searches_is_kept_once(self):
        get = searching({"cook": [COOK, PREDICTED], "commercial cook": [COOK]})
        jobs = fetch_jobs.fetch("id", "key", get)
        self.assertEqual([j["id"] for j in jobs], ["4821", "4822"])

    def test_it_stays_far_below_the_rate_limit_and_caps_each_occupation(self):
        many = [dict(COOK, id=str(n)) for n in range(25)]
        get = searching({"cook": many, "commercial cook": many})
        jobs = fetch_jobs.fetch("id", "key", get)
        self.assertEqual(len(get.calls), 6)
        self.assertEqual(len(jobs), fetch_jobs.PER_OCCUPATION)
        self.assertTrue(all("/jobs/au/search/" in url and "where=Sydney" in url
                            for url in get.calls))


CANDIDATES = [{"code": "SITHCCC027", "title": "Prepare dishes using basic methods of cookery"},
              {"code": "SITXFSA005", "title": "Use hygienic practices for food safety"}]

THREE = CANDIDATES + [{"code": "SITXFSA006", "title": "Participate in safe food handling practices"}]
COOK_UNIT = {"code": "SITHCCC043", "title": "Work effectively as a cook"}


class Mapping(unittest.TestCase):
    def setUp(self):
        self.job = fetch_jobs.keep(COOK, "cookery")

    def test_a_unit_quoted_from_the_snippet_is_stated(self):
        post = answering([{"code": "SITHCCC027", "quote": "prepare dishes for a la carte",
                           "basis": "stated"}])
        self.assertEqual(fetch_jobs.required_units(self.job, CANDIDATES, "k", "m", post),
                         [{"code": "SITHCCC027", "quote": "prepare dishes for a la carte",
                           "basis": "stated"}])

    def test_a_unit_quoted_from_the_title_is_marked_title(self):
        """Adzuna's snippet is a teaser, so a unit may rest on the title alone.
        The page must be able to say so rather than imply the ad said it."""
        job = fetch_jobs.keep(dict(COOK, title="Commercial Cook - Aged Care Kitchen",
                                   description="Apply now."), "cookery")
        post = answering([{"code": "SITHCCC027", "quote": "Commercial Cook", "basis": "title"}])
        self.assertEqual(fetch_jobs.required_units(job, CANDIDATES, "k", "m", post),
                         [{"code": "SITHCCC027", "quote": "Commercial Cook", "basis": "title"}])

    def test_the_basis_recorded_is_where_the_quote_was_found(self):
        """The model's own label is not evidence; where the words are is."""
        post = answering([{"code": "SITHCCC027", "quote": "prepare dishes for a la carte",
                           "basis": "title"}])
        units = fetch_jobs.required_units(self.job, CANDIDATES, "k", "m", post)
        self.assertEqual(units[0]["basis"], "stated")

    def test_a_unit_outside_the_candidates_is_dropped(self):
        post = answering([{"code": "SITHCCC999", "quote": "prepare dishes for a la carte",
                           "basis": "stated"},
                          {"code": "SITXFSA005", "quote": "food safety & hygiene",
                           "basis": "stated"}])
        self.assertEqual(fetch_jobs.required_units(self.job, CANDIDATES, "k", "m", post),
                         [{"code": "SITXFSA005", "quote": "food safety & hygiene",
                           "basis": "stated"}])

    def test_a_quote_in_neither_the_snippet_nor_the_title_is_dropped(self):
        """A paraphrase is no citation: the page would cite words the ad never said."""
        post = answering([{"code": "SITHCCC027", "quote": "cooks meals from scratch",
                           "basis": "stated"},
                          {"code": "SITXFSA005", "quote": "", "basis": "title"}])
        self.assertEqual(fetch_jobs.required_units(self.job, CANDIDATES, "k", "m", post), [])

    def test_a_quote_shorter_than_the_minimum_is_dropped(self):
        """One word like "welding" cites nothing; it fits any welding ad."""
        job = fetch_jobs.keep(dict(COOK, description="MIG welding, Sydney."), "welding")
        post = answering([{"code": "SITHCCC027", "quote": "welding", "basis": "stated"}])
        self.assertEqual(fetch_jobs.required_units(job, CANDIDATES, "k", "m", post), [])
        self.assertEqual(fetch_jobs.MIN_QUOTE, 12)

    def test_a_vague_title_and_a_short_snippet_map_to_nothing(self):
        """Empty is the honest answer; the page says the ad was too short."""
        job = fetch_jobs.keep(WELDER, "welding")
        post = answering([{"code": "SITHCCC027", "quote": "prepare dishes for a la carte",
                           "basis": "stated"}])
        self.assertEqual(fetch_jobs.required_units(job, CANDIDATES, "k", "m", post), [])

    def test_a_stated_quote_may_carry_two_units(self):
        """Some words name two kinds of work, and the prompt allows it."""
        post = answering([{"code": c, "quote": "food safety & hygiene", "basis": "stated"}
                          for c in ("SITXFSA005", "SITXFSA006")])
        units = fetch_jobs.required_units(self.job, THREE, "k", "m", post)
        self.assertEqual([(u["code"], u["basis"]) for u in units],
                         [("SITXFSA005", "stated"), ("SITXFSA006", "stated")])

    def test_a_stated_quote_used_for_three_units_is_dropped_for_all_three(self):
        """PR #16's real ad: "nutritious meals and snacks" stood for hygiene,
        food handling and cookery. A phrase that general evidences none of
        them, and code cannot tell which one it meant."""
        job = fetch_jobs.keep(dict(COOK, title="Cook", description=(
            "An experienced Cook to join the team to produce nutritious meals and snacks.")),
            "cookery")
        post = answering([{"code": c, "quote": "nutritious meals and snacks", "basis": "stated"}
                          for c in ("SITHCCC027", "SITXFSA005", "SITXFSA006")]
                         + [{"code": "SITHCCC043", "quote": "experienced Cook to join the team",
                             "basis": "stated"}])
        self.assertEqual(fetch_jobs.required_units(job, THREE + [COOK_UNIT], "k", "m", post),
                         [{"code": "SITHCCC043", "quote": "experienced Cook to join the team",
                           "basis": "stated"}])

    def test_an_overused_quote_that_is_also_the_title_is_demoted_to_title(self):
        """The words still support "a job with this title needs this", just
        not "the ad says so"."""
        job = fetch_jobs.keep(dict(COOK, title="Coded Welder | Sydney", description=(
            "We are seeking an experienced Coded Welder for our Sydney workshop.")), "cookery")
        post = answering([{"code": c, "quote": "Coded Welder", "basis": "stated"}
                          for c in ("SITHCCC027", "SITXFSA005", "SITXFSA006")])
        units = fetch_jobs.required_units(job, THREE, "k", "m", post)
        self.assertEqual([(u["code"], u["quote"], u["basis"]) for u in units],
                         [(c, "Coded Welder", "title")
                          for c in ("SITHCCC027", "SITXFSA005", "SITXFSA006")])

    def test_only_stated_quotes_are_limited(self):
        """A title quote already claims only what the title implies."""
        units = [{"code": c, "quote": "Commercial Cook", "basis": "title"}
                 for c in ("SITHCCC027", "SITXFSA005", "SITXFSA006")]
        self.assertEqual(fetch_jobs.limit_shared(units, "Commercial Cook"), units)

    def test_the_request_names_only_the_candidates_and_forbids_a_score(self):
        sent = {}

        def fake_post(url, headers, payload):
            sent.update(url=url, headers=headers, payload=payload)
            return {"content": [{"type": "text", "text": "[]"}]}

        fetch_jobs.required_units(self.job, CANDIDATES, "k", "claude-sonnet-5", fake_post)
        self.assertEqual(sent["url"], "https://api.anthropic.com/v1/messages")
        self.assertEqual(sent["headers"]["x-api-key"], "k")
        self.assertEqual(sent["payload"]["model"], "claude-sonnet-5")
        content = json.loads(sent["payload"]["messages"][0]["content"])
        self.assertEqual(content["candidate_units"], CANDIDATES)
        self.assertEqual(content["snippet"], self.job["snippet"])
        self.assertEqual(content["title"], self.job["title"])
        prompt = sent["payload"]["system"]
        self.assertIn("Never output a score", prompt)
        self.assertIn("3 to 6 units", prompt)
        self.assertIn("never write a quote shorter than 12 characters", prompt)


class Main(unittest.TestCase):
    def test_without_adzuna_keys_it_prints_how_to_run_and_exits_non_zero(self):
        code, saved, out, err = run()
        self.assertNotEqual(code, 0)
        self.assertIsNone(saved)
        self.assertIn("ADZUNA_APP_ID=... ADZUNA_APP_KEY=... "
                      "python3 -m skeleton.tools.fetch_jobs", err)

    def test_without_an_anthropic_key_jobs_are_saved_unmapped(self):
        code, saved, out, _ = run(get=searching({"cook": [COOK]}), env=KEYS)
        self.assertEqual(code, 0)
        self.assertEqual(saved["source"], "Adzuna")
        self.assertEqual(saved["attribution"], "Jobs by Adzuna")
        self.assertEqual(saved["fetched_at"], "2026-09-21T00:00:00+00:00")
        self.assertIsNone(saved["jobs"][0]["required_units"])
        self.assertIsNone(saved["jobs"][0]["mapped_by"])
        self.assertIn("ANTHROPIC_API_KEY is not set", out)

    def test_with_every_key_the_snapshot_is_mapped_and_carries_no_key(self):
        env = dict(KEYS, ANTHROPIC_API_KEY="sk-secret")
        post = answering([{"code": "SITHCCC027", "quote": "prepare dishes for a la carte",
                           "basis": "stated"}])
        code, saved, out, _ = run(get=searching({"cook": [COOK], "welder": [WELDER]}),
                                  post=post, env=env)
        self.assertEqual(code, 0)
        cook, welder = saved["jobs"]
        self.assertEqual(cook["required_units"],
                         [{"code": "SITHCCC027", "quote": "prepare dishes for a la carte",
                           "basis": "stated"}])
        self.assertEqual(cook["mapped_by"], "claude-sonnet-5")
        # Mapped, but nothing the ad says could be cited: [] rather than a guess.
        self.assertEqual(welder["required_units"], [])
        self.assertEqual(welder["mapped_by"], "claude-sonnet-5")
        text = json.dumps(saved)
        for secret in ("id-123", "key-456", "sk-secret"):
            self.assertNotIn(secret, text)
        self.assertIn("cookery: 1 jobs, 1 mapped units", out)

    def test_the_app_id_in_adzunas_own_redirect_url_is_saved(self):
        """Adzuna's tracking link carries the app id; it is the public link people click."""
        tracked = dict(COOK, redirect_url="https://www.adzuna.com.au/land/ad/4821?se=x&v=id-123")
        code, saved, _, err = run(get=searching({"cook": [tracked]}), env=KEYS)
        self.assertEqual(code, 0, err)
        self.assertIn("id-123", saved["jobs"][0]["redirect_url"])

    def test_a_key_anywhere_or_the_app_id_outside_redirect_url_is_refused(self):
        env = dict(KEYS, ANTHROPIC_API_KEY="sk-secret")
        leaks = [
            dict(COOK, description="Apply with id-123 today."),
            dict(COOK, redirect_url="https://www.adzuna.com.au/land/ad/4821?k=key-456"),
            dict(COOK, redirect_url="https://www.adzuna.com.au/land/ad/4821?k=sk-secret"),
        ]
        for leak in leaks:
            code, saved, _, err = run(get=searching({"cook": [leak]}),
                                     post=answering([]), env=env)
            self.assertEqual(code, 1)
            self.assertIsNone(saved)
            self.assertIn("A key appeared in the snapshot", err)

    def test_a_failed_model_call_leaves_that_job_unmapped(self):
        def broken_post(*args):
            raise OSError("venue wifi")

        env = dict(KEYS, ANTHROPIC_API_KEY="sk-secret")
        code, saved, out, _ = run(get=searching({"cook": [COOK]}), post=broken_post, env=env)
        self.assertEqual(code, 0)
        self.assertIsNone(saved["jobs"][0]["required_units"])
        self.assertIn("1 jobs could not be mapped", out)

    def test_a_job_is_tried_again_before_it_is_written_off(self):
        """A real run lost 8 of 30 ads to rate limits; every one of them
        mapped on a retry, so a single failure must not decide the snapshot."""
        calls = []

        def flaky_post(url, headers, payload):
            calls.append(url)
            if len(calls) < fetch_jobs.ATTEMPTS:
                raise OSError("overloaded")
            return {"content": [{"type": "text", "text": json.dumps(
                [{"code": "SITHCCC027", "quote": "prepare dishes for a la carte",
                  "basis": "stated"}])}]}

        env = dict(KEYS, ANTHROPIC_API_KEY="sk-secret")
        code, saved, out, _ = run(get=searching({"cook": [COOK]}), post=flaky_post, env=env)
        self.assertEqual(code, 0)
        self.assertEqual(len(calls), fetch_jobs.ATTEMPTS)
        self.assertEqual([u["code"] for u in saved["jobs"][0]["required_units"]],
                         ["SITHCCC027"])
        self.assertNotIn("could not be mapped", out)

    def test_it_waits_longer_between_tries_and_gives_up(self):
        waits = []

        def broken_post(*args):
            raise OSError("overloaded")

        failed = fetch_jobs.map_jobs(
            [fetch_jobs.keep(COOK, "cookery")],
            {"cookery": {"units": CANDIDATES}}, "k", "m", broken_post, waits.append)
        self.assertEqual(failed, 1)
        self.assertEqual(waits, [fetch_jobs.BACKOFF * 2 ** n
                                 for n in range(fetch_jobs.ATTEMPTS - 1)])

    def test_recheck_rewrites_the_saved_snapshot_offline(self):
        """No keys and no network: the snapshot's ads stay, only their
        mappings are checked again."""
        def no_network(*args):
            raise AssertionError("recheck must not call Adzuna or the model")

        overused = [{"code": c, "quote": "nutritious meals and snacks", "basis": "stated"}
                    for c in ("SITHCCC027", "SITXFSA005", "SITXFSA006")]
        fine = [{"code": "SITHCCC043", "quote": "experienced Cook to join the team",
                 "basis": "stated"}]
        data = fetch_jobs.snapshot([
            dict(fetch_jobs.keep(COOK, "cookery"), title="Cook", required_units=overused + fine,
                 mapped_by="m"),
            dict(fetch_jobs.keep(WELDER, "welding"), required_units=None, mapped_by=None)],
            now=datetime(2026, 9, 21, tzinfo=timezone.utc))
        out, err = io.StringIO(), io.StringIO()
        with tempfile.TemporaryDirectory() as tmp, mock.patch.dict(os.environ, CLEAR), \
                contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            path = Path(tmp) / "jobs_adzuna.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            code = fetch_jobs.main(get=no_network, post=no_network, out=path,
                                   argv=["--recheck"])
            saved = json.loads(path.read_text())
        self.assertEqual(code, 0, err.getvalue())
        cook, welder = saved["jobs"]
        self.assertEqual(cook["required_units"], fine)
        self.assertEqual(cook["mapped_by"], "m")
        self.assertIsNone(welder["required_units"])
        self.assertEqual(saved["fetched_at"], "2026-09-21T00:00:00+00:00")
        self.assertIn("1 jobs changed, 3 units dropped", out.getvalue())

    def test_the_committed_snapshot_has_no_overused_stated_quote(self):
        """The demo reads this file, so the rule must hold for it, not only
        for the next fetch."""
        data = json.loads(fetch_jobs.SNAPSHOT.read_text(encoding="utf-8"))
        for job in data["jobs"]:
            units = job["required_units"] or []
            with self.subTest(job=job["id"]):
                self.assertEqual(fetch_jobs.limit_shared(units, job["title"]), units)

    def test_a_network_failure_is_a_message_without_the_key(self):
        def broken_get(url):
            raise OSError(f"cannot reach {url}")

        code, saved, _, err = run(get=broken_get, env=KEYS)
        self.assertEqual(code, 1)
        self.assertIsNone(saved)
        self.assertIn("Adzuna search failed", err)
        self.assertNotIn("key-456", err)


if __name__ == "__main__":
    unittest.main()
