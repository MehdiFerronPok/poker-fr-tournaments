#!/bin/bash
# Bootstrap production deployment for Poker France Tournaments.
#
# This script provides a skeleton for deploying the API to Fly.io (or
# Render) and the frontend to Vercel. Because deployment requires
# authentication tokens and resources created under your own account,
# the script uses environment variables that you must export beforehand.
#
# Required environment variables (replace placeholders before running):
#   FLY_API_TOKEN      – Fly.io API token (`fly auth token`)
#   FLY_APP_NAME       – Name of your Fly.io app (e.g. poker-fr-tournaments)
#   DATABASE_URL       – SQLAlchemy URL to your Neon Postgres instance
#   GEOCODER_USER_AGENT – User agent for Nominatim (see .env.example)
#   ADMIN_USERNAME/ADMIN_PASSWORD – credentials for admin endpoint
#   VERCEL_TOKEN       – Personal Vercel token
#   VERCEL_ORG_ID      – Vercel organisation ID
#   VERCEL_PROJECT_ID  – Vercel project ID
#
# Usage: bash scripts/bootstrap_prod.sh

set -euo pipefail

if [[ -z "${FLY_API_TOKEN:-}" || -z "${FLY_APP_NAME:-}" ]]; then
  echo "FLY_API_TOKEN and FLY_APP_NAME must be set to deploy the API."
  exit 1
fi

# Login to Fly.io
echo "Authenticating to Fly.io..."
flyctl auth token "$FLY_API_TOKEN"

echo "Creating Fly.io app (if it doesn't already exist)..."
flyctl apps create "${FLY_APP_NAME}-api" || true

echo "Setting secrets on Fly.io..."
flyctl secrets set \
  DATABASE_URL="$DATABASE_URL" \
  GEOCODER_USER_AGENT="$GEOCODER_USER_AGENT" \
  ADMIN_USERNAME="$ADMIN_USERNAME" \
  ADMIN_PASSWORD="$ADMIN_PASSWORD" \
  -a "${FLY_APP_NAME}-api"

echo "Deploying API to Fly.io..."
flyctl deploy --remote-only --app "${FLY_APP_NAME}-api"

echo "API deployed. Note the URL above."

if [[ -n "${VERCEL_TOKEN:-}" && -n "${VERCEL_ORG_ID:-}" && -n "${VERCEL_PROJECT_ID:-}" ]]; then
  echo "Deploying frontend to Vercel..."
  (cd web && vercel deploy --prod --token "$VERCEL_TOKEN" --confirm --org "$VERCEL_ORG_ID" --proj "$VERCEL_PROJECT_ID")
else
  echo "Skipping Vercel deployment because VERCEL_TOKEN, VERCEL_ORG_ID or VERCEL_PROJECT_ID is not set."
fi

echo "Production bootstrap complete. You should verify the deployment via the URLs provided by Fly.io and Vercel."