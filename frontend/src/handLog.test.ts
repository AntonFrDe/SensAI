import { describe, expect, it } from 'vitest';
import type { GameState } from './api';
import { replaySteps, stackHistory, toPlayedHand, type PlayedHand } from './handLog';
import type { CardData } from './PlayingCard';

const board: CardData[] = [
  { rank: 'A', suit: 'spades' }, { rank: '7', suit: 'hearts' }, { rank: '2', suit: 'clubs' },
  { rank: 'J', suit: 'diamonds' }, { rank: '4', suit: 'spades' },
];

function hand(overrides: Partial<PlayedHand>): PlayedHand {
  return {
    number: 1, playerCards: [], opponentCards: [], board, history: [], awards: [], playerHand: null, opponentHand: null, net: 0,
    stackAfter: 1000,
    ...overrides,
  };
}

describe('toPlayedHand', () => {
  it('keeps the cards, actions, result and chip change of the hand', () => {
    const state = {
      playerCards: [board[0]], opponentCards: [board[1]], communityCards: board, history: [], awards: [],
      hands: { player: { rank: 'one_pair', cards: [] }, opponent: null },
      seats: { player: { stack: 1120 } },
    } as unknown as GameState;
    expect(toPlayedHand({ gameId: 'g1', number: 4, state, stackAtStart: 1000 })).toMatchObject({
      number: 4, playerCards: [board[0]], opponentCards: [board[1]], board, playerHand: { rank: 'one_pair' }, net: 120, stackAfter: 1120,
    });
  });
});

describe('stackHistory', () => {
  it('starts from the stack before the first hand and follows each hand in order', () => {
    expect(stackHistory([
      hand({ number: 2, net: -50, stackAfter: 1070 }), hand({ number: 1, net: 120, stackAfter: 1120 }),
    ])).toEqual([{ hand: 0, stack: 1000 }, { hand: 1, stack: 1120 }, { hand: 2, stack: 1070 }]);
    expect(stackHistory([])).toEqual([]);
  });
});

describe('replaySteps', () => {
  it('reveals the board street by street between the actions', () => {
    const steps = replaySteps(hand({ history: [
      { street: 'pre_flop', player: 'IA', action: 'call', amount: 10 },
      { street: 'pre_flop', player: 'Vous', action: 'check' },
      { street: 'flop', player: 'IA', action: 'bet', amount: 40 },
      { street: 'flop', player: 'Vous', action: 'call', amount: 40 },
      { street: 'turn', player: 'IA', action: 'check' },
    ] }));
    expect(steps.map(step => [step.street, step.board.length, step.entry?.action ?? null, step.showdown])).toEqual([
      ['pre_flop', 0, null, false], ['pre_flop', 0, 'call', false], ['pre_flop', 0, 'check', false],
      ['flop', 3, null, false], ['flop', 3, 'bet', false], ['flop', 3, 'call', false],
      ['turn', 4, null, false], ['turn', 4, 'check', false],
      ['showdown', 5, null, true],
    ]);
  });

  it('ends on the full board after an all-in before the flop', () => {
    const steps = replaySteps(hand({ history: [
      { street: 'pre_flop', player: 'IA', action: 'raise', amount: 1000 },
      { street: 'pre_flop', player: 'Vous', action: 'call', amount: 980 },
    ] }));
    expect(steps).toHaveLength(4);
    expect(steps[3]).toEqual({ street: 'showdown', board, showdown: true });
  });

  it('stops before the flop when someone folds', () => {
    const steps = replaySteps(hand({ board: [], history: [{ street: 'pre_flop', player: 'Vous', action: 'fold' }] }));
    expect(steps.at(-1)).toEqual({ street: 'showdown', board: [], showdown: true });
  });
});
