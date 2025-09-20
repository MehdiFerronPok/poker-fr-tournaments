"""
RSS ingestor for poker tournaments.

This ingestor uses the `feedparser` library to parse an RSS feed and extract
information about poker tournaments. Each entry in the feed is converted into
a dictionary containing the raw fields expected by the normalisation pipeline.
"""
from __future__ import annotations

import hashlib
import logging
import re
from datetime import datetime, timezone
from typing import Dict, Iterable, Optional

import feedparser

logger = logging.getLogger(__name__)


class RssIngestor:
    """Parses an RSS/Atom feed and yields raw event dictionaries."""

    def __init__(self, url: str, source_name: str) -> None:
        self.url = url
        self.source_name = source_name

    def fetch(self) -> feedparser.FeedParserDict:
        """Download and parse the RSS feed."""
        logger.info("Fetching RSS feed: %s", self.url)
        return feedparser.parse(self.url)

    def parse(self) -> Iterable[Dict[str, Optional[str]]]:
        """Yield raw event dicts extracted from the feed."""
        feed = self.fetch()
        for entry in feed.entries:
            title = entry.get("title", "").strip()
            description = entry.get("summary", "").strip()
            link = entry.get("link")
            published = entry.get("published") or entry.get("updated")
            published_parsed = None
            if published:
                try:
                    published_parsed = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
                except Exception:  # noqa: BLE001
                    published_parsed = None
            # Attempt to extract buy-in from description (e.g. "Buy-in: 150 €")
            buy_in = None
            match = re.search(r"buy[- ]?in[:\s]*([0-9]+)\s*€", description, re.IGNORECASE)
            if match:
                buy_in = match.group(1)
            raw_event = {
                "source_name": self.source_name,
                "source_url": link,
                "title": title,
                "description": description,
                "start": published_parsed.isoformat() if published_parsed else None,
                "end": None,
                "buy_in": buy_in,
                "variant": None,
                "venue_name": None,
                "address": None,
                "city": None,
            }
            # Compute a hash of the raw event for deduplication/traceability
            raw_event_str = str(raw_event).encode("utf-8", errors="ignore")
            raw_event["source_hash"] = hashlib.sha1(raw_event_str).hexdigest()
            yield raw_event
