import { fireEvent, render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it, vi } from 'vitest';
import HandLog from './HandLog';
import HandReplay from './HandReplay';
import type { PlayedHand } from './handLog';

const hand: PlayedHand = {
  number: 3,
  playerCards: [{ rank: 'A', suit: 'spades' }, { rank: 'K', suit: 'spades' }],
  opponentCards: [{ rank: 'Q', suit: 'hearts' }, { rank: 'Q', suit: 'clubs' }],
  board: [{ rank: 'K', suit: 'hearts' }, { rank: '7', suit: 'clubs' }, { rank: '2', suit: 'diamonds' }],
  history: [
    { street: 'pre_flop', player: 'IA', action: 'call', amount: 10 },
    { street: 'pre_flop', player: 'Vous', action: 'check' },
    { street: 'flop', player: 'IA', action: 'bet', amount: 40 },
    { street: 'flop', player: 'Vous', action: 'raise', amount: 1000 },
    { street: 'flop', player: 'IA', action: 'call', amount: 960 },
  ],
  awards: [{ amount: 2000, winners: ['Vous'], reason: 'showdown' }],
  playerHand: { rank: 'one_pair', cards: [] },
  opponentHand: { rank: 'one_pair', cards: [] },
  net: 1000,
  stackAfter: 2000,
};

describe('HandReplay', () => {
  it('walks through the hand and reveals the opponent at the end', async () => {
    render(<HandReplay hand={hand} onClose={vi.fn()} />);
    expect(screen.getByText('Étape 1 / 8')).toBeInTheDocument();
    expect(screen.getByText('Les cartes sont distribuées.')).toBeInTheDocument();
    expect(screen.getAllByRole('img', { name: 'Carte non distribuée' })).toHaveLength(7);

    await userEvent.click(screen.getByRole('button', { name: 'Suivant' }));
    expect(screen.getByText('L’IA : Call 10 jetons')).toBeInTheDocument();
    await userEvent.click(screen.getByRole('button', { name: 'Suivant' }));
    await userEvent.click(screen.getByRole('button', { name: 'Suivant' }));
    expect(screen.getByText('Flop', { selector: '.replay-street' })).toBeInTheDocument();
    expect(screen.getByRole('img', { name: 'K de cœur' })).toBeInTheDocument();

    await userEvent.click(screen.getByRole('button', { name: 'Fin' }));
    expect(screen.getByText(/^Tu gagnes 1\s000 jetons\.$/)).toBeInTheDocument();
    expect(screen.getByRole('img', { name: 'Q de cœur' })).toBeInTheDocument();
    expect(screen.getByLabelText('Main de l’IA : Paire')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Suivant' })).toBeDisabled();
  });

  it('follows the arrow keys and closes on Escape', () => {
    const onClose = vi.fn();
    render(<HandReplay hand={hand} onClose={onClose} />);
    const box = screen.getByRole('region', { name: 'Revoir la main n°3' });
    expect(box).toHaveFocus();
    fireEvent.keyDown(box, { key: 'End' });
    expect(screen.getByText('Étape 8 / 8')).toBeInTheDocument();
    fireEvent.keyDown(box, { key: 'ArrowLeft' });
    expect(screen.getByText('L’IA : Call 960 jetons')).toBeInTheDocument();
    fireEvent.keyDown(box, { key: 'Escape' });
    expect(onClose).toHaveBeenCalledOnce();
  });
});

describe('HandLog', () => {
  it('lists the hands with their result and opens a replay', async () => {
    render(<HandLog hands={[hand, { ...hand, number: 2, playerHand: null, net: -20, history: [{ street: 'pre_flop', player: 'Vous', action: 'fold' }] }]} />);
    const rows = screen.getAllByRole('listitem');
    expect(rows[0]).toHaveTextContent(/n°3A♠ K♠Paire\+1\s000/);
    expect(rows[1]).toHaveTextContent('n°2A♠ K♠Fold-20');
    await userEvent.click(screen.getByRole('button', { name: 'Revoir la main n°2' }));
    expect(screen.getByRole('region', { name: 'Revoir la main n°2' })).toBeInTheDocument();
    await userEvent.click(screen.getByRole('button', { name: 'Fermer' }));
    expect(screen.queryByRole('region', { name: 'Revoir la main n°2' })).not.toBeInTheDocument();
  });

  it('explains where the hands will appear', () => {
    render(<HandLog hands={[]} />);
    expect(screen.getByText('Les mains terminées apparaîtront ici.')).toBeInTheDocument();
  });

  it('downloads the hands as a text file', async () => {
    const createObjectURL = vi.fn().mockReturnValue('blob:hands');
    Object.assign(URL, { createObjectURL, revokeObjectURL: vi.fn() });
    const click = vi.spyOn(HTMLAnchorElement.prototype, 'click').mockImplementation(() => {});
    render(<HandLog hands={[hand]} />);
    await userEvent.click(screen.getByRole('button', { name: 'Exporter en texte' }));
    const blob = createObjectURL.mock.calls[0][0] as Blob;
    expect(await blob.text()).toContain('Main n°3');
    expect((click.mock.contexts[0] as HTMLAnchorElement).download).toBe('sensai-mains.txt');
  });
});

