"""Australian occupational and vocational reference data.

Kept here rather than in the direction module because it is reference data about
the country, not about our product. Every code in occupations.json was verified
against an official source on 2026-09-21; nothing here may be invented.
"""
import json
import urllib.request
from functools import lru_cache
from pathlib import Path

REFERENCE = Path(__file__).resolve().parent.parent / "demo_data" / "reference"


@lru_cache(maxsize=1)
def load_occupations():
    return json.loads((REFERENCE / "occupations.json").read_text(encoding="utf-8"))


def occupation(key):
    try:
        return load_occupations()[key]
    except KeyError:
        raise KeyError(f"{key}: not a seeded occupation") from None


def all_units(key):
    return tuple(occupation(key)["units"])


def classifications(key):
    """Both codes, because migration runs on ANZSCO while the ABS runs on OSCA."""
    occ = occupation(key)
    return occ["anzsco"], occ["osca"]


def fetch_pdf_head(url):
    """Default fetcher. Kept separate so tests never touch the network."""
    with urllib.request.urlopen(url, timeout=6) as response:
        return response.read(8)


def source_check(key, fetch=None):
    """Confirm the qualification's published source is reachable right now.

    This proves the document is there, NOT that it is current: a superseded
    qualification's PDF still returns 200 (MEM31922 did on 2026-09-21). Currency
    comes from the seeded record, verified against the national register that
    day. Degrades to unchecked rather than raising, so bad venue wifi is fine.
    """
    qualification = occupation(key)["qualification"]
    result = {
        "code": qualification["code"],
        "status": qualification["status"],
        "superseded_code": qualification["superseded_code"],
        "reachable": False,
        "source": qualification["pdf"],
    }
    if fetch is None:
        return result
    try:
        head = fetch(qualification["pdf"])
    except Exception:
        return result
    result["reachable"] = head.startswith(b"%PDF")
    return result
