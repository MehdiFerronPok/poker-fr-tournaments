"""
Main application entry point for the FastAPI server.
"""
from __future__ import annotations

import base64
import os
from datetime import datetime
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Query, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session

from . import crud, deps
from .models import Tournament, Venue
from .schemas import TournamentOut, VenueOut


app = FastAPI(title="Poker France Tournaments API", version="1.0.0")

deps.init_db()

# Configure CORS to allow frontend domain(s)
origins = ["*"]  # Adjust to specific domains in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


security = HTTPBasic()


def verify_admin(credentials: HTTPBasicCredentials = Depends(security)) -> None:
    username = os.environ.get("ADMIN_USERNAME", "admin")
    password = os.environ.get("ADMIN_PASSWORD", "admin")
    correct = credentials.username == username and credentials.password == password
    if not correct:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")


def get_jsonld_for_tournament(t: Tournament, v: Venue) -> dict:
    """Build a JSON‑LD representation of a tournament using Schema.org Event."""
    return {
        "@context": "https://schema.org",
        "@type": "Event",
        "name": t.title,
        "startDate": t.start_datetime_local.isoformat(),
        "endDate": t.end_datetime_local.isoformat() if t.end_datetime_local else None,
        "location": {
            "@type": "Place",
            "name": v.name,
            "address": {
                "@type": "PostalAddress",
                "streetAddress": v.address,
                "addressLocality": v.city,
                "addressRegion": v.region,
                "addressCountry": v.country or "France",
            },
            "geo": {
                "@type": "GeoCoordinates",
                "latitude": v.latitude,
                "longitude": v.longitude,
            },
        },
        "offers": {
            "@type": "Offer",
            "price": (t.buy_in_cents / 100) if t.buy_in_cents else None,
            "priceCurrency": t.currency or "EUR",
            "availability": "https://schema.org/InStock",
        },
        "eventStatus": f"https://schema.org/{t.status.capitalize()}" if t.status else None,
        "description": t.description,
        "url": t.source_url,
        "organizer": {
            "@type": "Organization",
            "name": v.name,
        },
    }


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}


@app.get("/tournaments", response_model=List[TournamentOut])
def list_tournaments(
    city: Optional[str] = Query(None, description="Filter by city"),
    date_from: Optional[datetime] = Query(None, description="Start date (UTC)"),
    date_to: Optional[datetime] = Query(None, description="End date (UTC)"),
    buy_in_min: Optional[int] = Query(None, description="Minimum buy‑in in cents"),
    buy_in_max: Optional[int] = Query(None, description="Maximum buy‑in in cents"),
    variant: Optional[str] = Query(None, description="Filter by variant"),
    offset: int = 0,
    limit: int = 20,
    db: Session = Depends(deps.get_db),
) -> List[TournamentOut]:
    ts = crud.list_tournaments(
        db,
        city=city,
        date_from=date_from,
        date_to=date_to,
        buy_in_min=buy_in_min,
        buy_in_max=buy_in_max,
        variant=variant,
        offset=offset,
        limit=limit,
    )
    # convert to Pydantic model; includes nested venue due to orm_mode
    return ts  # type: ignore[return-value]


@app.get("/tournaments/{tournament_id}")
def get_tournament(tournament_id: int, db: Session = Depends(deps.get_db)) -> dict:
    t = crud.get_tournament(db, tournament_id)
    if not t:
        raise HTTPException(status_code=404, detail="Tournament not found")
    v = t.venue
    jsonld = get_jsonld_for_tournament(t, v)
    return {
        "tournament": TournamentOut.from_orm(t),
        "json_ld": jsonld,
    }


@app.get("/venues", response_model=List[VenueOut])
def list_venues(db: Session = Depends(deps.get_db)) -> List[VenueOut]:
    return crud.list_venues(db)  # type: ignore[return-value]


@app.post("/admin/ingest")
def admin_ingest(credentials: HTTPBasicCredentials = Depends(security)) -> dict:
    # Basic authentication
    verify_admin(credentials)
    # Run ingestion + normalisation synchronously
    from ingestion.run_all import main as ingestion_main  # imported here to avoid overhead
    from normalize.normalizer import normalize_and_upsert

    ingestion_main()
    normalize_and_upsert()
    return {"status": "ok", "message": "Ingestion and normalisation executed"}
