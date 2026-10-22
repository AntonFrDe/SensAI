import type { TrainerNiveau, TrainerTheme, TrainerVerdict } from './api';

export const THEME_LABELS: Record<TrainerTheme, string> = {
  ouverture: 'Ouvrir ou se coucher',
  tirage: 'Suivre un tirage',
  qui_gagne: 'Qui gagne ?',
  defense_bb: 'Défendre sa grosse blinde',
};

export const SOURCE_FAITS: Record<TrainerTheme, string> = {
  ouverture: 'preflop.py',
  tirage: 'odds.py',
  qui_gagne: 'equity.py',
  defense_bb: 'equity.py',
};

export const HYPOTHESE_FAITS: Record<TrainerTheme, string> = {
  ouverture: 'ranges d’ouverture 6-max à 100 blindes, issues d’une source tierce.',
  tirage: 'tu vois le turn et la river sans nouvelle mise, sans gains implicites.',
  qui_gagne: 'mains évaluées par le code, départage par la hauteur puis le kicker.',
  defense_bb: 'équité réalisée à environ 80 % hors position, contre une range d’ouverture pondérée.',
};

export const RANG_LABELS: Record<TrainerNiveau, string> = {
  debutant: 'Je découvre',
  intermediaire: 'Je joue un peu',
  avance: 'Je joue souvent',
};

export const VERDICT_TEXTES: Record<TrainerVerdict, { titre: string; phrase: string; pts: number; humeur: 'happy' | 'think' | 'sad' }> = {
  bon: { titre: 'Bon coup !', phrase: 'Trop fort ! Tu as joué comme la référence.', pts: 20, humeur: 'happy' },
  acceptable: { titre: 'Pas mal !', phrase: 'Défendable, mais il y avait mieux.', pts: 10, humeur: 'think' },
  erreur: { titre: 'Oups !', phrase: 'Pas grave, c’est comme ça qu’on progresse.', pts: 5, humeur: 'sad' },
};

export const ACTION_LIBELLES: Record<string, string> = {
  fold: 'se coucher',
  call: 'suivre',
  raise: 'relancer',
  moi: 'tu gagnes',
  adversaire: 'ton adversaire gagne',
  egalite: 'égalité, pot partagé',
};

export const RACCOURCIS: Record<string, string> = { fold: 'F', call: 'C', raise: 'R' };
