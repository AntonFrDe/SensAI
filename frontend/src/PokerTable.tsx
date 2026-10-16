import PlayingCard, { type CardData } from './PlayingCard';
import CommunityCards from './CommunityCards';
import ChipAmount from './ChipAmount';
import ActionControls, { type ActionControlsProps } from './ActionControls';
import HandInfo, { type GamePhase } from './HandInfo';
import HandHistory, { shortAction, type HistoryEntry } from './HandHistory';
import OpponentNote from './OpponentNote';
import Seat, { type SeatData } from './Seat';
import Term from './Term';
import HandBadge, { sameCard, type BestHand } from './HandBadge';

export type Seats = { player: SeatData; opponent: SeatData };
export type Blinds = { small: number; big: number };
export type Hands = { player: BestHand | null; opponent: BestHand | null };
export type PotAward = { amount: number; winners: string[] };

type Props = {
  playerCards?: CardData[];
  opponentCards?: CardData[];
  opponentNote?: string;
  opponentThinking?: boolean;
  communityCards?: CardData[];
  pot?: number;
  playerStack?: number;
  opponentStack?: number;
  controls?: ActionControlsProps;
  currentPlayer?: 'player' | 'opponent';
  phase?: GamePhase;
  currentBet?: number;
  history?: HistoryEntry[];
  seats?: Seats;
  blinds?: Blinds;
  hands?: Hands;
  awards?: PotAward[];
  revealedForTraining?: boolean;
};

function highlightedCards(phase: GamePhase | undefined, hands: Hands | undefined, awards: PotAward[]): CardData[] {
  const opponentWon = awards.some(award => award.winners.includes('IA') && !award.winners.includes('Vous'));
  if (phase === 'showdown' && opponentWon && hands?.opponent) return hands.opponent.cards;
  return hands?.player?.cards ?? [];
}

function lastActionOf(history: HistoryEntry[], player: string, phase: GamePhase | undefined): string | undefined {
  const entry = [...history].reverse().find(item => item.player === player && item.street === phase);
  return entry && shortAction(entry);
}

function seatOrStack(seat: SeatData | undefined, name: string, stack: number | undefined): SeatData | undefined {
  if (seat || stack === undefined) return seat;
  return { name, stack, bet: 0, folded: false, allIn: false, dealer: false, blind: null };
}

export default function PokerTable({
  playerCards = [], opponentCards = [], opponentNote, opponentThinking = false, communityCards = [], pot, playerStack, opponentStack, controls,
  currentPlayer, phase, currentBet, history = [], seats, blinds, hands, awards = [], revealedForTraining = false,
}: Props) {
  const playing = phase !== undefined && phase !== 'showdown';
  const best = highlightedCards(phase, hands, awards);
  const isBest = (card?: CardData) => card !== undefined && best.some(other => sameCard(other, card));
  return (
    <section className="poker-table" aria-label="Table de Texas Hold’em à deux joueurs">
      <HandInfo phase={phase} currentBet={currentBet} />
      <Seat seat={seatOrStack(seats?.opponent, 'IA', opponentStack)} label="Adversaire IA" avatar="IA" position="top"
        active={playing && currentPlayer === 'opponent'} lastAction={lastActionOf(history, 'IA', phase)}>
        {opponentCards.length > 0 && <div className="cards" role="group" aria-label="Cartes de l’IA">
          {opponentCards.map(card => <PlayingCard key={card.rank + card.suit} card={card} highlighted={isBest(card)} />)}
        </div>}
        {revealedForTraining && opponentCards.length > 0 && <p className="training-note">Dévoilées pour l’entraînement</p>}
        <HandBadge hand={hands?.opponent} owner="Main de l’IA" />
      </Seat>
      <OpponentNote thinking={opponentThinking} note={opponentNote} />
      <div className="table-center">
        <CommunityCards cards={communityCards} highlighted={best} />
        <p className="chip-info pot" aria-live="polite"><Term term="pot">Pot</Term> : <ChipAmount amount={pot} /></p>
        {blinds && <p className="blinds">Blindes : {blinds.small} / {blinds.big}</p>}
      </div>
      <Seat seat={seatOrStack(seats?.player, 'Vous', playerStack)} label="Vous" avatar="V" position="bottom"
        active={playing && currentPlayer === 'player'} lastAction={lastActionOf(history, 'Vous', phase)}>
        <div className="cards" role="group" aria-label="Vos cartes privées">
          <PlayingCard card={playerCards[0]} highlighted={isBest(playerCards[0])} />
          <PlayingCard card={playerCards[1]} highlighted={isBest(playerCards[1])} />
        </div>
        <HandBadge hand={hands?.player} owner="Votre main" />
      </Seat>
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
