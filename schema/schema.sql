-- Schema definition for the Poker France Tournaments project.
-- Requires PostGIS extension for geographic columns.

CREATE EXTENSION IF NOT EXISTS postgis;

-- Enumerated type for tournament status.
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'event_status') THEN
        CREATE TYPE event_status AS ENUM ('scheduled', 'cancelled', 'updated');
    END IF;
END$$;

-- Table of venues (casinos or organisers).
CREATE TABLE IF NOT EXISTS venues (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    address TEXT,
    city TEXT,
    department TEXT,
    region TEXT,
    postcode TEXT,
    country TEXT DEFAULT 'France',
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    geom geometry(Point, 4326),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_venues_geom ON venues USING GIST (geom);
CREATE INDEX IF NOT EXISTS idx_venues_city ON venues (city);

-- Table of tournaments/events.
CREATE TABLE IF NOT EXISTS tournaments (
    id SERIAL PRIMARY KEY,
    venue_id INTEGER NOT NULL REFERENCES venues(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    description TEXT,
    start_datetime_local TIMESTAMPTZ NOT NULL,
    end_datetime_local TIMESTAMPTZ,
    timezone TEXT DEFAULT '{{TIMEZONE}}',
    buy_in_cents INTEGER,
    currency TEXT DEFAULT 'EUR',
    variant TEXT,
    status event_status DEFAULT 'scheduled',
    source_url TEXT,
    source_hash TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT unique_event UNIQUE (venue_id, title, start_datetime_local)
);

CREATE INDEX IF NOT EXISTS idx_tournaments_start ON tournaments (start_datetime_local);
CREATE INDEX IF NOT EXISTS idx_tournaments_status ON tournaments (status);
CREATE INDEX IF NOT EXISTS idx_tournaments_variant ON tournaments (variant);
