import { fireEvent, render, screen, within } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import GameSummary, { summarize } from './GameSummary';
import StackChart, { niceTicks } from './StackChart';
import type { PlayedHand } from './handLog';

const points = [{ hand: 0, stack: 1000 }, { hand: 1, stack: 1120 }, { hand: 2, stack: 870 }, { hand: 3, stack: 1400 }];

function played(number: number, net: number, stackAfter: number, extra: Partial<PlayedHand> = {}): PlayedHand {
  return {
    number, playerCards: [], opponentCards: [], board: [], history: [], playerHand: null, opponentHand: null, net, stackAfter,
    awards: [{ amount: Math.abs(net) * 2, winners: [net > 0 ? 'Vous' : 'IA'], reason: 'showdown' }], ...extra,
  };
}

describe('niceTicks', () => {
  it('rounds the axis to clean steps around the data', () => {
    expect(niceTicks(870, 1400)).toEqual([800, 1000, 1200, 1400]);
    expect(niceTicks(1000, 1000)).toEqual([950, 1000, 1050]);
  });
});

describe('StackChart', () => {
  it('describes the curve and lists the values in a table', () => {
    render(<StackChart points={points} title="Évolution de ton tapis" />);
    expect(screen.getByRole('img', { name: /de 1\s000 à 1\s400 jetons en 3 mains/ })).toBeInTheDocument();
    const rows = within(screen.getByRole('table')).getAllByRole('row');
    expect(rows.map(row => row.textContent?.replace(/\s/g, ' '))).toEqual([
      'MomentTon tapis', 'Départ1 000', 'Main n°11 120', 'Main n°2870', 'Main n°31 400',
    ]);
  });

  it('shows a tooltip on focus and moves with the arrow keys', () => {
    render(<StackChart points={points} title="Évolution de ton tapis" />);
    const chart = screen.getByRole('img');
    fireEvent.focus(chart);
    expect(screen.getByRole('status')).toHaveTextContent(/1\s400 jetonsMain n°3/);
    fireEvent.keyDown(chart, { key: 'ArrowLeft' });
    expect(screen.getByRole('status')).toHaveTextContent('870 jetonsMain n°2');
    fireEvent.blur(chart);
    expect(screen.queryByRole('status')).not.toBeInTheDocument();
  });

  it('needs at least one finished hand', () => {
    const { container } = render(<StackChart points={[points[0]]} title="Évolution" />);
    expect(container).toBeEmptyDOMElement();
  });
});

describe('GameSummary', () => {
  const hands = [
    played(1, 120, 1120, { playerHand: { rank: 'two_pair', cards: [] } }),
    played(2, -250, 870),
    played(3, 530, 1400, { playerHand: { rank: 'flush', cards: [] } }),
  ];

  it('counts the hands, the biggest pot and the best winning hand', () => {
    expect(summarize(hands)).toEqual({ played: 3, won: 2, biggestPot: 1060, best: 'flush' });
  });

  it('announces the winner and draws the stack history', () => {
    render(<GameSummary hands={hands} playerWon />);
    expect(screen.getByRole('heading')).toHaveTextContent('Victoire : l’IA n’a plus de jetons.');
    expect(screen.getByText('Couleur')).toBeInTheDocument();
    expect(screen.getByText('Ton tapis main après main')).toBeInTheDocument();
  });
});
