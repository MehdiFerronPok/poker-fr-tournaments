# Feuille de route (3 mois)

Ce document liste les améliorations prévues pour les prochaines itérations.
Chaque tâche est décrite avec ses critères d’acceptation, une estimation et
une priorité relative.

## Connecteurs supplémentaires

| Tâche | Description | Critères | Estimation | Priorité |
| --- | --- | --- | --- | --- |
| **Ingestor CSV/ICS** | Supporter des sources au format CSV et iCalendar (ICS) avec mapping des colonnes | Capable de lire un fichier CSV/ICS et de produire des événements bruts ; tests unitaires | 3 jours | Haute |
| **Authentification source** | Ajouter la possibilité de récupérer des pages protégées par mot de passe/captcha via Playwright | Playwright lance un navigateur headless et extrait les données ; respecter les ToS | 5 jours | Moyenne |

## Normalisation & données

| Tâche | Description | Critères | Estimation | Priorité |
| --- | --- | --- | --- | --- |
| **Améliorer le géocodage** | Utiliser un cache Redis plutôt que SQLite ; ajouter fallback vers API IGN | Diminuer la latence du géocodage ; logs sur le taux de hit | 4 jours | Moyenne |
| **Déduplication fuzzy** | Utiliser l’algorithme fuzzywuzzy pour éviter les doublons (titre + lieu ±2 h, score ≥90 %) | Implémentation dans normaliseur, tests sur jeux de données | 3 jours | Haute |

## API & backend

| Tâche | Description | Critères | Estimation | Priorité |
| --- | --- | --- | --- | --- |
| **Pagination cursor‑based** | Remplacer offset/limit par pagination via curseurs pour de meilleures perfs | Endpoints renvoient un `next_cursor` ; documentation mise à jour | 2 jours | Moyenne |
| **Filtre buy‑in/variante avancé** | Supporter les plages et la monnaie ; normaliser les variantes exotiques | Tests sur filtres combinés | 2 jours | Basse |

## Frontend

| Tâche | Description | Critères | Estimation | Priorité |
| --- | --- | --- | --- | --- |
| **Améliorer la carte** | Clustering des marqueurs ; filtre dynamique ; itinéraires | Utilisation de supercluster ; performance acceptée sur mobile | 4 jours | Haute |
| **Référencement avancé** | Générer des images OG dynamiques ; structurer les données pour les pages de ville | Amélioration du score Lighthouse SEO ; couverture Schema.org complète | 3 jours | Moyenne |

## DevOps & observabilité

| Tâche | Description | Critères | Estimation | Priorité |
| --- | --- | --- | --- | --- |
| **Grafana/Prometheus** | Exporter des métriques (durée d’ingestion, requêtes API) et créer des dashboards | Dashboard disponible ; alertes Slack si seuil dépassé | 5 jours | Basse |
| **Terraform** | Gérer l’infra (Neon, Fly, Vercel, monitor) via Terraform | Fichiers `.tf` versionnés ; apply idempotent | 6 jours | Basse |
