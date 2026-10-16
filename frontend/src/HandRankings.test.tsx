import { render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
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
    const onBack = vi.fn();
    render(<HandRankings onBack={onBack} />);
    const items = await screen.findAllByRole('listitem');
    expect(items.map(item => within(item).getByRole('heading').textContent)).toEqual(['Quinte flush royale', 'Paire']);
    expect(within(items[0]).getByRole('group', { name: 'Exemple de quinte flush royale' })).toHaveTextContent('A♠K♠Q♠J♠10♠');
    await userEvent.click(screen.getByRole('button', { name: '← Accueil' }));
    expect(onBack).toHaveBeenCalledOnce();
  });

  it('reports a failure', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(Response.json({}, { status: 500 }));
    render(<HandRankings onBack={vi.fn()} />);
    expect(await screen.findByRole('alert')).toHaveTextContent('Classement des mains indisponible.');
  });
});
