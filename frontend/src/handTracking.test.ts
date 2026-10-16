import { renderHook } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import type { GameResponse, GameState } from './api';
import { useHandTracking } from './handTracking';

function response(gameId: string, phase: GameState['phase'], stack: number, bet = 0): GameResponse {
  const seat = { name: 'Vous', stack, bet, folded: false, allIn: false, dealer: false, blind: null };
  return { gameId, state: { phase, seats: { player: seat, opponent: seat } } as unknown as GameState };
}

describe('useHandTracking', () => {
  it('reports each finished hand once, numbered, with the stack it started with', () => {
    const onHandEnd = vi.fn();
    const onNewGame = vi.fn();
    const { rerender } = renderHook(({ game }) => useHandTracking(game, { onHandEnd, onNewGame }), {
      initialProps: { game: response('g1', 'pre_flop', 990, 10) },
    });
    expect(onNewGame).toHaveBeenCalledWith('g1');

    rerender({ game: response('g1', 'flop', 960) });
    rerender({ game: response('g1', 'showdown', 1080) });
    rerender({ game: response('g1', 'showdown', 1080) });
    expect(onHandEnd).toHaveBeenCalledOnce();
    expect(onHandEnd.mock.calls[0][0]).toMatchObject({ gameId: 'g1', number: 1, stackAtStart: 1000 });

    rerender({ game: response('g1', 'pre_flop', 1060, 20) });
    rerender({ game: response('g1', 'showdown', 1040) });
    expect(onHandEnd.mock.calls[1][0]).toMatchObject({ number: 2, stackAtStart: 1080 });
  });

  it('starts counting again on a new game', () => {
    const onHandEnd = vi.fn();
    const onNewGame = vi.fn();
    const { rerender } = renderHook(({ game }) => useHandTracking(game, { onHandEnd, onNewGame }), {
      initialProps: { game: response('g1', 'showdown', 900) as GameResponse | null },
    });
    rerender({ game: response('g2', 'pre_flop', 980, 20) });
    rerender({ game: response('g2', 'showdown', 1040) });
    expect(onNewGame.mock.calls.map(call => call[0])).toEqual(['g1', 'g2']);
    expect(onHandEnd.mock.calls[1][0]).toMatchObject({ gameId: 'g2', number: 1, stackAtStart: 1000 });
  });

  it('waits for a game', () => {
    const onHandEnd = vi.fn();
    renderHook(() => useHandTracking(null, { onHandEnd }));
    expect(onHandEnd).not.toHaveBeenCalled();
  });
});
