"""Real API calls over urllib, so the project keeps zero dependencies.

Every function here degrades to offline rather than raising. At a venue with
bad wifi a demo that falls back is a demo; one that raises is a blank screen.
"""
import json
import os
import re
import urllib.request
import uuid

SCRIBE_URL = "https://api.elevenlabs.io/v1/speech-to-text"
# scribe_v1 is listed as deprecated in the ElevenLabs model docs (checked
# 2026-09-21), with scribe_v2 as its replacement; the plan's scribe_v1 would
# risk a live failure on stage.
SCRIBE_MODEL = "scribe_v2"
# The Scribe supported-languages list names Mandarin "Mandarin Chinese (zho)"
# (checked 2026-09-21). The API accepts ISO-639-1 or -3, but zh alone does not
# say which Chinese, so send the code the docs list. Arabic "ar" is ISO-639-1
# and passes through unchanged.
SCRIBE_LANGUAGE_CODES = {"zh": "zho"}
# Needs a decision: the offline stand-in is English whatever the session
# language, so it can never be mistaken for a real transcription.
OFFLINE_TEXT = "I cooked for two hundred people a day in the camp kitchen."

MESSAGES_URL = "https://api.anthropic.com/v1/messages"
DEFAULT_MODEL = "claude-sonnet-5"
FIELDS = ("anzsco_code", "osca_code", "qualification", "units_evidenced")
# The labels a source may carry: what was said, or what was written down.
CITED = ("transcript", "resume")
CODE = re.compile(r"\b(?:[A-Z]{3,7}\d{3,6}|\d{6})\b")

INSTRUCTIONS = """You extract and map evidence. You do nothing else.

Input: transcript lines from a refugee jobseeker describing their work history,
each with a timestamp t, the words said (text) and an English gloss (en), or
instead the lines of a resume they brought, each with a line number (line)
and the words written (text). Plus the candidate ANZSCO and OSCA codes and the
candidate units of competency.

Return only a JSON array. Each item is an object:
{"field": ..., "value": ..., "reason": ..., "confidence": ..., "sources": ...}
- field is one of: anzsco_code, osca_code, qualification, units_evidenced.
- value starts with a code copied exactly from the candidates, e.g.
  "351411 Cook". For units_evidenced, list unit codes separated by "; ".
  Never write a code that is not in the candidates.
- reason is one short English sentence naming what the person said.
- confidence is a number from 0 to 1.
- Every item must cite a transcript timestamp as ["transcript", "t=MM:SS"]
  in sources, or for resume lines a line number as ["resume", "line=N"].
  If there is no supporting line, omit the item.

Never output a score, rating or judgement about the person.

Extract work and learning only. If the transcript or resume mentions the person's
journey, how they came to Australia, detention, persecution or why they fled,
ignore it: never put it in any field, reason or value."""


def _multipart(url, headers, fields, files):
    boundary = uuid.uuid4().hex
    body = bytearray()
    for name, value in fields.items():
        body += f"--{boundary}\r\n".encode()
        body += f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode()
        body += f"{value}\r\n".encode()
    for name, (filename, payload) in files.items():
        body += f"--{boundary}\r\n".encode()
        body += (f'Content-Disposition: form-data; name="{name}"; '
                 f'filename="{filename}"\r\n').encode()
        body += b"Content-Type: application/octet-stream\r\n\r\n"
        body += payload + b"\r\n"
    body += f"--{boundary}--\r\n".encode()

    request = urllib.request.Request(url, data=bytes(body), method="POST")
    request.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    for key, value in headers.items():
        request.add_header(key, value)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def _post_json(url, headers, payload):
    """urlopen raises HTTPError on any non-2xx, so callers only see a body on success."""
    request = urllib.request.Request(
        url, data=json.dumps(payload).encode("utf-8"), method="POST"
    )
    for key, value in headers.items():
        request.add_header(key, value)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def transcribe(audio, language, post=None, api_key=None):
    key = os.environ.get("ELEVENLABS_API_KEY", "") if api_key is None else api_key
    if not key:
        return {"text": OFFLINE_TEXT, "offline": True}
    sender = _multipart if post is None else post
    try:
        body = sender(
            SCRIBE_URL,
            {"xi-api-key": key},
            {"model_id": SCRIBE_MODEL,
             "language_code": SCRIBE_LANGUAGE_CODES.get(language, language)},
            {"file": ("segment.webm", audio)},
        )
    except Exception:
        return {"text": OFFLINE_TEXT, "offline": True}
    return {"text": body.get("text", ""), "offline": False}


