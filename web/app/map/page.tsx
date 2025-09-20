'use client';

import { useEffect, useRef, useState } from 'react';
import axios from 'axios';
import maplibregl from 'maplibre-gl';

interface Venue {
  id: number;
  name: string;
  latitude?: number;
  longitude?: number;
}

interface Tournament {
  id: number;
  title: string;
  start_datetime_local: string;
  venue: Venue;
}

export default function MapPage() {
  const mapContainer = useRef<HTMLDivElement | null>(null);
  const [map, setMap] = useState<maplibregl.Map | null>(null);
  const [tournaments, setTournaments] = useState<Tournament[]>([]);

  useEffect(() => {
    // Fetch tournaments with coordinates
    const fetchData = async () => {
      const res = await axios.get<Tournament[]>(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/tournaments`);
      setTournaments(res.data);
    };
    fetchData();
  }, []);

  useEffect(() => {
    if (mapContainer.current && !map) {
      const m = new maplibregl.Map({
        container: mapContainer.current,
        style: 'https://demotiles.maplibre.org/style.json',
        center: [2.35, 48.85],
        zoom: 5
      });
      setMap(m);
    }
  }, [mapContainer, map]);

  useEffect(() => {
    if (map && tournaments.length > 0) {
      tournaments.forEach((t) => {
        const { latitude, longitude } = t.venue;
        if (latitude && longitude) {
          new maplibregl.Marker()
            .setLngLat([longitude, latitude])
            .setPopup(new maplibregl.Popup().setHTML(`<strong>${t.title}</strong><br/>${new Date(t.start_datetime_local).toLocaleDateString('fr-FR')}`))
            .addTo(map);
        }
      });
    }
  }, [map, tournaments]);

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Carte des tournois</h2>
      <div ref={mapContainer} className="w-full h-[500px] border rounded"></div>
    </div>
  );
}