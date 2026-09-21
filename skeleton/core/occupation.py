"""Which covered occupation a resume is about, so /review stops assuming a cook.

The reference data covers three occupations. The model only picks one of those
keys, or "none"; anything else, or no answer at all, comes back offline, and the
caseworker chooses. A suggestion is never final: /review shows it in a menu the
caseworker can change.
"""
import json
import os
from pathlib import Path

from skeleton.core import live

OCCUPATIONS = Path(__file__).resolve().parent.parent / "demo_data" / "reference" / "occupations.json"
NONE = "none"

INSTRUCTIONS = """You say which occupation a resume is about. You do nothing else.

The user message has the covered occupations (key and label) and a resume.
Answer with only JSON: {{"occupation": "<key>"}}
- Use a key from the list only when the resume's work is plainly that occupation.
- Otherwise answer {{"occupation": "{none}"}}. Do not pick the nearest one.
- Never add a score, rating or judgement about the person."""


def covered():
    """[{"key", "label"}] in file order, straight from the reference data."""
    data = json.loads(OCCUPATIONS.read_text(encoding="utf-8"))
    return [{"key": key, "label": value["label"]} for key, value in data.items()]


def _offline(reason):
    return {"offline": True, "reason": reason}


def suggest(text, post=None, api_key=None):
    """{"occupation": key or "none", "label": ...}, or offline with the reason."""
    key = os.environ.get("ANTHROPIC_API_KEY", "") if api_key is None else api_key
    if not key:
        return _offline("No ANTHROPIC_API_KEY is set, so no occupation was suggested. Choose one.")
    options = covered()
    payload = {
        "model": os.environ.get("ANTHROPIC_MODEL") or live.DEFAULT_MODEL,
        "max_tokens": 64,
        "system": INSTRUCTIONS.format(none=NONE),
        "messages": [{"role": "user", "content": json.dumps(
            {"occupations": options, "resume": text}, ensure_ascii=False)}],
    }
    headers = {"x-api-key": key, "anthropic-version": "2023-06-01",
               "content-type": "application/json"}
    try:
        body = (post or live._post_json)(live.MESSAGES_URL, headers, payload)
        said = next(b["text"] for b in body["content"] if b.get("type") == "text")
        chosen = json.loads(said[said.index("{"):said.rindex("}") + 1]).get("occupation")
    except Exception:
        return _offline("The occupation could not be suggested. Choose one.")
    labels = {o["key"]: o["label"] for o in options}
    if chosen == NONE:
        return {"occupation": NONE, "label": None}
    if chosen not in labels:
        return _offline("The suggestion was not a covered occupation. Choose one.")
    return {"occupation": chosen, "label": labels[chosen]}
