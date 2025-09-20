"""
Normalisation pipeline for raw events.

This module reads raw events produced by the ingestion layer, cleans and
transforms them into the canonical schema defined in the database, and upserts
them into the Postgres database. It performs parsing of dates, buy‑ins and
variants, geocoding of venues, deduplication and validation.
"""
from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, Optional

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from .geocode import geocode as geocode_address
from .utils import normalize_variant, parse_buy_in, parse_datetime


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def load_raw_events(path: str) -> Iterable[Dict]:
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            yield json.loads(line)


def get_engine() -> Engine:
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        raise RuntimeError("DATABASE_URL environment variable is not set")
    engine = create_engine(db_url, echo=False, future=True)
    return engine


def upsert_venue(conn, name: str, address: Optional[str], city: Optional[str], department: Optional[str], region: Optional[str], lat: Optional[float], lon: Optional[float]):
    """Insert or update a venue and return its ID."""
    # Attempt to find existing venue by name + city
    row = conn.execute(
        text("SELECT id FROM venues WHERE name = :name AND city = :city"),
        {"name": name, "city": city},
    ).fetchone()
    if row:
        return row.id
    # Insert new venue
    geom_expr = "ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)" if lat and lon else None
    if geom_expr:
        insert_sql = text(
            """
            INSERT INTO venues (name, address, city, department, region, postcode, latitude, longitude, geom)
            VALUES (:name, :address, :city, :department, :region, NULL, :lat, :lon, ST_SetSRID(ST_MakePoint(:lon, :lat), 4326))
            RETURNING id
            """
        )
        params = {
            "name": name,
            "address": address,
            "city": city,
            "department": department,
            "region": region,
            "lat": lat,
            "lon": lon,
        }
    else:
        insert_sql = text(
            """
            INSERT INTO venues (name, address, city, department, region)
            VALUES (:name, :address, :city, :department, :region)
            RETURNING id
            """
        )
        params = {
            "name": name,
            "address": address,
            "city": city,
            "department": department,
            "region": region,
        }
    res = conn.execute(insert_sql, params)
    vid = res.scalar()
    return vid


def upsert_tournament(conn, venue_id: int, event: Dict) -> None:
    """Insert or update a tournament based on unique constraint."""
    insert_sql = text(
        """
        INSERT INTO tournaments (venue_id, title, description, start_datetime_local, end_datetime_local, timezone, buy_in_cents, currency, variant, status, source_url, source_hash)
        VALUES (:venue_id, :title, :description, :start, :end, :tz, :buy_in_cents, :currency, :variant, :status, :source_url, :source_hash)
        ON CONFLICT (venue_id, title, start_datetime_local) DO UPDATE
        SET description = EXCLUDED.description,
            end_datetime_local = EXCLUDED.end_datetime_local,
            buy_in_cents = EXCLUDED.buy_in_cents,
            variant = EXCLUDED.variant,
            status = EXCLUDED.status,
            source_url = EXCLUDED.source_url,
            source_hash = EXCLUDED.source_hash,
            updated_at = NOW()
        ;
        """
    )
    conn.execute(insert_sql, {
        "venue_id": venue_id,
        "title": event["title"],
        "description": event.get("description"),
        "start": event["start"],
        "end": event.get("end"),
        "tz": event.get("timezone", "{{TIMEZONE}}"),
        "buy_in_cents": event.get("buy_in_cents"),
        "currency": "EUR",
        "variant": event.get("variant"),
        "status": event.get("status", "scheduled"),
        "source_url": event.get("source_url"),
        "source_hash": event.get("source_hash"),
    })


def normalize_event(raw: Dict) -> Optional[Dict]:
    """Normalize a raw event dictionary into DB-ready fields.

    Returns None if required fields are missing or invalid.
    """
    title = raw.get("title")
    if not title:
        return None
    start_dt = parse_datetime(raw.get("start"))
    if not start_dt:
        # Without a valid start date we cannot insert
        return None
    end_dt = parse_datetime(raw.get("end"))
    buy_in_cents = parse_buy_in(raw.get("buy_in"))
    variant = normalize_variant(raw.get("variant"))
    return {
        "title": title.strip(),
        "description": raw.get("description"),
        "start": start_dt.astimezone(timezone.utc),
        "end": end_dt.astimezone(timezone.utc) if end_dt else None,
        "buy_in_cents": buy_in_cents,
        "variant": variant,
        "venue_name": raw.get("venue_name"),
        "address": raw.get("address"),
        "city": raw.get("city"),
        "source_url": raw.get("source_url"),
        "source_hash": raw.get("source_hash"),
        "status": raw.get("status", "scheduled"),
        "timezone": "{{TIMEZONE}}",
    }


def normalize_and_upsert(raw_events_path: Optional[str] = None) -> None:
    """Main entry point: normalise all events from the given file and upsert them."""
    if raw_events_path is None:
        raw_events_path = str(Path(__file__).parents[1] / "ingestion" / "output" / "raw_events.jsonl")
    engine = get_engine()
    count = 0
    with engine.begin() as conn:
        for raw in load_raw_events(raw_events_path):
            ev = normalize_event(raw)
            if not ev:
                continue
            # Determine venue information and geocode if needed
            venue_name = ev.get("venue_name") or "Unknown Venue"
            address = ev.get("address")
            city = ev.get("city")
            lat = lon = dept = region = None
            if address or city:
                addr_str = ", ".join(filter(None, [venue_name, address, city, "France"]))
                geo = geocode_address(addr_str)
                if geo:
                    lat = geo.lat
                    lon = geo.lon
                    dept = geo.department
                    region = geo.region
            venue_id = upsert_venue(conn, venue_name, address, city, dept, region, lat, lon)
            upsert_tournament(conn, venue_id, ev)
            count += 1
    logger.info("Normalisation complete: inserted/updated %d events", count)


if __name__ == "__main__":
    normalize_and_upsert()
