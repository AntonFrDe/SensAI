type Suit = 'clubs' | 'diamonds' | 'hearts' | 'spades';
export type CardData = { rank: '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | '10' | 'J' | 'Q' | 'K' | 'A'; suit: Suit };
const symbols = { clubs: '♣', diamonds: '♦', hearts: '♥', spades: '♠' };
const names = { clubs: 'trèfle', diamonds: 'carreau', hearts: 'cœur', spades: 'pique' };

export type PlayingCardProps = { card?: CardData; highlighted?: boolean };

export default function PlayingCard({ card, highlighted = false }: PlayingCardProps) {
  const red = card?.suit === 'hearts' || card?.suit === 'diamonds';
  const label = card ? `${card.rank} de ${names[card.suit]}${highlighted ? ', dans la meilleure main' : ''}` : 'Carte non distribuée';
  return (
    <span className={`playing-card${red ? ' red' : ''}${card ? ` suit-${card.suit}` : ''}${highlighted ? ' best' : ''}`} role="img" aria-label={label}>
      {card ? `${card.rank}${symbols[card.suit]}` : '?'}
    </span>
  );
}
