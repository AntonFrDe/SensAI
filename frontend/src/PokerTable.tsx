import PlayingCard, { type CardData } from './PlayingCard';

export default function PokerTable({ playerCards = [] }: { playerCards?: CardData[] }) {
  return (
    <section className="poker-table" aria-label="Table de Texas Hold’em à deux joueurs">
      <div className="seat"><span aria-hidden="true">🤖</span><strong>Adversaire IA</strong></div>
      <div className="board" aria-hidden="true" />
      <div className="seat"><span aria-hidden="true">👤</span><strong>Vous</strong></div>
      <div className="cards" role="group" aria-label="Vos cartes privées">
        <PlayingCard card={playerCards[0]} /><PlayingCard card={playerCards[1]} />
      </div>
    </section>
  );
}
