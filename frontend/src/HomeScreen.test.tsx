import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it, vi } from 'vitest';
import HomeScreen from './HomeScreen';
import { defaultTableOptions } from './api';

describe('HomeScreen', () => {
  it('starts with the given options', async () => {
    const onPlay = vi.fn();
    render(<HomeScreen options={defaultTableOptions} busy={false} onPlay={onPlay} />);
    expect(screen.getByRole('radio', { name: '10/20' })).toBeChecked();
    expect(screen.getByText(/^Chaque joueur commence avec 1\s000 jetons\.$/)).toBeInTheDocument();
    await userEvent.click(screen.getByRole('button', { name: 'Jouer' }));
    expect(onPlay).toHaveBeenCalledWith({ blinds: '10/20', stackBigBlinds: 50, revealAtEnd: false });
  });

  it('plays with the chosen blinds and stack depth', async () => {
    const onPlay = vi.fn();
    render(<HomeScreen options={defaultTableOptions} busy={false} onPlay={onPlay} />);
    await userEvent.click(screen.getByRole('radio', { name: '25/50' }));
    await userEvent.click(screen.getByRole('button', { name: /^Profond/ }));
    expect(screen.getByRole('button', { name: /^Profond/ })).toHaveAttribute('aria-pressed', 'true');
    expect(screen.getByText(/^Chaque joueur commence avec 5\s000 jetons\.$/)).toBeInTheDocument();
    await userEvent.click(screen.getByRole('button', { name: 'Jouer' }));
    expect(onPlay).toHaveBeenCalledWith({ blinds: '25/50', stackBigBlinds: 100, revealAtEnd: false });
  });

  it('refuses a stack outside the allowed range', async () => {
    const onPlay = vi.fn();
    render(<HomeScreen options={defaultTableOptions} busy={false} onPlay={onPlay} />);
    const depth = screen.getByRole('spinbutton', { name: /En grosses blindes/ });
    await userEvent.clear(depth);
    await userEvent.type(depth, '1000');
    expect(depth).toHaveAttribute('aria-invalid', 'true');
    expect(screen.getByText('Choisissez entre 20 et 500 grosses blindes.')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Jouer' })).toBeDisabled();
  });

  it('waits while a game is dealt', () => {
    render(<HomeScreen options={defaultTableOptions} busy onPlay={vi.fn()} />);
    expect(screen.getByRole('button', { name: 'Distribution…' })).toBeDisabled();
  });

  it('turns on the training reveal of the opponent cards', async () => {
    const onPlay = vi.fn();
    render(<HomeScreen options={defaultTableOptions} busy={false} onPlay={onPlay} />);
    await userEvent.click(screen.getByRole('checkbox', { name: /Montrer les cartes de l’IA/ }));
    await userEvent.click(screen.getByRole('button', { name: 'Jouer' }));
    expect(onPlay).toHaveBeenCalledWith({ blinds: '10/20', stackBigBlinds: 50, revealAtEnd: true });
  });
});
