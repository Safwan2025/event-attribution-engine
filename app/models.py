from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field, field_validator


class EventType(StrEnum):
    VISIT = "visit"
    CLICK = "click"
    SIGNUP = "signup"
    ACTIVATION = "activation"
    CONVERSION = "conversion"


class EventIn(BaseModel):
    event_id: str = Field(min_length=3, max_length=100, pattern=r"^[A-Za-z0-9_-]+$")
    event_type: EventType
    user_id: str = Field(min_length=1, max_length=100)
    occurred_at: datetime
    source: str | None = Field(default=None, max_length=120)
    properties: dict[str, Any] = Field(default_factory=dict)

    @field_validator("occurred_at")
    @classmethod
    def timestamp_must_have_timezone(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("occurred_at must include a timezone")
        return value.astimezone(UTC)


class StoredEvent(EventIn):
    received_at: datetime


class IngestResult(BaseModel):
    status: str
    event: StoredEvent


class AttributionResult(BaseModel):
    user_id: str
    first_touch: str | None
    last_touch: str | None
    converted: bool
    ordered_events: list[str]
