import type { PokerAction } from './ActionControls';
import type { HistoryEntry } from './HandHistory';
import type { GamePhase } from './HandInfo';
import type { CardData } from './PlayingCard';
import type { Blinds, Hands, Seats } from './PokerTable';

export type Award = { amount: number; winners: string[]; reason: 'fold' | 'showdown' };
export type GameState = {
  playerCards: CardData[];
  opponentCards: CardData[];
  communityCards: CardData[];
  pot: number;
  playerStack: number;
  opponentStack: number;
  currentPlayer: 'player' | 'opponent';
  phase: GamePhase;
  currentBet: number;
  controls: { allowedActions: PokerAction[]; minAmount?: number; maxAmount?: number; toCall?: number };
  awards: Award[];
  history: HistoryEntry[];
  seats: Seats;
  blinds: Blinds;
  hands: Hands;
  gameOver: boolean;
  revealedForTraining?: boolean;
};
export type BlindLevel = '5/10' | '10/20' | '25/50';
export type TableOptions = { blinds: BlindLevel; stackBigBlinds: number; revealAtEnd?: boolean };
export const defaultTableOptions: TableOptions = { blinds: '10/20', stackBigBlinds: 50 };
export type OpponentAction = { action: PokerAction; amount?: number; source: 'llm' | 'fallback' };
export type GameResponse = { gameId: string; state: GameState; opponentAction?: OpponentAction };

export async function postGame(path: string, body: object): Promise<GameResponse> {
  const response = await fetch(path, {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body),
  });
  const result = await response.json();
  if (!response.ok) throw new Error(result.error || 'Impossible de terminer cette action.');
  return result;
}

export type Theme = 'ouverture' | 'tirage';
export type Niveau = 'debutant' | 'intermediaire' | 'avance';
/** One training situation from the bank (same shape as the JSON contract in docs/PLAN_GENERATION.md). */
export type Situation = {
  id: string;
  theme: Theme;
  niveau: Niveau;
  position: string;
  cartes: string[];
  board: string[];
  pot: number;
  a_payer: number;
  historique: string;
  actions: PokerAction[];
  reference: { bonnes: PokerAction[]; acceptables: PokerAction[]; faits: string[] };
  source: 'llm' | 'repli';
  tentatives: number;
  erreurs: string[][];
  cree_le: string;
};

const suits = { s: 'spades', h: 'hearts', d: 'diamonds', c: 'clubs' } as const;

/** Converts a card code such as "Kd" or "Th" (T = 10) into card data for PlayingCard. */
export function toCard(code: string): CardData {
  const rank = code[0] === 'T' ? '10' : code[0];
  return { rank: rank as CardData['rank'], suit: suits[code[1] as keyof typeof suits] };
}

export async function fetchBanque(): Promise<Situation[]> {
  const response = await fetch('/api/banque');
  const result = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(result.error || 'Banque indisponible.');
  return result.situations;
}

export async function genererSituation(theme: Theme, niveau: Niveau): Promise<Situation> {
  const response = await fetch('/api/banque', {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ theme, niveau }),
  });
  const result = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(result.error || 'Banque indisponible.');
  return result.situation;
}

/** Streams the coach's advice: calls onToken for each piece of text, throws on a server or model error. */
export type CoachMessage = { role: 'user' | 'assistant'; content: string };

export async function streamCoach(
  gameId: string, onToken: (text: string) => void, signal: AbortSignal, messages: CoachMessage[] = [],
) {
  const body = messages.length > 0 ? { gameId, messages } : { gameId };
  const response = await fetch('/api/coach', {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body), signal,
  });
  if (!response.ok || !response.body) {
    const result = await response.json().catch(() => ({}));
    throw new Error(result.error || 'Le coach est indisponible.');
  }
  const reader = response.body.pipeThrough(new TextDecoderStream()).getReader();
  let buffer = '';
  for (;;) {
    const { done, value } = await reader.read();
    if (done) return;
    buffer += value;
    const lines = buffer.split('\n');
    buffer = lines.pop() ?? '';
    for (const line of lines.filter(Boolean)) {
      const event = JSON.parse(line);
      if (event.error) throw new Error(event.error);
      if (event.token) onToken(event.token);
    }
  }
}

