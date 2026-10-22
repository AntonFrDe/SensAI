import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it, vi } from 'vitest';
import SituationScreen from './SituationScreen';
import type { TrainerSituation } from './api';

const ouverture: TrainerSituation = {
  id: 'a1',
  theme: 'ouverture',
  niveau: 'debutant',
  position: 'SB',
  cartes: ['Kd', '9d'],
  board: [],
  pot: 1.5,
  a_payer: 0.5,
  historique: 'Tout le monde s’est couché jusqu’à toi (SB).',
  texte: 'Table 6 joueurs, 100 blindes · tu es à la petite blinde (SB).',
  question: 'Que fais-tu ?',
  actions: [{ action: 'fold', libelle: 'se coucher' }, { action: 'raise', libelle: 'relancer' }],
};

const quiz: TrainerSituation = {
  ...ouverture,
  id: 'q1',
  theme: 'qui_gagne',
  position: 'CO',
  cartes: ['As', 'Ks'],
  adversaire: ['2h', '7c'],
  board: ['Qd', 'Jh', '3s', '8c', '4d'],
  pot: 0,
  a_payer: 0,
  question: 'Qui gagne ?',
  actions: [{ action: 'moi', libelle: 'tu gagnes' }, { action: 'adversaire', libelle: 'ton adversaire gagne' }],
};

describe('SituationScreen', () => {
  it('marks the seats before the player as folded and the blinds with their amount', () => {
    render(<SituationScreen situation={ouverture} pseudo="sam" numero={1} combo={0} erreur="" occupe={false} onDecider={vi.fn()} onReessayer={vi.fn()} />);
    expect(screen.getByText('UTG · couché')).toBeInTheDocument();
    expect(screen.getByText('BTN · couché')).toBeInTheDocument();
    expect(screen.getByText('BB · 1 bb')).toBeInTheDocument();
    expect(screen.getByText('Pot 1,5 bb')).toBeInTheDocument();
  });

  it('plays the action of the letter pressed', async () => {
    const onDecider = vi.fn();
    render(<SituationScreen situation={ouverture} pseudo="sam" numero={1} combo={0} erreur="" occupe={false} onDecider={onDecider} onReessayer={vi.fn()} />);
    await userEvent.keyboard('r');
    expect(onDecider).toHaveBeenCalledWith('raise');
    await userEvent.keyboard('c');
    expect(onDecider).toHaveBeenCalledTimes(1);
  });

  it('shows both hands and the board of a showdown quiz', () => {
    const { container } = render(<SituationScreen situation={quiz} pseudo="sam" numero={2} combo={3} erreur="" occupe={false} onDecider={vi.fn()} onReessayer={vi.fn()} />);
    expect(screen.getByText('Adversaire')).toBeInTheDocument();
    expect(container.querySelectorAll('.jt-c3')).toHaveLength(9);
    expect(screen.getByText('Combo x3')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Tu gagnes' })).toBeEnabled();
  });

  it('offers a retry when no situation could be drawn', async () => {
    const onReessayer = vi.fn();
    render(<SituationScreen situation={null} pseudo="sam" numero={0} combo={0} erreur="Aucune situation." occupe={false} onDecider={vi.fn()} onReessayer={onReessayer} />);
    await userEvent.click(screen.getByRole('button', { name: 'Réessayer' }));
    expect(onReessayer).toHaveBeenCalledOnce();
  });
});
