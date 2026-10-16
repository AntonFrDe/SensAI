import { useState } from 'react';
import type { GameRecord } from './gameRecords';

export type GameRecordsProps = { records: GameRecord[]; onClear: () => void; onBack: () => void };

const results = { playing: 'En cours', won: 'Victoire', lost: 'Défaite' };
const formatter = new Intl.NumberFormat('fr-FR');
const dates = new Intl.DateTimeFormat('fr-FR', { dateStyle: 'short', timeStyle: 'short' });

function dateText(iso: string): string {
  const parsed = new Date(iso);
  return Number.isNaN(parsed.getTime()) ? '—' : dates.format(parsed);
}

export default function GameRecords({ records, onClear, onBack }: GameRecordsProps) {
  const [confirming, setConfirming] = useState(false);
  const finished = records.filter(record => record.result !== 'playing');
  const victories = finished.filter(record => record.result === 'won').length;

  function clear() {
    if (confirming) onClear();
    setConfirming(!confirming);
  }

  return (
    <section className="game-records" aria-label="Mes parties">
      <h2>Mes parties</h2>
      <button type="button" onClick={onBack}>← Accueil</button>
      {records.length === 0 ? <p>Aucune partie enregistrée : elles apparaissent ici dès la première main jouée.</p> : <>
        <p>{finished.length} partie{finished.length > 1 ? 's' : ''} terminée{finished.length > 1 ? 's' : ''}, {victories} victoire{victories > 1 ? 's' : ''}.</p>
        <table>
          <thead>
            <tr><th scope="col">Début</th><th scope="col">Blindes</th><th scope="col">Mains</th><th scope="col">Gagnées</th><th scope="col">Bilan</th><th scope="col">Résultat</th></tr>
          </thead>
          <tbody>
            {records.map(record => (
              <tr key={record.gameId}>
                <td>{dateText(record.startedAt)}</td>
                <td>{record.blinds}</td>
                <td>{record.hands}</td>
                <td>{record.won}</td>
                <td className={record.net > 0 ? 'up' : record.net < 0 ? 'down' : undefined}>{record.net > 0 ? '+' : ''}{formatter.format(record.net)}</td>
                <td>{results[record.result]}</td>
              </tr>
            ))}
          </tbody>
        </table>
        <button type="button" className="link-button" onClick={clear}>
          {confirming ? 'Confirmer l’effacement' : 'Effacer l’historique'}
        </button>
      </>}
    </section>
  );
}
