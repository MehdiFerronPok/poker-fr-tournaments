export const metadata = { title: 'À propos' };

export default function AboutPage() {
  return (
    <div>
      <h2 className="text-2xl font-bold mb-2">À propos</h2>
      <p>
        Ce projet open‑source recense les tournois de poker officiels en
        France. Il a été conçu pour centraliser des informations dispersées et
        faciliter la recherche pour les passionnés. Les données sont
        collectées automatiquement à partir de sites publics et normalisées
        quotidiennement.
      </p>
      <p className="mt-2">
        Pour contribuer, signaler un bug ou proposer une amélioration,
        rendez‑vous sur le dépôt GitHub du projet.
      </p>
    </div>
  );
}