import { useEffect, useRef, useState, type MouseEvent as ReactMouseEvent } from 'react';
import '@fontsource/rubik/400.css';
import '@fontsource/rubik/500.css';
import '@fontsource/rubik/600.css';
import '@fontsource/rubik/700.css';
import '@fontsource/rubik/800.css';
import '@fontsource/rubik/900.css';
import {
  choisirNiveau as choisirNiveauApi, creerSession, decider as deciderApi, ecrireFiche, nouvelleSituation as nouvelleSituationApi,
  reprendreDebrief, type TrainerActionKey, type TrainerFiche, type TrainerMessage, type TrainerReference,
  type TrainerResultats, type TrainerSession, type TrainerSituation, type TrainerTheme, type TrainerVerdict,
} from './api';
import BadgeToast from './BadgeToast';
import DebriefScreen from './DebriefScreen';
import LevelScreen from './LevelScreen';
import LevelUpOverlay from './LevelUpOverlay';
import { JetonContext, type JetonLook } from './JetonContext';
import Particules from './Particules';
import SituationScreen from './SituationScreen';
import SummaryScreen from './SummaryScreen';
import TrainerHeader from './TrainerHeader';
import VerdictScreen from './VerdictScreen';
import {
  BADGES, NIVEAU_MENTHE, OBJECTIF_JOUR, chatouiller, chargerProgression, couleurDeJeton, enregistrerProgression, enregistrerPseudo,
  jourDe, lirePseudo, niveauDe, noterExercice, objectifDuJour, ouvrirCoffre, serieEnCours, type Progress,
} from './progress';
import { SFX, sonActif } from './sfx';
import { ecouterInclinaisons } from './tilt';

export type TrainerAppProps = { onBack: () => void };

type Decision = { action: TrainerActionKey; verdict: TrainerVerdict; reference: TrainerReference; gain: number };
type Rafale = { id: number; x: string; y: string; nombre: number; distance: number; duree: number; grand: boolean };
type FicheEtat = { fiche: TrainerFiche | null; chargement: boolean; erreur: string };

const ETAPES = ['Niveau', 'Situation', 'Correction', 'Débrief', 'Fiche'];
const LIGNES = [
  'Hihi, ça chatouille !',
  'Encore une fois ?',
  'Je suis un jeton, pas un bouton !',
  'Ok ok, je suis bien réveillé.',
  'Continue et tu auras une surprise…',
  'Badge secret débloqué !',
];
const FICHE_VIDE: FicheEtat = { fiche: null, chargement: false, erreur: '' };

function messageDe(cause: unknown, repli: string): string {
  return cause instanceof Error ? cause.message : repli;
}

function ajouterResultat(resultats: TrainerResultats, theme: TrainerTheme, verdict: TrainerVerdict): TrainerResultats {
  const compte = resultats[theme] ?? { bon: 0, acceptable: 0, erreur: 0 };
  return { ...resultats, [theme]: { ...compte, [verdict]: compte[verdict] + 1 } };
}

