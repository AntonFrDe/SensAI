import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { beforeEach, describe, expect, it, vi } from 'vitest';
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

const bodies: unknown[] = [];
const status = { ollama: true, models: { coach: { name: 'qwen', installed: true }, opponent: { name: 'qwen', installed: true } } };

function fakeServer(routes: Record<string, (body: Record<string, unknown>) => object>) {
  const calls: string[] = [];
  bodies.length = 0;
  vi.spyOn(globalThis, 'fetch').mockImplementation(async (input, init) => {
    const path = String(input);
    if (path === '/api/status') return Response.json(status);
    calls.push(path);
    bodies.push(JSON.parse(String(init?.body ?? '{}')));
    const reply = routes[path];
    if (!reply) return Response.json({ error: 'Not found.' }, { status: 404 });
    return Response.json(reply(JSON.parse(String(init?.body ?? '{}'))));
  });
  return calls;
}

describe('App', () => {
  beforeEach(() => localStorage.clear());

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
    expect(bodies[0]).toEqual({ options: { blinds: '10/20', stackBigBlinds: 50 } });

    await userEvent.click(screen.getByRole('button', { name: 'Fold' }));
    expect(await screen.findByText('L’IA remporte 80 jetons (adversaire couché).')).toBeInTheDocument();

    const stats = screen.getByRole('region', { name: 'Statistiques' });
    expect(stats).toHaveTextContent('Mains jouées1');
    expect(stats).toHaveTextContent('Bilan-10 jetons');

    await userEvent.click(screen.getByRole('button', { name: 'Main suivante' }));
    expect(calls.at(-1)).toBe('/api/next-hand');
    expect(await screen.findByText(/à vous de jouer/)).toBeInTheDocument();
  });

  it('shows a readable error when the server is down', async () => {
    vi.spyOn(globalThis, 'fetch').mockRejectedValue(new TypeError('Failed to fetch'));
    render(<App />);
    await userEvent.click(screen.getByRole('button', { name: 'Jouer' }));
    expect(await screen.findByText(/^Failed to fetch/, { selector: 'main > p' })).toHaveAttribute('role', 'alert');
  });

  it('names the winning hand at the showdown', async () => {
    fakeServer({
      '/api/games': () => ({ gameId: 'g2', state: state({
        phase: 'showdown', controls: { allowedActions: [] },
        awards: [{ amount: 200, winners: ['Vous'], reason: 'showdown' }],
        hands: { player: { rank: 'flush', cards: [] }, opponent: { rank: 'two_pair', cards: [] } },
      }) }),
    });
    render(<App />);
    await userEvent.click(screen.getByRole('button', { name: 'Jouer' }));
    expect(await screen.findByText('Vous remportez 200 jetons avec : couleur.')).toBeInTheDocument();
  });

  it('resumes the game saved before a reload', async () => {
    localStorage.setItem('sensai-game-id', 'g9');
    fakeServer({
      '/api/state': body => ({ gameId: String(body.gameId), state: state({ playerStack: 1500 }) }),
    });
    render(<App />);
    await userEvent.click(await screen.findByRole('button', { name: 'Reprendre la partie' }));
    expect(await screen.findByText(/à vous de jouer/)).toBeInTheDocument();
    expect(bodies[0]).toEqual({ gameId: 'g9' });

    await userEvent.click(screen.getByRole('button', { name: 'Retour à l’accueil' }));
    await userEvent.click(screen.getByRole('button', { name: 'Reprendre la partie' }));
    expect(screen.getByRole('region', { name: 'Partie' })).toBeInTheDocument();
  });

  it('forgets a saved game the server no longer knows', async () => {
    localStorage.setItem('sensai-game-id', 'gone');
    fakeServer({});
    render(<App />);
    await waitFor(() => expect(localStorage.getItem('sensai-game-id')).toBeNull());
    expect(screen.queryByRole('button', { name: 'Reprendre la partie' })).not.toBeInTheDocument();
  });
});

