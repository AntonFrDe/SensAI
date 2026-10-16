import { useEffect, useState } from 'react';
import { postGame, type GameResponse } from './api';

const storageKey = 'sensai-game-id';

export function rememberGame(gameId: string | null): void {
  if (gameId) localStorage.setItem(storageKey, gameId);
  else localStorage.removeItem(storageKey);
}

export function useSavedGame(): [GameResponse | null, () => void] {
  const [saved, setSaved] = useState<GameResponse | null>(null);

  useEffect(() => {
    const gameId = localStorage.getItem(storageKey);
    if (!gameId) return;
    let cancelled = false;
    postGame('/api/state', { gameId })
      .then(result => {
        if (cancelled) return;
        if (result.state.gameOver) rememberGame(null);
        else setSaved(result);
      })
      .catch(() => {
        if (!cancelled) rememberGame(null);
      });
    return () => { cancelled = true; };
  }, []);

  return [saved, () => setSaved(null)];
}
