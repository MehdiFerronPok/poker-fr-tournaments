# Plan de rollback

Ce document décrit comment revenir à un état antérieur de l’application
Poker France Tournaments en cas de déploiement raté ou de problème
critique. Le rollback concerne la base de données, l’API et
l’interface web.

## Sauvegardes de la base de données

### Création de snapshots (Neon)

Neon permet de créer des *branches* ou des *points de restauration*
automatiques. Avant chaque déploiement majeur, créez une branche de
sauvegarde :

```bash
# Dans l’interface Neon
# 1. Ouvrez le projet, rubrique "Branches"
# 2. Cliquez sur "New Branch" et nommez‑la avec la date, par ex. backup-2025-09-19
```

Vous pouvez également créer un snapshot via `psql` :

```bash
pg_dump "$DATABASE_URL" > backup_$(date +%F).sql
```

Conservez ces fichiers dans un espace sécurisé.

### Restauration

Si un incident survient (corruption des données, ingestion erronée), vous
pouvez revenir à la branche sauvegardée ou restaurer le dump :

#### Option A : Basculer sur la branche de sauvegarde

1. Dans Neon, sélectionnez la branche de sauvegarde dans la liste.
2. Copiez l’URL de connexion de cette branche et mettez à jour
   `DATABASE_URL` dans vos secrets (GitHub, Fly.io, Render).
3. Redeployez l’API pour qu’elle pointe vers cette branche.

#### Option B : Restaurer un dump SQL

```bash
psql "$DATABASE_URL" < backup_2025-09-19.sql
```

## Rollback de l’API (Fly.io)

Fly.io conserve l’historique des releases. Pour revenir à une version
précédente :

1. Listez les releases :

   ```bash
   flyctl releases -a <app-name>
   ```

2. Sélectionnez l’ID de la release souhaitée (par ex. `v7`).

3. Exécutez :

   ```bash
   flyctl releases revert --app <app-name> v7
   ```

Fly redéploiera l’image correspondante. Vérifiez ensuite les endpoints.

## Rollback de l’API (Render)

Render propose un bouton "Rollback" dans l’interface. Sélectionnez le
build précédant celui qui a échoué et cliquez sur *Rollback*. Toutes
les variables d’environnement resteront inchangées.

## Rollback du front (Vercel)

Vercel conserve l’historique des déploiements. Pour revenir à un
déploiement antérieur :

1. Ouvrez le tableau de bord Vercel.
2. Sélectionnez votre projet et ouvrez l’onglet *Deployments*.
3. Cliquez sur la ligne du déploiement stable (identifié par
   l’empreinte Git ou la date) et choisissez *Promote to production*.

## Rollback du code source

Si l’erreur est liée au code, créez un nouveau commit sur la branche
`main` ou effectuez un revert via GitHub :

```bash
git revert <commit-sha>
git push origin main
```

Le workflow `deploy.yml` déploiera automatiquement la version revertie.

## Vérifications après rollback

* Testez à nouveau `curl https://<api-url>/health` : le statut doit être
  `{"status": "ok"}`.
* Naviguez sur l’interface web et assurez‑vous que les données
  réapparaissent correctement.
* Lancez les scripts de monitoring pour vérifier qu’il n’y a pas
  d’anomalies.