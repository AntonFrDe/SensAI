export type Verdict = 'bon' | 'acceptable' | 'erreur';

export type Progress = {
  xp: number;
  combo: number;
  exercices: number;
  bons: number;
  serie: number;
  dernierJour: string | null;
  objectifJour: string | null;
  objectif: number;
  badges: string[];
  son: boolean;
};

export const BADGES = {
  roiDuBouton: 'Roi du bouton',
  chasseurDeTirages: 'Chasseur de tirages',
  serie: 'Série de 7 jours',
} as const;

export const XP_PAR_NIVEAU = 500;
export const OBJECTIF_JOUR = 5;
const XP_PAR_VERDICT: Record<Verdict, number> = { bon: 20, acceptable: 10, erreur: 5 };
const SERIE_BADGE = 7;
const STORAGE_KEY = 'sensai-trainer-progress';
const PSEUDO_KEY = 'sensai-trainer-pseudo';
export const PSEUDO_VALIDE = /^[a-z0-9_-]{1,32}$/;

export const PROGRESSION_INITIALE: Progress = {
  xp: 0,
  combo: 0,
  exercices: 0,
  bons: 0,
  serie: 0,
  dernierJour: null,
  objectifJour: null,
  objectif: 0,
  badges: [],
  son: true,
};

export type ExerciceNote = { verdict: Verdict; theme: string; position: string };
export type ResultatExercice = { progression: Progress; xp: number; nouveauNiveau: boolean; badges: string[] };

export function jourDe(date: Date = new Date()): string {
  const mois = String(date.getMonth() + 1).padStart(2, '0');
  const jour = String(date.getDate()).padStart(2, '0');
  return `${date.getFullYear()}-${mois}-${jour}`;
}

function veille(jour: string): string {
  const [annee, mois, quantieme] = jour.split('-').map(Number);
  return jourDe(new Date(annee, mois - 1, quantieme - 1));
}

export function niveauDe(xp: number): number {
  return Math.floor(xp / XP_PAR_NIVEAU) + 1;
}

export function avancementDuNiveau(xp: number): number {
  return (xp % XP_PAR_NIVEAU) / XP_PAR_NIVEAU;
}

export function serieEnCours(progression: Progress, aujourdhui: string): number {
  const { dernierJour, serie } = progression;
  return dernierJour === aujourdhui || dernierJour === veille(aujourdhui) ? serie : 0;
}

export function objectifDuJour(progression: Progress, aujourdhui: string): number {
  return progression.objectifJour === aujourdhui ? progression.objectif : 0;
}

export function noterExercice(progression: Progress, { verdict, theme, position }: ExerciceNote, aujourdhui: string): ResultatExercice {
  const bon = verdict === 'bon';
  const serie = progression.dernierJour === aujourdhui ? progression.serie
    : progression.dernierJour === veille(aujourdhui) ? progression.serie + 1 : 1;
  const gagnes = XP_PAR_VERDICT[verdict];
  const candidats: string[] = [];
  if (bon && theme === 'ouverture' && position === 'BTN') candidats.push(BADGES.roiDuBouton);
  if (bon && theme === 'tirage') candidats.push(BADGES.chasseurDeTirages);
  if (serie >= SERIE_BADGE) candidats.push(BADGES.serie);
  const gagnees = candidats.filter(badge => !progression.badges.includes(badge));
  const suivante: Progress = {
    ...progression,
    xp: progression.xp + gagnes,
    combo: bon ? progression.combo + 1 : 0,
    exercices: progression.exercices + 1,
    bons: progression.bons + (bon ? 1 : 0),
    serie,
    dernierJour: aujourdhui,
    objectifJour: aujourdhui,
    objectif: objectifDuJour(progression, aujourdhui) + 1,
    badges: [...progression.badges, ...gagnees],
  };
  return {
    progression: suivante,
    xp: gagnes,
    nouveauNiveau: niveauDe(suivante.xp) > niveauDe(progression.xp),
    badges: gagnees,
  };
}

export function chargerProgression(): Progress {
  try {
    const brut: unknown = JSON.parse(localStorage.getItem(STORAGE_KEY) ?? 'null');
    return brut && typeof brut === 'object' ? { ...PROGRESSION_INITIALE, ...brut } as Progress : PROGRESSION_INITIALE;
  } catch {
    return PROGRESSION_INITIALE;
  }
}

export function enregistrerProgression(progression: Progress): void {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(progression));
  } catch {
  }
}

export function lirePseudo(): string {
  try {
    return localStorage.getItem(PSEUDO_KEY) ?? '';
  } catch {
    return '';
  }
}

export function enregistrerPseudo(pseudo: string): void {
  try {
    localStorage.setItem(PSEUDO_KEY, pseudo);
  } catch {
  }
}

export function effacerPseudo(): void {
  try {
    localStorage.removeItem(PSEUDO_KEY);
  } catch {
  }
}
