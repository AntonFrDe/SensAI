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
});
