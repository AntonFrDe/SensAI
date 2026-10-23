import { useEffect, useState } from 'react';
import { fetchHandRankings, type HandRanking } from './api';
import PlayingCard from './PlayingCard';

export default function HandRankings() {
  const [rankings, setRankings] = useState<HandRanking[]>([]);
  const [error, setError] = useState('');

  useEffect(() => {
    let cancelled = false;
    fetchHandRankings()
      .then(list => { if (!cancelled) setRankings(list); })
      .catch(cause => { if (!cancelled) setError(cause instanceof Error ? cause.message : 'Classement des mains indisponible.'); });
    return () => { cancelled = true; };
  }, []);

  return (
    <section className="rankings" aria-label="Classement des mains">
      <h2>Classement des mains</h2>
      <p>De la plus forte à la plus faible. Votre main est la meilleure combinaison de 5 cartes parmi vos 2 cartes et les 5 du board.</p>
      {error && <p role="alert">{error}</p>}
      <ol className="rankings-list">
        {rankings.map(ranking => (
          <li key={ranking.rank}>
            <span className="ranking-number" aria-hidden="true">{ranking.rank}</span>
            <div className="ranking-text">
              <h3>{ranking.name}</h3>
              <p>{ranking.description}</p>
            </div>
            <div className="cards" role="group" aria-label={`Exemple de ${ranking.name.toLowerCase()}`}>
              {ranking.cards.map(card => <PlayingCard key={card.rank + card.suit} card={card} />)}
            </div>
          </li>
        ))}
      </ol>
    </section>
  );
}
