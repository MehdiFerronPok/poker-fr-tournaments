export const metadata = { title: 'Mentions légales' };

export default function MentionsPage() {
  return (
    <div>
      <h2 className="text-2xl font-bold mb-2">Mentions légales</h2>
      <p>
        Ce site est édité à titre de démonstration. Les informations affichées
        proviennent de sources publiques et officielles. Les données sont mises à
        jour quotidiennement mais ne constituent pas un engagement contractuel.
      </p>
      <p className="mt-2">
        Pour toute demande, veuillez contacter l’éditeur via l’adresse
        électronique indiquée sur la page « À propos ».
      </p>
    </div>
  );
}