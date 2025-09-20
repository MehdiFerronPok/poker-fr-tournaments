# Guide de déploiement

Ce document décrit comment déployer l’infrastructure de Poker France Tournaments
en utilisant vos propres comptes. Plusieurs alternatives sont proposées pour
l’API (Fly.io ou Render). L’interface web est déployée sur Vercel.

## Prérequis

* **GitHub CLI** : installez et connectez‑vous avec `gh auth login`.
* **Neon CLI** (ou utilisez l’interface Web) pour créer la base Postgres.
* **Fly.io CLI** : `brew install flyctl` puis `flyctl auth login`.
* **Render CLI** (optionnel) : `npm install -g render-cli`.
* **Vercel CLI** : `npm install -g vercel` puis `vercel login`.
* **psql** et **poetry** pour exécuter localement.

## 1. Création de la base de données Neon

1. Connectez‑vous sur [neon.tech](https://neon.tech/) et créez un nouveau projet.
2. Copiez l’URL de connexion Postgres (format
   `postgres://user:password@hostname/dbname`). Convertissez‑la au format SQLAlchemy
   utilisé par l’API :

   ```bash
   export DATABASE_URL="postgresql+psycopg://USER:PASSWORD@HOSTNAME/DBNAME"
   ```

3. Activez l’extension PostGIS et créez les tables :

   ```bash
   psql "$DATABASE_URL" -c "CREATE EXTENSION IF NOT EXISTS postgis;"
   psql "$DATABASE_URL" -f schema/schema.sql
   ```

4. Insérez des données de démonstration (optionnel) :

   ```bash
   DATABASE_URL=$DATABASE_URL poetry run python schema/seed.py
   ```

## 2. Configuration du dépôt GitHub

1. Créez le dépôt sur votre compte :

   ```bash
   gh repo create {{GITHUB_USERNAME}}/poker-fr-tournaments --public --description "Monorepo des tournois de poker en France" --confirm
   ```

2. Poussez le code initial :

   ```bash
   cd poker-fr-tournaments
   git init
   git remote add origin git@github.com:{{GITHUB_USERNAME}}/poker-fr-tournaments.git
   git add .
   git commit -m "Initial commit"
   git push -u origin main
   ```

3. Ajoutez les secrets nécessaires :

   ```bash
   gh secret set DATABASE_URL -b "$DATABASE_URL"
   gh secret set GEOCODER_USER_AGENT -b "poker-fr-tournaments/1.0 ({{USER_EMAIL}})"
   gh secret set ADMIN_USERNAME -b "admin"
   gh secret set ADMIN_PASSWORD -b "change-this-password"
   # Pour Fly.io
   gh secret set FLY_API_TOKEN -b "<votre-fly-api-token>"
   gh secret set FLY_APP_NAME -b "poker-fr-tournaments"
   # Pour Vercel
   gh secret set VERCEL_TOKEN -b "<votre-vercel-token>"
   gh secret set VERCEL_ORG_ID -b "<votre-org-id>"
   gh secret set VERCEL_PROJECT_ID -b "<votre-projet-id>"
   # Monitoring
   gh secret set MONITOR_API_URL -b "https://api.votre-domaine"
   ```

## 3. Déploiement de l’API

### Option A : Fly.io

1. Créez l’application :

   ```bash
   flyctl apps create ${{ secrets.FLY_APP_NAME }}-api
   ```

2. Configurez les secrets sur Fly.io :

   ```bash
   flyctl secrets set DATABASE_URL="$DATABASE_URL" GEOCODER_USER_AGENT="poker-fr-tournaments/1.0 ({{USER_EMAIL}})" ADMIN_USERNAME="admin" ADMIN_PASSWORD="change-this-password" -a ${{ secrets.FLY_APP_NAME }}-api
   ```

3. Déployez l’API :

   ```bash
   flyctl deploy --remote-only --app ${{ secrets.FLY_APP_NAME }}-api
   ```

4. Notez l’URL de l’API (ex. `https://poker-fr-tournaments-api.fly.dev`) et
   définissez `NEXT_PUBLIC_API_URL` sur cette valeur dans Vercel et `.env`.

### Option B : Render.com

1. Créez un service Web sur Render (type « Docker »). Utilisez le dépôt GitHub
   `poker-fr-tournaments` et pointez sur le dossier `api`.
2. Définissez les variables d’environnement `DATABASE_URL`, `GEOCODER_USER_AGENT`,
   `ADMIN_USERNAME` et `ADMIN_PASSWORD` via l’interface Render.
3. Déployez. L’URL sera du type `https://poker-fr-tournaments.onrender.com`.

## 4. Déploiement du frontend (Vercel)

1. Créez un projet Vercel lié au dossier `web` du dépôt.
2. Ajoutez la variable d’environnement `NEXT_PUBLIC_API_URL` pointant vers
   l’URL de l’API déployée.
3. Laissez Vercel détecter Next.js et déployer. L’URL sera du type
   `https://poker-fr-tournaments.vercel.app`.

## 5. Vérifications post‑déploiement

* Accédez à `https://poker-fr-tournaments.vercel.app` : la page d’accueil
  doit afficher les tournois de démonstration.
* Testez l’endpoint santé : `curl https://<api_url>/health` doit renvoyer
  `{"status":"ok"}`.
* Exécutez l’ingestion manuellement via l’endpoint protégé :

  ```bash
  curl -u admin:change-this-password -X POST https://<api_url>/admin/ingest
  ```

* Consultez la carte et les pages légales pour vérifier qu’elles s’affichent.

## 6. Alternative : déploiement local complet

Pour lancer l’architecture complète en local :

```bash
git clone git@github.com:{{GITHUB_USERNAME}}/poker-fr-tournaments.git
cd poker-fr-tournaments
cp .env.example .env
export DATABASE_URL=postgresql+psycopg://app:app@localhost:5433/poker
docker-compose -f infra/docker-compose.yml up --build
```

L’API sera disponible sur `http://localhost:8000` et le front sur
`http://localhost:3000` après avoir lancé `npm run dev` dans `web/`.
