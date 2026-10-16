import type { CardData } from './PlayingCard';

export const handLabels = {
  high_card: 'Carte haute',
  one_pair: 'Paire',
  two_pair: 'Double paire',
  three_of_a_kind: 'Brelan',
  straight: 'Quinte',
  flush: 'Couleur',
  full_house: 'Full',
  four_of_a_kind: 'Carré',
  straight_flush: 'Quinte flush',
};
export type HandRank = keyof typeof handLabels;
export type BestHand = { rank: HandRank; cards: CardData[] };
export type HandBadgeProps = { hand?: BestHand | null; owner: string };

export function sameCard(first: CardData, second: CardData): boolean {
  return first.rank === second.rank && first.suit === second.suit;
}

export default function HandBadge({ hand, owner }: HandBadgeProps) {
  if (!hand) return null;
  return (
    <p className={`hand-badge rank-${hand.rank}`} aria-label={`${owner} : ${handLabels[hand.rank]}`}>
      {handLabels[hand.rank]}
    </p>
  );
}
