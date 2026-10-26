import type { PokerAction } from './ActionControls';
import { phaseLabels, type GamePhase } from './HandInfo';
import { ACTION_NAMES } from './pokerTerms';

export type HistoryEntry = { street: GamePhase; player: string; action: PokerAction; amount?: number };
export type HandHistoryProps = { entries: HistoryEntry[] };

const formatter = new Intl.NumberFormat('fr-FR');

export function shortAction(entry: HistoryEntry): string {
  const label = entry.action === 'raise' ? `${ACTION_NAMES.raise} à` : ACTION_NAMES[entry.action];
  return entry.amount === undefined ? label : `${label} ${formatter.format(entry.amount)}`;
}

export function describeEntry(entry: HistoryEntry): string {
  const sentence = `${entry.player === 'Vous' ? 'Toi' : 'L’IA'} : ${shortAction(entry)}`;
  return entry.amount === undefined ? sentence : `${sentence} jetons`;
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
