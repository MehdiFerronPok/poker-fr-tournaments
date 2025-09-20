# Schéma de base de données

Le dossier `schema` contient la définition des tables nécessaires au projet
Poker France Tournaments. La base repose sur Postgres et l'extension
[PostGIS](https://postgis.net/) afin de manipuler des coordonnées géographiques.

## Création et initialisation

1. **Créer la base Neon**

   Utilisez l'interface Web Neon ou le CLI pour créer une instance Postgres.
   Activez l'extension PostGIS :

   ```sql
   CREATE EXTENSION IF NOT EXISTS postgis;
   ```

2. **Importer le schéma**

   Depuis votre terminal :

   ```bash
   # Remplacez la chaîne de connexion par votre URL Neon
   psql "$DATABASE_URL" -f schema/schema.sql
   ```

3. **Insérer des données factices (optionnel)**

   Le script `seed.py` permet d'insérer deux lieux et deux tournois de
   démonstration. Exécutez‑le ainsi :

   ```bash
   DATABASE_URL=postgresql+psycopg://user:pass@host/dbname poetry run python schema/seed.py
   ```

## Contraintes et index

* Un type énuméré `event_status` est créé pour contrôler le statut des
  tournois (`scheduled`, `cancelled`, `updated`).
* La table `venues` stocke les lieux avec un champ géométrique de type
  `Point` (EPSG 4326). Des index sont ajoutés sur la géométrie et la ville
  pour optimiser les recherches.
* La table `tournaments` référence un `venue_id`, enregistre le titre, les
  dates, le montant du buy‑in en centimes (pour éviter les flottants), la
  variante, le statut et un hachage de la source pour la traçabilité. Une
  contrainte d'unicité (`unique_event`) empêche l'insertion de doublons sur
  `(venue_id, title, start_datetime_local)`.
