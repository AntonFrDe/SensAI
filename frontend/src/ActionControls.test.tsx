import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it, vi } from 'vitest';
import ActionControls from './ActionControls';

describe('ActionControls', () => {
  it('only enables the legal actions', () => {
    render(<ActionControls allowedActions={['fold', 'call']} onAction={vi.fn()} />);
    expect(screen.getByRole('button', { name: 'Fold' })).toBeEnabled();
    expect(screen.getByRole('button', { name: 'Call' })).toBeEnabled();
    expect(screen.getByRole('button', { name: 'Check' })).toBeDisabled();
    expect(screen.getByRole('spinbutton')).toBeDisabled();
  });

  it('sends a simple action without an amount', async () => {
    const onAction = vi.fn();
    render(<ActionControls allowedActions={['fold', 'check']} onAction={onAction} />);
    await userEvent.click(screen.getByRole('button', { name: 'Check' }));
    expect(onAction).toHaveBeenCalledWith('check', undefined);
  });

  it('accepts a raise only inside the bounds given by the server', async () => {
    const onAction = vi.fn();
    render(<ActionControls allowedActions={['fold', 'call', 'raise']} minAmount={40} maxAmount={1000} onAction={onAction} />);
    const amount = screen.getByRole('spinbutton');
    const raise = screen.getByRole('button', { name: 'Raise' });
    await userEvent.type(amount, '30');
    expect(raise).toBeDisabled();
    await userEvent.clear(amount);
    await userEvent.type(amount, '1001');
    expect(raise).toBeDisabled();
    await userEvent.clear(amount);
    await userEvent.type(amount, '120');
    await userEvent.click(raise);
    expect(onAction).toHaveBeenCalledWith('raise', 120);
  });

  it('disables everything while no handler is available', () => {
    render(<ActionControls allowedActions={['fold', 'check']} />);
    expect(screen.getByRole('button', { name: 'Fold' })).toBeDisabled();
  });
});
