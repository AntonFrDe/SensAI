import { useEffect, useRef } from 'react';
import type { GameResponse, GameState } from './api';

export type FinishedHand = { gameId: string; number: number; state: GameState; stackAtStart: number };
export type HandEvents = { onNewGame?: (gameId: string) => void; onHandEnd: (hand: FinishedHand) => void };

type Tracked = { gameId: string; number: number; stackAtStart: number; ended: boolean };

export function useHandTracking(game: GameResponse | null, events: HandEvents) {
  const tracked = useRef<Tracked | null>(null);
  const handlers = useRef(events);
  useEffect(() => {
    handlers.current = events;
  });

  useEffect(() => {
    if (!game) return;
    const { gameId, state } = game;
    const seat = state.seats.player;
    const previous = tracked.current;
    if (previous?.gameId !== gameId) {
      tracked.current = { gameId, number: 1, stackAtStart: seat.stack + seat.bet, ended: false };
      handlers.current.onNewGame?.(gameId);
    } else if (previous.ended && state.phase !== 'showdown') {
      tracked.current = { gameId, number: previous.number + 1, stackAtStart: seat.stack + seat.bet, ended: false };
    }
    const current = tracked.current;
    if (current && state.phase === 'showdown' && !current.ended) {
      current.ended = true;
      handlers.current.onHandEnd({ gameId, number: current.number, state, stackAtStart: current.stackAtStart });
    }
  }, [game]);
}
