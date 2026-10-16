import PlayingCard, { type CardData } from './PlayingCard';
import CommunityCards from './CommunityCards';
import ChipAmount from './ChipAmount';
import ActionControls, { type ActionControlsProps } from './ActionControls';
import HandInfo, { type GamePhase } from './HandInfo';
import HandHistory, { type HistoryEntry } from './HandHistory';
import Seat, { type SeatData } from './Seat';
import HandBadge, { sameCard, type BestHand } from './HandBadge';

export type Seats = { player: SeatData; opponent: SeatData };
export type Blinds = { small: number; big: number };
export type Hands = { player: BestHand | null; opponent: BestHand | null };
export type PotAward = { amount: number; winners: string[] };

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
  seats?: Seats;
  blinds?: Blinds;
  hands?: Hands;
  awards?: PotAward[];
};

function highlightedCards(phase: GamePhase | undefined, hands: Hands | undefined, awards: PotAward[]): CardData[] {
  const opponentWon = awards.some(award => award.winners.includes('IA') && !award.winners.includes('Vous'));
  if (phase === 'showdown' && opponentWon && hands?.opponent) return hands.opponent.cards;
  return hands?.player?.cards ?? [];
}

function seatOrStack(seat: SeatData | undefined, name: string, stack: number | undefined): SeatData | undefined {
  if (seat || stack === undefined) return seat;
  return { name, stack, bet: 0, folded: false, allIn: false, dealer: false, blind: null };
}

export default function PokerTable({
  playerCards = [], opponentCards = [], opponentNote, communityCards = [], pot, playerStack, opponentStack, controls,
  currentPlayer, phase, currentBet, history = [], seats, blinds, hands, awards = [],
}: Props) {
  const playing = phase !== undefined && phase !== 'showdown';
  const best = highlightedCards(phase, hands, awards);
  const isBest = (card?: CardData) => card !== undefined && best.some(other => sameCard(other, card));
  return (
    <section className="poker-table" aria-label="Table de Texas Hold’em à deux joueurs">
      <HandInfo phase={phase} currentBet={currentBet} />
      <Seat seat={seatOrStack(seats?.opponent, 'IA', opponentStack)} label="Adversaire IA" avatar="IA" position="top"
        active={playing && currentPlayer === 'opponent'}>
        {opponentCards.length > 0 && <div className="cards" role="group" aria-label="Cartes de l’IA">
          {opponentCards.map(card => <PlayingCard key={card.rank + card.suit} card={card} highlighted={isBest(card)} />)}
        </div>}
        <HandBadge hand={hands?.opponent} owner="Main de l’IA" />
      </Seat>
      <p className="ai-note" aria-live="polite">{opponentNote}</p>
      <div className="table-center">
        <CommunityCards cards={communityCards} highlighted={best} />
        <p className="chip-info pot" aria-live="polite">Pot : <ChipAmount amount={pot} /></p>
        {blinds && <p className="blinds">Blindes : {blinds.small} / {blinds.big}</p>}
      </div>
      <Seat seat={seatOrStack(seats?.player, 'Vous', playerStack)} label="Vous" avatar="V" position="bottom"
        active={playing && currentPlayer === 'player'}>
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
