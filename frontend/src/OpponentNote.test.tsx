import { act, render, screen } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import OpponentNote from './OpponentNote';
import PokerTable from './PokerTable';
import { shortAction } from './HandHistory';

describe('OpponentNote', () => {
  beforeEach(() => vi.useFakeTimers());
  afterEach(() => vi.useRealTimers());

  it('counts the seconds while the opponent thinks and explains a slow model', () => {
    const { rerender } = render(<OpponentNote thinking />);
    expect(screen.getByText(/L’IA réfléchit/)).toHaveTextContent('L’IA réfléchit… 0 s');
    act(() => vi.advanceTimersByTime(3000));
    expect(screen.getByText(/L’IA réfléchit/)).toHaveTextContent('3 s');
    expect(screen.queryByText(/15 à 40 s/)).not.toBeInTheDocument();
    act(() => vi.advanceTimersByTime(17000));
    expect(screen.getByText(/15 à 40 s/)).toBeInTheDocument();
    rerender(<OpponentNote thinking={false} note="L’IA suit." />);
    expect(screen.getByText('L’IA suit.')).toBeInTheDocument();
    rerender(<OpponentNote thinking />);
    expect(screen.getByText(/L’IA réfléchit/)).toHaveTextContent('0 s');
  });
});

describe('last actions on the seats', () => {
  it('shortens an action with its amount', () => {
    expect(shortAction({ street: 'flop', player: 'IA', action: 'raise', amount: 1200 })).toMatch(/^Raise à 1\s200$/);
    expect(shortAction({ street: 'flop', player: 'Vous', action: 'check' })).toBe('Check');
  });

  it('shows the last action of each player on the current street only', () => {
    render(<PokerTable phase="flop" history={[
      { street: 'pre_flop', player: 'Vous', action: 'call', amount: 10 },
      { street: 'pre_flop', player: 'IA', action: 'check' },
      { street: 'flop', player: 'IA', action: 'bet', amount: 40 },
    ]} />);
    expect(screen.getByLabelText('Dernière action : Bet 40')).toBeInTheDocument();
    expect(screen.queryByLabelText(/Dernière action : Call/)).not.toBeInTheDocument();
  });
});
