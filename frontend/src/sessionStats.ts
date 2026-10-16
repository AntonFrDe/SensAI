import { useEffect, useState } from 'react';
import type { GameResponse, GameState } from './api';
import { useHandTracking } from './handTracking';

export type HandOutcome = { result: 'won' | 'lost' | 'split'; byFold: boolean; pot: number; net: number };
export type Stats = {
  hands: number;
  won: number;
  lost: number;
  split: number;
  showdowns: number;
  showdownsWon: number;
  biggestPotWon: number;
  net: number;
  streak: number;
  bestStreak: number;
};

export const emptyStats: Stats = {
  hands: 0, won: 0, lost: 0, split: 0, showdowns: 0, showdownsWon: 0, biggestPotWon: 0, net: 0, streak: 0, bestStreak: 0,
};
const storageKey = 'sensai-lifetime-stats';

export function handOutcome(state: GameState, stackAtStart: number): HandOutcome {
  const pot = state.awards.reduce((total, award) => total + award.amount, 0);
  const mine = state.awards.filter(award => award.winners.includes('Vous'));
  const shared = mine.some(award => award.winners.length > 1);
  const result = mine.length === 0 ? 'lost' : shared && mine.every(award => award.winners.length > 1) ? 'split' : 'won';
  return { result, byFold: state.awards.some(award => award.reason === 'fold'), pot, net: state.seats.player.stack - stackAtStart };
}

export function recordHand(stats: Stats, outcome: HandOutcome): Stats {
  const won = outcome.result === 'won';
  const streak = won ? Math.max(stats.streak, 0) + 1 : outcome.result === 'lost' ? Math.min(stats.streak, 0) - 1 : 0;
  return {
    hands: stats.hands + 1,
    won: stats.won + (won ? 1 : 0),
    lost: stats.lost + (outcome.result === 'lost' ? 1 : 0),
    split: stats.split + (outcome.result === 'split' ? 1 : 0),
    showdowns: stats.showdowns + (outcome.byFold ? 0 : 1),
    showdownsWon: stats.showdownsWon + (!outcome.byFold && won ? 1 : 0),
    biggestPotWon: won ? Math.max(stats.biggestPotWon, outcome.pot) : stats.biggestPotWon,
    net: stats.net + outcome.net,
    streak,
    bestStreak: Math.max(stats.bestStreak, streak),
  };
}

export function loadLifetime(storage: Storage = localStorage): Stats {
  try {
    const saved = JSON.parse(storage.getItem(storageKey) ?? 'null');
    return saved && typeof saved.hands === 'number' ? { ...emptyStats, ...saved } : emptyStats;
  } catch {
    return emptyStats;
  }
}

export function saveLifetime(stats: Stats, storage: Storage = localStorage): boolean {
  try {
    storage.setItem(storageKey, JSON.stringify(stats));
    return true;
  } catch {
    return false;
  }
}

export function useSessionStats(game: GameResponse | null) {
  const [session, setSession] = useState<Stats>(emptyStats);
  const [lifetime, setLifetime] = useState<Stats>(() => loadLifetime());

  useHandTracking(game, {
    onNewGame: () => setSession(emptyStats),
    onHandEnd: ({ state, stackAtStart }) => {
      const outcome = handOutcome(state, stackAtStart);
      setSession(previous => recordHand(previous, outcome));
      setLifetime(previous => recordHand(previous, outcome));
    },
  });

  useEffect(() => {
    saveLifetime(lifetime);
  }, [lifetime]);

  return { session, lifetime, resetLifetime: () => setLifetime(emptyStats) };
}
