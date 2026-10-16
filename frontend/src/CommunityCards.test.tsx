import { render, screen, within } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import CommunityCards from './CommunityCards';

describe('CommunityCards', () => {
  it('places the flop, turn and river in their own groups', () => {
    render(<CommunityCards cards={[
      { rank: 'A', suit: 'spades' }, { rank: 'K', suit: 'hearts' }, { rank: '2', suit: 'clubs' },
      { rank: '7', suit: 'diamonds' },
    ]} />);
    expect(within(screen.getByRole('group', { name: 'Flop' })).getAllByRole('img').map(card => card.getAttribute('aria-label')))
      .toEqual(['A de pique', 'K de cœur', '2 de trèfle']);
    expect(within(screen.getByRole('group', { name: 'Turn' })).getByRole('img', { name: '7 de carreau' })).toBeInTheDocument();
    expect(within(screen.getByRole('group', { name: 'River' })).getByRole('img', { name: 'Carte non distribuée' })).toBeInTheDocument();
  });
});
