"""The one-time phone setup tool: exit codes and output, never the network."""
import contextlib
import io
import os
import unittest
from unittest import mock

from skeleton.tools import phone_agent

KEYS = {"ELEVENLABS_API_KEY": "key", "TWILIO_ACCOUNT_SID": "AC1",
        "TWILIO_AUTH_TOKEN": "tok", "TWILIO_PHONE_NUMBER": "+61200000000"}


def run(argv=(), env=KEYS, post=None):
    out, err = io.StringIO(), io.StringIO()
    with mock.patch.dict(os.environ, env, clear=True), \
            contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = phone_agent.main(argv=argv, post=post)
    return code, out.getvalue(), err.getvalue()


def answering(post_answers):
    sent = []

    def post(url, headers, payload):
        sent.append(url)
        return post_answers.pop(0)
    post.sent = sent
    return post


class Setup(unittest.TestCase):
    def test_creates_the_agent_imports_the_number_and_prints_both_ids(self):
        post = answering([{"agent_id": "agent_1"}, {"phone_number_id": "phnum_1"}])
        code, out, _ = run(post=post)
        self.assertEqual(code, 0)
        self.assertIn("ELEVENLABS_AGENT_ID=agent_1", out)
        self.assertIn("ELEVENLABS_PHONE_NUMBER_ID=phnum_1", out)
        self.assertNotIn("tok", out)

    def test_ids_already_set_are_not_created_twice(self):
        env = dict(KEYS, ELEVENLABS_AGENT_ID="agent_0", ELEVENLABS_PHONE_NUMBER_ID="phnum_0")
        post = answering([])
        code, out, _ = run(env=env, post=post)
        self.assertEqual((code, post.sent), (0, []))
        self.assertIn("ELEVENLABS_AGENT_ID=agent_0", out)

    def test_a_missing_key_names_it_and_calls_nothing(self):
        post = answering([])
        code, _, err = run(env=dict(KEYS, TWILIO_AUTH_TOKEN=""), post=post)
        self.assertEqual((code, post.sent), (2, []))
        self.assertIn("TWILIO_AUTH_TOKEN", err)

    def test_a_failed_request_is_an_exit_status_not_a_traceback(self):
        def post(*args):
            raise OSError("no network")
        code, _, err = run(post=post)
        self.assertEqual(code, 1)
        self.assertIn("OSError", err)


class TestCall(unittest.TestCase):
    def test_call_prints_the_conversation_id(self):
        with mock.patch.object(phone_agent.phone, "start_call",
                               return_value={"conversation_id": "conv_1"}) as start:
            code, out, _ = run(argv=["--call", "+61400000000"])
        self.assertEqual(code, 0)
        self.assertIn("conv_1", out)
        start.assert_called_once_with("+61400000000")

    def test_a_call_that_was_not_placed_is_exit_1_with_the_reason(self):
        with mock.patch.object(phone_agent.phone, "start_call",
                               return_value={"offline": True, "reason": "Geo permission"}):
            code, _, err = run(argv=["--call", "+61400000000"])
        self.assertEqual(code, 1)
        self.assertIn("Geo permission", err)


if __name__ == "__main__":
    unittest.main()
