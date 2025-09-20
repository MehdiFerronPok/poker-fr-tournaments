"""
Database access functions.
"""
from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from .models import Tournament, Venue


def get_tournament(db: Session, tournament_id: int) -> Optional[Tournament]:
    return db.query(Tournament).filter(Tournament.id == tournament_id).first()


def list_tournaments(
    db: Session,
    *,
    city: Optional[str] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    buy_in_min: Optional[int] = None,
    buy_in_max: Optional[int] = None,
    variant: Optional[str] = None,
    offset: int = 0,
    limit: int = 20,
) -> List[Tournament]:
    query = db.query(Tournament).join(Venue)
    if city:
        query = query.filter(Venue.city.ilike(f"%{city}%"))
    if date_from:
        query = query.filter(Tournament.start_datetime_local >= date_from)
    if date_to:
        query = query.filter(Tournament.start_datetime_local <= date_to)
    if buy_in_min is not None:
        query = query.filter(Tournament.buy_in_cents >= buy_in_min)
    if buy_in_max is not None:
        query = query.filter(Tournament.buy_in_cents <= buy_in_max)
    if variant:
        query = query.filter(Tournament.variant.ilike(f"%{variant}%"))
    query = query.order_by(Tournament.start_datetime_local.asc())
    return query.offset(offset).limit(limit).all()


def list_venues(db: Session) -> List[Venue]:
    return db.query(Venue).all()
