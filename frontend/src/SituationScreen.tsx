import { useEffect, useState } from 'react';
import { IconBolt, IconTarget } from '@tabler/icons-react';
import type { TrainerActionKey, TrainerSituation } from './api';
import CarteTable from './CarteTable';
import { useJeton, type Palette } from './JetonContext';
import Mascot, { type Mood } from './Mascot';
import { RACCOURCIS, THEME_LABELS } from './trainerLabels';

export type SituationScreenProps = {
  situation: TrainerSituation | null;
  pseudo: string;
  numero: number;
  combo: number;
  erreur: string;
  occupe: boolean;
  onDecider: (action: TrainerActionKey) => void;
  onReessayer: () => void;
};

const ORDRE = ['UTG', 'MP', 'CO', 'BTN', 'SB', 'BB'];
const PLACES: [number, number][] = [[50, 100], [3, 70], [3, 28], [50, 0], [97, 28], [97, 70]];
const COULEURS: (Palette | undefined)[] = [undefined, 'sky', 'mint', 'yel', 'lav', 'pink'];
const SURVOL: Partial<Record<TrainerActionKey, { humeur: Mood; phrase: string }>> = {
  fold: { humeur: 'think', phrase: 'Hmm, prudent…' },
  call: { humeur: 'wow', phrase: 'On paie pour voir ?' },
  raise: { humeur: 'wow', phrase: 'Ooh, on attaque ?' },
};
const CLASSES: Partial<Record<TrainerActionKey, string>> = {
  call: 'jt-sky',
  raise: 'jt-pink',
  moi: 'jt-mint',
  adversaire: 'jt-pink',
  egalite: 'jt-yel',
};
const BLINDES: Record<string, string> = { SB: '0,5 bb', BB: '1 bb' };

type Siege = {
  k: number;
  position: string;
  etat: 'couche' | 'blinde' | 'attente' | 'adversaire';
  tag: string;
};

function sieges(situation: TrainerSituation): Siege[] {
  const hi = ORDRE.indexOf(situation.position);
  const sieges: Siege[] = [];
  for (let k = 1; k < ORDRE.length; k++) {
    const position = ORDRE[(hi + k) % ORDRE.length];
    if (situation.theme !== 'ouverture') {
      if (k === 3) {
        const tag = situation.theme === 'tirage' ? `Adversaire · mise ${formater(situation.a_payer)} bb`
          : situation.theme === 'defense_bb' ? 'Ouvreur' : 'Adversaire';
        sieges.push({ k, position, etat: 'adversaire', tag });
      }
      continue;
    }
    const ordre = ORDRE.indexOf(position);
    if (ordre < hi) {
      sieges.push({ k, position, etat: 'couche', tag: `${position} · couché` });
    } else if (BLINDES[position]) {
      sieges.push({ k, position, etat: 'blinde', tag: `${position} · ${BLINDES[position]}` });
    } else {
      sieges.push({ k, position, etat: 'attente', tag: position });
    }
  }
  return sieges;
}

function formater(nombre: number): string {
  return nombre.toLocaleString('fr-FR', { maximumFractionDigits: 1 });
}

function majuscule(texte: string): string {
  return texte.charAt(0).toUpperCase() + texte.slice(1);
}

