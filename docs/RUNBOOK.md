# Runbook d’exploitation

Ce document décrit les opérations quotidiennes pour maintenir le site
Poker France Tournaments en bonne santé. Il explique comment lancer
l’ingestion, vérifier la fraîcheur des données, investiguer les alertes et
effectuer des opérations de maintenance.

## Environnement

Toutes les commandes supposent que vous avez cloné le dépôt et que les
variables d’environnement (`DATABASE_URL`, `GEOCODER_USER_AGENT`, etc.) sont
correctement définies. Utilisez `poetry shell` pour activer l’environnement
Python.

## Lancer manuellement l’ingestion

L’ingestion complète (récupération des sources + normalisation + upsert) est
programmée chaque nuit par GitHub Actions. Pour lancer manuellement :

```bash
poetry run python ingestion/run_all.py
poetry run python normalize/normalizer.py
```

Les événements bruts sont écrits dans `ingestion/output/raw_events.jsonl`. La
normalisation lit ce fichier et met à jour la base. Consultez les logs pour
contrôler le nombre d’événements importés.

## Redémarrer l’ingestion via l’API

Une route `/admin/ingest` est exposée par l’API et protégée par basic auth.
Pour l’exécuter :

```bash
curl -u $ADMIN_USERNAME:$ADMIN_PASSWORD -X POST https://<api-url>/admin/ingest
```

## Vérifier la fraîcheur des données

Utilisez le script de monitoring pour vérifier qu’il y a des tournois à venir :

```bash
DATABASE_URL=$DATABASE_URL python monitoring/data_freshness.py
```

S’il n’y a aucun tournoi futur, vérifiez la bonne exécution de l’ingestion.

## Vérifier l’état de l’API

```bash
API_URL=https://<api-url> python monitoring/endpoint_checks.py
```

Ce script vérifie les endpoints `/health` et `/tournaments` et mesure le temps
de réponse. En cas d’échec ou de latence excessive (>1s), contactez
l’administrateur ou relancez le conteneur sur Fly.io/Render.

## Détecter les anomalies

```bash
DATABASE_URL=$DATABASE_URL python monitoring/anomaly_detection.py
```

Les alertes possibles :

- **duplicate events** : plusieurs entrées avec même titre/lieu/date. La
  normalisation devrait éviter les doublons grâce à la contrainte d’unicité;
  investiguez les sources.
- **non‑positive buy‑in** : montants nuls ou négatifs ; ajustez les règles de
  parsing dans `normalize/utils.py`.
- **past events** : événements dont la date de début est dans le passé ; ces
  entrées peuvent être purgées périodiquement.

## Logs et audit

* **GitHub Actions** : consultez l’onglet *Actions* du dépôt pour suivre les
  exécutions de `ingest.yml`, `deploy.yml` et `monitor.yml`.
* **Fly.io/Render logs** : utilisez `flyctl logs -a <app-name>` ou consultez
  l’interface Render.
* **Base de données** : les tables `tournaments` et `venues` contiennent les
  colonnes `created_at` et `updated_at` pour tracer les modifications.

## Mise à jour du code

* Clonez le dépôt, créez une branche et soumettez une PR.
* Le workflow `test.yml` s’assure que les tests et linters passent.
* Après merge sur `main`, le workflow `deploy.yml` déploie automatiquement.
