"""Direction 7 - the interview's answers drafted into resume sections.

POST /api/resume-sections, and POST /api/resume-polish for a resume the person
already has, in any language. The model only rearranges what the person said
into the resume's sections; the caseworker edits and confirms every section
on /review before anything is matched. Missing information stays an empty
string or list: a blank a caseworker can see beats a fact nobody said.
"""
import json
import os

from skeleton.core import live
from skeleton.directions.d7_credentials import WRITTEN_LANGUAGES

LIST_FIELDS = {
    "education": ("major", "school", "location", "dates", "description"),
    "employment": ("position", "company", "location", "dates", "description"),
    "volunteer": ("role", "location", "dates", "description"),
}
STRING_LISTS = ("skills", "certificates")

INSTRUCTIONS = """You draft the sections of a resume from a jobseeker's interview
answers. You do nothing else.

Input: a JSON array of answers, each with the question asked (question_en) and
the person's answer in English (answer_en), sometimes also the original words
(answer_zh).

Return only one JSON object, exactly this shape:
{"profile": str,
 "contacts": {"phone": str, "email": str},
 "education": [{"major": str, "school": str, "location": str, "dates": str, "description": str}],
 "employment": [{"position": str, "company": str, "location": str, "dates": str, "description": str}],
 "volunteer": [{"role": str, "location": str, "dates": str, "description": str}],
 "skills": [str],
 "certificates": [str]}

Rules:
- Use only facts the person stated in the answers. Never invent or guess an
  employer, school, date, place, duration, number, skill or certificate.
- If something was not said, leave that string empty or that list empty.
- Write in plain Australian English, without "I", as a resume is written.
  The profile is two or three short sentences.
- Keep the person's own numbers and names exactly as given. Do not add praise
  or qualifiers they did not say ("experienced", "known for", "up to").
- Never output a score, rating or judgement about the person.
- If an answer mentions how the person came to Australia, their journey,
  detention, persecution or why they left, leave it out of every section."""


POLISH_INSTRUCTIONS = """You turn a jobseeker's existing resume into the sections
of an Australian resume. You do nothing else.

Input: the resume's text as it was extracted from the file, in any language
(the language code is given first). Lines may be out of order or broken.

Return only one JSON object, exactly this shape:
{"profile": str,
 "contacts": {"phone": str, "email": str},
 "education": [{"major": str, "school": str, "location": str, "dates": str, "description": str}],
 "employment": [{"position": str, "company": str, "location": str, "dates": str, "description": str}],
 "volunteer": [{"role": str, "location": str, "dates": str, "description": str}],
 "skills": [str],
 "certificates": [str]}

Rules:
- Translate into plain Australian English and use professional resume wording,
  without "I". The profile is two or three short sentences.
- Use only facts the resume states. Never invent or guess an employer, school,
  date, place, duration, number, skill or certificate.
- If something is not in the resume, leave that string empty or that list empty.
- Keep the person's own numbers and names exactly as given; romanise a name
  only where it has no English form. Do not add praise or qualifiers the
  resume does not say ("experienced", "known for", "up to").
- Never output a score, rating or judgement about the person.
- If the resume mentions how the person came to Australia, their journey,
  detention, persecution or why they left, leave it out of every section."""

# The page's textarea takes 100 000 characters; a resume is far shorter, and a
# longer body is a paste mistake, not a resume.
MAX_POLISH_CHARS = 100_000


def _clean_string(value):
    return value.strip() if isinstance(value, str) else ""


def _clean(raw):
    """Force the model's object into the contract. A wrong-typed value becomes
    empty rather than failing the whole draft; an empty entry is dropped so the
    page does not show a card for nothing."""
    raw = raw if isinstance(raw, dict) else {}
    contacts = raw.get("contacts") if isinstance(raw.get("contacts"), dict) else {}
    sections = {
        "profile": _clean_string(raw.get("profile")),
        "contacts": {"phone": _clean_string(contacts.get("phone")),
                     "email": _clean_string(contacts.get("email"))},
    }
    for name, fields in LIST_FIELDS.items():
        entries = raw.get(name) if isinstance(raw.get(name), list) else []
        cleaned = [{field: _clean_string(entry.get(field)) for field in fields}
                   for entry in entries if isinstance(entry, dict)]
        sections[name] = [entry for entry in cleaned if any(entry.values())]
    for name in STRING_LISTS:
        items = raw.get(name) if isinstance(raw.get(name), list) else []
        sections[name] = [text for text in map(_clean_string, items) if text]
    return sections


