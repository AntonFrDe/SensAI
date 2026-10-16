import { fireEvent, render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import GuidedTour, { tourDoneKey, tourSteps } from './GuidedTour';

describe('GuidedTour', () => {
  beforeEach(() => localStorage.clear());

  it('walks through the steps, highlights each zone and remembers the end', async () => {
    document.body.innerHTML = '<div class="seat-box bottom"></div><div class="actions"></div>';
    const onClose = vi.fn();
    render(<GuidedTour onClose={onClose} />);
    expect(screen.getByRole('dialog', { name: tourSteps[0].title })).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: tourSteps[0].title })).toHaveFocus();
    expect(document.querySelector('.seat-box')).toHaveClass('tour-target');

    await userEvent.click(screen.getByRole('button', { name: 'Suivant' }));
    expect(screen.getByText('Étape 2 sur 4')).toBeInTheDocument();
    expect(document.querySelector('.seat-box')).not.toHaveClass('tour-target');
    expect(document.querySelector('.actions')).toHaveClass('tour-target');

    await userEvent.click(screen.getByRole('button', { name: 'Suivant' }));
    await userEvent.click(screen.getByRole('button', { name: 'Suivant' }));
    await userEvent.click(screen.getByRole('button', { name: 'Terminer' }));
    expect(onClose).toHaveBeenCalledOnce();
    expect(localStorage.getItem(tourDoneKey)).toBe('true');
  });

  it('can be skipped or closed with Escape', async () => {
    const onClose = vi.fn();
    render(<GuidedTour onClose={onClose} />);
    expect(screen.getByRole('button', { name: 'Précédent' })).toBeDisabled();
    fireEvent.keyDown(screen.getByRole('dialog'), { key: 'Escape' });
    await userEvent.click(screen.getByRole('button', { name: 'Passer la visite' }));
    expect(onClose).toHaveBeenCalledTimes(2);
    expect(localStorage.getItem(tourDoneKey)).toBe('true');
  });
});
