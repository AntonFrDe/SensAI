export type View = 'trainer' | 'setup' | 'game' | 'banque' | 'glossary' | 'rankings' | 'records';

export type Mode = Exclude<View, 'trainer' | 'game'>;

export const modes: { view: Mode; label: string }[] = [
  { view: 'setup', label: 'Partie contre l’IA' },
  { view: 'banque', label: 'Banque de situations' },
  { view: 'glossary', label: 'Glossaire' },
  { view: 'rankings', label: 'Classement des mains' },
  { view: 'records', label: 'Mes parties' },
];

export function modeOf(view: View): Mode | null {
  if (view === 'trainer') return null;
  return view === 'game' ? 'setup' : view;
}
