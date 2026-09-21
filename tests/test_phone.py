"""The phone interview: an ElevenLabs agent calls through the team's Twilio number.

No test here touches the network: every call goes through a fake post or get.
"""
import io
import json
import unittest
import urllib.error
from unittest import mock
from urllib.error import HTTPError
from urllib.request import urlopen

from skeleton import app
from skeleton.core import interview, phone
from tests.test_http import Server


def broken(*args, **kwargs):
    raise OSError("venue wifi")


def http_error(status, detail):
    def fail(*args, **kwargs):
        raise urllib.error.HTTPError("https://api.elevenlabs.io", status, "error", {},
                                     io.BytesIO(json.dumps({"detail": detail}).encode("utf-8")))
    return fail


def recording(answer):
    """A fake post that keeps what it was sent and answers with `answer`."""
    sent = []

    def post(url, headers, payload):
        sent.append((url, headers, payload))
        return answer
    post.sent = sent
    return post


TURNS = [
    {"role": "agent", "message": "你好，可以简单介绍一下你自己吗？"},
    {"role": "user", "message": "我叫李伟，做了六年厨师。"},
    {"role": "agent", "message": "你最近一份工作是什么？"},
    {"role": "user", "message": "在成都蓉香楼当主厨。"},
    {"role": "user", "message": "每天熬高汤。"},
    {"role": "agent", "message": "谢谢，再见。"},
]


def conversation(status, turns=TURNS):
    def get(url, headers):
        get.url = url
        return {"status": status, "transcript": turns}
    return get


def model_says(items):
    return recording({"content": [{"type": "text", "text": json.dumps(items)}]})


class AgentConfig(unittest.TestCase):
    def test_the_prompt_asks_every_fixed_question_in_order(self):
        prompt = phone.agent_prompt()
        positions = [prompt.index(q["zh"]) for q in interview.questions()["questions"]]
        self.assertEqual(positions, sorted(positions))

    def test_the_prompt_forbids_asking_about_flight_or_visa(self):
        prompt = phone.agent_prompt()
        for topic in ("逃难", "签证"):
            self.assertIn(topic, prompt)

    def test_the_first_message_asks_the_whole_first_question(self):
        first = interview.questions()["questions"][0]["zh"]
        self.assertIn(first, phone.agent_config()["conversation_config"]["agent"]["first_message"])

    def test_the_prompt_keeps_order_asks_every_part_and_adds_nothing(self):
        prompt = phone.agent_prompt()
        for rule in ("严格按顺序", "每个小问题", "不要加上对方没说过的内容"):
            self.assertIn(rule, prompt)

    def test_the_split_keeps_alternatives_as_alternatives(self):
        self.assertIn("alternatives", phone.SPLIT_INSTRUCTIONS)

    def test_update_agent_patches_the_same_agent_with_the_current_config(self):
        sent = []

        def patch(url, headers, payload):
            sent.append((url, payload))
            return {"agent_id": "agent_1"}
        phone.update_agent("key", "agent_1", patch=patch)
        url, payload = sent[0]
        self.assertEqual(url, phone.AGENT_URL.format(id="agent_1"))
        self.assertEqual(payload, phone.agent_config())

    def test_the_agent_speaks_mandarin_with_a_multilingual_voice_and_can_hang_up(self):
        config = phone.agent_config()["conversation_config"]
        self.assertEqual(config["agent"]["language"], "zh")
        self.assertEqual(config["tts"]["model_id"], "eleven_flash_v2_5")
        end_call = config["agent"]["prompt"]["built_in_tools"]["end_call"]
        self.assertEqual(end_call["params"]["system_tool_type"], "end_call")

    def test_create_agent_returns_the_agent_id(self):
        post = recording({"agent_id": "agent_1"})
        self.assertEqual(phone.create_agent("key", post=post), "agent_1")
        url, headers, payload = post.sent[0]
        self.assertEqual(url, phone.CREATE_AGENT_URL)
        self.assertEqual(headers["xi-api-key"], "key")
        self.assertIn("conversation_config", payload)

    def test_import_number_sends_the_twilio_credentials_and_returns_the_id(self):
        post = recording({"phone_number_id": "phnum_1"})
        got = phone.import_number("key", "+61200000000", "AC1", "tok", post=post)
        self.assertEqual(got, "phnum_1")
        url, _, payload = post.sent[0]
        self.assertEqual(url, phone.PHONE_NUMBERS_URL)
        self.assertEqual(payload["provider"], "twilio")
        self.assertEqual((payload["phone_number"], payload["sid"], payload["token"]),
                         ("+61200000000", "AC1", "tok"))


