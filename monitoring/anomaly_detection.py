"""
Detect anomalies in the tournaments dataset.

Anomalies include duplicate events (same venue, title, start date), negative
buy‑ins, or events scheduled in the past. This script prints alerts for
any anomalies found.
"""
from __future__ import annotations

import datetime as _dt
import os
import sys

from sqlalchemy import create_engine, text


def main() -> None:
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        print("DATABASE_URL is not set", file=sys.stderr)
        sys.exit(1)
    engine = create_engine(db_url)
    alerts = []
    with engine.connect() as conn:
        # Duplicate check
        dup = conn.execute(
            text(
                """
                SELECT venue_id, title, start_datetime_local, COUNT(*)
                FROM tournaments
                GROUP BY venue_id, title, start_datetime_local
                HAVING COUNT(*) > 1;
                """
            )
        ).fetchall()
        if dup:
            alerts.append(f"Found {len(dup)} duplicate events")
        # Negative or zero buy‑ins
        neg = conn.execute(
            text("SELECT COUNT(*) FROM tournaments WHERE buy_in_cents <= 0 AND buy_in_cents IS NOT NULL"),
        ).scalar() or 0
        if neg > 0:
            alerts.append(f"{neg} events have non‑positive buy‑in")
        # Past events check
        now = _dt.datetime.now(_dt.timezone.utc)
        past = conn.execute(
            text("SELECT COUNT(*) FROM tournaments WHERE start_datetime_local < :now"),
            {"now": now},
        ).scalar() or 0
        if past > 0:
            alerts.append(f"{past} events are scheduled in the past")
    if alerts:
        for a in alerts:
            print(f"ALERT: {a}")
    else:
        print("OK: No anomalies detected")


if __name__ == "__main__":
    main()
