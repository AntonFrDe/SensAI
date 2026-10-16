import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import PlayingCard from './PlayingCard';

describe('PlayingCard', () => {
  it('names the card for screen readers and paints red suits', () => {
    render(<PlayingCard card={{ rank: 'Q', suit: 'hearts' }} />);
    const card = screen.getByRole('img', { name: 'Q de cœur' });
    expect(card).toHaveTextContent('Q♥');
    expect(card).toHaveClass('red');
  });

  it('keeps black suits black', () => {
    render(<PlayingCard card={{ rank: '10', suit: 'spades' }} />);
    expect(screen.getByRole('img', { name: '10 de pique' })).not.toHaveClass('red');
  });

  it('shows a placeholder for a card not dealt yet', () => {
    render(<PlayingCard />);
    expect(screen.getByRole('img', { name: 'Carte non distribuée' })).toHaveTextContent('?');
  });
});
