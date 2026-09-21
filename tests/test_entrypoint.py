"""The app must start both ways a person will actually type it.

Running `python3 skeleton/app.py` puts skeleton/ on sys.path instead of the
repo root, so the package imports fail. That is not a hypothetical: it is how
this was first shipped.
"""
import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


class Entrypoint(unittest.TestCase):
    def run_check(self, *argv):
        return subprocess.run(
            [sys.executable, *argv, "--check"],
            cwd=REPO_ROOT, capture_output=True, text=True, timeout=30,
        )

    def test_running_the_file_by_path_works(self):
        done = self.run_check("skeleton/app.py")
        self.assertEqual(done.returncode, 0, done.stderr)

    def test_running_it_as_a_module_works(self):
        done = self.run_check("-m", "skeleton.app")
        self.assertEqual(done.returncode, 0, done.stderr)


if __name__ == "__main__":
    unittest.main()
