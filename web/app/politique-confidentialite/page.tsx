export const metadata = { title: 'Politique de confidentialité' };

export default function PrivacyPage() {
  return (
    <div>
      <h2 className="text-2xl font-bold mb-2">Politique de confidentialité</h2>
      <p>
        Nous collectons uniquement des données d’usage anonymisées à des fins de
        mesure d’audience. Aucune donnée personnelle n’est stockée en base.
      </p>
      <p className="mt-2">
        Nous utilisons des cookies techniques pour assurer le fonctionnement du
        site. Vous pouvez configurer votre navigateur pour bloquer ces cookies,
        mais certaines fonctionnalités pourraient ne plus fonctionner.
      </p>
    </div>
  );
}