"""
Geocoding utilities with caching and rate limiting.

This module wraps the geopy Nominatim geocoder with a RateLimiter to respect
the usage policy of Nominatim (max 1 request per second, valid user agent,
and caching)【512638780003458†L27-L47】. Results are cached in a local SQLite database to
avoid repeated calls for the same address【512638780003458†L49-L65】.
"""
from __future__ import annotations

import os
import sqlite3
from dataclasses import dataclass
from typing import Optional, Tuple

from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim

DB_PATH = os.environ.get("GEOCODE_CACHE_PATH", os.path.join(os.path.dirname(__file__), "geocode_cache.sqlite"))


@dataclass
class GeocodeResult:
    lat: float
    lon: float
    department: Optional[str]
    region: Optional[str]


def _init_db(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS cache (
            address TEXT PRIMARY KEY,
            lat REAL,
            lon REAL,
            department TEXT,
            region TEXT
        )
        """
    )
    conn.commit()


def geocode(address: str) -> Optional[GeocodeResult]:
    """
    Geocode an address using Nominatim with caching.

    Returns a GeocodeResult or None if not found.
    """
    if not address:
        return None
    conn = sqlite3.connect(DB_PATH)
    _init_db(conn)
    cur = conn.cursor()
    row = cur.execute("SELECT lat, lon, department, region FROM cache WHERE address = ?", (address,)).fetchone()
    if row:
        return GeocodeResult(lat=row[0], lon=row[1], department=row[2], region=row[3])
    # Not cached; query geocoding service
    user_agent = os.environ.get("GEOCODER_USER_AGENT", "poker-fr-tournaments/1.0")
    geolocator = Nominatim(user_agent=user_agent)
    min_delay = float(os.environ.get("GEOCODER_MIN_DELAY_SECONDS", "1"))
    geocode_fn = RateLimiter(geolocator.geocode, min_delay_seconds=min_delay)
    location = geocode_fn(address)
    if not location:
        return None
    lat = location.latitude
    lon = location.longitude
    # Attempt to extract department and region from address details
    address_raw = location.raw.get("address", {})
    department = address_raw.get("county") or address_raw.get("state_district")
    region = address_raw.get("state")
    cur.execute(
        "INSERT OR REPLACE INTO cache (address, lat, lon, department, region) VALUES (?, ?, ?, ?, ?)",
        (address, lat, lon, department, region),
    )
    conn.commit()
    return GeocodeResult(lat=lat, lon=lon, department=department, region=region)
