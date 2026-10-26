import { useEffect, useRef, useState } from 'react';
import { IconGift, IconLock, IconPlayerPlay, IconQuestionMark } from '@tabler/icons-react';
import type { TrainerFiche, TrainerResultats, TrainerTheme } from './api';
import CountUp from './CountUp';
import Mascot from './Mascot';
import Particules from './Particules';
import { BADGE_ICONES } from './BadgeToast';
import { BADGES, OBJECTIF_JOUR, serieEnCours, type Progress } from './progress';
import { SFX } from './sfx';
import { THEME_LABELS } from './trainerLabels';

export type SummaryScreenProps = {
  progression: Progress;
  gain: number;
  objectif: number;
  resultats: TrainerResultats;
  aujourdhui: string;
  fiche: TrainerFiche | null;
  chargementFiche: boolean;
  erreurFiche: string;
  onDemanderFiche: () => void;
  onCoffre: () => void;
  onSuivant: () => void;
};

const THEMES: TrainerTheme[] = ['ouverture', 'tirage', 'defense_bb', 'qui_gagne'];
const LETTRES_JOUR = ['D', 'L', 'M', 'M', 'J', 'V', 'S'];
const BADGES_AFFICHES = [
  { nom: BADGES.roiDuBouton, couleur: 'var(--yel)' },
  { nom: BADGES.chasseurDeTirages, couleur: 'var(--sky)' },
  { nom: BADGES.serie, couleur: '#FF9F3D' },
  { nom: BADGES.chatouilleur, couleur: 'var(--pink)', secret: true },
];

