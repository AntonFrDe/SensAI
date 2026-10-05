import PlayingCard, { type CardData } from './PlayingCard';
import CommunityCards from './CommunityCards';
import ChipAmount from './ChipAmount';

type Props = {
  playerCards?: CardData[];
  communityCards?: CardData[];
  pot?: number;
  playerStack?: number;
  opponentStack?: number;
};

export default function PokerTable({ playerCards = [], communityCards = [], pot, playerStack, opponentStack }: Props) {
  return (
    <section className="poker-table" aria-label="Table de Texas Hold’em à deux joueurs">
      <div className="seat"><span aria-hidden="true">🤖</span><strong>Adversaire IA</strong></div>
      <p className="chip-info">Stack IA : <ChipAmount amount={opponentStack} /></p>
      <CommunityCards cards={communityCards} />
      <p className="chip-info pot" aria-live="polite">Pot : <ChipAmount amount={pot} /></p>
      <div className="seat"><span aria-hidden="true">👤</span><strong>Vous</strong></div>
      <p className="chip-info">Votre stack : <ChipAmount amount={playerStack} /></p>
      <div className="cards" role="group" aria-label="Vos cartes privées">
        <PlayingCard card={playerCards[0]} /><PlayingCard card={playerCards[1]} />
      </div>
    </section>
  );
}