def _allowed_codes(prepared):
    """Codes the model may cite, per field. A code outside these is invented."""
    def code(entry):
        return {entry["code"]} if isinstance(entry, dict) and entry.get("code") else set()

    return {
        "anzsco_code": code(prepared.get("anzsco")),
        "osca_code": code(prepared.get("osca")),
        # Needs a decision: the plan's prepare() carries no qualification, so
        # without one there is nothing to check against and the item is dropped.
        "qualification": code(prepared.get("qualification")),
        "units_evidenced": {u["code"] for u in prepared.get("candidate_units", ())},
    }


def _keep(item, allowed, locators):
    """One bad item is dropped here; left in, schema.Suggestion would raise
    and take the whole batch down with it."""
    if not isinstance(item, dict) or item.get("field") not in FIELDS:
        return False
    confidence = item.get("confidence")
    if isinstance(confidence, bool) or not isinstance(confidence, (int, float)):
        return False
    if not 0.0 <= confidence <= 1.0:
        return False
    sources = item.get("sources")
    if not isinstance(sources, list) or not sources:
        return False
    if not all(isinstance(s, list) and len(s) == 2
               and all(isinstance(p, str) for p in s) for s in sources):
        return False
    # A locator the transcript or resume does not have is a source in name
    # only. Pairs, not bare locators, so a resume line cannot stand in for a
    # timestamp or the other way round.
    cited = {(label, locator) for label, locator in sources if label in CITED}
    if not cited or not cited <= locators:
        return False
    if not isinstance(item.get("value"), str) or not isinstance(item.get("reason"), str):
        return False
    codes = set(CODE.findall(item["value"]))
    return bool(codes) and codes <= allowed[item["field"]]


def _parse(body):
    """The array from the first text block; models sometimes wrap it in prose."""
    text = next(b["text"] for b in body["content"] if b.get("type") == "text")
    return json.loads(text[text.index("["):text.rindex("]") + 1])


class LiveModel:
    """A real model behind StubModel's suggest() signature.

    Anything short of a clean answer (no key, no network, a non-200, output
    that does not parse) returns the fallback's answer instead.
    """

    def __init__(self, fallback, api_key=None, post=None, model=None):
        self._fallback = fallback
        self._api_key = api_key
        self._post = _post_json if post is None else post
        self._model = model

    def suggest(self, direction_key, prepared):
        key = (os.environ.get("ANTHROPIC_API_KEY", "")
               if self._api_key is None else self._api_key)
        if not key:
            return self._fallback.suggest(direction_key, prepared)
        model = self._model or os.environ.get("ANTHROPIC_MODEL") or DEFAULT_MODEL
        lines_key = "resume" if "resume" in prepared else "transcript"
        payload = {
            "model": model,
            "max_tokens": 2048,
            "system": INSTRUCTIONS,
            "messages": [{"role": "user", "content": json.dumps(
                {lines_key: prepared.get(lines_key, []),
                 "candidates": {k: v for k, v in prepared.items() if k != lines_key}},
                ensure_ascii=False)}],
        }
        headers = {
            "x-api-key": key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }
        try:
            items = _parse(self._post(MESSAGES_URL, headers, payload))
            if not isinstance(items, list):
                raise ValueError("model output is not a JSON array")
            allowed = _allowed_codes(prepared)
            if lines_key == "resume":
                locators = {("resume", f"line={line['line']}") for line in prepared["resume"]}
            else:
                locators = {("transcript", "t=" + line["t"])
                            for line in prepared.get("transcript", [])}
        except Exception:
            return self._fallback.suggest(direction_key, prepared)
        return [item for item in items if _keep(item, allowed, locators)]