export type OddsSummary = {
  pot: number;
  toCall: number;
  potOdds: number | null;
  equity: { win: number; tie: number; share: number; exact: boolean };
  outs: { count: number; byHand: Record<string, number>; nextCard: number; byRiver: number | null } | null;
};

export async function fetchOdds(gameId: string): Promise<OddsSummary> {
  const response = await fetch('/api/odds', {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ gameId }),
  });
  const result = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(result.error || 'Calcul des repères impossible.');
  return result.odds;
}

export type ModelStatus = { name: string; installed: boolean };
export type ModelRole = 'coach' | 'opponent';
export type ServerStatusData = {
  ollama: boolean; error?: string; available?: string[]; models: Record<ModelRole, ModelStatus>;
};

export async function fetchStatus(): Promise<ServerStatusData> {
  const response = await fetch('/api/status');
  const result = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(result.error || 'Serveur SensAI injoignable.');
  return result;
}

/** Switches the model a role plays with, for every request from now on; returns the new status. */
export async function switchModel(role: ModelRole, name: string): Promise<ServerStatusData> {
  const response = await fetch('/api/models', {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ role, name }),
  });
  const result = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(result.error || 'Changement de modèle impossible.');
  return result;
}

export type GlossaryEntry = { term: string; aliases: string[]; definition: string };
const definitions = new Map<string, Promise<GlossaryEntry>>();

export function defineTerm(term: string): Promise<GlossaryEntry> {
  const cached = definitions.get(term);
  if (cached) return cached;
  const request = fetch(`/api/glossary?term=${encodeURIComponent(term)}`).then(async response => {
    const result = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(result.error === 'Unknown term.' ? 'Terme absent du glossaire.' : 'Glossaire indisponible.');
    return { term: result.term, aliases: [], definition: result.definition };
  });
  definitions.set(term, request);
  request.catch(() => definitions.delete(term));
  return request;
}

export async function fetchGlossary(): Promise<GlossaryEntry[]> {
  const response = await fetch('/api/glossary');
  const result = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error('Glossaire indisponible.');
  return result.entries;
}

export type HandRanking = { rank: number; name: string; description: string; cards: CardData[] };

export async function fetchHandRankings(): Promise<HandRanking[]> {
  const response = await fetch('/api/hand-rankings');
  const result = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error('Classement des mains indisponible.');
  return result.rankings;
}

export async function saveSessionNote(hands: number, won: number, net: number, remark: string): Promise<string> {
  const response = await fetch('/api/notes', {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ hands, won, net, remark }),
  });
  const result = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(result.error || 'Impossible d’écrire dans les notes.');
  return result.line;
}

export type TrainerNiveau = 'debutant' | 'intermediaire' | 'avance';
export type TrainerTheme = 'ouverture' | 'tirage' | 'qui_gagne' | 'defense_bb';
export type TrainerVerdict = 'bon' | 'acceptable' | 'erreur';
export type TrainerActionKey = 'fold' | 'call' | 'raise' | 'moi' | 'adversaire' | 'egalite';
export type TrainerAction = { action: TrainerActionKey; libelle: string };
export type TrainerSituation = {
  id: string;
  theme: TrainerTheme;
  niveau: TrainerNiveau;
  position: string;
  cartes: string[];
  adversaire?: string[];
  board: string[];
  pot: number;
  a_payer: number;
  historique: string;
  texte: string;
  question: string;
  actions: TrainerAction[];
};
export type TrainerReference = { bonnes: TrainerActionKey[]; acceptables: TrainerActionKey[]; faits: string[] };
export type TrainerDecision = { verdict: TrainerVerdict; reference: TrainerReference };
export type TrainerResultatsTheme = Record<TrainerVerdict, number>;
export type TrainerResultats = Partial<Record<TrainerTheme, TrainerResultatsTheme>>;
export type TrainerProfil = {
  pseudo: string;
  resultats: TrainerResultats;
  exercices: number;
  themesARevoir: TrainerTheme[];
  reprise: boolean;
};
export type TrainerSession = {
  sessionId: string;
  niveau: TrainerNiveau | null;
  niveaux: { niveau: TrainerNiveau; libelle: string }[];
  profil: TrainerProfil | null;
};
export type TrainerFiche = { a_retenir: string; theme_a_revoir: string };
export type TrainerMessage = { role: 'user' | 'assistant'; content: string };
export type TrainerReprise = TrainerDecision & { situation: TrainerSituation; action: TrainerActionKey; debrief: TrainerMessage[] };
export type DebriefEvent =
  | { type: 'queued' }
  | { type: 'thinking' }
  | { type: 'token'; texte: string }
  | { type: 'outil'; nom: string }
  | { type: 'question'; question: string; choix: string[]; bonne: number | null }
  | { type: 'done' }
  | { type: 'error'; message: string };

