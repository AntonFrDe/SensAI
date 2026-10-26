import type { PokerAction } from './ActionControls';

export const ACTION_NAMES: Record<PokerAction, string> = { fold: 'Fold', check: 'Check', call: 'Call', bet: 'Bet', raise: 'Raise' };

export function isPokerAction(key: string): key is PokerAction {
  return key in ACTION_NAMES;
}
