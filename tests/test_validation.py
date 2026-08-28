from datetime import datetime

import pytest
from pydantic import ValidationError

from app.models import EventIn


def test_naive_timestamp_is_rejected() -> None:
    with pytest.raises(ValidationError):
        EventIn(
            event_id="evt-1",
            event_type="visit",
            user_id="user-1",
            occurred_at=datetime(2026, 8, 20, 12, 0),
        )


def test_missing_identity_is_rejected() -> None:
    with pytest.raises(ValidationError):
        EventIn(
            event_id="evt-1",
            event_type="visit",
            user_id="",
            occurred_at="2026-08-20T12:00:00Z",
        )
