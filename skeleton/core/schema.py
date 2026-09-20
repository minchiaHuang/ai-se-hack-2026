"""Data shapes shared by every direction.

Two rules live here rather than in each direction, because both are promises
the pitch makes and neither should depend on a module remembering to check:

1. Nothing is shown without a source.
2. Below the confidence threshold, the value is withheld and a human is asked.
"""
from dataclasses import dataclass, replace

MIN_GROUP_SIZE = 5

# Field names that mean a row is about one person rather than a group.
INDIVIDUAL_MARKERS = ("name", "employee_id", "dob", "email", "address", "phone")


class AggregationError(Exception):
    """Raised when output would identify, or narrow in on, an individual."""


@dataclass(frozen=True)
class Source:
    label: str
    locator: str


@dataclass(frozen=True)
class Suggestion:
    field: str
    value: str
    reason: str
    confidence: float
    sources: tuple
    shown: bool = True

    def __post_init__(self):
        if not self.sources:
            raise ValueError(f"{self.field}: a suggestion must cite at least one source")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(f"{self.field}: confidence {self.confidence} is outside 0..1")

    def displayed_value(self):
        """The value, or None when the pipeline decided a human should look."""
        return self.value if self.shown else None


@dataclass(frozen=True)
class Result:
    suggestions: tuple
    needs_human: tuple
    gaps: tuple
    metric_name: str
    metric_value: float | None


def sort_by_confidence(suggestions, threshold):
    """Split into what may be shown and what a human must decide instead."""
    shown, needs_human = [], []
    for suggestion in suggestions:
        if suggestion.confidence >= threshold:
            shown.append(replace(suggestion, shown=True))
        else:
            needs_human.append(replace(suggestion, shown=False))
    return tuple(shown), tuple(needs_human)


def check_aggregate(record, group_size):
    """Direction 6 red line. Raises AggregationError rather than returning a flag."""
    for field in record:
        lowered = field.lower()
        if any(marker in lowered for marker in INDIVIDUAL_MARKERS):
            raise AggregationError(
                f"{field}: individual-level field must not reach an outcomes report"
            )
    if group_size < MIN_GROUP_SIZE:
        raise AggregationError(
            f"group of {group_size} is below the minimum of {MIN_GROUP_SIZE}; "
            "cannot aggregate without narrowing in on individuals"
        )
