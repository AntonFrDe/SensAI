import PlayingCard, { type CardData } from './PlayingCard';

const stages = [{ name: 'Flop', slots: [0, 1, 2] }, { name: 'Turn', slots: [3] }, { name: 'River', slots: [4] }];

export default function CommunityCards({ cards }: { cards: CardData[] }) {
  return (
    <div className="board" role="group" aria-label="Cartes communes">
      {stages.map(({ name, slots }) => (
        <div className="street" key={name} role="group" aria-label={name}>
          <div className="cards">{slots.map(slot => <PlayingCard key={slot} card={cards[slot]} />)}</div>
          <small>{name}</small>
        </div>
      ))}
    </div>
  );
}
