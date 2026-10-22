import { useEffect, useRef, useState, type FormEvent } from 'react';
import { IconArrowsShuffle, IconCalculator, IconFlag, IconHelp, IconPuzzle, IconSend } from '@tabler/icons-react';
import { envoyerDebrief, type TrainerMessage, type TrainerReference, type TrainerSituation, type TrainerVerdict } from './api';
import Mascot from './Mascot';
import { ACTION_LIBELLES, VERDICT_TEXTES } from './trainerLabels';

export type DebriefScreenProps = {
  sessionId: string;
  situation: TrainerSituation;
  verdict: TrainerVerdict;
  reference: TrainerReference;
  reprise?: TrainerMessage[];
  onFini: () => void;
};

type Question = { question: string; choix: string[]; reponse: number | null };
type Bulle = {
  id: number;
  auteur: 'jeton' | 'moi';
  texte: string;
  outils: string[];
  enCours: boolean;
  attente: boolean;
  question?: Question;
};

const SUGGESTIONS = [
  { cle: 'pourquoi', libelle: 'Pourquoi ce verdict ?', envoi: 'Pourquoi ce verdict ?', icone: IconHelp },
  { cle: 'autre', libelle: 'Et si la situation changeait ?', envoi: 'Et si la situation avait été différente ?', icone: IconArrowsShuffle },
  { cle: 'question', libelle: 'Pose-moi une question', envoi: 'Pose-moi une question de contrôle.', icone: IconPuzzle },
];

function introduction(verdict: TrainerVerdict, situation: TrainerSituation, reference: TrainerReference): string {
  const meilleures = (reference.bonnes.length > 0 ? reference.bonnes : reference.acceptables)
    .map(cle => situation.actions.find(choix => choix.action === cle)?.libelle ?? ACTION_LIBELLES[cle] ?? cle);
  return `${VERDICT_TEXTES[verdict].phrase} La référence préfère : ${meilleures.join(' ou ') || 'aucune action précise'}. Pose ta question, ou demande-moi pourquoi.`;
}

