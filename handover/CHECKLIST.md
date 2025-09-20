# Checklist de déploiement et de transfert

Cette checklist présente toutes les étapes à suivre pour
provisionner, déployer et tester l’application Poker France
Tournaments, du clonage initial jusqu’à la mise en production.

## 1. Préparation

1. Installez les outils : GitHub CLI (`gh`), Fly.io CLI (`flyctl`),
   Vercel CLI (`vercel`), Neon CLI ou accès Web, Docker, `psql`, `poetry`.
2. Créez un nouveau projet sur [neon.tech](https://neon.tech/) et notez
   l’URL de connexion. Activez l’extension PostGIS.
3. Copiez ce dépôt sous votre compte GitHub :

   ```bash
   gh repo create {{GITHUB_USERNAME}}/poker-fr-tournaments --public --description "Monorepo des tournois de poker en France" --confirm
   git remote add origin git@github.com:{{GITHUB_USERNAME}}/poker-fr-tournaments.git
   git add . && git commit -m "Initial import" && git push -u origin main
   ```

## 2. Configuration des secrets

1. Exportez les variables d’environnement nécessaires :

   ```bash
   export DATABASE_URL="postgresql+psycopg://USER:PASSWORD@HOST/DB"
   export GEOCODER_USER_AGENT="poker-fr-tournaments/1.0 ({{USER_EMAIL}})"
   export ADMIN_USERNAME="admin"
   export ADMIN_PASSWORD="change-this-password"
   export FLY_API_TOKEN="<fly-token>"
   export FLY_APP_NAME="poker-fr-tournaments"
   export VERCEL_TOKEN="<vercel-token>"
   export VERCEL_ORG_ID="<vercel-org-id>"
   export VERCEL_PROJECT_ID="<vercel-project-id>"
   export MONITOR_API_URL="https://<future-api-url>"
   ```

2. Ajoutez ces secrets au dépôt GitHub :

   ```bash
   gh secret set DATABASE_URL -b "$DATABASE_URL"
   gh secret set GEOCODER_USER_AGENT -b "$GEOCODER_USER_AGENT"
   gh secret set ADMIN_USERNAME -b "$ADMIN_USERNAME"
   gh secret set ADMIN_PASSWORD -b "$ADMIN_PASSWORD"
   gh secret set FLY_API_TOKEN -b "$FLY_API_TOKEN"
   gh secret set FLY_APP_NAME -b "$FLY_APP_NAME"
   gh secret set VERCEL_TOKEN -b "$VERCEL_TOKEN"
   gh secret set VERCEL_ORG_ID -b "$VERCEL_ORG_ID"
   gh secret set VERCEL_PROJECT_ID -b "$VERCEL_PROJECT_ID"
   gh secret set MONITOR_API_URL -b "$MONITOR_API_URL"
   ```

## 3. Provisionnement de la base

1. Dans Neon, ouvrez votre projet et exécutez :

   ```bash
   psql "$DATABASE_URL" -c "CREATE EXTENSION IF NOT EXISTS postgis;"
   psql "$DATABASE_URL" -f schema/schema.sql
   ```

2. (Optionnel) Exécutez le script de seed :

   ```bash
   poetry run DATABASE_URL="$DATABASE_URL" python schema/seed.py
   ```

## 4. Tests locaux

1. Installez les dépendances Python et JS :

   ```bash
   poetry install --no-root
   cd web && npm install && cd ..
   ```

2. Exécutez les tests et le lint :

   ```bash
   make test
   make lint
   make e2e
   ```

3. Lancez le stack local pour tester manuellement :

   ```bash
   cp .env.example .env
   # Mettez à jour .env avec vos variables locales
   bash scripts/bootstrap_local.sh
   # Dans un autre terminal
   poetry run uvicorn api.main:app --reload --port 8000
   cd web && npm run dev
   ```

4. Ouvrez `http://localhost:3000` et vérifiez que la page d’accueil
   affiche les tournois de démonstration. Testez également `curl
   http://localhost:8000/health`.

## 5. Déploiement initial

1. Authentifiez‑vous auprès de Fly.io :

   ```bash
   flyctl auth token "$FLY_API_TOKEN"
   flyctl apps create "${FLY_APP_NAME}-api"
   ```

2. Déployez l’API :

   ```bash
   bash scripts/bootstrap_prod.sh
   ```

3. Notez l’URL de l’API Fly.io (ex : `https://poker-fr-tournaments-api.fly.dev`) et
   mettez à jour `MONITOR_API_URL` et `NEXT_PUBLIC_API_URL` (dans GitHub
   Secrets et Vercel).

4. Déployez le frontend avec Vercel. L’action GitHub `deploy.yml`
   exécutera automatiquement `vercel deploy` à chaque merge. Vous pouvez
   forcer un déploiement manuel :

   ```bash
   cd web && vercel deploy --prod --token "$VERCEL_TOKEN" --confirm --org "$VERCEL_ORG_ID" --proj "$VERCEL_PROJECT_ID"
   ```

## 6. Vérifications post‑déploiement

1. Ouvrez l’URL de l’API `/health` et assurez‑vous que la réponse est
   `{"status":"ok"}`.
2. Ouvrez l’URL du front et cherchez les tournois de démonstration.
3. Lancez les scripts de monitoring :

   ```bash
   DATABASE_URL="$DATABASE_URL" python monitoring/data_freshness.py
   API_URL="https://poker-fr-tournaments-api.fly.dev" python monitoring/endpoint_checks.py
   ```

4. Déclenchez l’ingestion via l’endpoint admin et vérifiez que les
   nouveaux événements apparaissent sur le site.

## 7. Opérations courantes

* Mettre à jour les sources dans `ingestion/sources/catalog.yml` lorsque
  de nouveaux organisateurs sont ajoutés.
* Consulter le runbook (`handover/RUNBOOK.md`) pour les procédures de
  monitoring et d’audit.
* Utiliser le plan de rollback (`handover/ROLLBACK.md`) en cas de
  problème.

## 8. Transfert à un nouvel opérateur

* Fournir l’accès au dépôt GitHub via `gh api` (voir `handover/ACCESS.md`).
* Créer un utilisateur Neon et fournir un accès restreint à la base.
* Inviter la personne aux projets Fly.io et Vercel.
* Partager ce dossier `handover/` pour qu’elle puisse reprendre l’exploitation.