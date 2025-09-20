'use client';

import { useEffect, useState } from 'react';
import axios from 'axios';

interface Venue {
  id: number;
  name: string;
  city?: string;
}

interface Tournament {
  id: number;
  title: string;
  start_datetime_local: string;
  buy_in_cents?: number;
  variant?: string;
  venue: Venue;
}

export default function HomePage() {
  const [city, setCity] = useState('');
  const [tournaments, setTournaments] = useState<Tournament[]>([]);
  const [loading, setLoading] = useState(false);

  const fetchTournaments = async () => {
    setLoading(true);
    try {
      const params: any = {};
      if (city) params.city = city;
      const res = await axios.get<Tournament[]>(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/tournaments`, { params });
      setTournaments(res.data);
    } catch (err) {
      console.error(err);
      setTournaments([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTournaments();
  }, []);

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Rechercher des tournois</h2>
      <div className="flex items-center space-x-2 mb-4">
        <input
          type="text"
          value={city}
          onChange={(e) => setCity(e.target.value)}
          placeholder="Ville (optionnel)"
          className="border rounded px-2 py-1"
        />
        <button onClick={fetchTournaments} className="bg-blue-600 text-white px-4 py-1 rounded">Rechercher</button>
      </div>
      {loading ? (
        <p>Chargement…</p>
      ) : tournaments.length === 0 ? (
        <p>Aucun tournoi trouvé.</p>
      ) : (
        <ul className="space-y-2">
          {tournaments.map((t) => (
            <li key={t.id} className="border p-2 rounded">
              <a href={`/tournaments/${t.id}`} className="text-lg font-semibold text-blue-600 hover:underline">
                {t.title}
              </a>
              <div className="text-sm text-gray-600">
                {new Date(t.start_datetime_local).toLocaleString('fr-FR', { dateStyle: 'short', timeStyle: 'short' })}
                {' – '} {t.venue?.name}
                {t.buy_in_cents ? ` – Buy-in : ${t.buy_in_cents / 100} €` : ''}
                {t.variant ? ` – ${t.variant}` : ''}
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}