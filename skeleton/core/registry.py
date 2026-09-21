"""Australian occupational and vocational reference data.

Kept here rather than in the direction module because it is reference data about
the country, not about our product. Every code in occupations.json was verified
against an official source on 2026-09-21; nothing here may be invented.
"""
import json
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
