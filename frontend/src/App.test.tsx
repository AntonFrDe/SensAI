import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it, vi } from 'vitest';
import App from './App';
import type { GameState } from './api';

function state(overrides: Partial<GameState>): GameState {
  return {
    playerCards: [{ rank: 'A', suit: 'spades' }, { rank: '7', suit: 'hearts' }], opponentCards: [], communityCards: [],
    pot: 30, playerStack: 990, opponentStack: 980, currentPlayer: 'player', phase: 'pre_flop', currentBet: 20,
    controls: { allowedActions: ['fold', 'call', 'raise'], minAmount: 40, maxAmount: 1000 },
    awards: [], history: [], gameOver: false, blinds: { small: 10, big: 20 }, hands: { player: null, opponent: null },
    seats: {
      player: { name: 'Vous', stack: 990, bet: 10, folded: false, allIn: false, dealer: false, blind: 'small' },
      opponent: { name: 'IA', stack: 980, bet: 20, folded: false, allIn: false, dealer: true, blind: 'big' },
    },
    ...overrides,
  };
}

function fakeServer(routes: Record<string, (body: Record<string, unknown>) => object>) {
  const calls: string[] = [];
  vi.spyOn(globalThis, 'fetch').mockImplementation(async (input, init) => {
    const path = String(input);
    calls.push(path);
    const reply = routes[path];
    if (!reply) return Response.json({ error: 'Not found.' }, { status: 404 });
    return Response.json(reply(JSON.parse(String(init?.body ?? '{}'))));
  });
  return calls;
}

describe('App', () => {
  it('lets the AI speak first, then plays the human action and deals the next hand', async () => {
    const calls = fakeServer({
      '/api/games': () => ({ gameId: 'g1', state: state({ currentPlayer: 'opponent', controls: { allowedActions: [] } }) }),
      '/api/opponent': () => ({
        gameId: 'g1', state: state({ history: [{ street: 'pre_flop', player: 'IA', action: 'raise', amount: 60 }] }),
        opponentAction: { action: 'raise', amount: 60, source: 'llm' },
      }),
      '/api/actions': body => ({
        gameId: 'g1',
        state: state({
          phase: 'showdown', currentPlayer: 'opponent', controls: { allowedActions: [] }, playerStack: 980, opponentStack: 1020,
          awards: [{ amount: 80, winners: ['IA'], reason: 'fold' }],
          history: [{ street: 'pre_flop', player: 'IA', action: 'raise', amount: 60 }, { street: 'pre_flop', player: 'Vous', action: String(body.action) as 'fold' }],
        }),
      }),
      '/api/next-hand': () => ({ gameId: 'g1', state: state({}) }),
    });
    render(<App />);

    await userEvent.click(screen.getByRole('button', { name: 'Jouer' }));
    expect(await screen.findByText('L’IA relance à 60.')).toBeInTheDocument();
    expect(calls).toEqual(['/api/games', '/api/opponent']);

    await userEvent.click(screen.getByRole('button', { name: 'Fold' }));
    expect(await screen.findByText('L’IA remporte 80 jetons (adversaire couché).')).toBeInTheDocument();

    await userEvent.click(screen.getByRole('button', { name: 'Main suivante' }));
    expect(calls.at(-1)).toBe('/api/next-hand');
    expect(await screen.findByText(/à vous de jouer/)).toBeInTheDocument();
  });

  it('shows a readable error when the server is down', async () => {
    vi.spyOn(globalThis, 'fetch').mockRejectedValue(new TypeError('Failed to fetch'));
    render(<App />);
    await userEvent.click(screen.getByRole('button', { name: 'Jouer' }));
    expect(await screen.findByRole('alert')).toHaveTextContent('Failed to fetch');
  });
});
