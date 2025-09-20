"""
ICS (iCalendar) ingestor skeleton.

Some organisers publish tournament schedules as .ics files. This ingestor
demonstrates how to parse such files and yield events. It uses the
`ics` library if available.
"""
from __future__ import annotations

import hashlib
import logging
from datetime import datetime
from typing import Dict, Iterable, Optional

try:
    from ics import Calendar
except ImportError:
    Calendar = None  # type: ignore

logger = logging.getLogger(__name__)


class IcsIngestor:
    def __init__(self, url: str, source_name: str) -> None:
        self.url = url
        self.source_name = source_name

    def fetch(self) -> str:
        # For demo purposes, assume local file path
        logger.info("Loading .ics file: %s", self.url)
        return self.url

    def parse(self) -> Iterable[Dict[str, Optional[str]]]:
        if Calendar is None:
            raise RuntimeError("ics library not installed; run 'poetry add ics'")
        path = self.fetch()
        with open(path, "r", encoding="utf-8") as f:
            cal = Calendar(f.read())
        for event in cal.events:
            start = event.begin.datetime
            end = event.end.datetime if event.end else None
            raw_event = {
                "source_name": self.source_name,
                "source_url": self.url,
                "title": event.name,
                "description": event.description,
                "start": start.isoformat() if isinstance(start, datetime) else None,
                "end": end.isoformat() if isinstance(end, datetime) else None,
                "buy_in": None,
                "variant": None,
                "venue_name": None,
                "address": None,
                "city": None,
            }
            raw_event_str = str(raw_event).encode("utf-8", errors="ignore")
            raw_event["source_hash"] = hashlib.sha1(raw_event_str).hexdigest()
            yield raw_event
