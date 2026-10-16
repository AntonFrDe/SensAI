import PlayingCard, { type CardData } from './PlayingCard';
import CommunityCards from './CommunityCards';
import ChipAmount from './ChipAmount';
import ActionControls, { type ActionControlsProps } from './ActionControls';
import HandInfo, { type GamePhase } from './HandInfo';
import HandHistory, { type HistoryEntry } from './HandHistory';

type Props = {
  playerCards?: CardData[];
  opponentCards?: CardData[];
  opponentNote?: string;
  communityCards?: CardData[];
  pot?: number;
  playerStack?: number;
  opponentStack?: number;
  controls?: ActionControlsProps;
  currentPlayer?: 'player' | 'opponent';
  phase?: GamePhase;
  currentBet?: number;
  history?: HistoryEntry[];
};

export default function PokerTable({
  playerCards = [], opponentCards = [], opponentNote, communityCards = [], pot, playerStack, opponentStack, controls,
  currentPlayer, phase, currentBet, history = [],
}: Props) {
  return (
    <section className="poker-table" aria-label="Table de Texas Hold’em à deux joueurs">
      <HandInfo phase={phase} currentBet={currentBet} />
      <div className="seat"><span aria-hidden="true">🤖</span><strong>Adversaire IA</strong></div>
      <p className="chip-info">Stack IA : <ChipAmount amount={opponentStack} /></p>
      {opponentCards.length > 0 && <div className="cards" role="group" aria-label="Cartes de l’IA">
        {opponentCards.map(card => <PlayingCard key={card.rank + card.suit} card={card} />)}
      </div>}
      <p className="ai-note" aria-live="polite">{opponentNote}</p>
      <CommunityCards cards={communityCards} />
      <p className="chip-info pot" aria-live="polite">Pot : <ChipAmount amount={pot} /></p>
      <div className="seat"><span aria-hidden="true">👤</span><strong>Vous</strong></div>
      <p className="chip-info">Votre stack : <ChipAmount amount={playerStack} /></p>
      <div className="cards" role="group" aria-label="Vos cartes privées">
        <PlayingCard card={playerCards[0]} /><PlayingCard card={playerCards[1]} />
      </div>
      <p className="chip-info" aria-live="polite">Tour : {phase === 'showdown' ? 'main terminée' : currentPlayer === 'player' ? 'à vous de jouer' : currentPlayer === 'opponent' ? 'adversaire IA' : '—'}</p>
      <ActionControls
        {...controls}
        pot={pot}
        currentBet={currentBet}
        allowedActions={currentPlayer === 'player' ? controls?.allowedActions : []}
      />
      <HandHistory entries={history} />
    </section>
  );
}
