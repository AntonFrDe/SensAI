import { useState } from 'react';

export type PokerAction = 'fold' | 'check' | 'call' | 'bet' | 'raise';
type Props = {
  allowedActions?: PokerAction[];
  onAction?: (action: PokerAction, amount?: number) => void;
  minAmount?: number;
  maxAmount?: number;
};
const actions: PokerAction[] = ['fold', 'check', 'call', 'bet', 'raise'];

export default function ActionControls({ allowedActions = [], onAction, minAmount = 1, maxAmount }: Props) {
  const [amount, setAmount] = useState('');
  const value = Number(amount);
  const validAmount = Number.isSafeInteger(value) && value >= minAmount && maxAmount !== undefined && value <= maxAmount;
  return (
    <div className="actions" role="group" aria-label="Actions du joueur">
      <label>Montant total (Bet / Raise)
        <input type="number" min={minAmount} max={maxAmount} step="1" value={amount}
          disabled={!onAction || !allowedActions.some(action => action === 'bet' || action === 'raise')}
          onChange={event => setAmount(event.target.value)} />
      </label>
      {actions.map(action => (
        <button key={action} type="button"
          disabled={!onAction || !allowedActions.includes(action) || ((action === 'bet' || action === 'raise') && !validAmount)}
          onClick={() => onAction?.(action, action === 'bet' || action === 'raise' ? value : undefined)}>
          {action[0].toUpperCase() + action.slice(1)}
        </button>
      ))}
    </div>
  );
}
