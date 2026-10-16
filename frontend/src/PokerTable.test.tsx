import { render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import PokerTable from './PokerTable';

describe('PokerTable', () => {
  it('shows the stacks, the pot and the private cards', () => {
    render(<PokerTable playerCards={[{ rank: 'A', suit: 'spades' }, { rank: 'K', suit: 'spades' }]}
      pot={60} playerStack={970} opponentStack={970} currentPlayer="player" phase="pre_flop" currentBet={20} />);
    expect(screen.getByText(/^Pot/)).toHaveTextContent('Pot : 60 jetons');
    expect(screen.getByText(/^Votre stack/)).toHaveTextContent('970 jetons');
    expect(screen.getByRole('group', { name: 'Vos cartes privées' })).toHaveTextContent('A♠K♠');
    expect(screen.getByText(/^Tour/)).toHaveTextContent('à vous de jouer');
  });

  it('hides the opponent cards until they are revealed', () => {
    const { rerender } = render(<PokerTable phase="river" />);
    expect(screen.queryByRole('group', { name: 'Cartes de l’IA' })).not.toBeInTheDocument();
    rerender(<PokerTable phase="showdown" opponentCards={[{ rank: '9', suit: 'hearts' }, { rank: '9', suit: 'clubs' }]} />);
    expect(screen.getByRole('group', { name: 'Cartes de l’IA' })).toHaveTextContent('9♥9♣');
    expect(screen.getByText(/^Tour/)).toHaveTextContent('main terminée');
  });

  it('locks the controls while the opponent is playing', () => {
    render(<PokerTable currentPlayer="opponent" phase="flop"
      controls={{ allowedActions: ['fold', 'check'], onAction: vi.fn() }} />);
    expect(screen.getByRole('button', { name: 'Check' })).toBeDisabled();
    expect(screen.getByText(/^Tour/)).toHaveTextContent('adversaire IA');
  });

  it('shows the opponent note and the hand history', () => {
    render(<PokerTable opponentNote="L’IA réfléchit…" history={[{ street: 'pre_flop', player: 'IA', action: 'fold' }]} />);
    expect(screen.getByText('L’IA réfléchit…')).toBeInTheDocument();
    expect(screen.getByText('Historique de la main (1)')).toBeInTheDocument();
  });
});
