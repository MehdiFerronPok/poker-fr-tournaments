"""
CSV ingestor skeleton.

Many poker organisers publish schedules as CSV files. This ingestor reads a
CSV file and yields raw events. The mapping between columns and event fields
can be specified per source.
"""
from __future__ import annotations

import csv
import hashlib
import logging
from typing import Dict, Iterable, Optional

logger = logging.getLogger(__name__)


class CsvIngestor:
    def __init__(self, url: str, source_name: str, field_map: Dict[str, str]):
        """
        :param url: HTTP or file URL to the CSV resource.
        :param field_map: mapping from CSV column names to expected raw event keys
            (title, start, end, buy_in, variant, venue_name, address, city).
        """
        self.url = url
        self.source_name = source_name
        self.field_map = field_map

    def fetch(self) -> str:
        # For brevity, only support local file paths in this demonstration.
        logger.info("Loading CSV file: %s", self.url)
        return self.url

    def parse(self) -> Iterable[Dict[str, Optional[str]]]:
        path = self.fetch()
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                raw_event: Dict[str, Optional[str]] = {
                    "source_name": self.source_name,
                    "source_url": self.url,
                }
                for csv_field, event_key in self.field_map.items():
                    raw_event[event_key] = row.get(csv_field)
                # compute hash
                raw_event_str = str(raw_event).encode("utf-8", errors="ignore")
                raw_event["source_hash"] = hashlib.sha1(raw_event_str).hexdigest()
                yield raw_event
