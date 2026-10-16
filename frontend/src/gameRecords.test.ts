import { describe, expect, it } from 'vitest';
import type { GameState } from './api';
import { loadRecords, recordHandEnd, saveRecords, type GameRecord } from './gameRecords';

function finished(gameId: string, stack: number, opponentStack: number, winners: string[], gameOver = false) {
  const state = {
    awards: [{ amount: 100, winners, reason: 'showdown' }], blinds: { small: 10, big: 20 }, gameOver,
    seats: { player: { stack }, opponent: { stack: opponentStack } },
  } as unknown as GameState;
  return { gameId, number: 1, state, stackAtStart: 1000 };
}

describe('recordHandEnd', () => {
  const now = new Date('2026-10-16T10:00:00Z');

  it('creates the record of a new game and updates it hand after hand', () => {
    let records = recordHandEnd([], finished('g1', 1050, 950, ['Vous']), now);
    records = recordHandEnd(records, finished('g1', 1020, 980, ['IA']), now);
    expect(records).toEqual([{
      gameId: 'g1', startedAt: '2026-10-16T10:00:00.000Z', blinds: '10/20', startStack: 1000, hands: 2, won: 1, net: 20,
      result: 'playing',
    }]);
  });

  it('puts the latest game first and marks the winner when it ends', () => {
    const older: GameRecord = { gameId: 'g0', startedAt: '', blinds: '5/10', startStack: 500, hands: 9, won: 4, net: -500, result: 'lost' };
    const records = recordHandEnd([older], finished('g2', 2000, 0, ['Vous'], true), now);
    expect(records.map(record => [record.gameId, record.result])).toEqual([['g2', 'won'], ['g0', 'lost']]);
  });

  it('does not count a split pot as a win', () => {
    expect(recordHandEnd([], finished('g3', 1000, 1000, ['Vous', 'IA']), now)[0].won).toBe(0);
  });
});

describe('records storage', () => {
  it('saves, reloads and ignores broken data', () => {
    const record: GameRecord = { gameId: 'g1', startedAt: 'x', blinds: '10/20', startStack: 1000, hands: 1, won: 1, net: 30, result: 'playing' };
    saveRecords([record]);
    expect(loadRecords()).toEqual([record]);
    localStorage.setItem('sensai-games', '{"not": "a list"}');
    expect(loadRecords()).toEqual([]);
    localStorage.setItem('sensai-games', '[oops');
    expect(loadRecords()).toEqual([]);
  });
});
