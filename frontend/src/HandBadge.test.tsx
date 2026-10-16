import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import HandBadge, { sameCard } from './HandBadge';
import PlayingCard from './PlayingCard';

describe('HandBadge', () => {
  it('names the hand in French for its owner', () => {
    render(<HandBadge owner="Votre main" hand={{ rank: 'full_house', cards: [] }} />);
    expect(screen.getByLabelText('Votre main : Full')).toHaveTextContent('Full');
  });

  it('renders nothing before the flop', () => {
    const { container } = render(<HandBadge owner="Votre main" hand={null} />);
    expect(container).toBeEmptyDOMElement();
  });

  it('compares cards by rank and suit', () => {
    expect(sameCard({ rank: '10', suit: 'hearts' }, { rank: '10', suit: 'hearts' })).toBe(true);
    expect(sameCard({ rank: '10', suit: 'hearts' }, { rank: '10', suit: 'spades' })).toBe(false);
  });

  it('marks a card of the best hand for sight and screen readers', () => {
    render(<PlayingCard card={{ rank: 'A', suit: 'clubs' }} highlighted />);
    expect(screen.getByRole('img', { name: 'A de trèfle, dans la meilleure main' })).toHaveClass('best');
  });
});
