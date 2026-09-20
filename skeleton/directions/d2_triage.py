"""Direction 2 - op shop intake triage. Constrained task: classify and suggest.

Never prices, never delists, never decides. The value is that the routes come
from the shop's own list, which is why the shop's list is the input.
"""
KEY = "d2"
NAME = "Intake triage"
METRIC = "disposal cost avoided today (AUD)"
TARGET_FIELDS = ("destination", "condition")


def guard(payload):
    """No red line beyond the shared ones."""


def prepare(payload):
    return {"item": payload.get("item"), "routes": payload.get("routes", [])}


def target_fields(payload):
    return TARGET_FIELDS


def metric(accepted, payload):
    """Per accepted routing decision, the gap between that route and landfill.

    The unit cost must come from the shop. With no cost supplied we report
    nothing rather than invent a number.
    """
    unit = payload.get("landfill_cost")
    if unit is None:
        return None
    routed = [s for s in accepted if s.field == "destination" and s.value != "landfill"]
    return len(routed) * unit