export default function TrainerApp({ onBack }: TrainerAppProps) {
  const racine = useRef<HTMLElement>(null);
  const [pseudo, setPseudo] = useState(lirePseudo);
  const [session, setSession] = useState<TrainerSession | null>(null);
  const [erreurSession, setErreurSession] = useState('');
  const [progression, setProgression] = useState<Progress>(chargerProgression);
  const [resultats, setResultats] = useState<TrainerResultats>({});
  const [etape, setEtape] = useState(0);
  const [atteinte, setAtteinte] = useState(0);
  const [situation, setSituation] = useState<TrainerSituation | null>(null);
  const [numero, setNumero] = useState(0);
  const [erreurSituation, setErreurSituation] = useState('');
  const [chargementSituation, setChargementSituation] = useState(false);
  const [decision, setDecision] = useState<Decision | null>(null);
  const [erreurDecision, setErreurDecision] = useState('');
  const [occupe, setOccupe] = useState(false);
  const [messagesReprise, setMessagesReprise] = useState<TrainerMessage[] | undefined>(undefined);
  const [fiche, setFiche] = useState<FicheEtat>(FICHE_VIDE);
  const [file, setFile] = useState<string[]>([]);
  const [toast, setToast] = useState<string | null>(null);
  const [niveauAtteint, setNiveauAtteint] = useState<number | null>(null);
  const [rafales, setRafales] = useState<Rafale[]>([]);
  const [pokeLine, setPokeLine] = useState('');

  useEffect(() => {
    if (pseudo) void creer(pseudo);
    const retirer = racine.current ? ecouterInclinaisons(racine.current) : undefined;
    return () => retirer?.();
  }, []);

  useEffect(() => enregistrerProgression(progression), [progression]);

  useEffect(() => sonActif(progression.son), [progression.son]);

  useEffect(() => {
    if (etape === 1 && !situation && session && !chargementSituation) void obtenirSituation();
  }, [etape]);

  useEffect(() => {
    if (toast || file.length === 0) return;
    setToast(file[0]);
    setFile(suite => suite.slice(1));
  }, [toast, file]);

  useEffect(() => {
    if (!toast) return undefined;
    const minuterie = window.setTimeout(() => setToast(null), 3200);
    return () => window.clearTimeout(minuterie);
  }, [toast]);

  async function creer(nom: string) {
    setErreurSession('');
    try {
      const nouvelle = await creerSession(nom);
      setSession(nouvelle);
      setResultats(nouvelle.profil?.resultats ?? {});
    } catch (cause) {
      setErreurSession(messageDe(cause, 'Impossible de créer la session.'));
    }
  }

  function saisirPseudo(nom: string) {
    enregistrerPseudo(nom);
    setPseudo(nom);
    void creer(nom);
  }

  async function choisirNiveau(reponse: string) {
    if (!session) throw new Error('La session n’est pas prête.');
    return choisirNiveauApi(session.sessionId, reponse);
  }

  function aller(index: number) {
    setEtape(index);
    setAtteinte(precedente => Math.max(precedente, index));
  }

  function nouvelleSituation() {
    setSituation(null);
    setDecision(null);
    setMessagesReprise(undefined);
    setFiche(FICHE_VIDE);
    setErreurSituation('');
    setErreurDecision('');
    setAtteinte(precedente => Math.min(precedente, 1));
    aller(1);
  }

  function allerEtape(index: number) {
    if (index === 1 && decision) nouvelleSituation();
    else aller(index);
  }

  async function obtenirSituation() {
    if (!session || chargementSituation) return;
    setChargementSituation(true);
    setErreurSituation('');
    try {
      const suivante = await nouvelleSituationApi(session.sessionId);
      setSituation(suivante);
      setNumero(precedent => precedent + 1);
    } catch (cause) {
      setErreurSituation(messageDe(cause, 'Impossible de tirer une situation.'));
    } finally {
      setChargementSituation(false);
    }
  }

  async function decider(action: TrainerActionKey) {
    if (!session || !situation || occupe) return;
    setOccupe(true);
    setErreurDecision('');
    try {
      const resultat = await deciderApi(session.sessionId, action);
      const note = noterExercice(progression, { verdict: resultat.verdict, theme: situation.theme, position: situation.position }, jourDe());
      setProgression(note.progression);
      setResultats(precedents => ajouterResultat(precedents, situation.theme, resultat.verdict));
      setDecision({ action, verdict: resultat.verdict, reference: resultat.reference, gain: note.xp });
      if (note.badges.length > 0) setFile(suite => [...suite, ...note.badges]);
      if (note.nouveauNiveau) {
        const niveauNouveau = niveauDe(note.progression.xp);
        window.setTimeout(() => setNiveauAtteint(niveauNouveau), 900);
      }
      setFiche(FICHE_VIDE);
      aller(2);
    } catch (cause) {
      setErreurDecision(messageDe(cause, 'La décision n’a pas pu être enregistrée.'));
    } finally {
      setOccupe(false);
    }
  }

  async function reprendre() {
    if (!session) return;
    try {
      const reprise = await reprendreDebrief(session.sessionId);
      setSituation(reprise.situation);
      setDecision({ action: reprise.action, verdict: reprise.verdict, reference: reprise.reference, gain: 0 });
      setMessagesReprise(reprise.debrief.length > 0 ? reprise.debrief : undefined);
      setFiche(FICHE_VIDE);
      aller(3);
    } catch (cause) {
      setErreurSession(messageDe(cause, 'Impossible de reprendre le débrief.'));
    }
  }

  async function demanderFiche() {
    if (!session) return;
    setFiche({ fiche: null, chargement: true, erreur: '' });
    try {
      setFiche({ fiche: await ecrireFiche(session.sessionId), chargement: false, erreur: '' });
    } catch (cause) {
      setFiche({ fiche: null, chargement: false, erreur: messageDe(cause, 'La fiche est indisponible.') });
    }
  }

  function ajouterRafale(rafale: Omit<Rafale, 'id'>) {
    const id = Date.now() + Math.random();
    setRafales(suite => [...suite, { ...rafale, id }]);
    window.setTimeout(() => setRafales(suite => suite.filter(item => item.id !== id)), rafale.duree + 300);
  }

  function rafaleAuClic(event: ReactMouseEvent<HTMLElement>) {
    const cible = event.target instanceof Element ? event.target.closest('.jt-btn, .jt-tile') : null;
    if (!cible || !racine.current) return;
    const boite = racine.current.getBoundingClientRect();
    SFX.pop();
    ajouterRafale({ x: `${event.clientX - boite.left}px`, y: `${event.clientY - boite.top}px`, nombre: 10, distance: 46, duree: 500, grand: false });
  }

  function caresser() {
    const resultat = chatouiller(progression);
    setProgression(resultat.progression);
    setPokeLine(LIGNES[Math.min(resultat.progression.chatouilles, LIGNES.length) - 1]);
    if (resultat.badges.length > 0) {
      setFile(suite => [...suite, ...resultat.badges]);
      ajouterRafale({ x: '50%', y: '40%', nombre: 60, distance: 200, duree: 1500, grand: true });
    }
  }

  const aujourdhui = jourDe();
  const serie = serieEnCours(progression, aujourdhui);
  const objectif = objectifDuJour(progression, aujourdhui);
  const look: JetonLook = {
    palette: couleurDeJeton(progression.xp),
    crown: progression.badges.includes(BADGES.roiDuBouton),
    shades: progression.coffre,
  };
  const largeurEtape = Math.max(4, (etape / (ETAPES.length - 1)) * 100);

  let ecran = null;
  if (etape === 0) {
    ecran = (
      <LevelScreen
        pseudo={pseudo}
        session={session}
        erreur={erreurSession}
        onPseudo={saisirPseudo}
        onChoisir={choisirNiveau}
        onContinuer={nouvelleSituation}
        onReprendre={() => void reprendre()}
      />
    );
  } else if (etape === 1) {
    ecran = (
      <SituationScreen
        situation={situation}
        pseudo={pseudo}
        numero={numero}
        combo={progression.combo}
        erreur={erreurSituation || erreurDecision}
        occupe={occupe || chargementSituation}
        onDecider={action => void decider(action)}
        onReessayer={() => void obtenirSituation()}
      />
    );
  } else if (situation && decision && session) {
    if (etape === 2) {
      ecran = (
        <VerdictScreen
          situation={situation}
          verdict={decision.verdict}
          reference={decision.reference}
          action={decision.action}
          gain={decision.gain}
          combo={progression.combo}
          onDebrief={() => aller(3)}
          onFiche={() => aller(4)}
        />
      );
    } else if (etape === 3) {
      ecran = (
        <DebriefScreen
          key={situation.id}
          sessionId={session.sessionId}
          situation={situation}
          verdict={decision.verdict}
          reference={decision.reference}
          reprise={messagesReprise}
          onFini={() => aller(4)}
        />
      );
    } else if (etape === 4) {
      ecran = (
        <SummaryScreen
          progression={progression}
          gain={decision.gain}
          objectif={objectif}
          resultats={resultats}
          aujourdhui={aujourdhui}
          fiche={fiche.fiche}
          chargementFiche={fiche.chargement}
          erreurFiche={fiche.erreur}
          onDemanderFiche={() => void demanderFiche()}
          onCoffre={() => setProgression(actuel => ouvrirCoffre(actuel))}
          onSuivant={nouvelleSituation}
        />
      );
    }
  }

  return (
    <JetonContext.Provider value={{ look, pokeLine, onPoke: caresser }}>
      <section className="jt-app" ref={racine} onClickCapture={rafaleAuClic} aria-label="Entraîneur Jeton">
        <span className="jt-blob jt-blob-1" />
        <span className="jt-blob jt-blob-2" />
        <span className="jt-blob jt-blob-3" />
        <span className="jt-suit jt-suit-1" aria-hidden="true">♠</span>
        <span className="jt-suit jt-suit-2" aria-hidden="true">♥</span>
        <span className="jt-suit jt-suit-3" aria-hidden="true">♣</span>
        <span className="jt-suit jt-suit-4" aria-hidden="true">♦</span>
        <div className="jt-wrap">
          <TrainerHeader
            pseudo={pseudo}
            progression={progression}
            serie={serie}
            objectif={objectif}
            onSon={() => setProgression(actuel => ({ ...actuel, son: !actuel.son }))}
            onAccueil={onBack}
          />
          <div className="jt-prog" aria-hidden="true">
            <div className="jt-progf" style={{ width: `${largeurEtape}%` }} />
          </div>
          <nav className="jt-steps" aria-label="Étapes de l’exercice">
            {ETAPES.map((nom, index) => (
              <button
                key={nom}
                type="button"
                className={index === etape ? 'jt-on' : undefined}
                disabled={index > atteinte}
                aria-current={index === etape ? 'step' : undefined}
                onClick={() => allerEtape(index)}
              >
                {index < etape ? '✓ ' : ''}{nom}
              </button>
            ))}
          </nav>
          <div className="jt-screen">{ecran}</div>
        </div>
        {toast && <BadgeToast badge={toast} />}
        {niveauAtteint !== null && (
          <LevelUpOverlay niveau={niveauAtteint} menthe={niveauAtteint === NIVEAU_MENTHE} onFermer={() => setNiveauAtteint(null)} />
        )}
        {rafales.map(rafale => (
          <span key={rafale.id} className="jt-burst" style={{ left: rafale.x, top: rafale.y }}>
            <Particules nombre={rafale.nombre} distance={rafale.distance} duree={rafale.duree} grand={rafale.grand} />
          </span>
        ))}
      </section>
    </JetonContext.Provider>
  );
}
