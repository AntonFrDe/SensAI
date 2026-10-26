import type { PokerAction } from './ActionControls';
import { phaseLabels, type GamePhase } from './HandInfo';

export type HistoryEntry = { street: GamePhase; player: string; action: PokerAction; amount?: number };
export type HandHistoryProps = { entries: HistoryEntry[] };

const verbs = {
  ai: { fold: 'se couche', check: 'checke', call: 'suit', bet: 'mise', raise: 'relance à' },
  you: { fold: 'te couches', check: 'checkes', call: 'suis', bet: 'mises', raise: 'relances à' },
};

const formatter = new Intl.NumberFormat('fr-FR');

const shortLabels = { fold: 'Couché', check: 'Check', call: 'Suit', bet: 'Mise', raise: 'Relance à' };

export function shortAction(entry: HistoryEntry): string {
  const label = shortLabels[entry.action];
  return entry.amount === undefined ? label : `${label} ${formatter.format(entry.amount)}`;
}

export function describeEntry(entry: HistoryEntry): string {
  const sentence = entry.player === 'Vous' ? `Tu ${verbs.you[entry.action]}` : `L’IA ${verbs.ai[entry.action]}`;
  return entry.amount === undefined ? sentence : `${sentence} ${formatter.format(entry.amount)} jetons`;
}

export default function HandHistory({ entries }: HandHistoryProps) {
  const streets = entries.reduce<{ street: GamePhase; entries: HistoryEntry[] }[]>((groups, entry) => {
    const last = groups[groups.length - 1];
    if (last?.street === entry.street) last.entries.push(entry);
    else groups.push({ street: entry.street, entries: [entry] });
    return groups;
  }, []);
  return (
    <details className="hand-history">
      <summary>Historique de la main ({entries.length})</summary>
      {streets.length === 0 ? <p>Aucune action pour cette main.</p> : streets.map(group => (
        <section key={group.street} aria-label={phaseLabels[group.street]}>
          <h3>{phaseLabels[group.street]}</h3>
          <ol>
            {group.entries.map((entry, index) => <li key={index}>{describeEntry(entry)}</li>)}
          </ol>
        </section>
      ))}
    </details>
  );
}
