import { useState, type FormEvent } from 'react';
import { IconCards, IconFlame, IconSeedling, IconSparkles } from '@tabler/icons-react';
import type { TrainerNiveau, TrainerSession } from './api';
import Mascot from './Mascot';
import { PSEUDO_VALIDE } from './progress';

export type LevelScreenProps = {
  pseudo: string;
  session: TrainerSession | null;
  erreur: string;
  onPseudo: (pseudo: string) => void;
  onChoisir: (reponse: string) => Promise<{ niveau: TrainerNiveau; raison: string | null }>;
  onContinuer: () => void;
  onReprendre: () => void;
};

const ICONES: Record<TrainerNiveau, { icone: typeof IconSeedling; couleur: string }> = {
  debutant: { icone: IconSeedling, couleur: 'jt-mint' },
  intermediaire: { icone: IconCards, couleur: 'jt-sky' },
  avance: { icone: IconFlame, couleur: 'jt-pink' },
};

function titre(libelle: string): [string, string] {
  const [nom, detail] = libelle.split(' (');
  return [nom, detail ? detail.replace(/\)$/, '').replace(/^./, lettre => lettre.toUpperCase()) : ''];
}

export default function LevelScreen({ pseudo, session, erreur, onPseudo, onChoisir, onContinuer, onReprendre }: LevelScreenProps) {
  const [saisie, setSaisie] = useState('');
  const [texteLibre, setTexteLibre] = useState('');
  const [classement, setClassement] = useState<{ niveau: TrainerNiveau; raison: string | null } | null>(null);
  const [erreurLibre, setErreurLibre] = useState('');
  const [occupe, setOccupe] = useState(false);
  const libelles = new Map((session?.niveaux ?? []).map(({ niveau, libelle }) => [niveau, libelle]));

  function envoyerPseudo(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const normalise = saisie.trim().toLowerCase();
    if (!PSEUDO_VALIDE.test(normalise)) {
      setErreurLibre('Pseudo : 1 à 32 lettres sans accent, chiffres, - ou _.');
      return;
    }
    onPseudo(saisie.trim());
  }

  async function classer(reponse: string) {
    const texte = reponse.trim();
    if (!texte || occupe) {
      setErreurLibre('Raconte-moi au moins une phrase sur ton jeu.');
      return;
    }
    setOccupe(true);
    setErreurLibre('');
    try {
      setClassement(await onChoisir(texte));
    } catch (cause) {
      setErreurLibre(cause instanceof Error ? cause.message : 'Réponse non comprise.');
    } finally {
      setOccupe(false);
    }
  }

  if (!pseudo) {
    return (
      <div className="jt-enter">
        <div className="jt-row">
          <Mascot mood="idle" size={90} pokable={false} />
          <div className="jt-say jt-say-big">Salut ! Moi c’est Jeton. Comment tu t’appelles ?</div>
        </div>
        <form className="jt-pseudo" onSubmit={envoyerPseudo}>
          <input value={saisie} onChange={event => setSaisie(event.target.value)} placeholder="Ton pseudo" aria-label="Ton pseudo" maxLength={32} />
          <button type="submit" className="jt-btn jt-sky">C’est moi</button>
        </form>
        <p className="jt-err">{erreurLibre || erreur}</p>
      </div>
    );
  }

  if (!session) {
    return (
      <div className="jt-enter">
        <div className="jt-row">
          <Mascot mood="think" size={90} pokable={false} />
          <div className="jt-say jt-say-big">{erreur || 'Je prépare ta session…'}</div>
        </div>
      </div>
    );
  }

  return (
    <div className="jt-enter">
      <div className="jt-row">
        <Mascot mood="idle" size={90} />
        <div className="jt-say jt-say-big">
          Salut {pseudo} ! Moi c’est Jeton. On joue à quel niveau aujourd’hui ?
        </div>
      </div>
      {session.profil?.reprise && (
        <div className="jt-glass jt-table-panel jt-row-tight">
          <p className="jt-soft-sm">Tu avais un débrief en cours.</p>
          <button type="button" className="jt-btn jt-pink" onClick={onReprendre}>Reprendre le débrief</button>
        </div>
      )}
      <div className="jt-tiles">
        {session.niveaux.map(({ niveau, libelle }, index) => {
          const [nom, detail] = titre(libelle);
          const { icone: Icone, couleur } = ICONES[niveau];
          return (
            <button
              key={niveau}
              type="button"
              className={`jt-tile jt-tilt ${couleur}`}
              style={{ animationDelay: `${150 + index * 100}ms` }}
              disabled={occupe}
              onClick={() => void onChoisir(niveau).then(onContinuer, () => setErreurLibre('Impossible de choisir ce niveau.'))}
            >
              <span className="jt-ic"><Icone size={28} stroke={1.8} aria-hidden="true" /></span>
              <span className="jt-tile-title">{nom}</span>
              <span className="jt-tile-sub">{detail}</span>
            </button>
          );
        })}
      </div>
      <div className="jt-or">
        <span className="jt-line" />ou raconte-moi ton jeu<span className="jt-line" />
      </div>
      <form className="jt-freeform" onSubmit={event => { event.preventDefault(); void classer(texteLibre); }}>
        <input
          id="free"
          value={texteLibre}
          onChange={event => { setTexteLibre(event.target.value); setErreurLibre(''); }}
          placeholder="Je joue le vendredi entre amis"
          aria-label="Décris ton niveau"
        />
        <button type="submit" className="jt-btn jt-sky" disabled={occupe}>
          <IconSparkles size={18} aria-hidden="true" />Évaluer
        </button>
      </form>
      <p className="jt-err">{erreurLibre || erreur}</p>
      {classement && (
        <div className="jt-glass jt-bub jt-free-out">
          <Mascot mood="wow" size={52} pokable={false} />
          <div>
            <div className="jt-tile-title">Tu es plutôt « {libelles.get(classement.niveau)?.split(' (')[0]} »</div>
            <div className="jt-soft-xs">{classement.raison ?? 'd’après ce que tu racontes.'}</div>
          </div>
          <button type="button" className="jt-btn jt-pink" onClick={onContinuer}>C’est parti</button>
        </div>
      )}
    </div>
  );
}
