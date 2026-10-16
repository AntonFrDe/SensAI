import { render, screen, within } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import HandHistory, { type HistoryEntry } from './HandHistory';

const entries: HistoryEntry[] = [
  { street: 'pre_flop', player: 'IA', action: 'call', amount: 10 },
  { street: 'pre_flop', player: 'Vous', action: 'check' },
  { street: 'flop', player: 'IA', action: 'bet', amount: 40 },
  { street: 'flop', player: 'Vous', action: 'raise', amount: 120 },
];

describe('HandHistory', () => {
  it('groups the actions by street in French', () => {
    render(<HandHistory entries={entries} />);
    expect(screen.getByText('Historique de la main (4)')).toBeInTheDocument();
    const preflop = within(screen.getByRole('region', { name: 'Préflop' })).getAllByRole('listitem');
    expect(preflop.map(item => item.textContent)).toEqual(['L’IA suit 10 jetons', 'Vous checkez']);
    const flop = within(screen.getByRole('region', { name: 'Flop' })).getAllByRole('listitem');
    expect(flop.map(item => item.textContent)).toEqual(['L’IA mise 40 jetons', 'Vous relancez à 120 jetons']);
  });

  it('opens a new group when the same street comes back after another one', () => {
    render(<HandHistory entries={[entries[0], entries[2], { street: 'pre_flop', player: 'Vous', action: 'fold' }]} />);
    expect(screen.getAllByRole('heading', { level: 3 }).map(heading => heading.textContent)).toEqual(['Préflop', 'Flop', 'Préflop']);
  });

  it('says when nothing has been played yet', () => {
    render(<HandHistory entries={[]} />);
    expect(screen.getByText('Aucune action pour cette main.')).toBeInTheDocument();
  });
});
