"""Direction 3 - evidence layer. Constrained task: extract and map.

Never writes a claim. A target field with no supporting evidence is reported
as a gap, which is the whole point: the tool must not make things up for you.
"""
KEY = "d3"
NAME = "Evidence mapping"
METRIC = "times one piece of evidence was reused"


def guard(payload):
    """No red line beyond the shared ones."""


def prepare(payload):
    return {"documents": payload.get("documents", []),
            "target": payload.get("target_fields", [])}


def target_fields(payload):
    return tuple(payload.get("target_fields", []))


def metric(accepted, payload):
    """How many target fields each cited source ended up serving."""
    if not accepted:
        return None
    uses = {}
    for suggestion in accepted:
        for source in suggestion.sources:
            uses[(source.label, source.locator)] = uses.get((source.label, source.locator), 0) + 1
    return max(uses.values())
