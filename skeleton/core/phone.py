"""The phone interview: an ElevenLabs agent talks with the jobseeker.

Two ways in, one agent: it rings them through Twilio, or they open the agent's
public talk page on their own phone (no phone number needed, so it works on a
Twilio trial account that cannot buy one).

ElevenLabs holds the Twilio number and runs the call itself, so this server only
makes outgoing HTTPS requests: no webhook, no tunnel, no websocket. The agent
asks the same fixed questions as /interview; the finished transcript is split
into those questions' answers and handed to /review like a browser interview.

Like interview.py, nothing here raises on a missing key or a failed call: the
caller gets {"offline": True, "reason": ...}.

Environment:
- ELEVENLABS_API_KEY: the agent, the call and the transcript.
- ELEVENLABS_AGENT_ID, ELEVENLABS_PHONE_NUMBER_ID: printed by
  python3 -m skeleton.tools.phone_agent, which creates both once.
- ANTHROPIC_API_KEY, ANTHROPIC_MODEL: splitting and translating the answers.
"""
import json
import os
import urllib.error
import urllib.parse
import urllib.request

from skeleton.core import interview, live

API = "https://api.elevenlabs.io/v1/convai"
CREATE_AGENT_URL = API + "/agents/create"
PHONE_NUMBERS_URL = API + "/phone-numbers"
OUTBOUND_URL = API + "/twilio/outbound-call"
CONVERSATION_URL = API + "/conversations/{id}"
CONVERSATIONS_URL = API + "/conversations?agent_id={agent}&call_start_after_unix={since}&page_size=5"
# ElevenLabs' own page for an agent without authentication: anyone with the link can talk.
TALK_URL = "https://elevenlabs.io/app/talk-to?agent_id={agent}"
# The default eleven_flash_v2 speaks English only; v2.5 is the multilingual one.
TTS_MODEL = "eleven_flash_v2_5"
SETUP = "Run python3 -m skeleton.tools.phone_agent once and set the IDs it prints."

FIRST_MESSAGE = ("你好，我是帮你整理工作经历的AI助手。接下来大概十分钟，我会问你一些关于学习和工作的问题，"
                 "你用中文回答就可以。我们开始吧，可以先简单介绍一下你自己吗？")

PROMPT = """你是一位友善、耐心的就业访谈员，用简体中文和一位刚到澳大利亚的求职者通电话。你的唯一任务是了解他的学习和工作经历，以便就业顾问之后帮他整理简历和资历认证材料。

按以下顺序提问，一次只问一个问题，等对方说完再问下一个。开场白已经问了第一个问题。对方回答太简短时，可以追问一次细节（例如具体做什么、用什么工具、做了多久），然后继续：
{questions}

规则：
- 只问学习、工作、技能和证书。绝对不要问对方为什么离开原来的国家、逃难经历、签证身份、宗教、政治、健康或家庭情况。
- 如果对方主动讲到逃难或创伤经历，简短、温和地回应（例如“谢谢你告诉我”），不要追问，然后回到工作相关的问题。
- 不要评价、打分或判断对方，不要给就业或法律建议，不要承诺任何工作机会。
- 句子要简短口语化，这是电话。
- 对方想停下或不想回答某题时，尊重并跳过。
- 所有问题都问完后，感谢对方，告诉他就业顾问会根据这次谈话帮他整理材料，然后结束通话。"""

SPLIT_INSTRUCTIONS = """You sort a phone interview's answers into its questions. You do nothing else.

The user message has the interview questions (id and text) and the call's
transcript as numbered turns. For every jobseeker turn (role "user"), output
which question it answers and its plain English translation.

Output only a JSON array: [{"turn": <number>, "id": "<question id>", "en": "<English>"}]
- Use only the listed question ids. A turn that answers none of them is left out.
- Translate what was said. Do not add, explain, summarise, correct or improve it.
- Keep names, places, dates, numbers, phone numbers and email addresses exactly.
- Never add a score, rating or judgement about the person."""


