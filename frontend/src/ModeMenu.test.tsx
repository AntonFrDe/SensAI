import { render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it, vi } from 'vitest';
import ModeMenu from './ModeMenu';

const labels = ['Partie contre l’IA', 'Banque de situations', 'Glossaire', 'Classement des mains', 'Mes parties'];

describe('ModeMenu', () => {
  it('lists the modes and opens the chosen one', async () => {
    const onSelect = vi.fn();
    render(<ModeMenu current="trainer" onSelect={onSelect} />);
    const toggle = screen.getByRole('button', { name: 'Plus' });
    expect(toggle).toHaveAttribute('aria-expanded', 'false');
    expect(screen.queryByRole('navigation', { name: 'Autres modes' })).not.toBeInTheDocument();

    await userEvent.click(toggle);
    expect(toggle).toHaveAttribute('aria-expanded', 'true');
    const menu = screen.getByRole('navigation', { name: 'Autres modes' });
    expect(within(menu).getAllByRole('button').map(button => button.textContent)).toEqual(labels);

    await userEvent.click(within(menu).getByRole('button', { name: 'Mes parties' }));
    expect(onSelect).toHaveBeenCalledWith('records');
    expect(toggle).toHaveAttribute('aria-expanded', 'false');
  });

  it('marks the current mode, the game page belonging to the game mode', async () => {
    render(<ModeMenu current="game" onSelect={vi.fn()} />);
    await userEvent.click(screen.getByRole('button', { name: 'Plus' }));
    const menu = screen.getByRole('navigation', { name: 'Autres modes' });
    expect(within(menu).getByRole('button', { name: 'Partie contre l’IA' })).toHaveAttribute('aria-current', 'page');
    expect(within(menu).getByRole('button', { name: 'Glossaire' })).not.toHaveAttribute('aria-current');
  });

  it('closes on Escape and gives the focus back to the toggle', async () => {
    render(<ModeMenu current="trainer" onSelect={vi.fn()} />);
    const toggle = screen.getByRole('button', { name: 'Plus' });
    await userEvent.click(toggle);
    await userEvent.keyboard('{Escape}');
    expect(screen.queryByRole('navigation', { name: 'Autres modes' })).not.toBeInTheDocument();
    expect(toggle).toHaveFocus();
  });

  it('closes on a click outside the menu without choosing a mode', async () => {
    const onSelect = vi.fn();
    render(<div><p>Ailleurs</p><ModeMenu current="trainer" onSelect={onSelect} /></div>);
    await userEvent.click(screen.getByRole('button', { name: 'Plus' }));
    await userEvent.click(screen.getByText('Ailleurs'));
    expect(screen.queryByRole('navigation', { name: 'Autres modes' })).not.toBeInTheDocument();
    expect(onSelect).not.toHaveBeenCalled();
  });
});
