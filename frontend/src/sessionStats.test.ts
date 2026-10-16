import { describe, expect, it } from 'vitest';
import type { GameState } from './api';
import { emptyStats, handOutcome, loadLifetime, recordHand, saveLifetime } from './sessionStats';

function ended(awards: GameState['awards'], stack: number): GameState {
  return {
    awards, seats: { player: { name: 'Vous', stack, bet: 0, folded: false, allIn: false, dealer: false, blind: null } },
  } as unknown as GameState;
}

describe('handOutcome', () => {
  it('reads a pot won at the showdown', () => {
    expect(handOutcome(ended([{ amount: 200, winners: ['Vous'], reason: 'showdown' }], 1100), 1000))
      .toEqual({ result: 'won', byFold: false, pot: 200, net: 100 });
  });

  it('reads a hand lost by folding', () => {
    expect(handOutcome(ended([{ amount: 40, winners: ['IA'], reason: 'fold' }], 980), 1000))
      .toEqual({ result: 'lost', byFold: true, pot: 40, net: -20 });
  });

  it('reads a split pot', () => {
    expect(handOutcome(ended([{ amount: 100, winners: ['Vous', 'IA'], reason: 'showdown' }], 1000), 1000).result).toBe('split');
  });
});

describe('recordHand', () => {
  it('counts results, showdowns, the biggest pot and the net', () => {
    let stats = recordHand(emptyStats, { result: 'won', byFold: false, pot: 200, net: 100 });
    stats = recordHand(stats, { result: 'won', byFold: true, pot: 60, net: 30 });
    stats = recordHand(stats, { result: 'lost', byFold: false, pot: 400, net: -200 });
    expect(stats).toEqual({
      hands: 3, won: 2, lost: 1, split: 0, showdowns: 2, showdownsWon: 1, biggestPotWon: 200, net: -70, streak: -1, bestStreak: 2,
    });
  });

  it('resets the streak on a split pot', () => {
    const stats = recordHand({ ...emptyStats, streak: 3, bestStreak: 3 }, { result: 'split', byFold: false, pot: 100, net: 0 });
    expect(stats.streak).toBe(0);
    expect(stats.bestStreak).toBe(3);
  });
});

describe('lifetime storage', () => {
  it('saves and reloads the totals', () => {
    const stats = { ...emptyStats, hands: 12, won: 7, net: 340 };
    expect(saveLifetime(stats, localStorage)).toBe(true);
    expect(loadLifetime(localStorage)).toEqual(stats);
  });

  it('starts from zero on missing or broken data', () => {
    localStorage.setItem('sensai-lifetime-stats', '{oops');
    expect(loadLifetime(localStorage)).toEqual(emptyStats);
    localStorage.clear();
    expect(loadLifetime(localStorage)).toEqual(emptyStats);
  });
});