def agent_prompt():
    lines = [f"{n}. {q['zh']}" for n, q in enumerate(interview.questions()["questions"], 1)]
    return PROMPT.format(questions="\n".join(lines))


def agent_config():
    return {
        "name": "D7 Work History Interview",
        "conversation_config": {
            "agent": {
                "language": "zh",
                "first_message": FIRST_MESSAGE,
                "prompt": {
                    "prompt": agent_prompt(),
                    "built_in_tools": {"end_call": {
                        "type": "system", "name": "end_call", "description": "",
                        "params": {"system_tool_type": "end_call"},
                    }},
                },
            },
            "tts": {"model_id": TTS_MODEL},
        },
    }


def _headers(key):
    return {"xi-api-key": key, "content-type": "application/json"}


def _get_json(url, headers):
    request = urllib.request.Request(url, method="GET")
    for name, value in headers.items():
        request.add_header(name, value)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def _offline(reason):
    return {"offline": True, "reason": reason}


def _failure(error, what):
    """The service's own reason when it gave one: it names the fix (a Twilio
    geo permission, an unverified number). It never carries our key."""
    if isinstance(error, urllib.error.HTTPError):
        try:
            detail = json.loads(error.read().decode("utf-8")).get("detail")
        except Exception:
            detail = None
        if isinstance(detail, dict):
            detail = detail.get("message") or json.dumps(detail)
        return _offline(f"{what} failed (HTTP {error.code}): {str(detail or '')[:300]}".rstrip(": "))
    return _offline(f"{what} did not answer.")


def _env(value, name):
    return os.environ.get(name, "") if value is None else value


def create_agent(key, post=None):
    """The new agent's id. Raises on failure: only the setup tool calls this."""
    return (post or live._post_json)(CREATE_AGENT_URL, _headers(key), agent_config())["agent_id"]


def import_number(key, number, sid, token, post=None):
    """The imported Twilio number's id. Raises on failure, like create_agent."""
    payload = {"phone_number": number, "label": "D7 demo", "sid": sid, "token": token,
               "provider": "twilio"}
    return (post or live._post_json)(PHONE_NUMBERS_URL, _headers(key), payload)["phone_number_id"]


def start_call(to_number, post=None, api_key=None, agent_id=None, phone_number_id=None):
    """{"conversation_id": ...} once the phone starts ringing, or offline."""
    key = _env(api_key, "ELEVENLABS_API_KEY")
    agent = _env(agent_id, "ELEVENLABS_AGENT_ID")
    number = _env(phone_number_id, "ELEVENLABS_PHONE_NUMBER_ID")
    if not (key and agent and number):
        return _offline("The phone interview is not set up. " + SETUP)
    payload = {"agent_id": agent, "agent_phone_number_id": number, "to_number": to_number}
    try:
        body = (post or live._post_json)(OUTBOUND_URL, _headers(key), payload)
    except Exception as error:
        return _failure(error, "The call")
    if not body.get("success") or not body.get("conversation_id"):
        return _offline("The call was not placed: " + str(body.get("message") or "no reason given"))
    return {"conversation_id": body["conversation_id"]}


def talk_link(agent_id=None):
    """{"url": ...} of the agent's public talk page, for the jobseeker's phone."""
    agent = _env(agent_id, "ELEVENLABS_AGENT_ID")
    if not agent:
        return _offline("The AI interviewer is not set up. " + SETUP)
    return {"url": TALK_URL.format(agent=urllib.parse.quote(agent, safe=""))}


def latest_conversation(since, get=None, api_key=None, agent_id=None):
    """The newest conversation with the agent that started at or after `since`
    (unix seconds, when the page began waiting), or {"waiting": True}."""
    key = _env(api_key, "ELEVENLABS_API_KEY")
    agent = _env(agent_id, "ELEVENLABS_AGENT_ID")
    if not (key and agent):
        return _offline("The AI interviewer is not set up. " + SETUP)
    url = CONVERSATIONS_URL.format(agent=urllib.parse.quote(agent, safe=""), since=int(since))
    try:
        listed = (get or _get_json)(url, {"xi-api-key": key}).get("conversations") or []
    except Exception as error:
        return _failure(error, "Looking for the conversation")
    # The filter is the service's; checked again so an older talk is never handed over.
    fresh = [c for c in listed if (c.get("start_time_unix_secs") or 0) >= since]
    if not fresh:
        return {"waiting": True}
    return {"conversation_id": max(fresh, key=lambda c: c["start_time_unix_secs"])["conversation_id"]}


