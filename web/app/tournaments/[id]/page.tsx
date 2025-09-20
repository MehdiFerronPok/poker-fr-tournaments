'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import axios from 'axios';

interface Venue {
  id: number;
  name: string;
  address?: string;
  city?: string;
  region?: string;
  latitude?: number;
  longitude?: number;
}

interface Tournament {
  id: number;
  title: string;
  description?: string;
  start_datetime_local: string;
  end_datetime_local?: string;
  buy_in_cents?: number;
  variant?: string;
  status?: string;
  source_url?: string;
  venue: Venue;
}

export default function TournamentPage({ params }: { params: { id: string } }) {
  const [tournament, setTournament] = useState<Tournament | null>(null);
  const [jsonld, setJsonld] = useState<any>(null);
  const router = useRouter();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await axios.get(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/tournaments/${params.id}`);
        setTournament(res.data.tournament);
        setJsonld(res.data.json_ld);
      } catch (err) {
        console.error(err);
      }
    };
    fetchData();
  }, [params.id]);

  if (!tournament) {
    return <p>Chargement…</p>;
  }
  return (
    <div>
      <h2 className="text-2xl font-bold mb-2">{tournament.title}</h2>
      <p className="text-gray-600 mb-2">
        {new Date(tournament.start_datetime_local).toLocaleString('fr-FR', { dateStyle: 'long', timeStyle: 'short' })}
        {tournament.venue?.name ? ` – ${tournament.venue.name}` : ''}
      </p>
      {tournament.description && <p className="mb-2">{tournament.description}</p>}
      <ul className="mb-4 text-sm">
        {tournament.buy_in_cents && (
          <li><strong>Buy-in :</strong> {tournament.buy_in_cents / 100} €</li>
        )}
        {tournament.variant && (
          <li><strong>Variante :</strong> {tournament.variant}</li>
        )}
        {tournament.status && (
          <li><strong>Statut :</strong> {tournament.status}</li>
        )}
        {tournament.source_url && (
          <li><strong>Source :</strong> <a href={tournament.source_url} className="text-blue-600 hover:underline" target="_blank">Lien</a></li>
        )}
      </ul>
      <pre className="bg-gray-100 p-2 rounded text-xs overflow-auto">
        {JSON.stringify(jsonld, null, 2)}
      </pre>
      {jsonld && (
        <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonld) }} />
      )}
    </div>
  );
}