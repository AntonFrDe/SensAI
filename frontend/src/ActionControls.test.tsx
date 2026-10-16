import { fireEvent, render, screen } from '@testing-library/react';
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

  it('shows the amount to call on the call button', () => {
    render(<ActionControls allowedActions={['fold', 'call', 'raise']} toCall={10} minAmount={40} maxAmount={1000} onAction={vi.fn()} />);
    expect(screen.getByRole('button', { name: 'Call 10' })).toBeEnabled();
  });

  it('fills the amount from a pot preset and plays it', async () => {
    const onAction = vi.fn();
    render(<ActionControls allowedActions={['fold', 'check', 'bet']} toCall={0} pot={80} currentBet={0}
      minAmount={20} maxAmount={980} onAction={onAction} />);
    await userEvent.click(screen.getByRole('button', { name: /^½ pot/ }));
    expect(screen.getByRole('spinbutton')).toHaveValue(40);
    expect(screen.getByRole('button', { name: /^½ pot/ })).toHaveAttribute('aria-pressed', 'true');
    await userEvent.click(screen.getByRole('button', { name: 'Bet 40' }));
    expect(onAction).toHaveBeenCalledWith('bet', 40);
  });

  it('names an all-in raise', async () => {
    render(<ActionControls allowedActions={['fold', 'call', 'raise']} toCall={10} pot={30} currentBet={20}
      minAmount={40} maxAmount={1000} onAction={vi.fn()} />);
    await userEvent.click(screen.getByRole('button', { name: /^Tapis/ }));
    expect(screen.getByRole('button', { name: /^Raise tapis \(1\s000\)$/ })).toBeEnabled();
  });

  it('moves the amount with the slider', () => {
    render(<ActionControls allowedActions={['fold', 'check', 'bet']} minAmount={20} maxAmount={980} onAction={vi.fn()} />);
    fireEvent.change(screen.getByRole('slider', { name: 'Curseur du montant' }), { target: { value: '300' } });
    expect(screen.getByRole('spinbutton')).toHaveValue(300);
    expect(screen.getByRole('button', { name: /^Bet 300/ })).toBeEnabled();
  });

  it('clears the amount when the bounds change on a new turn', async () => {
    const { rerender } = render(<ActionControls allowedActions={['fold', 'check', 'bet']} minAmount={20} maxAmount={980} onAction={vi.fn()} />);
    await userEvent.type(screen.getByRole('spinbutton'), '500');
    rerender(<ActionControls allowedActions={['fold', 'call', 'raise']} minAmount={1000} maxAmount={1500} onAction={vi.fn()} />);
    expect(screen.getByRole('spinbutton')).toHaveValue(null);
  });

  it('hides the sizing helpers when betting is impossible', () => {
    render(<ActionControls allowedActions={['fold', 'call']} toCall={500} onAction={vi.fn()} />);
    expect(screen.queryByRole('slider')).not.toBeInTheDocument();
    expect(screen.queryByRole('group', { name: 'Montants rapides' })).not.toBeInTheDocument();
  });

  it('plays with the keyboard shortcuts', async () => {
    const onAction = vi.fn();
    render(<ActionControls allowedActions={['fold', 'call', 'raise']} toCall={10} minAmount={40} maxAmount={1000} onAction={onAction} />);
    await userEvent.keyboard('c');
    expect(onAction).toHaveBeenLastCalledWith('call', undefined);
    await userEvent.keyboard('f');
    expect(onAction).toHaveBeenLastCalledWith('fold', undefined);
    expect(screen.getByRole('button', { name: 'Fold' })).toHaveAttribute('aria-keyshortcuts', 'F');
  });

  it('moves to the amount, prepares an all-in and raises with Enter', async () => {
    const onAction = vi.fn();
    render(<ActionControls allowedActions={['fold', 'call', 'raise']} toCall={10} minAmount={40} maxAmount={1000} onAction={onAction} />);
    await userEvent.keyboard('r');
    const amount = screen.getByRole('spinbutton');
    expect(amount).toHaveFocus();
    expect(onAction).not.toHaveBeenCalled();
    await userEvent.type(amount, 'f150{Enter}');
    expect(onAction).toHaveBeenCalledOnce();
    expect(onAction).toHaveBeenCalledWith('raise', 150);
    amount.blur();
    await userEvent.keyboard('t');
    expect(amount).toHaveValue(1000);
    await userEvent.keyboard('r');
    expect(onAction).toHaveBeenLastCalledWith('raise', 1000);
  });

  it('ignores shortcuts without a legal action or while typing elsewhere', async () => {
    const onAction = vi.fn();
    render(<>
      <input aria-label="Question" />
      <ActionControls allowedActions={['fold', 'check']} onAction={onAction} />
    </>);
    await userEvent.type(screen.getByRole('textbox', { name: 'Question' }), 'fc');
    await userEvent.click(document.body);
    await userEvent.keyboard('r');
    expect(onAction).not.toHaveBeenCalled();
  });
});

