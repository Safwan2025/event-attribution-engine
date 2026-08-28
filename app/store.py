from collections.abc import Iterable
from datetime import UTC, datetime
from threading import RLock

from .models import EventIn, StoredEvent


class EventStore:
    """Thread-safe demonstration store behind a persistence-shaped interface."""

    def __init__(self) -> None:
        self._events: dict[str, StoredEvent] = {}
        self._lock = RLock()

    def put(self, event: EventIn) -> tuple[StoredEvent, bool]:
        with self._lock:
            existing = self._events.get(event.event_id)
            if existing:
                return existing, False
            stored = StoredEvent(**event.model_dump(), received_at=datetime.now(UTC))
            self._events[event.event_id] = stored
            return stored, True

    def for_user(self, user_id: str) -> list[StoredEvent]:
        return self.ordered(event for event in self._events.values() if event.user_id == user_id)

    def all(self) -> list[StoredEvent]:
        return self.ordered(self._events.values())

    @staticmethod
    def ordered(events: Iterable[StoredEvent]) -> list[StoredEvent]:
        return sorted(events, key=lambda event: (event.occurred_at, event.event_id))
