import { render, screen, within } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import HandRankings from './HandRankings';

describe('HandRankings', () => {
  it('lists the hands from the strongest with an example', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(Response.json({ rankings: [
      { rank: 1, name: 'Quinte flush royale', description: 'As, Roi, Dame, Valet, 10 de la même couleur.', cards: [
        { rank: 'A', suit: 'spades' }, { rank: 'K', suit: 'spades' }, { rank: 'Q', suit: 'spades' },
        { rank: 'J', suit: 'spades' }, { rank: '10', suit: 'spades' },
      ] },
      { rank: 9, name: 'Paire', description: 'Deux cartes de même valeur.', cards: [] },
    ] }));
    render(<HandRankings />);
    const items = await screen.findAllByRole('listitem');
    expect(items.map(item => within(item).getByRole('heading').textContent)).toEqual(['Quinte flush royale', 'Paire']);
    expect(within(items[0]).getByRole('group', { name: 'Exemple de quinte flush royale' })).toHaveTextContent('A♠K♠Q♠J♠10♠');
  });

  it('reports a failure', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(Response.json({}, { status: 500 }));
    render(<HandRankings />);
    expect(await screen.findByRole('alert')).toHaveTextContent('Classement des mains indisponible.');
  });
});
