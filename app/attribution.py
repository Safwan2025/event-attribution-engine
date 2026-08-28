from collections import Counter

from .models import AttributionResult, EventType, StoredEvent


def attribute(user_id: str, events: list[StoredEvent]) -> AttributionResult:
    touches = [event.source for event in events if event.source]
    return AttributionResult(
        user_id=user_id,
        first_touch=touches[0] if touches else None,
        last_touch=touches[-1] if touches else None,
        converted=any(event.event_type == EventType.CONVERSION for event in events),
        ordered_events=[event.event_type.value for event in events],
    )


def aggregate(events: list[StoredEvent]) -> dict[str, object]:
    event_counts = Counter(event.event_type.value for event in events)
    converted_users = {
        event.user_id for event in events if event.event_type == EventType.CONVERSION
    }
    return {
        "total_events": len(events),
        "event_counts": dict(sorted(event_counts.items())),
        "converted_users": len(converted_users),
    }