class StartCall(unittest.TestCase):
    ENV = {"api_key": "key", "agent_id": "agent_1", "phone_number_id": "phnum_1"}

    def test_a_call_returns_the_conversation_id(self):
        post = recording({"success": True, "conversation_id": "conv_1", "callSid": "CA1"})
        body = phone.start_call("+61400000000", post=post, **self.ENV)
        self.assertEqual(body, {"conversation_id": "conv_1"})
        url, _, payload = post.sent[0]
        self.assertEqual(url, phone.OUTBOUND_URL)
        self.assertEqual(payload, {"agent_id": "agent_1", "agent_phone_number_id": "phnum_1",
                                   "to_number": "+61400000000"})

    def test_missing_setup_is_offline_and_names_the_setup_command(self):
        for missing in ("api_key", "agent_id", "phone_number_id"):
            with self.subTest(missing=missing):
                env = dict(self.ENV, **{missing: ""})
                post = recording({})
                body = phone.start_call("+61400000000", post=post, **env)
                self.assertTrue(body["offline"])
                self.assertIn("skeleton.tools.phone_agent", body["reason"])
                self.assertEqual(post.sent, [])

    def test_a_refused_call_is_offline_with_the_services_reason(self):
        body = phone.start_call("+61400000000", post=http_error(400, "Geo permission denied"),
                                **self.ENV)
        self.assertTrue(body["offline"])
        self.assertIn("Geo permission denied", body["reason"])

    def test_no_network_is_offline(self):
        body = phone.start_call("+61400000000", post=broken, **self.ENV)
        self.assertTrue(body["offline"])

    def test_an_unsuccessful_answer_is_offline(self):
        post = recording({"success": False, "message": "busy", "conversation_id": None})
        body = phone.start_call("+61400000000", post=post, **self.ENV)
        self.assertTrue(body["offline"])
        self.assertIn("busy", body["reason"])


class CallResult(unittest.TestCase):
    def test_a_call_in_progress_shows_the_turns_so_far(self):
        get = conversation("in-progress", TURNS[:2])
        body = phone.call_result("conv_1", get=get, api_key="key", anthropic_key="")
        self.assertEqual(body["status"], "in-progress")
        self.assertFalse(body["done"])
        self.assertEqual(body["turns"], [{"role": "agent", "text": TURNS[0]["message"]},
                                         {"role": "user", "text": TURNS[1]["message"]}])
        self.assertEqual(get.url, phone.CONVERSATION_URL.format(id="conv_1"))

    def test_silence_is_not_a_turn(self):
        turns = [{"role": "agent", "message": "你好"}, {"role": "user", "message": "..."},
                 {"role": "user", "message": " … "}, {"role": "user", "message": None}]
        body = phone.call_result("conv_1", get=conversation("in-progress", turns), api_key="key")
        self.assertEqual(body["turns"], [{"role": "agent", "text": "你好"}])

    def test_a_finished_call_is_split_into_the_seven_answers_verbatim(self):
        post = model_says([
            {"turn": 1, "id": "profile", "en": "My name is Li Wei, a cook for six years."},
            {"turn": 3, "id": "employment", "en": "Head cook at Rongxiang Lou in Chengdu."},
            {"turn": 4, "id": "employment", "en": "I made stock every day."},
        ])
        body = phone.call_result("conv_1", get=conversation("done"), post=post,
                                 api_key="key", anthropic_key="akey")
        self.assertTrue(body["done"])
        answers = {a["id"]: a for a in body["answers"]}
        self.assertEqual([a["id"] for a in body["answers"]],
                         [q["id"] for q in interview.questions()["questions"]])
        self.assertEqual(answers["profile"]["answer_zh"], "我叫李伟，做了六年厨师。")
        self.assertEqual(answers["employment"]["answer_zh"], "在成都蓉香楼当主厨。\n每天熬高汤。")
        self.assertEqual(answers["employment"]["answer_en"],
                         "Head cook at Rongxiang Lou in Chengdu.\nI made stock every day.")
        self.assertEqual(answers["skills"]["answer_zh"], "")
        self.assertEqual(set(answers["profile"]),
                         {"id", "section", "question_en", "question_zh", "answer_zh", "answer_en"})

    def test_the_model_cannot_place_an_agent_turn_or_invent_a_question(self):
        post = model_says([
            {"turn": 0, "id": "profile", "en": "agent words"},
            {"turn": 1, "id": "journey", "en": "made up"},
            {"turn": 9, "id": "skills", "en": "no such turn"},
        ])
        body = phone.call_result("conv_1", get=conversation("done"), post=post,
                                 api_key="key", anthropic_key="akey")
        self.assertTrue(all(a["answer_zh"] == "" for a in body["answers"]))
        self.assertEqual(len(body["unplaced"]), 3)

    def test_without_a_model_every_answer_is_kept_unsplit_and_the_page_is_told(self):
        body = phone.call_result("conv_1", get=conversation("done"), post=broken,
                                 api_key="key", anthropic_key="")
        self.assertTrue(body["done"])
        self.assertTrue(body["offline"])
        profile = body["answers"][0]
        self.assertEqual(profile["answer_zh"], "我叫李伟，做了六年厨师。\n在成都蓉香楼当主厨。\n每天熬高汤。")
        self.assertEqual(profile["answer_en"], "")

    def test_a_failed_call_is_reported(self):
        body = phone.call_result("conv_1", get=conversation("failed", []), api_key="key",
                                 anthropic_key="")
        self.assertEqual(body["status"], "failed")
        self.assertTrue(body["done"])
        self.assertNotIn("answers", body)

    def test_no_key_or_no_network_is_offline(self):
        self.assertTrue(phone.call_result("conv_1", get=broken, api_key="")["offline"])
        self.assertTrue(phone.call_result("conv_1", get=broken, api_key="key")["offline"])


