import { useState } from 'react';

export default function App() {
  const [view, setView] = useState<'home' | 'game'>('home');
  return (
    <main>
      <h1>SensAI Poker</h1>
      {view === 'home' ? <section aria-label="Accueil">
        <h2>Entraînez-vous au Texas Hold’em</h2>
        <p>Affrontez une IA et apprenez à comprendre vos décisions.</p>
        <button type="button" onClick={() => setView('game')}>Jouer</button>
      </section> : <section aria-label="Partie">
        <h2>Table de poker</h2>
        <button type="button" onClick={() => setView('home')}>Retour à l’accueil</button>
      </section>}
    </main>
  );
}
