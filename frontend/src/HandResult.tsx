import ChipAmount from './ChipAmount';

export type PotAward = { winners: string[]; amount: number };
export default function HandResult({ awards }: { awards: PotAward[] }) {
  return (
    <section className="chip-info" aria-label="Résultat de la main" role="status">
      <h2>Main terminée</h2>
      <ul>
        {awards.map((award, index) => <li key={index}>{award.winners.join(' et ')} {award.winners.length > 1 ? 'se partagent' : 'remporte'} un pot de <ChipAmount amount={award.amount} />.</li>)}
      </ul>
    </section>
  );
}