export default function DebriefScreen({ sessionId, situation, verdict, reference, reprise, onFini }: DebriefScreenProps) {
  const [bulles, setBulles] = useState<Bulle[]>(() => (reprise
    ? reprise.map((message, index) => ({
      id: index, auteur: message.role === 'user' ? 'moi' : 'jeton', texte: message.content, outils: [], enCours: false, attente: false,
    }))
    : [{ id: 0, auteur: 'jeton', texte: introduction(verdict, situation, reference), outils: [], enCours: false, attente: false }]));
  const [saisie, setSaisie] = useState('');
  const [occupe, setOccupe] = useState(false);
  const [erreur, setErreur] = useState('');
  const [utilisees, setUtilisees] = useState<string[]>([]);
  const prochain = useRef(bulles.length);
  const controleur = useRef<AbortController | null>(null);

  useEffect(() => () => controleur.current?.abort(), []);

  function ajouter(bulle: Omit<Bulle, 'id'>): number {
    const id = prochain.current++;
    setBulles(precedentes => [...precedentes, { ...bulle, id }]);
    return id;
  }

  function mettre(id: number, changement: (bulle: Bulle) => Bulle) {
    setBulles(precedentes => precedentes.map(bulle => (bulle.id === id ? changement(bulle) : bulle)));
  }

  async function envoyer(texte: string, affiche: string) {
    if (occupe || !texte.trim()) return;
    setOccupe(true);
    setErreur('');
    ajouter({ auteur: 'moi', texte: affiche, outils: [], enCours: false, attente: false });
    const jeton = ajouter({ auteur: 'jeton', texte: '', outils: [], enCours: true, attente: false });
    controleur.current = new AbortController();
    try {
      await envoyerDebrief(sessionId, texte, evenement => {
        if (evenement.type === 'queued') mettre(jeton, bulle => ({ ...bulle, attente: true }));
        if (evenement.type === 'token') mettre(jeton, bulle => ({ ...bulle, attente: false, texte: bulle.texte + evenement.texte }));
        if (evenement.type === 'outil') mettre(jeton, bulle => ({ ...bulle, outils: [...bulle.outils, evenement.nom] }));
        if (evenement.type === 'question') {
          ajouter({ auteur: 'jeton', texte: '', outils: [], enCours: false, attente: false,
            question: { question: evenement.question, choix: evenement.choix, reponse: null } });
        }
        if (evenement.type === 'error') setErreur(evenement.message);
        if (evenement.type === 'done') mettre(jeton, bulle => ({ ...bulle, enCours: false }));
      }, controleur.current.signal);
    } catch (cause) {
      if (!(cause instanceof DOMException && cause.name === 'AbortError')) {
        setErreur(cause instanceof Error ? cause.message : 'Le débrief est indisponible.');
      }
    } finally {
      setBulles(precedentes => precedentes.filter(bulle => bulle.id !== jeton || bulle.texte || bulle.outils.length > 0 || bulle.question));
      mettre(jeton, bulle => ({ ...bulle, enCours: false, attente: false }));
      setOccupe(false);
    }
  }

  function repondre(bulle: Bulle, index: number) {
    if (!bulle.question || bulle.question.reponse !== null || occupe) return;
    const choix = bulle.question.choix[index];
    mettre(bulle.id, precedente => ({ ...precedente, question: { ...precedente.question!, reponse: index } }));
    void envoyer(String(index + 1), choix);
  }

  function soumettre(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const texte = saisie.trim();
    if (!texte) {
      setErreur('Écris ta question à Jeton.');
      return;
    }
    setSaisie('');
    void envoyer(texte, texte);
  }

  function suggerer(cle: string, envoi: string, affiche: string) {
    setUtilisees(precedentes => [...precedentes, cle]);
    void envoyer(envoi, affiche);
  }

  return (
    <div className="jt-enter">
      <div className="jt-log" aria-live="polite">
        {bulles.map(bulle => (
          bulle.auteur === 'moi' ? (
            <div key={bulle.id} className="jt-bub jt-me">{bulle.texte}</div>
          ) : (
            <div key={bulle.id} className="jt-bub-row">
              <span className="jt-mw">
                <Mascot mood={bulle.question ? 'wow' : bulle.enCours && !bulle.texte ? 'think' : 'idle'} size={42} pokable={false} />
              </span>
              <div className="jt-bub jt-co">
                {bulle.outils.map((nom, index) => (
                  <span key={index} className="jt-tool">
                    <span className="jt-tool-ic"><IconCalculator size={14} aria-hidden="true" /></span>{nom}
                  </span>
                ))}
                {bulle.outils.length > 0 && <br />}
                {bulle.enCours && !bulle.texte && (
                  <span className="jt-dots"><i /><i /><i /></span>
                )}
                {bulle.attente && <span className="jt-soft-xs">Jeton attend une place libre…</span>}
                <span className="jt-texte-bulle">{bulle.texte}</span>
                {bulle.question && (
                  <div className="jt-quiz-box">
                    <div className="jt-ask">{bulle.question.question}</div>
                    <div className="jt-quiz-opts">
                      {bulle.question.choix.map((choix, index) => (
                        <button
                          key={index}
                          type="button"
                          className="jt-btn jt-yel"
                          disabled={occupe || bulle.question?.reponse !== null}
                          onClick={() => repondre(bulle, index)}
                        >
                          {choix}
                        </button>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          )
        ))}
      </div>
      <div className="jt-sug">
        {SUGGESTIONS.filter(({ cle }) => !utilisees.includes(cle)).map(({ cle, libelle, envoi, icone: Icone }) => (
          <button key={cle} type="button" className="jt-btn" disabled={occupe}
            onClick={() => suggerer(cle, envoi, libelle)}>
            <Icone size={16} aria-hidden="true" />{libelle}
          </button>
        ))}
      </div>
      <form className="jt-input-row" onSubmit={soumettre}>
        <input
          value={saisie}
          onChange={event => setSaisie(event.target.value)}
          placeholder="Et si j’avais eu A♠ K♠ ?"
          aria-label="Ton message à Jeton"
          disabled={occupe}
        />
        <button type="submit" className="jt-btn jt-sky jt-send" disabled={occupe} aria-label="Envoyer">
          <IconSend size={20} aria-hidden="true" />
        </button>
      </form>
      <p className="jt-err">{erreur}</p>
      <div className="jt-end">
        <button type="button" className="jt-btn jt-mint jt-shine" onClick={onFini}>
          <IconFlag size={18} aria-hidden="true" />Terminer l’exercice
        </button>
      </div>
    </div>
  );
}
