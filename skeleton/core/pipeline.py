"""Input -> constrained task -> sourced, scored output -> human -> one metric.

Every direction runs through here. The differences live in the direction
modules: what gets prepared, which fields are expected, and which metric.
"""
from skeleton.core.schema import Result, Source, Suggestion, sort_by_confidence


def run(direction, payload, model, threshold=0.6):
    """Raises whatever the direction's guard raises, before calling the model."""
    direction.guard(payload)

    raw = model.suggest(direction.KEY, direction.prepare(payload))
    suggestions = [
        Suggestion(
            field=item["field"],
            value=item["value"],
            reason=item["reason"],
            confidence=item["confidence"],
            sources=tuple(Source(*pair) for pair in item["sources"]),
        )
        for item in raw
    ]

    shown, needs_human = sort_by_confidence(suggestions, threshold)

    answered = {s.field for s in suggestions}
    gaps = tuple(f for f in direction.target_fields(payload) if f not in answered)

    return Result(
        suggestions=shown,
        needs_human=needs_human,
        gaps=gaps,
        metric_name=direction.METRIC,
        metric_value=direction.metric(shown, payload),
    )
