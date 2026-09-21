"""Fetch a Sydney job snapshot from the Adzuna API and map each ad to units.

    ADZUNA_APP_ID=... ADZUNA_APP_KEY=... ANTHROPIC_API_KEY=... \\
        python3 -m skeleton.tools.fetch_jobs

Run once, ahead of time: the demo reads the saved snapshot, so it works
offline on stage. Standard library only, keys from the environment only.

The fit the page later shows is unit coverage, evidenced required units over
required units. So every required unit here must be traceable to words in the
ad: the model picks only from the occupation's candidate units and quotes the
snippet, and code drops anything it cannot check.
"""
import html
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from skeleton.core.live import DEFAULT_MODEL, MESSAGES_URL, _parse, _post_json

REFERENCE = Path(__file__).resolve().parent.parent / "demo_data" / "reference"
OCCUPATIONS = REFERENCE / "occupations.json"
SNAPSHOT = REFERENCE / "jobs_adzuna.json"

# Not confirmed in the Adzuna docs pages fetched on 2026-09-21 (they only show
# gb); au is the country of adzuna.com.au. A wrong code fails loudly on the
# first real run rather than silently returning another country's jobs.
SEARCH_URL = "https://api.adzuna.com/v1/api/jobs/au/search/1"
WHERE = "Sydney"
PER_OCCUPATION = 10
# Two searches per occupation, six calls in total: far below the free tier's
# 25 a minute and 250 a day.
SEARCHES = {
    "cookery": ("cook", "commercial cook"),
    "welding": ("welder", "metal fabricator"),
    "aged_care": ("aged care worker", "personal care assistant"),
}

USAGE = ("Adzuna keys are not set. Get a free app id and key at "
         "https://developer.adzuna.com, then run:\n"
         "  ADZUNA_APP_ID=... ADZUNA_APP_KEY=... python3 -m skeleton.tools.fetch_jobs\n"
         "Add ANTHROPIC_API_KEY=... to map each job to its required units.")

INSTRUCTIONS = """You read one job advertisement and list the units of
competency it requires. You do nothing else.

Input: the job title, the ad snippet, and the candidate units of competency.
Adzuna's snippet is about 500 characters, so it rarely names everything the
job needs; the title often says more about the role than the snippet does.

List the 3 to 6 units a competent worker in this role must be able to do,
chosen only from the candidate units.

Return only a JSON array. Each item is an object:
{"code": ..., "quote": ..., "basis": ...}
- code is copied exactly from the candidate units. Never write another code.
- basis is "stated" when the snippet itself says the job requires this unit,
  or "title" when it is what a job with this title normally requires.
- quote is copied character for character from the snippet (for "stated") or
  from the title (for "title"): the words you took it from. Never paraphrase,
  and never write a quote shorter than 12 characters.
- If neither the snippet nor the title supports a unit, leave the unit out.
  An empty array is a correct answer for a vague title and a short snippet.

The quote is what a person will read to check the unit for themselves, so it
has to be the words that name this unit's work:
- A phrase that only names the role, the seniority, the employer or the team
  is not a "stated" quote. "experienced Cook to join their team" says someone
  cooks; it does not say the job requires food safety. When the snippet only
  names the role like this, the basis is "title" and the quote comes from the
  title.
- Give each unit its own quote. Use one quote for two units only when those
  words really do name both kinds of work — "safe and hygienic environment"
  can carry both a food-safety and a food-handling unit. Reaching for the
  same phrase a third time means the phrase is too general: drop the unit, or
  cite the title instead.
- Prefer the most specific words available. If the snippet says both
  "nutritious meals and snacks" and "prepare dishes to order", the second is
  the better quote for a cookery method unit.

Never output a score, rating or judgement about any person."""

