"""Every link in the product's pages goes to a page the server has, never back to
the first version's /intake, and the demo flags ride along.

Read from the HTML text: the pages build some links in script, so both the
static hrefs and the routes handed to asRoute() or written as string literals
are checked.
"""
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

WEB = Path(__file__).resolve().parent.parent / "skeleton" / "web"
APP = Path(__file__).resolve().parent.parent / "skeleton" / "app.py"

# The product's flow, in order. intake.html is the first version, kept for
# /scenarios and the README; nothing in the flow may lead back to it.
FLOW = ("home", "start", "path", "interview", "upload", "review", "jobs")
# Pages that hand over to the next with the flags in the URL.
FLAGGED = ("interview", "upload", "review", "jobs")

ROUTE = re.compile(r"""(?:href=|asRoute\(|location\.(?:href|assign)\s*=?\s*\(?)\s*["'](/[a-z0-9/._-]*)""")


def page(name):
    return (WEB / f"{name}.html").read_text(encoding="utf-8")


def served():
    """The page routes app.py answers, from its own `parsed.path == "..."` lines."""
    return set(re.findall(r'parsed\.path == "(/[a-z0-9/._-]*)"', APP.read_text(encoding="utf-8")))


class Links(unittest.TestCase):
    def test_every_route_a_page_links_to_is_served(self):
        routes = served()
        for name in FLOW:
            for route in ROUTE.findall(page(name)):
                with self.subTest(page=name, route=route):
                    self.assertIn(route, routes)

    def test_nothing_in_the_flow_leads_back_to_the_first_version(self):
        for name in FLOW:
            with self.subTest(page=name):
                self.assertNotIn("/intake", ROUTE.findall(page(name)))

    def test_upload_goes_back_to_choosing_a_path(self):
        self.assertIn("/start/path", ROUTE.findall(page("upload")))

    def test_every_hand_over_carries_the_mock_flag(self):
        # A demo opened with ?mock=1 must stay in mock mode on the next page.
        for name in FLAGGED:
            with self.subTest(page=name):
                self.assertRegex(page(name), r'"mock=1"|\.set\("mock"')


if __name__ == "__main__":
    unittest.main()


class JobsPage(unittest.TestCase):
    def test_the_employer_mark_does_not_call_itself(self):
        # It once did, and the board rendered its count but not a single card.
        body = re.search(r"function initialsMark\(job\) \{(.*?)\n\}", page("jobs"), re.S).group(1)
        self.assertNotIn("initialsMark(", body)


class Wording(unittest.TestCase):
    def test_the_interview_page_does_not_write_down_a_question_count(self):
        # The count lives in interview_questions.json; the page said "seven" long after it became six.
        words = r"\b(?:one|two|three|four|five|six|seven|eight|nine|ten|\d+) questions\b"
        self.assertNotRegex(page("interview").lower(), words)

    def test_the_home_page_does_not_claim_applications_are_sent(self):
        # Apply is simulated: /jobs says "Nothing was sent."
        self.assertNotIn("submitted", page("home"))


@unittest.skipUnless(shutil.which("node"), "node is not installed")
class Scripts(unittest.TestCase):
    def test_every_pages_script_parses(self):
        # Twice on 2026-09-22 a page's script broke while every Python test passed.
        for path in sorted(WEB.glob("*.html")):
            script = "\n".join(re.findall(r"<script>(.*?)</script>", path.read_text(encoding="utf-8"), re.S))
            with self.subTest(page=path.name), tempfile.NamedTemporaryFile("w", suffix=".js") as js:
                js.write(script)
                js.flush()
                result = subprocess.run(["node", "--check", js.name], capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
