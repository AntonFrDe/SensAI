import { useEffect, useState } from 'react';
import type { GameResponse } from './api';
import { useHandTracking, type FinishedHand } from './handTracking';

export type GameRecord = {
  gameId: string;
  startedAt: string;
  blinds: string;
  startStack: number;
  hands: number;
  won: number;
  net: number;
  result: 'playing' | 'won' | 'lost';
};

const storageKey = 'sensai-games';
const maxRecords = 30;

export function loadRecords(storage: Storage = localStorage): GameRecord[] {
  try {
    const saved = JSON.parse(storage.getItem(storageKey) ?? '[]');
    return Array.isArray(saved) ? saved.filter(record => typeof record?.gameId === 'string') : [];
  } catch {
    return [];
  }
}

export function saveRecords(records: GameRecord[], storage: Storage = localStorage): boolean {
  try {
    storage.setItem(storageKey, JSON.stringify(records));
    return true;
  } catch {
    return false;
  }
}

export function recordHandEnd(records: GameRecord[], { gameId, state, stackAtStart }: FinishedHand, now: Date): GameRecord[] {
  const previous = records.find(record => record.gameId === gameId);
  const won = state.awards.some(award => award.winners.length === 1 && award.winners[0] === 'Vous');
  const stack = state.seats.player.stack;
  const base: GameRecord = previous ?? {
    gameId, startedAt: now.toISOString(), blinds: `${state.blinds.small}/${state.blinds.big}`,
    startStack: stackAtStart, hands: 0, won: 0, net: 0, result: 'playing',
  };
  const result: GameRecord['result'] = !state.gameOver ? 'playing' : state.seats.opponent.stack === 0 ? 'won' : 'lost';
  const updated = { ...base, hands: base.hands + 1, won: base.won + (won ? 1 : 0), net: stack - base.startStack, result };
  return [updated, ...records.filter(record => record.gameId !== gameId)].slice(0, maxRecords);
}

export function useGameRecords(game: GameResponse | null) {
  const [records, setRecords] = useState<GameRecord[]>(() => loadRecords());
  useHandTracking(game, { onHandEnd: hand => setRecords(previous => recordHandEnd(previous, hand, new Date())) });
  useEffect(() => {
    saveRecords(records);
  }, [records]);
  return [records, () => setRecords([])] as const;
}
