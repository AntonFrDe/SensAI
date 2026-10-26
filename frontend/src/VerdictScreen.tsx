import { useEffect } from 'react';
import { IconCalculator, IconInfoCircle, IconMessageCircle, IconMoodSad, IconScale, IconThumbUp, IconBolt } from '@tabler/icons-react';
import type { TrainerActionKey, TrainerReference, TrainerSituation, TrainerVerdict } from './api';
import Mascot from './Mascot';
import Particules from './Particules';
import { SFX } from './sfx';
import { HYPOTHESE_FAITS, SOURCE_FAITS, VERDICT_TEXTES, nomAction } from './trainerLabels';

export type VerdictScreenProps = {
  situation: TrainerSituation;
  verdict: TrainerVerdict;
  reference: TrainerReference;
  action: TrainerActionKey;
  gain: number;
  combo: number;
  onDebrief: () => void;
  onFiche: () => void;
};

const STYLE: Record<TrainerVerdict, { couleur: string; texte: string; titre: string; icone: typeof IconThumbUp }> = {
  bon: { couleur: 'var(--mint)', texte: '#063A25', titre: 'var(--mintText)', icone: IconThumbUp },
  acceptable: { couleur: 'var(--yel)', texte: '#3D2600', titre: 'var(--yelText)', icone: IconScale },
  erreur: { couleur: 'var(--red)', texte: '#fff', titre: 'var(--redText)', icone: IconMoodSad },
};

const CADRE = /^(Hypothèse|Référence) : /;

export default function VerdictScreen({ situation, verdict, reference, action, gain, combo, onDebrief, onFiche }: VerdictScreenProps) {
  const texte = VERDICT_TEXTES[verdict];
  const style = STYLE[verdict];
  const Icone = style.icone;
  const faits = reference.faits.filter(fait => !CADRE.test(fait));
  const hypothese = reference.faits.find(fait => fait.startsWith('Hypothèse : '))?.replace(CADRE, '') ?? HYPOTHESE_FAITS[situation.theme];
  const meilleures = (reference.bonnes.length > 0 ? reference.bonnes : reference.acceptables).map(cle => nomAction(situation, cle));

  useEffect(() => {
    if (verdict === 'bon') SFX.bon();
    else if (verdict === 'erreur') SFX.mauvais();
    else SFX.tic();
  }, [verdict]);

  return (
    <div className="jt-enter">
      <div className="jt-row jt-verdict-head">
        <span className={`jt-badge-wrap${verdict === 'erreur' ? ' jt-shake' : ''}`}>
          {verdict === 'bon' && <span className="jt-rays" />}
          <span className="jt-badge" style={{ background: style.couleur, color: style.texte }}>
            <Icone size={52} stroke={2} aria-hidden="true" />
          </span>
          <span className="jt-flt" style={{ animationDelay: '300ms' }}>+{gain} XP</span>
          {verdict === 'bon' && <Particules nombre={90} distance={260} duree={1500} grand />}
        </span>
        <div className="jt-verdict-text">
          <div className="jt-verdict-label" style={{ color: style.titre }}>{texte.titre}</div>
          <div className="jt-verdict-line">{texte.phrase}</div>
          <div className="jt-soft-sm">
            Tu as choisi <b className="jt-strong">{nomAction(situation, action)}</b>, la référence dit{' '}
            <b className="jt-strong">{meilleures.join(' ou ') || 'rien de précis'}</b>.
          </div>
        </div>
        <Mascot mood={texte.humeur} size={80} />
      </div>
      <div className="jt-meta jt-verdict-pills">
        {verdict === 'bon' ? (
          <>
            <span className={`jt-pill${combo >= 3 ? ' jt-fire' : ''}`}>
              <span className="jt-flame"><IconBolt size={16} aria-hidden="true" /></span>Combo x{combo}
            </span>
            <span className="jt-pill jt-pill-yel">+{gain} XP</span>
          </>
        ) : (
          <span className="jt-pill">+{gain} XP pour l’effort</span>
        )}
      </div>
      <div className="jt-facts-title">
        <span className="jt-facts-ic"><IconCalculator size={16} aria-hidden="true" /></span>
        Ce que le calcul établit
      </div>
      <div className="jt-facts">
        {faits.map((fait, index) => (
          <div key={index} className="jt-fact jt-tilt">
            <span className="jt-fact-text">{fait}</span>
            <span className="jt-src">{SOURCE_FAITS[situation.theme]}</span>
          </div>
        ))}
      </div>
      <div className="jt-hyp">
        <IconInfoCircle size={14} aria-hidden="true" /> Hypothèse : {hypothese}
      </div>
      <div className="jt-actions-row">
        <button type="button" className="jt-btn jt-pink jt-shine" onClick={onDebrief}>
          <IconMessageCircle size={18} aria-hidden="true" />Discuter avec Jeton
        </button>
        <button type="button" className="jt-btn" onClick={onFiche}>Voir ma fiche</button>
      </div>
    </div>
  );
}
