import { handLabels } from './HandBadge';
import { describeEntry } from './HandHistory';
import { phaseLabels, type GamePhase } from './HandInfo';
import type { PlayedHand } from './handLog';
import type { CardData } from './PlayingCard';

const symbols = { clubs: '♣', diamonds: '♦', hearts: '♥', spades: '♠' };
const boardSize: Partial<Record<GamePhase, number>> = { flop: 3, turn: 4, river: 5 };
const formatter = new Intl.NumberFormat('fr-FR');

function cardsText(cards: CardData[]): string {
  return cards.map(card => `${card.rank}${symbols[card.suit]}`).join(' ');
}

function streetLine(hand: PlayedHand, street: GamePhase): string | null {
  const entries = hand.history.filter(entry => entry.street === street);
  const size = boardSize[street];
  if (entries.length === 0 && (size === undefined || hand.board.length < size)) return null;
  const board = size === undefined ? '' : ` [${cardsText(hand.board.slice(0, size))}]`;
  const actions = entries.length ? entries.map(describeEntry).join(' ; ') : 'pas d’action (tapis)';
  return `${phaseLabels[street]}${board} : ${actions}`;
}

export function handToText(hand: PlayedHand): string {
  const lines = [`Main n°${hand.number}`, `Vos cartes : ${cardsText(hand.playerCards)}`];
  for (const street of ['pre_flop', 'flop', 'turn', 'river'] as GamePhase[]) {
    const line = streetLine(hand, street);
    if (line) lines.push(line);
  }
  if (hand.opponentCards.length > 0) {
    const theirs = hand.opponentHand ? ` (${handLabels[hand.opponentHand.rank]})` : '';
    const yours = hand.playerHand ? ` ; vous : ${handLabels[hand.playerHand.rank]}` : '';
    const byFold = hand.awards.some(award => award.reason === 'fold');
    const intro = byFold ? 'Cartes de l’IA (dévoilées pour l’entraînement) :' : 'Abattage : l’IA montre';
    lines.push(`${intro} ${cardsText(hand.opponentCards)}${theirs}${yours}`);
  }
  const result = hand.net > 0 ? `vous gagnez ${formatter.format(hand.net)} jetons`
    : hand.net < 0 ? `vous perdez ${formatter.format(-hand.net)} jetons` : 'ni gain ni perte';
  lines.push(`Résultat : ${result} (tapis : ${formatter.format(hand.stackAfter)}).`);
  return lines.join('\n');
}

export function handsToText(hands: PlayedHand[], exportedAt = new Date()): string {
  const ordered = [...hands].sort((first, second) => first.number - second.number);
  const header = `SensAI Poker : historique exporté le ${exportedAt.toLocaleString('fr-FR')} (${ordered.length} main${ordered.length > 1 ? 's' : ''})`;
  return [header, ...ordered.map(handToText)].join('\n\n') + '\n';
}

export function handsToJson(hands: PlayedHand[]): string {
  return JSON.stringify([...hands].sort((first, second) => first.number - second.number), null, 2) + '\n';
}

export function download(filename: string, content: string, type: string): void {
  const url = URL.createObjectURL(new Blob([content], { type }));
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  link.click();
  URL.revokeObjectURL(url);
}
