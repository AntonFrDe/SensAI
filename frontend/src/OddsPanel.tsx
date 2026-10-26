import { useEffect, useState } from 'react';
import { fetchOdds, type OddsSummary } from './api';

export type OddsPanelProps = { gameId: string; available: boolean };

const autoKey = 'sensai-odds-auto';
const percent = new Intl.NumberFormat('fr-FR', { style: 'percent', maximumFractionDigits: 0 });
const formatter = new Intl.NumberFormat('fr-FR');

function verdict({ potOdds, equity }: OddsSummary): string {
  if (potOdds === null) return 'Rien à payer : tu peux checker sans risque.';
  return equity.share >= potOdds
    ? 'Suivre est rentable à long terme contre une main au hasard.'
    : 'Suivre coûte plus que ce que la main rapporte en moyenne contre une main au hasard.';
}

export default function OddsPanel({ gameId, available }: OddsPanelProps) {
  const [auto, setAuto] = useState(() => localStorage.getItem(autoKey) === 'true');
  const [odds, setOdds] = useState<OddsSummary | null>(null);
  const [status, setStatus] = useState<'idle' | 'loading' | 'error'>('idle');
  const [error, setError] = useState('');

  async function load() {
    setStatus('loading');
    setError('');
    try {
      setOdds(await fetchOdds(gameId));
      setStatus('idle');
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : 'Calcul des repères impossible.');
      setStatus('error');
    }
  }

  useEffect(() => {
    if (auto && available && !odds) void load();
  }, [auto, available]);

  function toggleAuto(checked: boolean) {
    setAuto(checked);
    localStorage.setItem(autoKey, String(checked));
  }

  return (
    <section className="odds" aria-label="Repères chiffrés">
      <h3>Repères</h3>
      {!odds && <p>{available ? 'Cote du pot, équité et outs calculés par le code.' : 'Les repères se calculent à ton tour.'}</p>}
      {odds && <div className="odds-figures" aria-live="polite">
        <p>{odds.toCall > 0
          ? `À payer : ${formatter.format(odds.toCall)} jetons pour un pot de ${formatter.format(odds.pot)}.`
          : `Pot de ${formatter.format(odds.pot)} jetons, rien à payer.`}</p>
        {odds.potOdds !== null && <p>Cote du pot : il faut <strong>{percent.format(odds.potOdds)}</strong> d’équité pour suivre.</p>}
        <div className="meter" role="meter" aria-label="Équité" aria-valuemin={0} aria-valuemax={100}
          aria-valuenow={Math.round(odds.equity.share * 100)} aria-valuetext={percent.format(odds.equity.share)}>
          <span className="meter-fill" style={{ width: `${odds.equity.share * 100}%` }} />
          {odds.potOdds !== null && <span className="meter-mark" style={{ left: `${odds.potOdds * 100}%` }} />}
        </div>
        <p>Équité : <strong>{percent.format(odds.equity.share)}</strong> contre une main au hasard
          {odds.equity.exact ? ' (calcul exact).' : ' (estimation sur 3 000 tirages).'}</p>
        <p className="odds-verdict">{verdict(odds)}</p>
        {odds.outs && <p>
          {odds.outs.count} out{odds.outs.count > 1 ? 's' : ''}
          {odds.outs.count > 0 && ` (${Object.entries(odds.outs.byHand).map(([name, count]) => `${name} ${count}`).join(', ')})`}
          {` : ${percent.format(odds.outs.nextCard)} à la prochaine carte`}
          {odds.outs.byRiver !== null && `, ${percent.format(odds.outs.byRiver)} d’ici la river`}.
        </p>}
      </div>}
      {error && <p className="coach-error" role="alert">{error}</p>}
      <div className="odds-actions">
        <button type="button" disabled={!available || status === 'loading'} onClick={() => void load()}>
          {status === 'loading' ? 'Calcul…' : odds ? 'Recalculer' : 'Afficher mes repères'}
        </button>
        <label className="auto-toggle">
          <input type="checkbox" checked={auto} onChange={event => toggleAuto(event.target.checked)} /> À chaque décision
        </label>
      </div>
    </section>
  );
}
