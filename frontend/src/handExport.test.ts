import { describe, expect, it } from 'vitest';
import { handToText, handsToJson, handsToText } from './handExport';
import type { PlayedHand } from './handLog';

const showdown: PlayedHand = {
  number: 2,
  playerCards: [{ rank: 'A', suit: 'spades' }, { rank: 'K', suit: 'spades' }],
  opponentCards: [{ rank: 'Q', suit: 'hearts' }, { rank: 'Q', suit: 'clubs' }],
  board: [
    { rank: 'K', suit: 'hearts' }, { rank: '7', suit: 'clubs' }, { rank: '2', suit: 'diamonds' },
    { rank: '9', suit: 'spades' }, { rank: '3', suit: 'hearts' },
  ],
  history: [
    { street: 'pre_flop', player: 'IA', action: 'call', amount: 10 },
    { street: 'pre_flop', player: 'Vous', action: 'raise', amount: 1000 },
    { street: 'pre_flop', player: 'IA', action: 'call', amount: 960 },
  ],
  awards: [{ amount: 2000, winners: ['Vous'], reason: 'showdown' }],
  playerHand: { rank: 'one_pair', cards: [] },
  opponentHand: { rank: 'one_pair', cards: [] },
  net: 1000,
  stackAfter: 2000,
};
const folded: PlayedHand = {
  ...showdown, number: 1, opponentCards: [], board: [], opponentHand: null, playerHand: null, net: -10, stackAfter: 990,
  history: [{ street: 'pre_flop', player: 'Vous', action: 'fold' }], awards: [{ amount: 30, winners: ['IA'], reason: 'fold' }],
};

function plain(text: string): string {
  return text.replace(/[\u00a0\u202f]/g, ' ');
}

describe('handToText', () => {
  it('writes an all-in hand street by street with the showdown', () => {
    expect(plain(handToText(showdown)).split('\n')).toEqual([
      'Main n°2',
      'Tes cartes : A♠ K♠',
      'Préflop : L’IA : Call 10 jetons ; Toi : Raise à 1 000 jetons ; L’IA : Call 960 jetons',
      'Flop [K♥ 7♣ 2♦] : pas d’action (tapis)',
      'Turn [K♥ 7♣ 2♦ 9♠] : pas d’action (tapis)',
      'River [K♥ 7♣ 2♦ 9♠ 3♥] : pas d’action (tapis)',
      'Abattage : l’IA montre Q♥ Q♣ (Paire) ; toi : Paire',
      'Résultat : tu gagnes 1 000 jetons (tapis : 2 000).',
    ]);
  });

  it('stops where a hand ended by a fold', () => {
    expect(plain(handToText(folded)).split('\n')).toEqual([
      'Main n°1', 'Tes cartes : A♠ K♠', 'Préflop : Toi : Fold', 'Résultat : tu perds 10 jetons (tapis : 990).',
    ]);
  });
});

describe('handsToText and handsToJson', () => {
  it('orders the hands and adds a header', () => {
    const text = handsToText([showdown, folded], new Date(2026, 9, 16, 12, 0));
    expect(text.split('\n')[0]).toMatch(/^SensAI Poker : historique exporté le 16\/10\/2026.* \(2 mains\)$/);
    expect(text.indexOf('Main n°1')).toBeLessThan(text.indexOf('Main n°2'));
    expect(JSON.parse(handsToJson([showdown, folded])).map((hand: PlayedHand) => hand.number)).toEqual([1, 2]);
  });

  it('says when the opponent cards were shown after a fold', () => {
    const text = handToText({ ...folded, opponentCards: showdown.opponentCards });
    expect(text).toContain('Cartes de l’IA (dévoilées pour l’entraînement) : Q♥ Q♣');
  });
});

