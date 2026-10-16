import type { PokerAction } from './ActionControls';

export type ShortcutResult = { type: 'play'; action: PokerAction } | { type: 'focus-amount' } | { type: 'all-in' } | null;
export const shortcutKeys: Partial<Record<PokerAction, string>> = { fold: 'F', check: 'C', call: 'C', bet: 'R', raise: 'R' };
export const shortcutHelp: [string, string][] = [
  ['F', 'Se coucher (fold)'],
  ['C', 'Checker ou suivre (check / call)'],
  ['R', 'Miser ou relancer avec le montant choisi, sinon aller au montant'],
  ['T', 'Préparer un tapis'],
  ['Entrée', 'Dans le champ du montant : miser ou relancer'],
];

export function isTypingTarget(target: EventTarget | null): boolean {
  if (!(target instanceof HTMLElement)) return false;
  return target.isContentEditable || ['INPUT', 'TEXTAREA', 'SELECT'].includes(target.tagName);
}

export function shortcutAction(key: string, allowed: PokerAction[], validAmount: boolean): ShortcutResult {
  const sizing = allowed.find(action => action === 'bet' || action === 'raise');
  switch (key.toLowerCase()) {
    case 'f':
      return allowed.includes('fold') ? { type: 'play', action: 'fold' } : null;
    case 'c':
      if (allowed.includes('check')) return { type: 'play', action: 'check' };
      return allowed.includes('call') ? { type: 'play', action: 'call' } : null;
    case 'r':
    case 'b':
      if (!sizing) return null;
      return validAmount ? { type: 'play', action: sizing } : { type: 'focus-amount' };
    case 't':
      return sizing ? { type: 'all-in' } : null;
    default:
      return null;
  }
}
