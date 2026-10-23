import { IconFlame, IconVolume, IconVolumeOff } from '@tabler/icons-react';
import CountUp from './CountUp';
import JetonBrand from './JetonBrand';
import ModeMenu from './ModeMenu';
import type { View } from './navigation';
import { OBJECTIF_JOUR, avancementDuNiveau, niveauDe, type Progress } from './progress';

export type TrainerHeaderProps = {
  pseudo: string;
  progression: Progress;
  serie: number;
  objectif: number;
  onSon: () => void;
  onNavigate: (view: View) => void;
};

const RAYON = 14;
const CIRCONFERENCE = 88;

export default function TrainerHeader({ pseudo, progression, serie, objectif, onSon, onNavigate }: TrainerHeaderProps) {
  const niveau = niveauDe(progression.xp);
  const initiale = pseudo ? pseudo[0].toUpperCase() : '?';
  return (
    <header className="jt-head">
      <JetonBrand />
      <div className="jt-pills">
        <button type="button" className="jt-pill jt-pill-round" onClick={onSon}
          aria-label={progression.son ? 'Couper le son' : 'Activer le son'}>
          {progression.son ? <IconVolume size={17} aria-hidden="true" /> : <IconVolumeOff size={17} aria-hidden="true" />}
        </button>
        <span className="jt-pill" title="Série de jours">
          <span className="jt-streak-ic"><IconFlame size={17} aria-hidden="true" /></span>
          <span>{serie}</span>
        </span>
        <span className="jt-pill" title="Objectif du jour">
          <svg className="jt-ring" width="22" height="22" viewBox="0 0 36 36" aria-hidden="true">
            <circle cx="18" cy="18" r={RAYON} fill="none" stroke="rgba(0,0,0,.35)" strokeWidth="6" />
            <circle className="jt-ring-arc" cx="18" cy="18" r={RAYON} fill="none" stroke="#2EE59D" strokeWidth="6"
              strokeLinecap="round" strokeDasharray={CIRCONFERENCE}
              strokeDashoffset={CIRCONFERENCE - (CIRCONFERENCE * Math.min(objectif, OBJECTIF_JOUR)) / OBJECTIF_JOUR}
              transform="rotate(-90 18 18)" />
          </svg>
          <span>{Math.min(objectif, OBJECTIF_JOUR)}/{OBJECTIF_JOUR}</span>
        </span>
        <span className="jt-pill jt-pill-lvl">
          <span className="jt-lvl">Niv. {niveau}</span>
          <span className="jt-xpt">
            <span className="jt-xpf" style={{ width: `${avancementDuNiveau(progression.xp) * 100}%` }} />
          </span>
          <span><CountUp valeur={progression.xp % 500} /></span>
        </span>
        <span className="jt-avatar" aria-label={pseudo ? `Joueur ${pseudo}` : 'Joueur'}>{initiale}</span>
        <ModeMenu current="trainer" onSelect={onNavigate} />
      </div>
    </header>
  );
}
