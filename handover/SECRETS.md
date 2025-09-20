# Inventaire des secrets

Les secrets nécessaires au fonctionnement du projet ne doivent jamais être
commis dans le dépôt. Ils sont stockés dans des gestionnaires dédiés
(GitHub Secrets, Fly.io secrets, Vercel environment variables). Voici la
liste complète des secrets utilisés :

| Nom du secret | Description | Emplacement |
| --- | --- | --- |
| `DATABASE_URL` | Chaîne de connexion SQLAlchemy vers la base Neon (inclut utilisateur, mot de passe, hôte, base). | GitHub Secrets, Fly.io secrets, Render env |
| `GEOCODER_USER_AGENT` | User-Agent personnalisé requis par Nominatim【512638780003458†L27-L33】. | GitHub Secrets, Fly.io secrets |
| `ADMIN_USERNAME`/`ADMIN_PASSWORD` | Identifiants Basic Auth pour l’endpoint `/admin/ingest`. | GitHub Secrets, Fly.io secrets |
| `FLY_API_TOKEN` | Jeton API Fly.io permettant de déployer via CLI. | GitHub Secrets |
| `FLY_APP_NAME` | Nom de l’app Fly.io. | GitHub Secrets |
| `RENDER_API_KEY` | (Optionnel) Clé API pour Render. | GitHub Secrets |
| `VERCEL_TOKEN` | Jeton personnel Vercel utilisé par les actions GitHub pour déployer. | GitHub Secrets |
| `VERCEL_ORG_ID` / `VERCEL_PROJECT_ID` | Identifiants du projet Vercel. | GitHub Secrets |
| `MONITOR_API_URL` | URL publique de l’API pour les scripts de monitoring. | GitHub Secrets |
| `ALERT_EMAIL` | Adresse mail recevant les alertes de monitoring. | Variables d’environnement `.env` ou GitHub Secrets |
| `SLACK_WEBHOOK_URL` | URL du webhook Slack pour notifications. | Variables d’environnement ou secrets externes |

Pour définir un secret dans GitHub :

```bash
gh secret set NOM_DU_SECRET -b "valeur"
```

Pour définir un secret sur Fly.io :

```bash
flyctl secrets set NOM_DU_SECRET="valeur" -a <app-name>
```

Pour Vercel :

```bash
vercel env add NOM_DU_SECRET
```
