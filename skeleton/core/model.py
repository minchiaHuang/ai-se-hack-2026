"""The one model call, behind an interface.

The stub exists so the golden path runs with no network, no API key and no
dependency to install. That is also the demo backup: if the venue wifi dies,
the same code path still runs.

On the day, add a real client with the same suggest() signature. Installing an
SDK needs the user's approval first.
"""
import json
from pathlib import Path

CANNED = Path(__file__).resolve().parent.parent / "demo_data" / "canned"


class StubModel:
    """Returns canned suggestions. Constructed with a dict, or loaded from disk."""

    def __init__(self, canned):
        self._canned = canned

    @classmethod
    def from_demo_data(cls):
        canned = {}
        for path in sorted(CANNED.glob("*.json")):
            canned[path.stem] = json.loads(path.read_text(encoding="utf-8"))
        return cls(canned)

    def suggest(self, direction_key, prepared):
        """prepared is unused by the stub; a real client would send it."""
        return self._canned.get(direction_key, [])
