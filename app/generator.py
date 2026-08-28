import argparse
import random
from datetime import UTC, datetime, timedelta

import httpx

EVENT_TYPES = ["visit", "click", "signup", "activation", "conversion"]


def generate(count: int) -> list[dict[str, object]]:
    now = datetime.now(UTC)
    events: list[dict[str, object]] = []
    for index in range(count):
        user_number = index // len(EVENT_TYPES)
        event_type = EVENT_TYPES[index % len(EVENT_TYPES)]
        events.append(
            {
                "event_id": f"demo-{user_number}-{event_type}",
                "event_type": event_type,
                "user_id": f"demo-user-{user_number}",
                "occurred_at": (now + timedelta(minutes=index)).isoformat(),
                "source": random.choice(["docs", "newsletter", "partner-demo"]),
                "properties": {"synthetic": True},
            }
        )
    random.shuffle(events)
    return events


def main() -> None:
    parser = argparse.ArgumentParser(description="Send synthetic events in random order")
    parser.add_argument("--count", type=int, default=20)
    parser.add_argument("--base-url", default="http://localhost:8000")
    args = parser.parse_args()
    for event in generate(args.count):
        response = httpx.post(f"{args.base_url}/v1/events", json=event, timeout=5)
        print(response.status_code, response.json()["status"], event["event_id"])


if __name__ == "__main__":
    main()
