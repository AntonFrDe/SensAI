import PlayingCard, { type CardData } from './PlayingCard';
import CommunityCards from './CommunityCards';
import ChipAmount from './ChipAmount';
import ActionControls, { type ActionControlsProps } from './ActionControls';
import HandInfo, { type GamePhase } from './HandInfo';
import HandHistory, { type HistoryEntry } from './HandHistory';
import HandResult, { type PotAward } from './HandResult';

type Props = {
  playerCards?: CardData[];
  communityCards?: CardData[];
  pot?: number;
  playerStack?: number;
  opponentStack?: number;
  controls?: ActionControlsProps;
  currentPlayer?: 'player' | 'opponent';
  phase?: GamePhase;
  currentBet?: number;
  history?: HistoryEntry[];
  awards?: PotAward[];
};

export default function PokerTable({
  playerCards = [], communityCards = [], pot, playerStack, opponentStack, controls, currentPlayer,
  phase, currentBet, history = [], awards = [],
}: Props) {
  return (
    <section className="poker-table" aria-label="Table de Texas Hold’em à deux joueurs">
      <HandInfo phase={phase} currentBet={currentBet} />
      <div className="seat"><span aria-hidden="true">🤖</span><strong>Adversaire IA</strong></div>
      <p className="chip-info">Stack IA : <ChipAmount amount={opponentStack} /></p>
      <CommunityCards cards={communityCards} />
      <p className="chip-info pot" aria-live="polite">Pot : <ChipAmount amount={pot} /></p>
      <div className="seat"><span aria-hidden="true">👤</span><strong>Vous</strong></div>
      <p className="chip-info">Votre stack : <ChipAmount amount={playerStack} /></p>
      <div className="cards" role="group" aria-label="Vos cartes privées">
        <PlayingCard card={playerCards[0]} /><PlayingCard card={playerCards[1]} />
      </div>
      {phase !== 'showdown' && <p className="chip-info" aria-live="polite">Tour : {currentPlayer === 'player' ? 'à vous de jouer' : currentPlayer === 'opponent' ? 'adversaire IA' : '—'}</p>}
      {phase === 'showdown' && <HandResult awards={awards} />}
      <ActionControls
        {...controls}
        allowedActions={currentPlayer === 'player' ? controls?.allowedActions : []}
      />
      <HandHistory entries={history} />
    </section>
  );
}
