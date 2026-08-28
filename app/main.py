import logging

from fastapi import FastAPI, HTTPException, status

from .attribution import aggregate, attribute
from .logging_config import configure_logging
from .models import AttributionResult, EventIn, IngestResult
from .store import EventStore

configure_logging()
logger = logging.getLogger("event-attribution")
app = FastAPI(title="Event Attribution Engine", version="1.0.0")
store = EventStore()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/events", response_model=IngestResult, status_code=status.HTTP_202_ACCEPTED)
def ingest(event: EventIn) -> IngestResult:
    stored, created = store.put(event)
    logger.info("event_ingested type=%s created=%s", event.event_type.value, created)
    return IngestResult(status="accepted" if created else "duplicate", event=stored)


@app.get("/v1/attribution/{user_id}", response_model=AttributionResult)
def get_attribution(user_id: str) -> AttributionResult:
    events = store.for_user(user_id)
    if not events:
        raise HTTPException(status_code=404, detail="No events found for this user")
    return attribute(user_id, events)


@app.get("/v1/analytics")
def analytics() -> dict[str, object]:
    return aggregate(store.all())
