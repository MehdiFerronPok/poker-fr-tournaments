# Gestion des accès et permissions

Ce document décrit comment accorder ou révoquer l’accès aux différentes
ressources utilisées par le projet Poker France Tournaments. Chaque
ressource doit être administrée uniquement via le compte du propriétaire
(`{{GITHUB_USERNAME}}`).

## GitHub

Le dépôt `poker-fr-tournaments` se trouve dans votre compte ou
organisation GitHub. Pour gérer les permissions :

### Ajouter un collaborateur

```bash
gh api \
  --method PUT \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "/repos/{{GITHUB_USERNAME}}/poker-fr-tournaments/collaborators/<username>" \
  -f permission=maintain
```

Les niveaux de permission disponibles sont `read`, `triage`, `write`,
`maintain` et `admin`. Choisissez le niveau adapté.

### Retirer un collaborateur

```bash
gh api --method DELETE \
  "/repos/{{GITHUB_USERNAME}}/poker-fr-tournaments/collaborators/<username>"
```

### Activer la protection de branche

Afin de sécuriser la branche `main`, appliquez une règle de protection :

```bash
gh api --method PUT \
  "/repos/{{GITHUB_USERNAME}}/poker-fr-tournaments/branches/main/protection" \
  -F required_status_checks.strict=true \
  -F required_status_checks.contexts='["test", "lint"]' \
  -F enforce_admins=true \
  -F required_pull_request_reviews.dismiss_stale_reviews=true \
  -F restrictions=null
```

## Neon (base de données)

L’accès à la base est géré via l’interface Neon. Pour donner un accès
lecture/écriture à un collaborateur :

1. Dans Neon, ouvrez votre projet.
2. Cliquez sur *Manage Roles* et créez un rôle (par ex. `app_user`).
3. Dans votre base, exécutez :

   ```sql
   CREATE USER <username> WITH PASSWORD '<generated_password>';
   GRANT CONNECT ON DATABASE <dbname> TO <username>;
   GRANT USAGE ON SCHEMA public TO <username>;
   GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO <username>;
   ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO <username>;
   ```

4. Fournissez à la personne l’URL de connexion qui inclut son utilisateur et
   mot de passe.

Pour révoquer l’accès :

```sql
REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA public FROM <username>;
DROP USER <username>;
```

## Fly.io

Pour gérer l’accès à l’app Fly.io :

* **Ajouter un membre à l’organisation** :
  Ouvrez le tableau de bord Fly.io, sélectionnez votre organisation et
  invitez un utilisateur par email. Assignez le rôle `Developer` ou
  `Maintainer` selon le besoin.
* **Révoquer l’accès** : dans le même écran, sélectionnez la personne et
  cliquez sur *Remove*.

Note : Les tokens API Fly.io ne doivent jamais être partagés. Chaque
utilisateur doit générer son propre token via `flyctl auth token`.

## Render

Si vous utilisez Render comme alternative, les permissions se gèrent via
l’interface Render. Invitez de nouveaux utilisateurs au niveau de l’équipe
avec un rôle `Admin` ou `Developer`. Pour retirer l’accès, supprimez
l’utilisateur de l’équipe.

## Vercel

Pour ajouter un membre :

1. Connectez‑vous à Vercel et ouvrez votre projet.
2. Allez dans *Settings > Team* et cliquez sur *Invite*.
3. Entrez l’adresse email de l’utilisateur et choisissez un rôle (`Read` ou
   `Write`).

Pour révoquer l’accès, cliquez sur les trois points à droite du membre et
sélectionnez *Remove*.

## Sécurité des secrets

Ne partagez jamais les valeurs des secrets (mots de passe, tokens API). Les
variables sensibles doivent être définies dans :

* **GitHub Secrets** pour le dépôt.
* **Fly.io secrets** via `flyctl secrets set`.
* **Render environment variables** via l’interface.
* **Vercel environment variables** via `vercel env add`.

Pour changer un secret, mettez‑le à jour dans tous les emplacements où
il est utilisé, redéployez l’API et le front, puis supprimez l’ancienne
valeur si nécessaire.