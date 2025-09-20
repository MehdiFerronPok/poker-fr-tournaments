"""
Utility functions for normalisation.
"""
from __future__ import annotations

import re
from datetime import datetime
from typing import Optional

from dateutil import parser


def parse_datetime(value: Optional[str]) -> Optional[datetime]:
    """Parse a string into a timezone‑aware datetime.

    Accepts various formats; returns None if parsing fails.
    """
    if not value:
        return None
    try:
        dt = parser.isoparse(value)
        return dt
    except Exception:
        try:
            return parser.parse(value)
        except Exception:
            return None


def parse_buy_in(value: Optional[str]) -> Optional[int]:
    """Convert a buy‑in string or number into integer cents.

    Examples:
        "100" -> 10000
        "50 €" -> 5000
    Returns None if the input is not numeric.
    """
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return int(float(value) * 100)
    digits = re.findall(r"\d+", value.replace(".", ""))
    if not digits:
        return None
    amount = int(digits[0])
    return amount * 100


def normalize_variant(name: Optional[str]) -> Optional[str]:
    """Normalize variant names to a canonical set (Holdem, Omaha, Mixed)."""
    if not name:
        return None
    n = name.lower()
    if "hold" in n:
        return "Holdem"
    if "omaha" in n or "plo" in n:
        return "Omaha"
    if "mixed" in n:
        return "Mixed"
    return name.strip().capitalize()
