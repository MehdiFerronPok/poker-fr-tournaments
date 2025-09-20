import './globals.css';
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import Link from 'next/link';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Tournois de poker France',
  description: 'Tous les tournois de poker officiels en France'
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="fr">
      <body className={inter.className}>
        <header className="bg-white shadow">
          <div className="mx-auto max-w-7xl px-4 py-4 sm:px-6 lg:px-8 flex items-center justify-between">
            <h1 className="text-xl font-semibold"><Link href="/">Poker France Tournaments</Link></h1>
            <nav className="space-x-4">
              <Link href="/map" className="text-blue-600 hover:underline">Carte</Link>
              <Link href="/a-propos" className="text-blue-600 hover:underline">À propos</Link>
            </nav>
          </div>
        </header>
        <main className="mx-auto max-w-7xl p-4">{children}</main>
        <footer className="bg-white border-t mt-8">
          <div className="mx-auto max-w-7xl px-4 py-4 text-sm text-gray-600 flex justify-between">
            <span>&copy; {new Date().getFullYear()} Poker France Tournaments</span>
            <span>
              <Link href="/mentions-legales" className="hover:underline">Mentions légales</Link>
              {' | '}
              <Link href="/politique-confidentialite" className="hover:underline">Politique de confidentialité</Link>
            </span>
          </div>
        </footer>
      </body>
    </html>
  );
}