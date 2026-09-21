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
                               now=datetime(2026, 9, 21, tzinfo=timezone.utc))
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


class Mapping(unittest.TestCase):
    def setUp(self):
        self.job = fetch_jobs.keep(COOK, "cookery")

    def test_a_cited_candidate_unit_is_kept(self):
        post = answering([{"code": "SITHCCC027", "quote": "prepare dishes"}])
        self.assertEqual(fetch_jobs.required_units(self.job, CANDIDATES, "k", "m", post),
                         [{"code": "SITHCCC027", "quote": "prepare dishes"}])

    def test_a_unit_outside_the_candidates_is_dropped(self):
        post = answering([{"code": "SITHCCC999", "quote": "prepare dishes"},
                          {"code": "SITXFSA005", "quote": "food safety & hygiene"}])
        self.assertEqual(fetch_jobs.required_units(self.job, CANDIDATES, "k", "m", post),
                         [{"code": "SITXFSA005", "quote": "food safety & hygiene"}])

    def test_a_quote_not_in_the_snippet_is_dropped(self):
        """A paraphrase is no citation: the page would cite words the ad never said."""
        post = answering([{"code": "SITHCCC027", "quote": "cooks meals from scratch"},
                          {"code": "SITXFSA005", "quote": ""}])
        self.assertEqual(fetch_jobs.required_units(self.job, CANDIDATES, "k", "m", post), [])

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
        self.assertIn("Never output a score", sent["payload"]["system"])


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
        post = answering([{"code": "SITHCCC027", "quote": "prepare dishes"}])
        code, saved, out, _ = run(get=searching({"cook": [COOK], "welder": [WELDER]}),
                                  post=post, env=env)
        self.assertEqual(code, 0)
        cook, welder = saved["jobs"]
        self.assertEqual(cook["required_units"], [{"code": "SITHCCC027", "quote": "prepare dishes"}])
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
