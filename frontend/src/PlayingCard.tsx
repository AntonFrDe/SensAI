type Suit = 'clubs' | 'diamonds' | 'hearts' | 'spades';
export type CardData = { rank: '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | '10' | 'J' | 'Q' | 'K' | 'A'; suit: Suit };
const symbols = { clubs: '♣', diamonds: '♦', hearts: '♥', spades: '♠' };
const names = { clubs: 'trèfle', diamonds: 'carreau', hearts: 'cœur', spades: 'pique' };

export default function PlayingCard({ card, hidden = false }: { card?: CardData; hidden?: boolean }) {
  const red = !hidden && (card?.suit === 'hearts' || card?.suit === 'diamonds');
  const label = hidden ? 'Carte cachée' : card ? `${card.rank} de ${names[card.suit]}` : 'Carte non distribuée';
  return (
    <span className={`playing-card${red ? ' red' : ''}`} role="img" aria-label={label}>
      {hidden ? '🂠' : card ? `${card.rank}${symbols[card.suit]}` : '?'}
    </span>
  );
}
