"""
SQLAlchemy models reflecting the database schema.
"""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class Venue(Base):
    __tablename__ = "venues"
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    address = Column(Text)
    city = Column(Text)
    department = Column(Text)
    region = Column(Text)
    postcode = Column(Text)
    country = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    tournaments = relationship("Tournament", back_populates="venue")


class Tournament(Base):
    __tablename__ = "tournaments"
    id = Column(Integer, primary_key=True)
    venue_id = Column(Integer, ForeignKey("venues.id"), nullable=False)
    title = Column(Text, nullable=False)
    description = Column(Text)
    start_datetime_local = Column(DateTime, nullable=False)
    end_datetime_local = Column(DateTime)
    timezone = Column(String)
    buy_in_cents = Column(Integer)
    currency = Column(String)
    variant = Column(String)
    status = Column(String)
    source_url = Column(Text)
    source_hash = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    venue = relationship("Venue", back_populates="tournaments")
