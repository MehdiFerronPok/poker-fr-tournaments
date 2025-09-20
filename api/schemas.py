"""
Pydantic schemas for API responses.
"""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class VenueOut(BaseModel):
    id: int
    name: str
    address: Optional[str] = None
    city: Optional[str] = None
    department: Optional[str] = None
    region: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    class Config:
        orm_mode = True


class TournamentOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    start_datetime: datetime = Field(..., alias="start_datetime_local")
    end_datetime: Optional[datetime] = Field(None, alias="end_datetime_local")
    timezone: Optional[str] = None
    buy_in_cents: Optional[int] = None
    currency: Optional[str] = None
    variant: Optional[str] = None
    status: Optional[str] = None
    source_url: Optional[str] = None
    venue: VenueOut

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
