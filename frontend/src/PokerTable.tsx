import PlayingCard, { type CardData } from './PlayingCard';
import CommunityCards from './CommunityCards';

type Props = { playerCards?: CardData[]; communityCards?: CardData[] };

export default function PokerTable({ playerCards = [], communityCards = [] }: Props) {
  return (
    <section className="poker-table" aria-label="Table de Texas Hold’em à deux joueurs">
      <div className="seat"><span aria-hidden="true">🤖</span><strong>Adversaire IA</strong></div>
      <CommunityCards cards={communityCards} />
      <div className="seat"><span aria-hidden="true">👤</span><strong>Vous</strong></div>
      <div className="cards" role="group" aria-label="Vos cartes privées">
        <PlayingCard card={playerCards[0]} /><PlayingCard card={playerCards[1]} />
      </div>
    </section>
  );
}
