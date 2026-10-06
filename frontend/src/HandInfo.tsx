import ChipAmount from './ChipAmount';

const phases = { pre_flop: 'Préflop', flop: 'Flop', turn: 'Turn', river: 'River', showdown: 'Abattage' };
export type GamePhase = keyof typeof phases;

export default function HandInfo({ phase, currentBet }: { phase?: GamePhase; currentBet?: number }) {
  return (
    <div className="chip-info" role="group" aria-label="Informations de la main">
      <p aria-live="polite">Phase : {phase ? phases[phase] : '—'}</p>
      <p>Mise actuelle : <ChipAmount amount={currentBet} /></p>
    </div>
  );
}
