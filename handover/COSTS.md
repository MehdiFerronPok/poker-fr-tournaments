# Estimation des coûts

Cette section donne une estimation approximative des coûts mensuels liés
à l’exploitation de l’application Poker France Tournaments. Les services
choisis proposent des niveaux gratuits mais certaines limites peuvent
être atteintes selon le trafic et le volume de données.

## Base de données (Neon)

Neon propose un **plan gratuit** incluant :

- 1 instance Postgres avec 10 Go de stockage.
- 1 Go de transfert sortant par jour.
- 1 branche et jusqu’à 4 compute hours par jour.

Si vous dépassez ces quotas (par ex. augmentation du stockage ou du
nombre d’heures de compute), le plan payant démarre à environ **0,01 € par
heure** de compute et **0,20 € par Go** de stockage supplémentaire. Pour la
plupart des déploiements de démonstration, le plan gratuit suffit.

## Hébergement API (Fly.io)

Fly.io propose un **Free Allowance** de 3 machines : 1 vCPU, 256 Mo RAM
chacune, avec 160 heures de compute par mois. Le conteneur API peut
fonctionner sur ce niveau gratuit. Le coût augmente si vous passez à des
machines plus grandes (0,007 € à 0,09 € par heure en fonction du gabarit).

Le trafic sortant est facturé après 1 Go/mois (0,09 € par Go). Les
notifications email et Slack sont gratuites via GitHub Actions et
webhooks.

## Alternative Render

Render offre un plan gratuit avec 750 heures de service web par mois,
512 Mo de RAM et 0,5 vCPU. Ce plan convient aux premiers tests. Au-delà,
les plans payants commencent à **7 € par mois** pour un service toujours
actif.

## Frontend (Vercel)

Vercel dispose d’un **plan gratuit** (Hobby) permettant jusqu’à 100 Go de
bande passante et 1 Mo de stockage par jour. Ce plan supporte très bien
un site statique et SSR de taille modérée. Le plan *Pro* commence à
environ **20 € par mois** et augmente les quotas.

## Monitoring & GitHub Actions

Les actions GitHub sur un dépôt public sont gratuites. Les minutes
d’exécution sur GitHub Actions restent sans coût tant que le dépôt est
public. Les webhooks Slack ou email n’entraînent pas de frais
supplémentaires de GitHub, mais notez que certains fournisseurs de Slack
peuvent facturer l’utilisation d’un certain nombre de notifications.

## Autres coûts

* **Nom de domaine** : un domaine personnalisé coûte environ 8–15 € par
  an selon le registrar. Vous pouvez commencer sans domaine et utiliser
  les URL fournies par Fly.io et Vercel.
* **Géocodage** : l’API Nominatim est gratuite pour un usage modéré, mais
  requiert de respecter la politique d’utilisation【512638780003458†L27-L51】. Pour des volumes
  importants, envisagez un service payant comme Mapbox ou Algolia.

## Résumé

Pour un site de démonstration avec quelques centaines de visites et
d’ingestions quotidiennes, l’ensemble **Neon + Fly.io + Vercel** reste sur
des plans gratuits. Les coûts ne deviendront significatifs qu’en cas
d’augmentation notable de trafic ou de stockage. Surveillez régulièrement
les quotas dans chaque service et ajustez le dimensionnement.