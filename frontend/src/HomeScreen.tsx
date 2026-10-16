import { useState, type FormEvent } from 'react';
import type { BlindLevel, GameResponse, TableOptions } from './api';
import ServerStatus from './ServerStatus';

export type HomeScreenProps = {
  options: TableOptions;
  busy: boolean;
  onPlay: (options: TableOptions) => void;
  onOpenBanque: () => void;
  onOpenGlossary?: () => void;
  onOpenRankings?: () => void;
  savedGame?: GameResponse | null;
  onResume?: () => void;
};

const blindLevels: BlindLevel[] = ['5/10', '10/20', '25/50'];
const depths = [{ value: 30, label: 'Court' }, { value: 50, label: 'Moyen' }, { value: 100, label: 'Profond' }, { value: 200, label: 'Très profond' }];
const minDepth = 20;
const maxDepth = 500;
const formatter = new Intl.NumberFormat('fr-FR');

export default function HomeScreen({
  options, busy, onPlay, onOpenBanque, onOpenGlossary, onOpenRankings, savedGame, onResume,
}: HomeScreenProps) {
  const [blinds, setBlinds] = useState<BlindLevel>(options.blinds);
  const [depth, setDepth] = useState(String(options.stackBigBlinds));
  const value = Number(depth);
  const validDepth = Number.isSafeInteger(value) && value >= minDepth && value <= maxDepth;
  const bigBlind = Number(blinds.split('/')[1]);

  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (validDepth && !busy) onPlay({ blinds, stackBigBlinds: value });
  }

  return (
    <section className="home" aria-label="Accueil">
      <h2>Entraînez-vous au Texas Hold’em</h2>
      <p>Affrontez une IA et apprenez à comprendre vos décisions.</p>
      {savedGame && onResume && <div className="resume" role="group" aria-label="Partie en cours">
        <p>Une partie est en cours : votre tapis est de {formatter.format(savedGame.state.seats.player.stack)} jetons,
          celui de l’IA de {formatter.format(savedGame.state.seats.opponent.stack)}.</p>
        <button type="button" className="primary" disabled={busy} onClick={onResume}>Reprendre la partie</button>
      </div>}
      <form className="table-options" onSubmit={submit}>
        <fieldset>
          <legend>Blindes</legend>
          <div className="choices">
            {blindLevels.map(level => (
              <label key={level} className="choice">
                <input type="radio" name="blinds" value={level} checked={blinds === level} onChange={() => setBlinds(level)} />
                {level}
              </label>
            ))}
          </div>
        </fieldset>
        <fieldset>
          <legend>Tapis de départ</legend>
          <div className="choices">
            {depths.map(({ value: preset, label }) => (
              <button key={preset} type="button" className="choice" aria-pressed={value === preset} onClick={() => setDepth(String(preset))}>
                {label} <small>{preset} bb</small>
              </button>
            ))}
          </div>
          <label className="depth-input">En grosses blindes ({minDepth} à {maxDepth})
            <input type="number" min={minDepth} max={maxDepth} step="1" value={depth} aria-invalid={!validDepth}
              onChange={event => setDepth(event.target.value)} />
          </label>
          <p className="hint" aria-live="polite">
            {validDepth ? `Chaque joueur commence avec ${formatter.format(value * bigBlind)} jetons.` : `Choisissez entre ${minDepth} et ${maxDepth} grosses blindes.`}
          </p>
        </fieldset>
        <div className="home-actions">
          <button type="submit" className="primary" disabled={busy || !validDepth}>{busy ? 'Distribution…' : 'Jouer'}</button>
          <button type="button" onClick={onOpenBanque}>Banque de situations</button>
          {onOpenGlossary && <button type="button" onClick={onOpenGlossary}>Glossaire</button>}
          {onOpenRankings && <button type="button" onClick={onOpenRankings}>Classement des mains</button>}
        </div>
      </form>
      <ServerStatus />
    </section>
  );
}
