import PlayingCard, { type CardData } from './PlayingCard';
import { sameCard } from './HandBadge';
import Term from './Term';

const stages = [{ name: 'Flop', slots: [0, 1, 2] }, { name: 'Turn', slots: [3] }, { name: 'River', slots: [4] }];

export type CommunityCardsProps = { cards: CardData[]; highlighted?: CardData[] };

export default function CommunityCards({ cards, highlighted = [] }: CommunityCardsProps) {
  return (
    <div className="board" role="group" aria-label="Cartes communes">
      {stages.map(({ name, slots }) => (
        <div className="street" key={name} role="group" aria-label={name}>
          <div className="cards">{slots.map(slot => {
            const card = cards[slot];
            return <PlayingCard key={card ? `${card.rank}${card.suit}` : `slot-${slot}`} card={card} highlighted={card !== undefined && highlighted.some(best => sameCard(best, card))} />;
          })}</div>
          <small><Term term={name}>{name}</Term></small>
        </div>
      ))}
    </div>
  );
}
