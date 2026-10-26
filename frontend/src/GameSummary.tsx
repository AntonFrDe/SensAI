import { handLabels, type HandRank } from './HandBadge';
import StackChart from './StackChart';
import { stackHistory, type PlayedHand } from './handLog';

export type GameSummaryProps = { hands: PlayedHand[]; playerWon: boolean };

const ranks = Object.keys(handLabels) as HandRank[];
const formatter = new Intl.NumberFormat('fr-FR');

export function summarize(hands: PlayedHand[]) {
  const won = hands.filter(hand => hand.awards.some(award => award.winners.includes('Vous') && award.winners.length === 1));
  const biggestPot = Math.max(0, ...won.flatMap(hand => hand.awards.filter(award => award.winners.includes('Vous')).map(award => award.amount)));
  const shown = won.filter(hand => hand.playerHand && hand.awards.some(award => award.reason === 'showdown'));
  const best = shown.reduce<HandRank | null>((top, hand) => {
    const rank = hand.playerHand?.rank ?? null;
    return rank && (!top || ranks.indexOf(rank) > ranks.indexOf(top)) ? rank : top;
  }, null);
  return { played: hands.length, won: won.length, biggestPot, best };
}

export default function GameSummary({ hands, playerWon }: GameSummaryProps) {
  const { played, won, biggestPot, best } = summarize(hands);
  return (
    <section className={`game-summary ${playerWon ? 'victory' : 'defeat'}`} aria-label="Bilan de la partie">
      <h3>{playerWon ? 'Victoire : l’IA n’a plus de jetons.' : 'Défaite : tu n’as plus de jetons.'}</h3>
      <dl className="summary-figures">
        <div><dt>Mains jouées</dt><dd>{played}</dd></div>
        <div><dt>Mains gagnées</dt><dd>{won}</dd></div>
        <div><dt>Plus gros pot gagné</dt><dd>{biggestPot ? `${formatter.format(biggestPot)} jetons` : '—'}</dd></div>
        <div><dt>Meilleure main gagnante</dt><dd>{best ? handLabels[best] : '—'}</dd></div>
      </dl>
      <StackChart points={stackHistory(hands)} title="Ton tapis main après main" />
    </section>
  );
}
