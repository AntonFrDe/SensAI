import ChipAmount from './ChipAmount';

export type HistoryEntry = { player: string; action: string; amount?: number; target_amount?: number };
export default function HandHistory({ entries }: { entries: HistoryEntry[] }) {
  return (
    <details>
      <summary>Historique des actions ({entries.length})</summary>
      {entries.length === 0 ? <p>Aucune action pour cette main.</p> : <ol>
        {entries.map((entry, index) => <li key={index}>{entry.player} : {entry.action}{entry.amount !== undefined && <> — <ChipAmount amount={entry.target_amount ?? entry.amount} /></>}</li>)}
      </ol>}
    </details>
  );
}
