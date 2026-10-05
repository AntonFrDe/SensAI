import { useState, type ComponentProps } from 'react';
import PokerTable from './PokerTable';
import './styles.css';

export default function App() {
  const [view, setView] = useState<'home' | 'game'>('home');
  const [game, setGame] = useState<{ gameId: string; state: ComponentProps<typeof PokerTable> } | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  async function updateGame(path: '/api/games' | '/api/actions', body: object) {
    if (loading) return;
    setLoading(true);
    setError('');
    try {
      const response = await fetch(path, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
      const result = await response.json();
      if (!response.ok) throw new Error(result.error || 'Impossible de terminer cette action.');
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
        <button type="button" disabled={loading} onClick={() => updateGame('/api/games', {})}>{loading ? 'Distribution…' : 'Jouer'}</button>
      </section> : <section aria-label="Partie">
        <h2>Table de poker</h2>
        {loading && <p role="status">Envoi de votre action…</p>}
        <PokerTable {...game?.state} controls={{
          ...game?.state.controls,
          onAction: loading || !game ? undefined : (action, amount) => {
            void updateGame('/api/actions', { gameId: game.gameId, action, amount });
          },
        }} />
        <button type="button" disabled={loading} onClick={() => setView('home')}>Retour à l’accueil</button>
      </section>}
    </main>
  );
}
