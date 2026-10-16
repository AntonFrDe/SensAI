import { useState } from 'react';
import { handLabels } from './HandBadge';
import HandReplay from './HandReplay';
import type { PlayedHand } from './handLog';
import type { CardData } from './PlayingCard';

export type HandLogProps = { hands: PlayedHand[] };

const symbols = { clubs: '♣', diamonds: '♦', hearts: '♥', spades: '♠' };
const formatter = new Intl.NumberFormat('fr-FR');

function cardsText(cards: CardData[]): string {
  return cards.map(card => `${card.rank}${symbols[card.suit]}`).join(' ');
}

function netText(net: number): string {
  return `${net > 0 ? '+' : ''}${formatter.format(net)}`;
}

export default function HandLog({ hands }: HandLogProps) {
  const [open, setOpen] = useState<number | null>(null);
  const selected = hands.find(hand => hand.number === open);
  return (
    <section className="hand-log" aria-label="Mains précédentes">
      <h3>Mains précédentes</h3>
      {hands.length === 0 ? <p>Les mains terminées apparaîtront ici.</p> : <ol className="hand-log-list">
        {hands.map(hand => (
          <li key={hand.number} className={open === hand.number ? 'selected' : undefined}>
            <span className="hand-number">n°{hand.number}</span>
            <span className="hand-cards">{cardsText(hand.playerCards)}</span>
            <span className="hand-made">{hand.playerHand ? handLabels[hand.playerHand.rank] : hand.history.some(entry => entry.action === 'fold') ? 'Couché' : '—'}</span>
            <span className={`hand-net ${hand.net > 0 ? 'up' : hand.net < 0 ? 'down' : ''}`}>{netText(hand.net)}</span>
            <button type="button" className="link-button" aria-label={`Revoir la main n°${hand.number}`}
              onClick={() => setOpen(hand.number)}>Revoir</button>
          </li>
        ))}
      </ol>}
      {selected && <HandReplay key={selected.number} hand={selected} onClose={() => setOpen(null)} />}
    </section>
  );
}
