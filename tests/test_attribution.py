from datetime import UTC, datetime

from app.attribution import aggregate, attribute
from app.models import EventIn
from app.store import EventStore


def event(event_id: str, event_type: str, minute: int, source: str | None = None) -> EventIn:
    return EventIn(
        event_id=event_id,
        event_type=event_type,
        user_id="user-1",
        occurred_at=datetime(2026, 8, 20, 12, minute, tzinfo=UTC),
        source=source,
    )


def test_duplicate_event_is_idempotent() -> None:
    store = EventStore()
    original, created = store.put(event("evt-1", "visit", 1, "docs"))
    duplicate, duplicate_created = store.put(event("evt-1", "visit", 1, "docs"))
    assert created is True
    assert duplicate_created is False
    assert duplicate == original
    assert aggregate(store.all())["total_events"] == 1


def test_late_events_are_ordered_by_event_time() -> None:
    store = EventStore()
    store.put(event("evt-2", "conversion", 20, "newsletter"))
    store.put(event("evt-1", "visit", 1, "docs"))
    result = attribute("user-1", store.for_user("user-1"))
    assert result.ordered_events == ["visit", "conversion"]
    assert result.first_touch == "docs"
    assert result.last_touch == "newsletter"
    assert result.converted is True


def test_same_timestamp_has_stable_event_id_order() -> None:
    store = EventStore()
    store.put(event("evt-b", "click", 3))
    store.put(event("evt-a", "visit", 3))
    assert [item.event_id for item in store.all()] == ["evt-a", "evt-b"]
