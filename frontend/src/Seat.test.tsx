import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import Seat, { type SeatData } from './Seat';

const seat: SeatData = { name: 'Vous', stack: 980, bet: 20, folded: false, allIn: false, dealer: true, blind: 'big' };

describe('Seat', () => {
  it('shows the stack, the street bet and the dealer and blind badges', () => {
    render(<Seat seat={seat} label="Vous" avatar="V" position="bottom" />);
    const box = screen.getByRole('region', { name: 'Vous' });
    expect(box).toHaveTextContent('Stack : 980 jetons');
    expect(screen.getByText(/^Mise/)).toHaveTextContent('Mise : 20 jetons');
    expect(screen.getByLabelText('Donneur')).toHaveTextContent('D');
    expect(screen.getByLabelText('Grosse blinde')).toHaveTextContent('BB');
  });

  it('marks the player who must act', () => {
    render(<Seat seat={{ ...seat, dealer: false, blind: null, bet: 0 }} label="IA" avatar="IA" position="top" active />);
    const box = screen.getByRole('region', { name: 'IA' });
    expect(box).toHaveAttribute('aria-current', 'true');
    expect(box).toHaveTextContent('Doit jouer');
    expect(screen.queryByText(/^Mise/)).not.toBeInTheDocument();
    expect(screen.queryByLabelText('Donneur')).not.toBeInTheDocument();
  });

  it('says when a player folded or is all-in', () => {
    const { rerender } = render(<Seat seat={{ ...seat, folded: true }} label="IA" avatar="IA" position="top" />);
    expect(screen.getByRole('region', { name: 'IA' })).toHaveClass('folded');
    expect(screen.getByText('Couché')).toBeInTheDocument();
    rerender(<Seat seat={{ ...seat, stack: 0, allIn: true }} label="IA" avatar="IA" position="top" />);
    expect(screen.getByText('Tapis')).toBeInTheDocument();
  });

  it('renders the cards given as children', () => {
    render(<Seat label="Vous" avatar="V" position="bottom"><span role="img" aria-label="A de pique">A♠</span></Seat>);
    expect(screen.getByRole('img', { name: 'A de pique' })).toBeInTheDocument();
    expect(screen.getByRole('region', { name: 'Vous' })).toHaveTextContent('Stack : —');
  });
});
