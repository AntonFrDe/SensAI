import { useState } from 'react';
import type { Stats } from './sessionStats';

export type SessionStatsProps = { session: Stats; lifetime: Stats; onResetLifetime: () => void };

const formatter = new Intl.NumberFormat('fr-FR');
const percent = new Intl.NumberFormat('fr-FR', { style: 'percent', maximumFractionDigits: 0 });

function signed(amount: number): string {
  return `${amount > 0 ? '+' : ''}${formatter.format(amount)} jetons`;
}

function streakText(streak: number): string {
  if (streak === 0) return '—';
  return streak > 0 ? `${streak} gagnée${streak > 1 ? 's' : ''}` : `${-streak} perdue${streak < -1 ? 's' : ''}`;
}

export default function SessionStats({ session, lifetime, onResetLifetime }: SessionStatsProps) {
  const [scope, setScope] = useState<'session' | 'lifetime'>('session');
  const [confirming, setConfirming] = useState(false);
  const stats = scope === 'session' ? session : lifetime;
  const rows: [string, string][] = [
    ['Mains jouées', formatter.format(stats.hands)],
    ['Gagnées / perdues / partagées', `${stats.won} / ${stats.lost} / ${stats.split}`],
    ['Taux de victoire', stats.hands ? percent.format(stats.won / stats.hands) : '—'],
    ['Abattages gagnés', `${stats.showdownsWon} sur ${stats.showdowns}`],
    ['Plus gros pot gagné', stats.biggestPotWon ? `${formatter.format(stats.biggestPotWon)} jetons` : '—'],
    ['Bilan', signed(stats.net)],
    ['Série en cours', streakText(stats.streak)],
    ['Meilleure série', stats.bestStreak ? `${stats.bestStreak} gagnée${stats.bestStreak > 1 ? 's' : ''}` : '—'],
  ];

  function reset() {
    if (!confirming) {
      setConfirming(true);
      return;
    }
    onResetLifetime();
    setConfirming(false);
  }

  return (
    <section className="stats" aria-label="Statistiques">
      <h3>Statistiques</h3>
      <div className="stats-scope" role="group" aria-label="Période">
        <button type="button" aria-pressed={scope === 'session'} onClick={() => setScope('session')}>Cette partie</button>
        <button type="button" aria-pressed={scope === 'lifetime'} onClick={() => { setScope('lifetime'); setConfirming(false); }}>
          Depuis toujours
        </button>
      </div>
      <dl>
        {rows.map(([label, value]) => (
          <div key={label} className={label === 'Bilan' ? `stat net ${stats.net < 0 ? 'down' : stats.net > 0 ? 'up' : ''}` : 'stat'}>
            <dt>{label}</dt>
            <dd>{value}</dd>
          </div>
        ))}
      </dl>
      {scope === 'lifetime' && <button type="button" className="link-button" onClick={reset}>
        {confirming ? 'Confirmer la remise à zéro' : 'Remettre à zéro'}
      </button>}
    </section>
  );
}
