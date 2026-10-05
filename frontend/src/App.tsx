import { useState, type ComponentProps } from 'react';
import PokerTable from './PokerTable';
import './styles.css';

export default function App() {
  const [view, setView] = useState<'home' | 'game'>('home');
  const [game, setGame] = useState<{ gameId: string; state: ComponentProps<typeof PokerTable> } | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  async function startGame() {
    setLoading(true);
    setError('');
    try {
      const response = await fetch('/api/games', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '{}' });
      const result = await response.json();
      if (!response.ok) throw new Error(result.error || 'Impossible de démarrer la partie.');
      setGame(result);
      setView('game');
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : 'Connexion au serveur impossible.');
    } finally {
      setLoading(false);
    }
  }
  return (
    <main>
      <h1>SensAI Poker</h1>
      {error && <p role="alert">{error}</p>}
      {view === 'home' ? <section aria-label="Accueil">
        <h2>Entraînez-vous au Texas Hold’em</h2>
        <p>Affrontez une IA et apprenez à comprendre vos décisions.</p>
        <button type="button" disabled={loading} onClick={startGame}>{loading ? 'Distribution…' : 'Jouer'}</button>
      </section> : <section aria-label="Partie">
        <h2>Table de poker</h2>
        <PokerTable {...game?.state} />
        <button type="button" onClick={() => setView('home')}>Retour à l’accueil</button>
      </section>}
    </main>
  );
}