TAG = re.compile(r"<[^>]+>")
# Adzuna's snippet is a teaser, so a unit may rest on the title alone. Which
# one it was has to travel with the unit: the page must be able to say "the ad
# says this" apart from "a job with this title normally needs this".
STATED, FROM_TITLE = "stated", "title"
# Short enough for a real phrase, long enough that a single word like
# "welding" cannot stand as the citation for a whole unit.
MIN_QUOTE = 12
# Tries per ad, and the first wait in seconds. Three tries over a few seconds
# is enough for the rate limits and overload replies seen on a real run, and
# the tool is run by hand the night before, so the wait costs nothing.
ATTEMPTS = 3
BACKOFF = 2


def _get_json(url):
    request = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def _text(value):
    """Adzuna highlights search terms with <strong> tags. Strip them so the
    page shows plain text and a verbatim quote can match the snippet."""
    return html.unescape(TAG.sub("", value or "")).strip()


def keep(result, occupation):
    """Only the fields the page needs. A predicted salary is dropped, so the
    page never has to carry Adzuna's "Jobsworth" label."""
    job = {
        "id": str(result["id"]),
        "occupation": occupation,
        "title": _text(result.get("title")),
        "company": (result.get("company") or {}).get("display_name", ""),
        "location": (result.get("location") or {}).get("display_name", ""),
        "contract_type": result.get("contract_type"),
        "contract_time": result.get("contract_time"),
        "created": result.get("created"),
        "redirect_url": result.get("redirect_url", ""),
        "snippet": _text(result.get("description")),
    }
    if str(result.get("salary_is_predicted")) in ("0", "False", "false"):
        for field in ("salary_min", "salary_max"):
            if result.get(field) is not None:
                job[field] = result[field]
    return job


def fetch(app_id, app_key, get=None):
    """About ten jobs per occupation, each id at most once across the snapshot."""
    getter = _get_json if get is None else get
    jobs, seen = [], set()
    for occupation, terms in SEARCHES.items():
        count = 0
        for what in terms:
            query = urllib.parse.urlencode({
                "app_id": app_id, "app_key": app_key, "what": what, "where": WHERE,
                "results_per_page": PER_OCCUPATION, "content-type": "application/json",
            })
            for result in getter(f"{SEARCH_URL}?{query}").get("results", []):
                if count >= PER_OCCUPATION:
                    break
                if "id" not in result or str(result["id"]) in seen:
                    continue
                seen.add(str(result["id"]))
                jobs.append(keep(result, occupation))
                count += 1
    return jobs


def required_units(job, candidates, key, model, post=None):
    """The model's units, minus any it could not have taken from this ad.

    A code outside the candidates is invented; a quote that is in neither the
    snippet nor the title is no citation. Either one drops the unit, never the
    job. The basis recorded is the one the quote was actually found in, not
    the one the model claimed.
    """
    sender = _post_json if post is None else post
    payload = {
        "model": model,
        "max_tokens": 1024,
        "system": INSTRUCTIONS,
        "messages": [{"role": "user", "content": json.dumps(
            {"title": job["title"], "snippet": job["snippet"],
             "candidate_units": candidates}, ensure_ascii=False)}],
    }
    headers = {"x-api-key": key, "anthropic-version": "2023-06-01",
               "content-type": "application/json"}
    items = _parse(sender(MESSAGES_URL, headers, payload))
    if not isinstance(items, list):
        raise ValueError("model output is not a JSON array")
    allowed = {unit["code"] for unit in candidates}
    kept, codes = [], set()
    for item in items:
        if not isinstance(item, dict):
            continue
        code, quote = item.get("code"), item.get("quote")
        if code not in allowed or code in codes:
            continue
        if not isinstance(quote, str) or len(quote.strip()) < MIN_QUOTE:
            continue
        if quote in job["snippet"]:
            basis = STATED
        elif quote in job["title"]:
            basis = FROM_TITLE
        else:
            continue
        codes.add(code)
        kept.append({"code": code, "quote": quote, "basis": basis})
    return kept