def _parse(body):
    """The object from the first text block; models sometimes wrap it in prose."""
    text = next(b["text"] for b in body["content"] if b.get("type") == "text")
    parsed = json.loads(text[text.index("{"):text.rindex("}") + 1])
    if not isinstance(parsed, dict):
        raise ValueError("model output is not a JSON object")
    return parsed


def _answers(payload):
    """Only the words said and the question they answer reach the model."""
    answers = payload.get("answers")
    if not isinstance(answers, list) or not all(isinstance(a, dict) for a in answers):
        raise ValueError("answers must be a list of objects")
    keep = ("id", "section", "question_en", "answer_en", "answer_zh")
    return [{key: a[key] for key in keep if isinstance(a.get(key), str)} for a in answers]


def draft(payload, post=None, api_key=None, model=None):
    """{"sections": {...}} per the contract, or {"offline": True, "reason": ...}.

    Offline is never a canned resume: someone else's sections shown as this
    person's draft is exactly the fabrication this page exists to prevent.
    """
    answers = _answers(payload)
    key = os.environ.get("ANTHROPIC_API_KEY", "") if api_key is None else api_key
    if not key:
        return {"offline": True, "reason": "No model key is set, so no resume was drafted."}
    if not any(a.get("answer_en", "").strip() for a in answers):
        return {"offline": True, "reason": "There are no English answers to draft from."}
    request = {
        "model": model or os.environ.get("ANTHROPIC_MODEL") or live.DEFAULT_MODEL,
        "max_tokens": 2048,
        "system": INSTRUCTIONS,
        "messages": [{"role": "user", "content": json.dumps(answers, ensure_ascii=False)}],
    }
    headers = {"x-api-key": key, "anthropic-version": "2023-06-01",
               "content-type": "application/json"}
    sender = live._post_json if post is None else post
    try:
        raw = _parse(sender(live.MESSAGES_URL, headers, request))
    except Exception:
        return {"offline": True, "reason": "The model could not be reached or did not answer "
                                           "in the expected shape. Nothing was drafted."}
    return {"sections": _clean(raw)}


def polish(payload, post=None, api_key=None, model=None):
    """A resume in any language, translated and reworded into the same sections
    as draft(): {"sections": {...}}, {"offline": True, "reason": ...}, or
    {"refused": ...} for a language the team cannot check.

    Same rule as draft(): offline is never a canned resume.
    """
    text, language = payload.get("text"), payload.get("language")
    if not isinstance(text, str) or not text.strip():
        raise ValueError("text must be a non-empty string")
    if len(text) > MAX_POLISH_CHARS:
        raise ValueError(f"text must be at most {MAX_POLISH_CHARS} characters")
    if language not in WRITTEN_LANGUAGES:
        return {"refused": f"{language}: not supported. A resume is read in "
                           f"{', '.join(WRITTEN_LANGUAGES)}. We will not fake a language we cannot verify."}
    key = os.environ.get("ANTHROPIC_API_KEY", "") if api_key is None else api_key
    if not key:
        return {"offline": True, "reason": "No model key is set, so the resume was not translated."}
    request = {
        "model": model or os.environ.get("ANTHROPIC_MODEL") or live.DEFAULT_MODEL,
        "max_tokens": 2048,
        "system": POLISH_INSTRUCTIONS,
        "messages": [{"role": "user", "content": f"Language: {language}\n\n{text.strip()}"}],
    }
    headers = {"x-api-key": key, "anthropic-version": "2023-06-01",
               "content-type": "application/json"}
    sender = live._post_json if post is None else post
    try:
        raw = _parse(sender(live.MESSAGES_URL, headers, request))
    except Exception:
        return {"offline": True, "reason": "The model could not be reached or did not answer "
                                           "in the expected shape. Nothing was translated."}
    return {"sections": _clean(raw)}
