import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it, vi } from 'vitest';
import VerdictScreen from './VerdictScreen';
import type { TrainerSituation } from './api';

const situation: TrainerSituation = {
  id: 'v1',
  theme: 'tirage',
  niveau: 'intermediaire',
  position: 'BB',
  cartes: ['Ah', '7h'],
  board: ['Kh', '9h', '2c'],
  pot: 6,
  a_payer: 3,
  historique: 'Au flop, ton adversaire mise 3 bb dans un pot de 6 bb.',
  texte: 'Table 6 joueurs.',
  question: 'Que fais-tu ?',
  actions: [{ action: 'fold', libelle: 'se coucher' }, { action: 'call', libelle: 'suivre' }, { action: 'raise', libelle: 'relancer' }],
};

describe('VerdictScreen', () => {
  it('shows the verdict, what the reference prefers and the facts with their source', async () => {
    const onDebrief = vi.fn();
    render(
      <VerdictScreen
        situation={situation}
        verdict="erreur"
        reference={{ bonnes: ['call'], acceptables: [], faits: ['Outs : 9', 'Chance de toucher d’ici la river : 35,0 %'] }}
        action="fold"
        gain={5}
        combo={0}
        onDebrief={onDebrief}
        onFiche={vi.fn()}
      />,
    );
    expect(screen.getByText('Oups !')).toBeInTheDocument();
    expect(screen.getByText(/la référence dit/)).toHaveTextContent('la référence dit suivre');
    expect(screen.getByText('Outs : 9')).toBeInTheDocument();
    expect(screen.getAllByText('odds.py')).toHaveLength(2);
    expect(screen.getByText(/Hypothèse : tu vois le turn et la river/)).toBeInTheDocument();
    expect(screen.getByText('+5 XP pour l’effort')).toBeInTheDocument();
    await userEvent.click(screen.getByRole('button', { name: 'Discuter avec Jeton' }));
    expect(onDebrief).toHaveBeenCalledOnce();
  });
});
