"""One real round trip, so the handler wiring is proven and not just the rendering."""
import threading
import unittest
from http.server import ThreadingHTTPServer
from urllib.request import urlopen

from skeleton.app import Handler


class HttpRoundTrip(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=5)

    def get(self, path):
        with urlopen(f"http://127.0.0.1:{self.port}{path}", timeout=5) as response:
            return response.status, response.read().decode("utf-8")

    def test_index_serves(self):
        status, body = self.get("/")
        self.assertEqual(status, 200)
        self.assertIn("Direction skeleton", body)

    def test_a_scenario_serves(self):
        status, body = self.get("/run?s=d2")
        self.assertEqual(status, 200)
        self.assertIn("Intake triage", body)

    def test_the_refusal_serves(self):
        status, body = self.get("/run?s=d6_small_group")
        self.assertEqual(status, 200)
        self.assertIn("Refused", body)

    def test_an_unknown_scenario_falls_back_to_the_index(self):
        status, body = self.get("/run?s=nope")
        self.assertEqual(status, 200)
        self.assertIn("Direction skeleton", body)


if __name__ == "__main__":
    unittest.main()
