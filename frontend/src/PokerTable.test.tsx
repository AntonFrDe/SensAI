import { render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import PokerTable from './PokerTable';

describe('PokerTable', () => {
  it('shows the stacks, the pot and the private cards', () => {
    render(<PokerTable playerCards={[{ rank: 'A', suit: 'spades' }, { rank: 'K', suit: 'spades' }]}
      pot={60} playerStack={970} opponentStack={970} currentPlayer="player" phase="pre_flop" currentBet={20} />);
    expect(screen.getByText(/^Pot/)).toHaveTextContent('Pot : 60 jetons');
    expect(screen.getByRole('region', { name: 'Vous' })).toHaveTextContent('Stack : 970 jetons');
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

  it('places both seats with their markers and the blinds', () => {
    render(<PokerTable phase="flop" currentPlayer="opponent" blinds={{ small: 10, big: 20 }} seats={{
      player: { name: 'Vous', stack: 940, bet: 0, folded: false, allIn: false, dealer: true, blind: 'big' },
      opponent: { name: 'IA', stack: 900, bet: 40, folded: false, allIn: false, dealer: false, blind: 'small' },
    }} />);
    const opponent = screen.getByRole('region', { name: 'Adversaire IA' });
    expect(opponent).toHaveAttribute('aria-current', 'true');
    expect(opponent).toHaveTextContent('Mise : 40 jetons');
    expect(screen.getByRole('region', { name: 'Vous' })).toHaveTextContent('D');
    expect(screen.getByText(/^Blindes/)).toHaveTextContent('Blindes : 10 / 20');
  });

  it('marks nobody as active once the hand is over', () => {
    render(<PokerTable phase="showdown" currentPlayer="player" playerStack={1000} opponentStack={1000} />);
    expect(screen.getByRole('region', { name: 'Vous' })).not.toHaveAttribute('aria-current');
  });
});

