import { useState } from 'react';
import type { Award, GameResponse } from './api';
import type { BestHand } from './HandBadge';
import type { HistoryEntry } from './HandHistory';
import type { GamePhase } from './HandInfo';
import type { CardData } from './PlayingCard';
import { useHandTracking, type FinishedHand } from './handTracking';

export type PlayedHand = {
  number: number;
  playerCards: CardData[];
  opponentCards: CardData[];
  board: CardData[];
  history: HistoryEntry[];
  awards: Award[];
  playerHand: BestHand | null;
  opponentHand: BestHand | null;
  net: number;
  stackAfter: number;
};
export type ReplayStep = { street: GamePhase; board: CardData[]; entry?: HistoryEntry; showdown: boolean };

const maxHands = 50;
const boardSize: Record<GamePhase, number> = { pre_flop: 0, flop: 3, turn: 4, river: 5, showdown: 5 };

export function toPlayedHand({ number, state, stackAtStart }: FinishedHand): PlayedHand {
  return {
    number,
    playerCards: state.playerCards,
    opponentCards: state.opponentCards,
    board: state.communityCards,
    history: state.history,
    awards: state.awards,
    playerHand: state.hands.player,
    opponentHand: state.hands.opponent,
    net: state.seats.player.stack - stackAtStart,
    stackAfter: state.seats.player.stack,
  };
}

export function replaySteps(hand: PlayedHand): ReplayStep[] {
  const steps: ReplayStep[] = [{ street: 'pre_flop', board: [], showdown: false }];
  let street: GamePhase = 'pre_flop';
  for (const entry of hand.history) {
    if (entry.street !== street) {
      street = entry.street;
      steps.push({ street, board: hand.board.slice(0, boardSize[street]), showdown: false });
    }
    steps.push({ street, board: hand.board.slice(0, boardSize[street]), entry, showdown: false });
  }
  steps.push({ street: 'showdown', board: hand.board, showdown: true });
  return steps;
}

export type StackPoint = { hand: number; stack: number };

export function stackHistory(hands: PlayedHand[]): StackPoint[] {
  const ordered = [...hands].sort((first, second) => first.number - second.number);
  if (ordered.length === 0) return [];
  const start = { hand: 0, stack: ordered[0].stackAfter - ordered[0].net };
  return [start, ...ordered.map(hand => ({ hand: hand.number, stack: hand.stackAfter }))];
}

export function useHandLog(game: GameResponse | null) {
  const [hands, setHands] = useState<PlayedHand[]>([]);
  useHandTracking(game, {
    onNewGame: () => setHands([]),
    onHandEnd: finished => setHands(previous => [toPlayedHand(finished), ...previous].slice(0, maxHands)),
  });
  return hands;
}
