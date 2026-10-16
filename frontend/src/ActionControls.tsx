import { useState } from 'react';
import { betPresets } from './betSizing';

export type PokerAction = 'fold' | 'check' | 'call' | 'bet' | 'raise';
export type ActionControlsProps = {
  allowedActions?: PokerAction[];
  onAction?: (action: PokerAction, amount?: number) => void;
  minAmount?: number;
  maxAmount?: number;
  toCall?: number;
  pot?: number;
  currentBet?: number;
};
const actions: PokerAction[] = ['fold', 'check', 'call', 'bet', 'raise'];
const formatter = new Intl.NumberFormat('fr-FR');

function actionLabel(action: PokerAction, amount: number | undefined, allIn: boolean): string {
  const name = action[0].toUpperCase() + action.slice(1);
  if (amount === undefined) return name;
  if (allIn) return `${name} tapis (${formatter.format(amount)})`;
  return action === 'raise' ? `${name} à ${formatter.format(amount)}` : `${name} ${formatter.format(amount)}`;
}

export default function ActionControls({
  allowedActions = [], onAction, minAmount = 1, maxAmount, toCall, pot = 0, currentBet = 0,
}: ActionControlsProps) {
  const [amount, setAmount] = useState('');
  const bounds = `${minAmount}-${maxAmount}`;
  const [shownBounds, setShownBounds] = useState(bounds);
  if (shownBounds !== bounds) {
    setShownBounds(bounds);
    setAmount('');
  }
  const value = Number(amount);
  const validAmount = amount !== '' && Number.isSafeInteger(value) && value >= minAmount && maxAmount !== undefined && value <= maxAmount;
  const canSize = Boolean(onAction) && allowedActions.some(action => action === 'bet' || action === 'raise') && maxAmount !== undefined;
  const presets = canSize && maxAmount !== undefined
    ? betPresets({ pot, toCall: toCall ?? 0, currentBet, minAmount, maxAmount }) : [];

  function amountOf(action: PokerAction): number | undefined {
    if (action === 'call') return toCall;
    if (action === 'bet' || action === 'raise') return validAmount ? value : undefined;
    return undefined;
  }

  return (
    <div className="actions" role="group" aria-label="Actions du joueur">
      <div className="bet-sizing">
        <label>Montant total (Bet / Raise)
          <input type="number" min={minAmount} max={maxAmount} step="1" value={amount}
            disabled={!canSize} onChange={event => setAmount(event.target.value)} />
        </label>
        {canSize && <input type="range" aria-label="Curseur du montant" min={minAmount} max={maxAmount} step="1"
          value={validAmount ? value : minAmount} onChange={event => setAmount(event.target.value)} />}
        {presets.length > 0 && <div className="bet-presets" role="group" aria-label="Montants rapides">
          {presets.map(preset => (
            <button key={preset.label} type="button" className="preset" aria-pressed={validAmount && value === preset.amount}
              onClick={() => setAmount(String(preset.amount))}>
              {preset.label} <small>{formatter.format(preset.amount)}</small>
            </button>
          ))}
        </div>}
      </div>
      {actions.map(action => {
        const shown = allowedActions.includes(action) ? amountOf(action) : undefined;
        return (
          <button key={action} type="button" className={`action ${action}`}
            disabled={!onAction || !allowedActions.includes(action) || ((action === 'bet' || action === 'raise') && !validAmount)}
            onClick={() => onAction?.(action, action === 'bet' || action === 'raise' ? value : undefined)}>
            {actionLabel(action, shown, shown !== undefined && action !== 'call' && shown === maxAmount)}
          </button>
        );
      })}
    </div>
  );
}
