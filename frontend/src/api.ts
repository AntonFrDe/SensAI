import type { PokerAction } from './ActionControls';
import type { GamePhase } from './HandInfo';
import type { CardData } from './PlayingCard';

export type Award = { amount: number; winners: string[]; reason: 'fold' | 'showdown' };
export type GameState = {
  playerCards: CardData[];
  opponentCards: CardData[];
  communityCards: CardData[];
  pot: number;
  playerStack: number;
  opponentStack: number;
  currentPlayer: 'player' | 'opponent';
  phase: GamePhase;
  currentBet: number;
  controls: { allowedActions: PokerAction[]; minAmount?: number; maxAmount?: number };
  awards: Award[];
  gameOver: boolean;
};
export type OpponentAction = { action: PokerAction; amount?: number; source: 'llm' | 'fallback' };
export type GameResponse = { gameId: string; state: GameState; opponentAction?: OpponentAction };

export async function postGame(path: string, body: object): Promise<GameResponse> {
  const response = await fetch(path, {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body),
  });
  const result = await response.json();
  if (!response.ok) throw new Error(result.error || 'Impossible de terminer cette action.');
  return result;
}

/** Streams the coach's advice: calls onToken for each piece of text, throws on a server or model error. */
export async function streamCoach(gameId: string, onToken: (text: string) => void, signal: AbortSignal) {
  const response = await fetch('/api/coach', {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ gameId }), signal,
  });
  if (!response.ok || !response.body) {
    const result = await response.json().catch(() => ({}));
    throw new Error(result.error || 'Le coach est indisponible.');
  }
  const reader = response.body.pipeThrough(new TextDecoderStream()).getReader();
  let buffer = '';
  for (;;) {
    const { done, value } = await reader.read();
    if (done) return;
    buffer += value;
    const lines = buffer.split('\n');
    buffer = lines.pop() ?? '';
    for (const line of lines.filter(Boolean)) {
      const event = JSON.parse(line);
      if (event.error) throw new Error(event.error);
      if (event.token) onToken(event.token);
    }
  }
}
