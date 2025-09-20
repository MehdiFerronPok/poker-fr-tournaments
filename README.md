# Poker France Tournaments

Bienvenue ! Ce projet recense les tournois de poker officiels (casinos et
organisateurs reconnus) en France et fournit une API et une interface web pour
les consulter. L'objectif est d'offrir une visibilité centralisée des
tournois à venir, avec mise à jour quotidienne automatique via un pipeline
d'ingestion et de normalisation.

## Aperçu de l'architecture

Ce monorepo est organisé en plusieurs sous‐répertoires :

- **schema** : schéma de base de données Postgres + PostGIS, scripts de
  migration et données factices.
- **ingestion** : connecteurs pour récupérer des informations de tournois
  (RSS, fichiers HTML, CSV, etc.) et les convertir en événements bruts.
- **normalize** : normalisation des événements (parsing de dates, buy‑in,
  variantes, géocodage) et upsert dans la base.
- **api** : API HTTP basée sur FastAPI qui expose les tournois et lieux via
  des endpoints REST et JSON‑LD.
- **web** : interface utilisateur Next.js 14 App Router avec Tailwind CSS.
- **monitoring** : scripts pour vérifier la santé de l'API et la fraîcheur
  des données.
- **infra** : Dockerfiles, docker‑compose et GitHub Actions.
- **docs** : documentation détaillée (déploiement, runbook, roadmap).
- **handover** : documents de transfert et de reprise.

## Principes de fonctionnement

1. **Ingestion** : chaque source définie dans `ingestion/sources/catalog.yml`
   est traitée quotidiennement. Des connecteurs (RSS, HTML, etc.) extraient
   les événements bruts avec leurs métadonnées (titre, date, buy‑in, lieu,
   url source).
2. **Normalisation** : les événements bruts sont transformés en
   instances structurées : dates sont converties en timezone Europe/Paris,
   montants convertis en euros, variantes normalisées, géocodage des
   adresses. Le module `geopy.extra.RateLimiter` est utilisé pour limiter
   les appels à Nominatim à un maximum de 1 requête par seconde【327003169146540†L552-L560】, en accord avec la
   politique d'utilisation de Nominatim qui impose de ne pas dépasser 1
   requête/seconde et d'activer un cache【512638780003458†L27-L51】.
3. **API** : la base de données est exposée via FastAPI. Les endpoints
   permettent de filtrer par ville, date, buy‑in, variante et d'obtenir
   l'JSON‑LD conforme au type `Event` de Schema.org. Selon la documentation
   Schema.org, un « Event » est un événement qui se produit à un certain
   moment et à un endroit donné【391882911108107†L22-L24】.
4. **Frontend** : l'application Next.js consomme l'API et propose une
   recherche, une carte interactive et des fiches détaillées.
5. **CI/CD & monitoring** : GitHub Actions effectue l'ingestion quotidienne,
   déploie l'API (Fly.io ou Render) et le frontend (Vercel), exécute les
   tests et les linters. D'autres workflows vérifient la fraîcheur des
   données et envoient des alertes.

## Démarrage rapide local

### Pré‐requis

* Python 3.11 avec [Poetry](https://python-poetry.org/) pour gérer les
  dépendances.
* Node.js 18+ pour le frontend Next.js.
* [Docker](https://www.docker.com/) et [docker-compose](https://docs.docker.com/compose/).
* Compte Neon pour la base Postgres + PostGIS.

### Lancer en local

1. Copiez `.env.example` vers `.env` et remplissez les variables (en
   particulier `DATABASE_URL`).
2. Lancez le script de bootstrap :

   ```bash
   cd poker-fr-tournaments
   bash scripts/bootstrap_local.sh
   ```

   Cela construit les images Docker, démarre la base de données, l'API et
   l'interface web. L'API est accessible sur `http://localhost:8000` et
   l'interface web sur `http://localhost:3000`.

3. Pour exécuter l'ingestion et la normalisation manuellement :

   ```bash
   poetry run python ingestion/run_all.py
   poetry run python normalize/normalizer.py
   ```

4. Pour exécuter les tests :

   ```bash
   make test
   ```

## Création des dépôts GitHub

Le projet est conçu comme un monorepo. Pour le créer sous votre compte GitHub,
utilisez les commandes suivantes (exécuter depuis le dossier parent) :

```bash
# Remplacez `{{GITHUB_USERNAME}}` par votre identifiant GitHub.
gh repo create {{GITHUB_USERNAME}}/poker-fr-tournaments --public --description "Monorepo pour les tournois de poker en France" --homepage "https://{{DOMAIN_NAME}}" --confirm

# Activez la protection de la branche main (obligation de PR, 1 review)
gh api -X PATCH -H "Accept: application/vnd.github+json" \
  /repos/{{GITHUB_USERNAME}}/poker-fr-tournaments/branches/main/protection \
  -f required_status_checks='{"strict":true,"contexts":[]}' \
  -f enforce_admins=true \
  -f required_pull_request_reviews='{"required_approving_review_count":1}' \
  -f restrictions='null'
```

Pour chaque sous‐répertoire (par exemple `web`), vous pouvez également créer un
projet Vercel/Fly/Render via leur CLI. Les instructions détaillées sont dans
`docs/DEPLOY.md`.

## Licence

Ce projet est publié sous licence MIT. Les données des tournois proviennent
exclusivement de sources publiques et officielles ; assurez‑vous de respecter
leurs conditions d'utilisation.
