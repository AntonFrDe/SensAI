import { act, render, screen, waitFor, within } from '@testing-library/react';
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

const setup = 'Partie contre l’IA';

async function openMode(name: string) {
  await userEvent.click(screen.getByRole('button', { name: 'Plus' }));
  await userEvent.click(screen.getByRole('button', { name }));
}

describe('App', () => {
  beforeEach(() => localStorage.clear());

  it('opens on the Jeton trainer, without the old home', () => {
    fakeServer({});
    render(<App />);
    expect(screen.getByRole('region', { name: 'Entraîneur Jeton' })).toBeInTheDocument();
    expect(screen.queryByRole('heading', { name: 'SensAI Poker' })).not.toBeInTheDocument();
    expect(screen.queryByRole('button', { name: 'Jouer' })).not.toBeInTheDocument();
  });

  it('gives every page a way back to the trainer', async () => {
    fakeServer({});
    for (const name of [setup, 'Banque de situations', 'Glossaire', 'Classement des mains', 'Mes parties']) {
      const { unmount } = render(<App />);
      await openMode(name);
      await userEvent.click(screen.getByRole('button', { name: 'Entraîneur' }));
      expect(screen.getByRole('region', { name: 'Entraîneur Jeton' })).toBeInTheDocument();
      unmount();
    }
  });

  it('stays where the player went when the AI answers later', async () => {
    let releaseOpponent: () => void = () => undefined;
    const answer = new Promise<void>(resolve => { releaseOpponent = resolve; });
    vi.spyOn(globalThis, 'fetch').mockImplementation(async (input, init) => {
      const path = String(input);
      if (path === '/api/status') return Response.json(status);
      if (path === '/api/games') return Response.json({ gameId: 'g5', state: state({ currentPlayer: 'opponent', controls: { allowedActions: [] } }) });
      if (path === '/api/opponent') {
        await answer;
        return Response.json({ gameId: 'g5', state: state({}), opponentAction: { action: 'call', source: 'llm' } });
      }
      return Response.json({ error: 'Not found.', body: init?.body }, { status: 404 });
    });
    render(<App />);
    await openMode(setup);
    await userEvent.click(screen.getByRole('button', { name: 'Jouer' }));
    await userEvent.click(screen.getByRole('button', { name: 'Entraîneur' }));
    await act(async () => {
      releaseOpponent();
      await new Promise(resolve => setTimeout(resolve, 20));
    });
    expect(screen.getByRole('region', { name: 'Entraîneur Jeton' })).toBeInTheDocument();
    expect(screen.queryByRole('region', { name: 'Partie' })).not.toBeInTheDocument();
  });

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

    await openMode(setup);
    await userEvent.click(screen.getByRole('button', { name: 'Jouer' }));
    expect(await screen.findByText('L’IA : Raise à 60.')).toBeInTheDocument();
    expect(calls).toEqual(['/api/games', '/api/opponent']);
    expect(bodies[0]).toEqual({ options: { blinds: '10/20', stackBigBlinds: 50, revealAtEnd: false } });

    await userEvent.click(screen.getByRole('button', { name: 'Fold' }));
    expect(await screen.findByText('L’IA remporte 80 jetons (tu as fold).')).toBeInTheDocument();

    const stats = screen.getByRole('region', { name: 'Statistiques' });
    expect(stats).toHaveTextContent('Mains jouées1');
    expect(stats).toHaveTextContent('Bilan-10 jetons');

    await userEvent.click(screen.getByRole('button', { name: 'Main suivante' }));
    expect(calls.at(-1)).toBe('/api/next-hand');
    expect(await screen.findByText(/Tour : à toi de jouer/)).toBeInTheDocument();

    await userEvent.click(screen.getByRole('button', { name: 'Retour à l’entraîneur' }));
    await openMode('Mes parties');
    const row = within(screen.getByRole('table')).getAllByRole('row')[1];
    expect(within(row).getAllByRole('cell').slice(1).map(cell => cell.textContent)).toEqual(['10/20', '1', '0', '-10', 'En cours']);
  });

  it('shows a readable error when the server is down', async () => {
    vi.spyOn(globalThis, 'fetch').mockRejectedValue(new TypeError('Failed to fetch'));
    render(<App />);
    await openMode(setup);
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
    await openMode(setup);
    await userEvent.click(screen.getByRole('button', { name: 'Jouer' }));
    expect(await screen.findByText('Tu remportes 200 jetons avec : couleur.')).toBeInTheDocument();
  });

  it('resumes the game saved before a reload', async () => {
    localStorage.setItem('sensai-game-id', 'g9');
    fakeServer({
      '/api/state': body => ({ gameId: String(body.gameId), state: state({ playerStack: 1500 }) }),
    });
    render(<App />);
    await openMode(setup);
    await userEvent.click(await screen.findByRole('button', { name: 'Reprendre la partie' }));
    expect(await screen.findByText(/Tour : à toi de jouer/)).toBeInTheDocument();
    expect(bodies[0]).toEqual({ gameId: 'g9' });

    await userEvent.click(screen.getByRole('button', { name: 'Retour à l’entraîneur' }));
    await openMode(setup);
    await userEvent.click(screen.getByRole('button', { name: 'Reprendre la partie' }));
    expect(screen.getByRole('region', { name: 'Partie' })).toBeInTheDocument();
  });

  it('forgets a saved game the server no longer knows', async () => {
    localStorage.setItem('sensai-game-id', 'gone');
    fakeServer({});
    render(<App />);
    await waitFor(() => expect(localStorage.getItem('sensai-game-id')).toBeNull());
    await openMode(setup);
    expect(screen.queryByRole('button', { name: 'Reprendre la partie' })).not.toBeInTheDocument();
  });

  it('offers the guided tour on the first game only', async () => {
    fakeServer({ '/api/games': () => ({ gameId: 'g3', state: state({}) }) });
    const { unmount } = render(<App />);
    await openMode(setup);
    await userEvent.click(screen.getByRole('button', { name: 'Jouer' }));
    expect(await screen.findByRole('dialog', { name: 'Tes cartes et le board' })).toBeInTheDocument();
    await userEvent.click(screen.getByRole('button', { name: 'Passer la visite' }));
    unmount();
    render(<App />);
    await openMode(setup);
    await userEvent.click(screen.getByRole('button', { name: 'Jouer' }));
    await screen.findByText(/Tour : à toi de jouer/);
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
    await userEvent.click(screen.getByRole('button', { name: 'Visite guidée' }));
    expect(screen.getByRole('dialog')).toBeInTheDocument();
  });
});
