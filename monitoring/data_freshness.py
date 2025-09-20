"""
Check that the tournaments table has upcoming events.

If no event is scheduled in the future, this script prints an alert. It is
intended to run as part of a monitoring workflow.
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
    now = _dt.datetime.now(_dt.timezone.utc)
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT COUNT(*) FROM tournaments WHERE start_datetime_local >= :now"),
            {"now": now},
        )
        count = result.scalar() or 0
        if count == 0:
            print("ALERT: No upcoming tournaments found")
        else:
            print(f"OK: {count} upcoming tournaments")


if __name__ == "__main__":
    main()
