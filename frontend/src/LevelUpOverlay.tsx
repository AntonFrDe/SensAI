import Mascot from './Mascot';
import Particules from './Particules';

export type LevelUpOverlayProps = { niveau: number; menthe: boolean; onFermer: () => void };

export default function LevelUpOverlay({ niveau, menthe, onFermer }: LevelUpOverlayProps) {
  return (
    <div className="jt-lvlup" role="dialog" aria-label={`Niveau ${niveau}`}>
      <div className="jt-lvlup-mascot">
        <span className="jt-rays" style={{ inset: '-70px' }} />
        <Mascot mood="happy" size={140} />
        <Particules nombre={130} distance={260} duree={1500} grand />
      </div>
      <div className="jt-lvlup-title">Niveau {niveau} !</div>
      <div className="jt-lvlup-text">
        {menthe ? 'Jeton a gagné une nouvelle couleur : menthe. Il est trop content.' : 'Jeton est fier de toi.'}
      </div>
      <button type="button" className="jt-btn jt-yel jt-shine" autoFocus onClick={onFermer}>Trop bien !</button>
    </div>
  );
}
