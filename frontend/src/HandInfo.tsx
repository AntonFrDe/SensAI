import ChipAmount from './ChipAmount';

export const phaseLabels = { pre_flop: 'Préflop', flop: 'Flop', turn: 'Turn', river: 'River', showdown: 'Abattage' };
export type GamePhase = keyof typeof phaseLabels;

export default function HandInfo({ phase, currentBet }: { phase?: GamePhase; currentBet?: number }) {
  return (
    <div className="chip-info" role="group" aria-label="Informations de la main">
      <p aria-live="polite">Phase : {phase ? phaseLabels[phase] : '—'}</p>
      <p>Mise actuelle : <ChipAmount amount={currentBet} /></p>
    </div>
  );
}