async function postTrainer<T>(chemin: string, corps: object): Promise<T> {
  const response = await fetch(chemin, {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(corps),
  });
  const result = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(result.error || 'L’entraîneur est indisponible.');
  return result as T;
}

export function creerSession(pseudo?: string): Promise<TrainerSession> {
  return postTrainer<TrainerSession>('/api/sessions', pseudo ? { pseudo } : {});
}

export function choisirNiveau(sessionId: string, reponse: string): Promise<{ niveau: TrainerNiveau; raison: string | null }> {
  return postTrainer(`/api/sessions/${sessionId}/niveau`, { reponse });
}

export async function nouvelleSituation(sessionId: string): Promise<TrainerSituation> {
  const { situation } = await postTrainer<{ numero: number; situation: TrainerSituation }>(`/api/sessions/${sessionId}/situations`, {});
  return situation;
}

export function decider(sessionId: string, action: TrainerActionKey): Promise<TrainerDecision> {
  return postTrainer<TrainerDecision>(`/api/sessions/${sessionId}/decision`, { action });
}

export async function ecrireFiche(sessionId: string): Promise<TrainerFiche> {
  const { fiche } = await postTrainer<{ fiche: TrainerFiche }>(`/api/sessions/${sessionId}/fiche`, {});
  return fiche;
}

export function reprendreDebrief(sessionId: string): Promise<TrainerReprise> {
  return postTrainer<TrainerReprise>(`/api/sessions/${sessionId}/reprendre`, {});
}

function lireEvenement(ligne: string): DebriefEvent | null {
  const evenement = JSON.parse(ligne) as Record<string, unknown>;
  if ('error' in evenement) return { type: 'error', message: String(evenement.error) };
  if ('queued' in evenement) return { type: 'queued' };
  if ('thinking' in evenement) return { type: 'thinking' };
  if (typeof evenement.token === 'string') return { type: 'token', texte: evenement.token };
  if ('done' in evenement) return { type: 'done' };
  if (evenement.outil && typeof evenement.outil === 'object') {
    return { type: 'outil', nom: String((evenement.outil as { name?: unknown }).name ?? 'outil') };
  }
  if (evenement.question && typeof evenement.question === 'object') {
    const { question, choix, bonne } = evenement.question as { question?: unknown; choix?: unknown; bonne?: unknown };
    return { type: 'question', question: String(question), choix: Array.isArray(choix) ? choix.map(String) : [],
      bonne: typeof bonne === 'number' ? bonne : null };
  }
  return null;
}

export async function envoyerDebrief(
  sessionId: string, texte: string, onEvent: (event: DebriefEvent) => void, signal?: AbortSignal,
): Promise<void> {
  const response = await fetch(`/api/sessions/${sessionId}/messages`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ texte }), signal,
  });
  if (!response.ok || !response.body) {
    const result = await response.json().catch(() => ({}));
    throw new Error(result.error || 'Le débrief est indisponible.');
  }
  const reader = response.body.pipeThrough(new TextDecoderStream()).getReader();
  let buffer = '';
  const traiter = (ligne: string) => {
    const evenement = lireEvenement(ligne);
    if (evenement) onEvent(evenement);
  };
  for (;;) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += value;
    const lignes = buffer.split('\n');
    buffer = lignes.pop() ?? '';
    lignes.filter(Boolean).forEach(traiter);
  }
  if (buffer.trim()) traiter(buffer);
}
