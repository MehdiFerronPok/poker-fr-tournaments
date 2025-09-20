# Inventaire des ressources

Ce document liste les ressources créées et nécessaires au fonctionnement du
projet. Toutes les ressources sont sous la propriété de l’utilisateur
(`{{GITHUB_USERNAME}}`) ; aucun compte tiers de l’assistant n’est utilisé.

## Dépôts GitHub

- **poker-fr-tournaments** : monorepo principal contenant le code (ingestion,
  normalisation, API, web, docs). Propriétaire : {{GITHUB_USERNAME}}.

## Base de données

- **Neon Postgres** : instance avec PostGIS activé. Nom du projet et de la
  base à renseigner lors de la création. Stocke les tables `venues` et
  `tournaments`. Accès via `DATABASE_URL`.

## Services API

- **Fly.io app** : application `{{FLY_APP_NAME}}-api` déployant le conteneur
  FastAPI. Héberge l’API, accessible publiquement. Secrets configurés via
  `flyctl secrets set`.
- **Alternative Render.com** : service Web Docker pouvant héberger l’API.

## Frontend

- **Vercel project** : projet Next.js nommé `poker-fr-tournaments-web`.
  Variables d’environnement : `NEXT_PUBLIC_API_URL`.

## Monitoring

- **GitHub Actions** : workflows `ingest.yml`, `deploy.yml`, `monitor.yml`.
  Génèrent des alertes via le job summary ; possibilité d’ajouter des
  notifications Slack via webhook.

## Autres

- **Cache géocodage** : fichier SQLite `normalize/geocode_cache.sqlite` qui
  stocke le cache des requêtes Nominatim.
