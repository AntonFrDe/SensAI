import { render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it, vi } from 'vitest';
import GameRecords from './GameRecords';
import type { GameRecord } from './gameRecords';

const records: GameRecord[] = [
  { gameId: 'g2', startedAt: '2026-10-16T10:00:00Z', blinds: '25/50', startStack: 5000, hands: 3, won: 2, net: 450, result: 'playing' },
  { gameId: 'g1', startedAt: '2026-10-15T20:30:00Z', blinds: '10/20', startStack: 1000, hands: 14, won: 9, net: 1000, result: 'won' },
  { gameId: 'g0', startedAt: 'invalid', blinds: '5/10', startStack: 500, hands: 6, won: 1, net: -500, result: 'lost' },
];

describe('GameRecords', () => {
  it('lists the games with their result and counts the victories', () => {
    render(<GameRecords records={records} onClear={vi.fn()} onBack={vi.fn()} />);
    expect(screen.getByText('2 parties terminées, 1 victoire.')).toBeInTheDocument();
    const rows = within(screen.getByRole('table')).getAllByRole('row').slice(1);
    expect(rows.map(row => within(row).getAllByRole('cell').slice(1).map(cell => cell.textContent?.replace(/\s/g, ' ')))).toEqual([
      ['25/50', '3', '2', '+450', 'En cours'],
      ['10/20', '14', '9', '+1 000', 'Victoire'],
      ['5/10', '6', '1', '-500', 'Défaite'],
    ]);
    expect(within(rows[2]).getAllByRole('cell')[0]).toHaveTextContent('—');
  });

  it('asks before clearing the history', async () => {
    const onClear = vi.fn();
    render(<GameRecords records={records} onClear={onClear} onBack={vi.fn()} />);
    await userEvent.click(screen.getByRole('button', { name: 'Effacer l’historique' }));
    expect(onClear).not.toHaveBeenCalled();
    await userEvent.click(screen.getByRole('button', { name: 'Confirmer l’effacement' }));
    expect(onClear).toHaveBeenCalledOnce();
  });

  it('explains when there is nothing yet', async () => {
    const onBack = vi.fn();
    render(<GameRecords records={[]} onClear={vi.fn()} onBack={onBack} />);
    expect(screen.getByText(/Aucune partie enregistrée/)).toBeInTheDocument();
    await userEvent.click(screen.getByRole('button', { name: '← Accueil' }));
    expect(onBack).toHaveBeenCalledOnce();
  });
});
