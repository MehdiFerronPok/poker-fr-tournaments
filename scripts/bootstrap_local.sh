#!/bin/bash
# Bootstrap local environment for the Poker France Tournaments project.
#
# This script installs dependencies, starts the local database using
# docker‑compose and runs the initial ingestion pipeline. It expects
# environment variables to be defined in a `.env` file in the root
# of the repository. Copy `.env.example` to `.env` and fill in the
# placeholders before running.
#
# Usage: bash scripts/bootstrap_local.sh

set -euo pipefail

# Check for required commands
command -v docker-compose >/dev/null 2>&1 || {
  echo >&2 "docker-compose is required. Please install Docker Desktop."; exit 1;
}
command -v poetry >/dev/null 2>&1 || {
  echo >&2 "Poetry is required. Install via 'pipx install poetry'."; exit 1;
}

# Load environment variables from .env
if [ ! -f .env ]; then
  echo "Missing .env file. Please copy .env.example to .env and fill in the variables."
  exit 1
fi
export $(grep -v '^#' .env | xargs)

echo "Installing Python dependencies via Poetry..."
poetry install --no-root

echo "Starting local database via docker-compose..."
docker-compose -f infra/docker-compose.yml up -d db

echo "Waiting for database to be ready..."
sleep 5

echo "Applying database schema..."
poetry run psql "$DATABASE_URL" -c "CREATE EXTENSION IF NOT EXISTS postgis;"
poetry run psql "$DATABASE_URL" -f schema/schema.sql

echo "Seeding demonstration data..."
poetry run DATABASE_URL="$DATABASE_URL" python schema/seed.py || true

echo "Running ingestion and normalization pipelines..."
poetry run GEOCODER_USER_AGENT="$GEOCODER_USER_AGENT" python ingestion/run_all.py
poetry run DATABASE_URL="$DATABASE_URL" GEOCODER_USER_AGENT="$GEOCODER_USER_AGENT" python normalize/normalizer.py

echo "Local bootstrap complete."
echo "You can now start the API with 'poetry run uvicorn api.main:app --reload' "
echo "and launch the frontend in the web folder with 'npm install' and 'npm run dev'."