class TalkLink(unittest.TestCase):
    def test_the_link_is_the_agents_public_talk_page(self):
        body = phone.talk_link(agent_id="agent_1")
        self.assertEqual(body, {"url": "https://elevenlabs.io/app/talk-to?agent_id=agent_1"})

    def test_no_agent_is_offline_and_names_the_setup_command(self):
        body = phone.talk_link(agent_id="")
        self.assertTrue(body["offline"])
        self.assertIn("skeleton.tools.phone_agent", body["reason"])


class LatestConversation(unittest.TestCase):
    ENV = {"api_key": "key", "agent_id": "agent_1"}

    def listing(self, conversations):
        def get(url, headers):
            get.url = url
            return {"conversations": conversations}
        return get

    def test_the_newest_conversation_since_the_page_started_waiting(self):
        get = self.listing([{"conversation_id": "conv_2", "start_time_unix_secs": 200}])
        body = phone.latest_conversation(150, get=get, **self.ENV)
        self.assertEqual(body, {"conversation_id": "conv_2"})
        self.assertIn("agent_id=agent_1", get.url)
        self.assertIn("call_start_after_unix=150", get.url)

    def test_nothing_yet_is_waiting_not_offline(self):
        body = phone.latest_conversation(150, get=self.listing([]), **self.ENV)
        self.assertEqual(body, {"waiting": True})

    def test_an_older_conversation_is_never_picked(self):
        get = self.listing([{"conversation_id": "conv_1", "start_time_unix_secs": 100}])
        self.assertEqual(phone.latest_conversation(150, get=get, **self.ENV), {"waiting": True})

    def test_missing_setup_or_no_network_is_offline(self):
        self.assertTrue(phone.latest_conversation(150, get=broken, api_key="", agent_id="a")["offline"])
        self.assertTrue(phone.latest_conversation(150, get=broken, **self.ENV)["offline"])


class CallRoutes(Server):
    def get_status(self, path):
        try:
            with urlopen(f"http://127.0.0.1:{self.port}{path}", timeout=5) as response:
                return response.status, json.loads(response.read())
        except HTTPError as error:
            return error.code, json.loads(error.read())

    def test_start_without_setup_is_a_200_offline(self):
        status, text = self.post("/api/call/start", {"to": "+61400000000"})
        self.assertEqual(status, 200)
        self.assertTrue(json.loads(text)["offline"])

    def test_start_passes_the_number_on(self):
        with mock.patch.object(app.phone, "start_call",
                               return_value={"conversation_id": "conv_1"}) as start:
            status, text = self.post("/api/call/start", {"to": " +61400000000 "})
        self.assertEqual((status, json.loads(text)), (200, {"conversation_id": "conv_1"}))
        start.assert_called_once_with("+61400000000")

    def test_a_number_not_in_international_format_is_refused_before_any_call(self):
        for to in ("0400000000", "+61 400 000 000", "", None, "+0400000000"):
            with self.subTest(to=to), mock.patch.object(app.phone, "start_call") as start:
                status, _ = self.post("/api/call/start", {"to": to})
                self.assertEqual(status, 400)
                start.assert_not_called()

    def test_result_passes_the_conversation_id_on(self):
        with mock.patch.object(app.phone, "call_result",
                               return_value={"status": "in-progress", "done": False}) as result:
            status, body = self.get_status("/api/call/result?id=conv_1")
        self.assertEqual((status, body["status"]), (200, "in-progress"))
        result.assert_called_once_with("conv_1")

    def test_talk_link_route(self):
        with mock.patch.object(app.phone, "talk_link", return_value={"url": "u"}):
            self.assertEqual(self.get_status("/api/talk/link"), (200, {"url": "u"}))

    def test_talk_latest_passes_the_start_time_on(self):
        with mock.patch.object(app.phone, "latest_conversation",
                               return_value={"waiting": True}) as latest:
            status, body = self.get_status("/api/talk/latest?since=1790000000")
        self.assertEqual((status, body), (200, {"waiting": True}))
        latest.assert_called_once_with(1790000000)

    def test_talk_latest_needs_a_whole_number_start_time(self):
        for query in ("", "?since=", "?since=abc", "?since=-5", "?since=1.5"):
            with self.subTest(query=query), mock.patch.object(app.phone, "latest_conversation") as latest:
                status, _ = self.get_status("/api/talk/latest" + query)
                self.assertEqual(status, 400)
                latest.assert_not_called()

    def test_a_malformed_conversation_id_is_refused(self):
        for query in ("", "?id=", "?id=../agents", "?id=a%20b"):
            with self.subTest(query=query), mock.patch.object(app.phone, "call_result") as result:
                status, _ = self.get_status("/api/call/result" + query)
                self.assertEqual(status, 400)
                result.assert_not_called()


if __name__ == "__main__":
    unittest.main()
