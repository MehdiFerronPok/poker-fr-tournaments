"""
Populate the database with example venues and tournaments.

Run this script after creating the database and applying the schema.

Example usage:

    DATABASE_URL=postgresql+psycopg://user:pass@host/dbname poetry run python schema/seed.py
"""
import datetime as _dt
import os
from sqlalchemy import create_engine, text


def seed():
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        raise RuntimeError("DATABASE_URL environment variable is not set")

    engine = create_engine(db_url)
    now = _dt.datetime.now(_dt.timezone.utc)

    with engine.begin() as conn:
        # Insert venues
        res = conn.execute(
            text(
                """
                INSERT INTO venues (name, address, city, department, region, postcode, latitude, longitude, geom)
                VALUES
                    (:name1, :addr1, :city1, :dept1, :region1, :postcode1, :lat1, :lon1, ST_SetSRID(ST_MakePoint(:lon1, :lat1), 4326)),
                    (:name2, :addr2, :city2, :dept2, :region2, :postcode2, :lat2, :lon2, ST_SetSRID(ST_MakePoint(:lon2, :lat2), 4326))
                ON CONFLICT DO NOTHING;
                """
            ),
            {
                "name1": "Casino Barrière",
                "addr1": "2 Rue des Casinos",
                "city1": "Deauville",
                "dept1": "Calvados",
                "region1": "Normandie",
                "postcode1": "14800",
                "lat1": 49.357,
                "lon1": 0.088,
                "name2": "Pasino Grand",
                "addr2": "1 Avenue de l'Europe",
                "city2": "Aix-en-Provence",
                "dept2": "Bouches-du-Rhône",
                "region2": "Provence-Alpes-Côte d'Azur",
                "postcode2": "13090",
                "lat2": 43.528,
                "lon2": 5.451,
            },
        )
        # Retrieve venue IDs
        rows = conn.execute(text("SELECT id, name FROM venues LIMIT 2"))
        venues = {row.name: row.id for row in rows}

        # Insert tournaments
        conn.execute(
            text(
                """
                INSERT INTO tournaments (venue_id, title, description, start_datetime_local, end_datetime_local, buy_in_cents, variant, status, source_url, source_hash)
                VALUES
                    (:vid1, 'Texas Hold'em Deepstack', 'Tournoi de démonstration', :start1, :end1, 15000, 'Holdem', 'scheduled', 'https://example.com/deepstack', 'hash1'),
                    (:vid2, 'Omaha High Rollers', 'Tournoi Omaha PLO', :start2, :end2, 50000, 'Omaha', 'scheduled', 'https://example.com/omaha', 'hash2')
                ON CONFLICT DO NOTHING;
                """
            ),
            {
                "vid1": venues.get("Casino Barrière"),
                "start1": now + _dt.timedelta(days=7),
                "end1": now + _dt.timedelta(days=7, hours=6),
                "vid2": venues.get("Pasino Grand"),
                "start2": now + _dt.timedelta(days=14),
                "end2": now + _dt.timedelta(days=14, hours=4),
            },
        )

    print("Seed data inserted successfully.")


if __name__ == "__main__":
    seed()
