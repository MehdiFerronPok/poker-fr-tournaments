# RUNBOOK d’exploitation

Ce runbook décrit toutes les actions nécessaires pour exploiter
l’application Poker France Tournaments au quotidien et en
mode opérateur. Il complète le guide de déploiement et centralise les
procédures de routine et de dépannage.

## Préparation de l’environnement

* Cloner le dépôt sur votre machine locale :

```bash
git clone git@github.com:{{GITHUB_USERNAME}}/poker-fr-tournaments.git
cd poker-fr-tournaments
```

* Copier le fichier `.env.example` en `.env` et renseigner les variables
  manquantes (`DATABASE_URL`, `GEOCODER_USER_AGENT`, `ADMIN_USERNAME`,
  `ADMIN_PASSWORD`, etc.).

* Installer les dépendances Python et JavaScript :

```bash
poetry install --no-root
cd web && npm install
```

* Démarrer la base de données locale et appliquer le schéma :

```bash
docker-compose -f infra/docker-compose.yml up -d db
poetry run psql "$DATABASE_URL" -c "CREATE EXTENSION IF NOT EXISTS postgis;"
poetry run psql "$DATABASE_URL" -f schema/schema.sql
```

* (Optionnel) Insérer des données de démonstration :

```bash
poetry run DATABASE_URL="$DATABASE_URL" python schema/seed.py
```

## Lancer et surveiller l’ingestion

L’ingestion est programmée via GitHub Actions (`ingest.yml`) tous les jours
à 05:00 Europe/Paris. Pour exécuter l’ingestion et la normalisation
manuellement :

```bash
poetry run GEOCODER_USER_AGENT="$GEOCODER_USER_AGENT" python ingestion/run_all.py
poetry run DATABASE_URL="$DATABASE_URL" GEOCODER_USER_AGENT="$GEOCODER_USER_AGENT" python normalize/normalizer.py
```

Les événements bruts sont enregistrés dans `ingestion/output/raw_events.jsonl`.
Après normalisation, vérifiez le nombre d’événements insérés dans la table
`tournaments` via un `SELECT COUNT(*)`.

Pour déclencher l’ingestion depuis l’API en production :

```bash
curl -u $ADMIN_USERNAME:$ADMIN_PASSWORD -X POST https://<api-url>/admin/ingest
```

## Vérifier la fraîcheur des données

Utilisez le script de monitoring pour contrôler qu’il existe des tournois à
venir :

```bash
DATABASE_URL="$DATABASE_URL" python monitoring/data_freshness.py
```

Si aucune ligne n’est retournée, cela indique que les sources n’ont pas
publié de nouveaux tournois ou que l’ingestion a échoué. Vérifiez le
workflow GitHub `ingest.yml` et les logs.

## Vérifier l’état de l’API

Testez le point de santé et la latence :

```bash
API_URL=https://<api-url> python monitoring/endpoint_checks.py
```

Ce script teste les endpoints `/health` et `/tournaments` et mesure le temps
de réponse. Une latence >1 seconde doit entraîner une investigation.

## Détecter les anomalies

Lancez la détection d’anomalies sur la base :

```bash
DATABASE_URL="$DATABASE_URL" python monitoring/anomaly_detection.py
```

Les anomalies typiques :

* **Duplicate events** : plusieurs lignes avec même titre, lieu et date. La
  contrainte d’unicité (`venue_id, title, start_datetime_local`) doit
  empêcher l’insertion de doublons.
* **Non‑positive buy‑in** : montants nuls ou négatifs. Corriger la source
  ou les règles de parsing dans `normalize/utils.py`.
* **Past events** : événements dont la date est antérieure à aujourd’hui.
  Ces lignes peuvent être purgées ou marquées comme `cancelled`.

## Consulter les logs

* **GitHub Actions** : l’onglet *Actions* dans GitHub affiche l’historique
  des exécutions de `ingest.yml`, `deploy.yml` et `monitor.yml`. Les logs
  JSON sont disponibles en artefacts.
* **Fly.io** : `flyctl logs -a <app-name>` affiche les logs du conteneur
  API. Utilisez `flyctl status` pour connaître l’état du service.
* **Render** : si l’API est hébergée sur Render, consultez la section
  *Logs* dans l’interface pour chaque build et runtime.
* **Vercel** : les logs d’accès et les builds sont accessibles depuis la
  console Vercel.

## Mise à jour du code et déploiement

1. Créez une branche et développez vos modifications. Validez avec
   `make test` puis `make lint`.
2. Soumettez une Pull Request. Le workflow `test.yml` vérifie les tests
   unitaires, le lint et la compilation.
3. Une fois la PR mergée sur `main`, `deploy.yml` déploie l’API (Fly.io
   et/ou Render) et le front (Vercel).
4. Surveillez l’exécution du workflow et vérifiez l’application
   déployée.

## Gestion des dépendances externes

Le géocodage repose sur l’API Nominatim (OpenStreetMap). Respectez la
politique d’utilisation : un minimum de 1 seconde entre deux requêtes et
l’utilisation d’un User‑Agent personnalisé【512638780003458†L27-L33】. Le
module `normalize/geocode.py` intègre `RateLimiter` pour respecter ce
délai【327003169146540†L552-L568】【327003169146540†L639-L668】. Mettez en
cache les résultats dans le fichier SQLite pour limiter les requêtes.

## Fin de vie et suppression

Pour supprimer l’infrastructure :

1. Supprimez l’application Fly.io : `flyctl apps destroy <app-name>`.
2. Supprimez le projet Vercel via la console Vercel.
3. Supprimez la base Neon depuis l’interface ou via l’API.
4. Supprimez le dépôt GitHub si nécessaire.

Documentez toute suppression et informez les parties prenantes avant de
détruire des ressources.