export default function SummaryScreen({ progression, gain, objectif, resultats, aujourdhui, fiche, chargementFiche, erreurFiche, onDemanderFiche, onCoffre, onSuivant }: SummaryScreenProps) {
  const [secoue, setSecoue] = useState(false);
  const [ouvert, setOuvert] = useState(false);
  const [barres, setBarres] = useState(false);
  const demande = useRef(false);

  useEffect(() => {
    if (!fiche && !chargementFiche && !erreurFiche && !demande.current) {
      demande.current = true;
      onDemanderFiche();
    }
  }, [fiche, chargementFiche, erreurFiche, onDemanderFiche]);

  useEffect(() => {
    const minuterie = window.setTimeout(() => setBarres(true), 300);
    return () => window.clearTimeout(minuterie);
  }, []);

  useEffect(() => {
    if (!secoue) return undefined;
    const minuterie = window.setTimeout(() => {
      setSecoue(false);
      setOuvert(true);
      SFX.coffre();
      onCoffre();
    }, 1200);
    return () => window.clearTimeout(minuterie);
  }, [secoue, onCoffre]);

  function ouvrirCoffre() {
    if (progression.coffre || secoue) return;
    SFX.tic();
    setSecoue(true);
  }

  const serie = serieEnCours(progression, aujourdhui);
  const precision = progression.exercices > 0 ? Math.round((progression.bons / progression.exercices) * 100) : 0;
  const jours = Array.from({ length: 7 }, (_, index) => {
    const date = new Date();
    date.setDate(date.getDate() - (6 - index));
    return { lettre: LETTRES_JOUR[date.getDay()], fait: 6 - index < serie };
  });
  const statistiques = [
    { valeur: gain, libelle: 'XP gagnés', couleur: 'var(--yel)', suffixe: '' },
    { valeur: precision, libelle: 'Précision totale', couleur: 'var(--mint)', suffixe: '%' },
    { valeur: progression.combo, libelle: 'Combo', couleur: '#FF9F3D', suffixe: '' },
  ];

  return (
    <div className="jt-enter">
      <div className="jt-fiche-head">
        <Mascot mood="happy" size={86} />
        <div>
          <div className="jt-title-xl">Exercice terminé !</div>
          <div className="jt-soft">Encore {Math.max(0, OBJECTIF_JOUR - objectif)} pour ton objectif du jour.</div>
        </div>
      </div>
      <div className="jt-stats">
        {statistiques.map(({ valeur, libelle, couleur, suffixe }) => (
          <div key={libelle} className="jt-fact jt-tilt jt-stat" style={{ borderColor: couleur }}>
            <span className="jt-stat-val" style={{ color: couleur }}><CountUp valeur={valeur} suffixe={suffixe} duree={900} /></span>
            <span className="jt-stat-label">{libelle}</span>
          </div>
        ))}
      </div>
      <button type="button" className="jt-glass jt-chest" onClick={ouvrirCoffre} aria-label={progression.coffre ? 'Coffre du jour ouvert' : 'Ouvrir le coffre du jour'}>
        {progression.coffre ? (
          <>
            <Mascot mood="happy" size={66} />
            <span>
              <span className="jt-chest-yel">Coffre ouvert</span>
              <span className="jt-chest-title">Lunettes de star pour Jeton !</span>
              <span className="jt-chest-sub">Il les porte maintenant partout, regarde-le.</span>
            </span>
          </>
        ) : (
          <>
            <span className={`jt-chest-ic ${secoue ? 'jt-shake3' : 'jt-wob'}`}><IconGift size={36} aria-hidden="true" /></span>
            <span>
              <span className="jt-chest-title">Coffre du jour</span>
              <span className="jt-chest-sub">Touche-le pour l’ouvrir. Qu’est-ce qu’il y a dedans ?</span>
            </span>
          </>
        )}
        {ouvert && <Particules nombre={110} distance={260} duree={1500} grand />}
      </button>
      <div className="jt-glass jt-streak">
        <div>
          <div className="jt-tile-title">Série de {serie} jour{serie > 1 ? 's' : ''}</div>
          <div className="jt-soft-xs">Reviens demain pour la garder.</div>
        </div>
        <div className="jt-days">
          {jours.map((jour, index) => (
            <span key={index} className={`jt-day${jour.fait ? ' jt-day-done' : ''}${index === 6 ? ' jt-day-today' : ''}`}>{jour.lettre}</span>
          ))}
        </div>
      </div>
      <div className="jt-keep">
        <div className="jt-keep-title">À retenir</div>
        <div className="jt-keep-text">
          {fiche ? fiche.a_retenir : erreurFiche || (chargementFiche ? 'Jeton écrit ta fiche…' : '')}
        </div>
        {erreurFiche && <button type="button" className="jt-btn" onClick={onDemanderFiche}>Réessayer la fiche</button>}
      </div>
      <div className="jt-glass jt-themes">
        <div className="jt-themes-head">
          <span className="jt-tile-title">Tes thèmes</span>
          {fiche && <span className="jt-pill jt-pill-pink jt-pill-end">À revoir : {fiche.theme_a_revoir}</span>}
        </div>
        {THEMES.map(theme => {
          const compte = resultats[theme] ?? { bon: 0, acceptable: 0, erreur: 0 };
          const total = compte.bon + compte.acceptable + compte.erreur;
          const bons = compte.bon;
          const pourcent = total ? Math.round((bons / total) * 100) : 0;
          return (
            <div key={theme} className="jt-theme-row">
              <span className="jt-theme-name">{THEME_LABELS[theme]}</span>
              <div className="jt-theme-bar">
                <div className="jt-fill" style={{ width: barres ? `${pourcent}%` : '0%', background: 'var(--mint)' }} />
              </div>
              <span className="jt-theme-val">{bons}/{total}</span>
            </div>
          );
        })}
      </div>
      <div className="jt-tile-title">Tes badges</div>
      <div className="jt-badges">
        {BADGES_AFFICHES.map(({ nom, couleur, secret }) => {
          const obtenu = progression.badges.includes(nom);
          const Icone = BADGE_ICONES[nom];
          return (
            <div key={nom} className="jt-bdg jt-tilt">
              <span className="jt-bdg-ic" style={{ background: obtenu ? couleur : 'var(--g2)', color: obtenu ? '#2A1860' : 'var(--soft)' }}>
                {obtenu ? <Icone size={28} aria-hidden="true" /> : secret ? <IconQuestionMark size={28} aria-hidden="true" /> : <IconLock size={28} aria-hidden="true" />}
              </span>
              <span style={{ color: obtenu ? '#fff' : 'var(--soft)' }}>{obtenu || !secret ? nom : 'Badge secret'}</span>
            </div>
          );
        })}
      </div>
      <button type="button" className="jt-btn jt-pink jt-shine jt-continue" onClick={onSuivant}>
        <IconPlayerPlay size={18} aria-hidden="true" />Continuer
      </button>
    </div>
  );
}