def _turns(transcript):
    return [{"role": t.get("role"), "text": (t.get("message") or "").strip()}
            for t in transcript or [] if (t.get("message") or "").strip()]


def _split(turns, post, key):
    """[(turn index, question id, English)] from the model; raises on anything unclean."""
    listed = [{"id": q["id"], "question": q["zh"]} for q in interview.questions()["questions"]]
    numbered = [{"turn": n, "role": t["role"], "text": t["text"]} for n, t in enumerate(turns)]
    payload = {
        "model": os.environ.get("ANTHROPIC_MODEL") or live.DEFAULT_MODEL,
        "max_tokens": 4096,
        "system": SPLIT_INSTRUCTIONS,
        "messages": [{"role": "user", "content": json.dumps(
            {"questions": listed, "transcript": numbered}, ensure_ascii=False)}],
    }
    headers = {"x-api-key": key, "anthropic-version": "2023-06-01",
               "content-type": "application/json"}
    return live._parse((post or live._post_json)(live.MESSAGES_URL, headers, payload))


def answers_from(turns, post=None, anthropic_key=None):
    """The contract's seven answers. The Mandarin is the transcript's own words;
    the model only says which question a turn answers, and translates it."""
    questions = interview.questions()["questions"]
    ids = {q["id"] for q in questions}
    user_turns = [n for n, t in enumerate(turns) if t["role"] == "user"]
    placed = {q["id"]: [] for q in questions}
    body = {}
    key = _env(anthropic_key, "ANTHROPIC_API_KEY")
    try:
        if not key:
            raise LookupError
        split = _split(turns, post, key)
    except Exception:
        # Nothing is guessed: every answer stays in the first question, untranslated.
        placed[questions[0]["id"]] = [(turns[n]["text"], "") for n in user_turns]
        body = _offline("The answers were not split into questions or translated. "
                        "They are all under the first question; move them on the next page.")
    else:
        used = set()
        for item in split if isinstance(split, list) else []:
            n = item.get("turn") if isinstance(item, dict) else None
            if n in user_turns and item.get("id") in ids and n not in used:
                used.add(n)
                placed[item["id"]].append((n, str(item.get("en") or "").strip()))
        # Transcript order within a question, whatever order the model listed them in.
        placed = {i: [(turns[n]["text"], en) for n, en in sorted(p)] for i, p in placed.items()}
        # What the jobseeker said that no question took, so the page can show it.
        body["unplaced"] = [turns[n]["text"] for n in user_turns if n not in used]
    body["answers"] = [{
        "id": q["id"], "section": q["section"], "question_en": q["en"], "question_zh": q["zh"],
        "answer_zh": "\n".join(zh for zh, _ in placed[q["id"]]),
        "answer_en": "\n".join(en for _, en in placed[q["id"]] if en),
    } for q in questions]
    return body


def call_result(conversation_id, get=None, post=None, api_key=None, anthropic_key=None):
    """The call's status and turns so far; once done, the seven answers too."""
    key = _env(api_key, "ELEVENLABS_API_KEY")
    if not key:
        return _offline("No ELEVENLABS_API_KEY is set. " + SETUP)
    url = CONVERSATION_URL.format(id=urllib.parse.quote(conversation_id, safe=""))
    try:
        conversation = (get or _get_json)(url, {"xi-api-key": key})
    except Exception as error:
        return _failure(error, "Reading the call")
    status = conversation.get("status", "")
    turns = _turns(conversation.get("transcript"))
    body = {"status": status, "done": status in ("done", "failed"), "turns": turns}
    if status == "done":
        body.update(answers_from(turns, post, anthropic_key), language="zh")
    return body
