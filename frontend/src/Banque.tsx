import { useEffect, useState, type FormEvent } from 'react';
import { fetchBanque, genererSituation, toCard, type Niveau, type Situation, type Theme } from './api';
import type { PokerAction } from './ActionControls';
import CommunityCards from './CommunityCards';
import PlayingCard from './PlayingCard';

const themes: Record<Theme, string> = { ouverture: 'Ouverture avant le flop', tirage: 'Suivre un tirage' };
const niveaux: Record<Niveau, string> = { debutant: 'Débutant', intermediaire: 'Intermédiaire', avance: 'Avancé' };
const actionLabels: Record<PokerAction, string> = {
  fold: 'Se coucher', check: 'Checker', call: 'Suivre', bet: 'Miser', raise: 'Relancer',
};
const formatter = new Intl.NumberFormat('fr-FR');

function Source({ situation }: { situation: Situation }) {
  if (situation.source !== 'llm') return <span className="badge repli">Repli : tirée par le code</span>;
  if (situation.tentatives === 1) return <span className="badge llm">LLM, 1er essai</span>;
  return <span className="badge retry">LLM après {situation.tentatives} essais</span>;
}

function verdict(situation: Situation, action: PokerAction): { icon: string; text: string; className: string } {
  if (situation.reference.bonnes.includes(action)) return { icon: '✅', text: 'bon', className: 'bon' };
  if (situation.reference.acceptables.includes(action)) return { icon: '🟡', text: 'acceptable', className: 'acceptable' };
  return { icon: '❌', text: 'erreur', className: 'erreur' };
}

function SituationCard({ situation }: { situation: Situation }) {
  return (
    <article className="situation" aria-label={`Situation : ${themes[situation.theme]}, ${niveaux[situation.niveau]}`}>
      <div className="badges">
        <span className="badge">{themes[situation.theme]}</span>
        <span className="badge">{niveaux[situation.niveau]}</span>
        <span className="badge">{situation.position}</span>
        <Source situation={situation} />
      </div>
      <div className="mini-table">
        <div className="cards" role="group" aria-label="Vos cartes privées">
          {situation.cartes.map(code => <PlayingCard key={code} card={toCard(code)} />)}
        </div>
        {situation.board.length > 0 && <CommunityCards cards={situation.board.map(toCard)} />}
        <p className="chip-info">Pot : {formatter.format(situation.pot)} bb · À payer : {formatter.format(situation.a_payer)} bb</p>
      </div>
      <p className="historique">{situation.historique}</p>
      <div>
        <h3>Référence</h3>
        <ul className="verdicts">
          {situation.actions.map(action => {
            const { icon, text, className } = verdict(situation, action);
            return <li key={action} className={className}>
              <span aria-hidden="true">{icon}</span> {actionLabels[action]} : {text}
            </li>;
          })}
        </ul>
        <ul className="faits">
          {situation.reference.faits.map(fait => <li key={fait}>{fait}</li>)}
        </ul>
      </div>
      {situation.erreurs.length > 0 && <details>
        <summary>Essais refusés ({situation.erreurs.length})</summary>
        <ol>
          {situation.erreurs.map((messages, index) => <li key={index}>Essai {index + 1} : {messages.join(' ; ')}</li>)}
        </ol>
      </details>}
    </article>
  );
}

export default function Banque({ onBack }: { onBack: () => void }) {
  const [situations, setSituations] = useState<Situation[]>([]);
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const [theme, setTheme] = useState<Theme>('ouverture');
  const [niveau, setNiveau] = useState<Niveau>('debutant');

  useEffect(() => {
    let cancelled = false;
    fetchBanque()
      .then(list => { if (!cancelled) setSituations(list); })
      .catch(cause => { if (!cancelled) setError(cause instanceof Error ? cause.message : 'Banque indisponible.'); })
      .finally(() => { if (!cancelled) setLoading(false); });
    return () => { cancelled = true; };
  }, []);

  async function generate(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (busy) return;
    setBusy(true);
    setError('');
    try {
      const situation = await genererSituation(theme, niveau);
      setSituations(previous => [situation, ...previous]);
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : 'Génération impossible.');
    } finally {
      setBusy(false);
    }
  }

  return (
    <section aria-label="Banque de situations">
      <h2>Banque de situations</h2>
      <button type="button" onClick={onBack}>← Accueil</button>
      <form className="banque-form" onSubmit={event => void generate(event)}>
        <label>Thème
          <select value={theme} disabled={busy} onChange={event => setTheme(event.target.value as Theme)}>
            {Object.entries(themes).map(([value, label]) => <option key={value} value={value}>{label}</option>)}
          </select>
        </label>
        <label>Niveau
          <select value={niveau} disabled={busy} onChange={event => setNiveau(event.target.value as Niveau)}>
            {Object.entries(niveaux).map(([value, label]) => <option key={value} value={value}>{label}</option>)}
          </select>
        </label>
        <button type="submit" disabled={busy}>Générer une situation</button>
        {busy && <p aria-live="polite">Génération en cours… (15 à 40 s par essai, 3 essais au plus)</p>}
      </form>
      {error && <p role="alert">{error}</p>}
      {loading ? <p aria-live="polite">Chargement de la banque…</p>
        : situations.length === 0 ? <p>La banque est vide pour l’instant.</p>
        : <div className="situations">
          {situations.map(situation => <SituationCard key={situation.id} situation={situation} />)}
        </div>}
    </section>
  );
}