export default function SituationScreen({ situation, pseudo, numero, combo, erreur, occupe, onDecider, onReessayer }: SituationScreenProps) {
  const { pokeLine } = useJeton();
  const [survol, setSurvol] = useState<TrainerActionKey | null>(null);

  useEffect(() => {
    if (!situation) return undefined;
    const clavier = (event: KeyboardEvent) => {
      if (event.target instanceof HTMLInputElement || occupe) return;
      const choisie = situation.actions.find(({ action }) => RACCOURCIS[action] === event.key.toUpperCase());
      if (choisie) onDecider(choisie.action);
    };
    document.addEventListener('keydown', clavier);
    return () => document.removeEventListener('keydown', clavier);
  }, [situation, occupe, onDecider]);

  if (!situation) {
    return (
      <div className="jt-enter">
        <p className="jt-loading">{erreur || 'Jeton tire une situation…'}</p>
        {erreur && <button type="button" className="jt-btn jt-sky" onClick={onReessayer}>Réessayer</button>}
      </div>
    );
  }

  const hi = ORDRE.indexOf(situation.position);
  const quiz = situation.theme === 'qui_gagne';
  const humeur = survol ? SURVOL[survol]?.humeur ?? 'idle' : 'idle';
  const bulle = survol ? SURVOL[survol]?.phrase ?? '' : pokeLine || `À toi de jouer, ${pseudo} !`;
  const cartesAdversaire = situation.adversaire ?? [];

  return (
    <div className="jt-enter">
      <div className="jt-meta">
        <span className="jt-pill jt-pill-yel"><IconTarget size={16} aria-hidden="true" />{THEME_LABELS[situation.theme]}</span>
        <span className="jt-pill">Exercice {numero}</span>
        <span className={`jt-pill jt-pill-end${combo >= 3 ? ' jt-fire' : ''}`}>
          <span className="jt-flame"><IconBolt size={16} aria-hidden="true" /></span>Combo x{combo}
        </span>
      </div>
      <div className="jt-felt">
        <span className="jt-felt-ring" />
        <span className="jt-felt-title">SensAI</span>
        <div className="jt-felt-center">
          <div className="jt-felt-cards">
            {situation.board.map((code, index) => (
              <CarteTable key={`${code}-${index}`} code={code} animation="deal" delai={600 + index * 130} />
            ))}
          </div>
          {!quiz && (
            <div className="jt-pot">
              <span className="jt-chips">
                <span className="jt-chip jt-chip-1" />
                <span className="jt-chip jt-chip-2" />
                <span className="jt-chip jt-chip-3" />
              </span>
              <span>Pot {formater(situation.pot)} bb</span>
            </div>
          )}
        </div>
        {sieges(situation).map(({ k, position, etat, tag }) => {
          const [x, y] = PLACES[k];
          return (
            <div key={`${position}-${k}`} className="jt-seat" style={{ left: `${x}%`, top: `${y}%`, animationDelay: `${k * 80}ms` }}>
              {etat === 'adversaire' && quiz && cartesAdversaire.length > 0 ? (
                <div className="jt-seat-hand">
                  {cartesAdversaire.map((code, index) => (
                    <CarteTable key={`${code}-${index}`} code={code} animation="flip" delai={400 + index * 160} />
                  ))}
                </div>
              ) : (
                <Mascot mood={etat === 'couche' ? 'sleep' : 'idle'} size={48} opponent={COULEURS[k]} />
              )}
              <span className={`jt-tag${etat === 'couche' ? ' jt-tag-off' : ''}`}>{tag}</span>
            </div>
          );
        })}
        <div className="jt-seat" style={{ left: `${PLACES[0][0]}%`, top: `${PLACES[0][1]}%`, animationDelay: '0ms' }}>
          <div className="jt-seat-hand">
            {situation.cartes.map((code, index) => (
              <CarteTable key={`${code}-${index}`} code={code} animation="flip" delai={400 + index * 160} />
            ))}
          </div>
          <span className="jt-av">Toi</span>
          <span className="jt-tag">{ORDRE[hi]}</span>
        </div>
      </div>
      <div className="jt-glass jt-table-panel">
        <div className="jt-panel-head">
          <Mascot mood={humeur} size={58} />
          <div className="jt-say">{bulle}</div>
        </div>
        <div className="jt-texte">{situation.texte}</div>
        <p className="jt-question">{situation.question}</p>
        <div className="jt-actions" style={{ ['--n' as string]: situation.actions.length }}>
          {situation.actions.map(({ action, libelle }) => (
            <button
              key={action}
              type="button"
              className={`jt-btn ${CLASSES[action] ?? ''}`}
              disabled={occupe}
              onClick={() => onDecider(action)}
              onPointerEnter={() => setSurvol(action)}
              onPointerLeave={() => setSurvol(null)}
            >
              {majuscule(libelle)}
              {RACCOURCIS[action] && <span className="jt-kbd">{RACCOURCIS[action]}</span>}
            </button>
          ))}
        </div>
        <p className="jt-err">{erreur}</p>
      </div>
    </div>
  );
}
