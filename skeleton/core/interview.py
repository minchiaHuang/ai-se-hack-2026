"""The AI interview's backend: fixed questions, answer translation, spoken questions.

Like live.py, nothing here raises on a missing key or a failed call. The
caller gets {"offline": True, "reason": ...} and the page says so on screen,
so a person can type the translation or read the question instead. Nothing
is faked: there is no placeholder translation and no placeholder audio.

Environment:
- ANTHROPIC_API_KEY, ANTHROPIC_MODEL: translation, same model call as live.py.
- ELEVENLABS_API_KEY: text to speech.
- ELEVENLABS_VOICE_ID: the voice that reads questions aloud. Defaults to
  DEFAULT_VOICE_ID below.
"""
import json
import os
import urllib.parse
import urllib.request
from pathlib import Path

from skeleton.core import live

QUESTIONS = Path(__file__).resolve().parent.parent / "demo_data" / "reference" / "interview_questions.json"

TTS_URL = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
# Multilingual v2 reads Mandarin with the same voice that could read English,
# so one voice id covers every supported language.
TTS_MODEL = "eleven_multilingual_v2"
# "George", a premade voice in ElevenLabs' own quickstart examples, so it is
# available on any account without cloning. NEEDS DECISION: the team may pick
# a voice that sounds better in Mandarin; set ELEVENLABS_VOICE_ID to override.
DEFAULT_VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"
# A question is read while the person waits: a stalled call must give up well
# before they give up on the page.
TTS_TIMEOUT = 20
# The longest fixed question is about 100 characters. The cap stops a stray
# request from turning the 1 MB JSON limit into a large text-to-speech bill.
MAX_SPEAK_CHARS = 1000

SOURCE_NAMES = {"zh": "Mandarin Chinese", "ar": "Arabic"}

TRANSLATE_INSTRUCTIONS = """You translate one interview answer into English. You do nothing else.

The answer was spoken by a jobseeker and transcribed; the {source} text is in
the user message. Write it in plain Australian English a caseworker can read.

- Output only the English translation: no preface, notes or quotation marks.
- Translate what was said. Do not add, explain, summarise, correct or improve it.
- Keep names, places, dates, numbers, phone numbers and email addresses exactly.
- If a word is unclear, translate it literally rather than guessing a meaning.
- Never add a score, rating or judgement about the person."""


def questions():
    """The fixed questions in file order, only the fields the contract names."""
    data = json.loads(QUESTIONS.read_text(encoding="utf-8"))
    return {"questions": [{k: q[k] for k in ("id", "section", "en", "zh")}
                          for q in data["questions"]]}


def _offline(reason):
    return {"offline": True, "reason": reason}


def translate(text, source, post=None, api_key=None):
    """{"en": ...} from the model, or offline with the reason."""
    key = os.environ.get("ANTHROPIC_API_KEY", "") if api_key is None else api_key
    if not key:
        return _offline("No ANTHROPIC_API_KEY is set, so the answer was not translated.")
    sender = live._post_json if post is None else post
    payload = {
        "model": os.environ.get("ANTHROPIC_MODEL") or live.DEFAULT_MODEL,
        "max_tokens": 1024,
        "system": TRANSLATE_INSTRUCTIONS.format(source=SOURCE_NAMES.get(source, source)),
        "messages": [{"role": "user", "content": text}],
    }
    headers = {
        "x-api-key": key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    try:
        body = sender(live.MESSAGES_URL, headers, payload)
        english = next(b["text"] for b in body["content"] if b.get("type") == "text").strip()
    except Exception:
        return _offline("The translation service did not answer.")
    if not english:
        return _offline("The translation came back empty.")
    return {"en": english}


def _post_audio(url, headers, payload):
    """Like live._post_json, but the answer is audio bytes, not JSON."""
    request = urllib.request.Request(
        url, data=json.dumps(payload).encode("utf-8"), method="POST"
    )
    for name, value in headers.items():
        request.add_header(name, value)
    with urllib.request.urlopen(request, timeout=TTS_TIMEOUT) as response:
        return response.read()


def speak(text, post=None, api_key=None):
    """MP3 bytes from ElevenLabs, or an offline dict with the reason."""
    key = os.environ.get("ELEVENLABS_API_KEY", "") if api_key is None else api_key
    if not key:
        return _offline("No ELEVENLABS_API_KEY is set, so the question was not read aloud.")
    voice_id = os.environ.get("ELEVENLABS_VOICE_ID") or DEFAULT_VOICE_ID
    sender = _post_audio if post is None else post
    url = (TTS_URL.format(voice_id=urllib.parse.quote(voice_id, safe=""))
           + "?output_format=mp3_44100_128")
    headers = {"xi-api-key": key, "content-type": "application/json",
               "accept": "audio/mpeg"}
    # No language_code: multilingual v2 detects the language from the text,
    # and ElevenLabs documents language enforcement for other models only.
    try:
        audio = sender(url, headers, {"text": text, "model_id": TTS_MODEL})
    except Exception:
        return _offline("The text-to-speech service did not answer.")
    if not isinstance(audio, bytes) or not audio:
        return _offline("The text-to-speech service returned no audio.")
    return audio
