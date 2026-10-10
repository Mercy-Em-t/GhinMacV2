import asyncio
from datetime import datetime
from typing import Any, Dict, List
from pydantic import BaseModel, Field

class Event(BaseModel):
    id: str = Field(default_factory=lambda: str(asyncio.get_event_loop().time()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    source: str  # e.g., "worker-orders-1", "manager", "system"
    type: str    # e.g., "task_started", "tool_call", "heartbeat", "quarantine"
    payload: Dict[str, Any]

class EventLog:
    def __init__(self):
        self._events: List[Event] = []
        self._subscribers = []

    def append(self, source: str, event_type: str, payload: Dict[str, Any]) -> Event:
        event = Event(source=source, type=event_type, payload=payload)
        self._events.append(event)
        for sub in self._subscribers:
            # We don't await here to keep append synchronous, instead we push to an async queue or create task
            asyncio.create_task(sub(event))
        return event

    def subscribe(self, callback):
        self._subscribers.append(callback)

    def get_recent(self, limit: int = 100) -> List[Event]:
        return self._events[-limit:]

# Global event log for the company
company_log = EventLog()
