"""Direction 6 - WISE outcomes reporting. Constrained task: aggregate and map.

The red line is enforced here, before the model is called: aggregate only,
never an individual, and never a group small enough to narrow in on one.
"""
from skeleton.core.schema import check_aggregate

KEY = "d6"
NAME = "Outcomes reporting"
METRIC = "reporting preparation hours"


def guard(payload):
    record = {k: v for k, v in payload.items() if k != "group_size"}
    check_aggregate(record, payload.get("group_size", 0))


def prepare(payload):
    return {k: v for k, v in payload.items() if k not in ("group_size", "prep_hours")}


def target_fields(payload):
    return tuple(payload.get("target_fields", []))


def metric(accepted, payload):
    return payload.get("prep_hours")
