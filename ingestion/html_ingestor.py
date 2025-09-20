"""
HTML ingestor using BeautifulSoup.

This ingestor fetches an HTML page containing a list of poker tournaments.
The page is expected to contain a table or list of events with fields
identifiable via CSS selectors. For demonstration purposes, selectors are
hard‑coded but can be customised per source in `sources/catalog.yml`.
"""
from __future__ import annotations

import hashlib
import logging
from datetime import datetime
from typing import Dict, Iterable, Optional

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class HtmlIngestor:
    def __init__(self, url: str, source_name: str) -> None:
        self.url = url
        self.source_name = source_name

    def fetch(self) -> str:
        logger.info("Fetching HTML page: %s", self.url)
        response = requests.get(self.url, timeout=30)
        response.raise_for_status()
        return response.text

    def parse(self) -> Iterable[Dict[str, Optional[str]]]:
        html = self.fetch()
        soup = BeautifulSoup(html, "html.parser")
        # Example: assume each event is in a div.event-item
        event_items = soup.select(".event-item")
        for item in event_items:
            title_el = item.select_one(".event-title")
            date_el = item.select_one(".event-date")
            venue_el = item.select_one(".event-venue")
            buyin_el = item.select_one(".event-buyin")
            title = title_el.get_text(strip=True) if title_el else ""
            date_text = date_el.get_text(strip=True) if date_el else ""
            start_iso: Optional[str] = None
            if date_text:
                # naive parsing; rely on normalizer to parse properly
                try:
                    start_iso = datetime.strptime(date_text, "%d/%m/%Y %H:%M").isoformat()
                except Exception:
                    start_iso = None
            venue = venue_el.get_text(strip=True) if venue_el else None
            buy_in = None
            if buyin_el:
                digits = ''.join(ch for ch in buyin_el.get_text() if ch.isdigit())
                buy_in = digits or None
            raw_event = {
                "source_name": self.source_name,
                "source_url": self.url,
                "title": title,
                "description": None,
                "start": start_iso,
                "end": None,
                "buy_in": buy_in,
                "variant": None,
                "venue_name": venue,
                "address": None,
                "city": None,
            }
            raw_event_str = str(raw_event).encode("utf-8", errors="ignore")
            raw_event["source_hash"] = hashlib.sha1(raw_event_str).hexdigest()
            yield raw_event
