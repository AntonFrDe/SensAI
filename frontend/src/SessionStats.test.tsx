import { render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it, vi } from 'vitest';
import SessionStats from './SessionStats';
import { emptyStats } from './sessionStats';

const session = { ...emptyStats, hands: 4, won: 3, lost: 1, showdowns: 2, showdownsWon: 1, biggestPotWon: 1200, net: 250, streak: 2, bestStreak: 2 };
const lifetime = { ...emptyStats, hands: 40, won: 18, lost: 20, split: 2, net: -310, streak: -1, bestStreak: 5 };

function value(label: string): string | null {
  return within(screen.getByText(label).closest('div') as HTMLElement).getByRole('definition').textContent;
}

describe('SessionStats', () => {
  it('summarises the current game', () => {
    render(<SessionStats session={session} lifetime={lifetime} onResetLifetime={vi.fn()} />);
    expect(value('Mains jouées')).toBe('4');
    expect(value('Taux de victoire')).toMatch(/^75\s%$/);
    expect(value('Abattages gagnés')).toBe('1 sur 2');
    expect(value('Plus gros pot gagné')).toMatch(/^1\s200 jetons$/);
    expect(value('Bilan')).toBe('+250 jetons');
    expect(value('Série en cours')).toBe('2 gagnées');
  });

  it('switches to the lifetime totals', async () => {
    render(<SessionStats session={session} lifetime={lifetime} onResetLifetime={vi.fn()} />);
    await userEvent.click(screen.getByRole('button', { name: 'Depuis toujours' }));
    expect(screen.getByRole('button', { name: 'Depuis toujours' })).toHaveAttribute('aria-pressed', 'true');
    expect(value('Gagnées / perdues / partagées')).toBe('18 / 20 / 2');
    expect(value('Bilan')).toBe('-310 jetons');
    expect(value('Série en cours')).toBe('1 perdue');
  });

  it('asks for a confirmation before clearing the lifetime totals', async () => {
    const onReset = vi.fn();
    render(<SessionStats session={session} lifetime={lifetime} onResetLifetime={onReset} />);
    expect(screen.queryByRole('button', { name: 'Remettre à zéro' })).not.toBeInTheDocument();
    await userEvent.click(screen.getByRole('button', { name: 'Depuis toujours' }));
    await userEvent.click(screen.getByRole('button', { name: 'Remettre à zéro' }));
    expect(onReset).not.toHaveBeenCalled();
    await userEvent.click(screen.getByRole('button', { name: 'Confirmer la remise à zéro' }));
    expect(onReset).toHaveBeenCalledOnce();
  });

  it('shows dashes before the first hand', () => {
    render(<SessionStats session={emptyStats} lifetime={emptyStats} onResetLifetime={vi.fn()} />);
    expect(value('Taux de victoire')).toBe('—');
    expect(value('Bilan')).toBe('0 jetons');
  });

  it('adds the session to the game notes with a remark', async () => {
    const fetchMock = vi.spyOn(globalThis, 'fetch').mockResolvedValue(Response.json({ line: '- 2026-10-16 : partie web, 4 mains.' }, { status: 201 }));
    render(<SessionStats session={session} lifetime={lifetime} onResetLifetime={vi.fn()} />);
    await userEvent.type(screen.getByRole('textbox', { name: 'Ce que je retiens (facultatif)' }), 'Je relance mieux.');
    await userEvent.click(screen.getByRole('button', { name: 'Ajouter à mes notes' }));
    expect(await screen.findByRole('status')).toHaveTextContent('partie web, 4 mains.');
    expect(JSON.parse(String(fetchMock.mock.calls[0][1]?.body))).toEqual({ hands: 4, won: 3, net: 250, remark: 'Je relance mieux.' });
    expect(screen.getByRole('textbox')).toHaveValue('');
  });

  it('reports a refused note and hides the form before the first hand', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(Response.json({ error: 'Invalid session numbers.' }, { status: 400 }));
    const { rerender } = render(<SessionStats session={session} lifetime={lifetime} onResetLifetime={vi.fn()} />);
    await userEvent.click(screen.getByRole('button', { name: 'Ajouter à mes notes' }));
    expect(await screen.findByRole('alert')).toHaveTextContent('Invalid session numbers.');
    rerender(<SessionStats session={emptyStats} lifetime={lifetime} onResetLifetime={vi.fn()} />);
    expect(screen.queryByRole('button', { name: 'Ajouter à mes notes' })).not.toBeInTheDocument();
  });
});