def map_jobs(jobs, occupations, key, model, post=None, sleep=time.sleep):
    """Mutates jobs in place; returns how many could not be mapped.

    Needs a decision: an unmapped job (no key, or its call failed) carries
    required_units None, so the page can tell it apart from a mapped ad with
    [] that was too short to name any unit.

    A run that is rate limited or hits an overloaded API leaves that job
    unmapped for good, because the snapshot is what the demo reads and the
    tool is not run again per job. One ad failing is not evidence the ad is
    unmappable, so each one is tried a few times with a growing wait before
    it is written off.
    """
    failed = 0
    for job in jobs:
        job["required_units"], job["mapped_by"] = None, None
        if not key:
            continue
        for attempt in range(ATTEMPTS):
            try:
                job["required_units"] = required_units(
                    job, occupations[job["occupation"]]["units"], key, model, post)
                job["mapped_by"] = model
                break
            except Exception:
                if attempt == ATTEMPTS - 1:
                    failed += 1
                else:
                    sleep(BACKOFF * 2 ** attempt)
    return failed


def snapshot(jobs, now=None):
    return {
        "source": "Adzuna",
        "fetched_at": (now or datetime.now(timezone.utc)).isoformat(timespec="seconds"),
        "attribution": "Jobs by Adzuna",
        "jobs": jobs,
    }


def main(get=None, post=None, out=SNAPSHOT, now=None, sleep=time.sleep):
    """Exit status, never a traceback: this is run by hand the night before."""
    app_id = os.environ.get("ADZUNA_APP_ID", "")
    app_key = os.environ.get("ADZUNA_APP_KEY", "")
    if not app_id or not app_key:
        print(USAGE, file=sys.stderr)
        return 2
    try:
        jobs = fetch(app_id, app_key, get)
    except Exception as error:
        # The request URL carries the key, so name the error type only.
        print(f"Adzuna search failed ({type(error).__name__}). "
              "Check the keys and the network, then run again.", file=sys.stderr)
        return 1
    if not jobs:
        print("Adzuna returned no jobs; nothing saved.", file=sys.stderr)
        return 1

    anthropic_key = os.environ.get("ANTHROPIC_API_KEY", "")
    model = os.environ.get("ANTHROPIC_MODEL") or DEFAULT_MODEL
    occupations = json.loads(OCCUPATIONS.read_text(encoding="utf-8"))
    failed = map_jobs(jobs, occupations, anthropic_key, model, post, sleep)

    text = json.dumps(snapshot(jobs, now), ensure_ascii=False, indent=2) + "\n"
    # A key in the snapshot would be committed to a public repo. The app id
    # is the one exception, and only inside redirect_url: Adzuna puts it in
    # its own tracking link, the public URL a person clicks.
    secrets = [s for s in (app_key, anthropic_key) if s]
    outside_links = json.dumps(snapshot(
        [{k: v for k, v in job.items() if k != "redirect_url"} for job in jobs], now),
        ensure_ascii=False)
    if (any(secret in text for secret in secrets)
            or (app_id and app_id in outside_links)):
        print("A key appeared in the snapshot; nothing saved.", file=sys.stderr)
        return 1
    try:
        Path(out).write_text(text, encoding="utf-8")
    except OSError as error:
        print(f"Could not save {out} ({error.strerror}).", file=sys.stderr)
        return 1

    for occupation in SEARCHES:
        mine = [j for j in jobs if j["occupation"] == occupation]
        units = sum(len(j["required_units"] or ()) for j in mine)
        print(f"{occupation}: {len(mine)} jobs, {units} mapped units")
    if not anthropic_key:
        print("ANTHROPIC_API_KEY is not set: jobs saved with required_units "
              "unmapped (null). Set it and run again to map them.")
    elif failed:
        print(f"{failed} jobs could not be mapped and are saved unmapped (null).")
    print(f"Saved {len(jobs)} jobs to {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
