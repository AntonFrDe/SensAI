import { render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it, vi } from 'vitest';
import Banque from './Banque';
import type { Situation } from './api';

const situation: Situation = {
  id: 's1', theme: 'ouverture', niveau: 'debutant', position: 'BTN', cartes: ['Ks', '9s'], board: [], pot: 1.5,
  a_payer: 1, historique: 'Tout le monde se couche jusqu’à vous.', actions: ['fold', 'call', 'raise'],
  reference: { bonnes: ['raise'], acceptables: ['call'], faits: ['K9s fait partie de la range BTN.'] },
  source: 'llm', tentatives: 2, erreurs: [['Carte en double.']], cree_le: '2026-10-08T10:00:00',
};

describe('Banque', () => {
  it('lists the stored situations with their reference', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(Response.json({ situations: [situation] }));
    render(<Banque />);
    const card = await screen.findByRole('article', { name: 'Situation : Ouverture avant le flop, Débutant' });
    expect(within(card).getByText('LLM après 2 essais')).toBeInTheDocument();
    expect(within(card).getByRole('group', { name: 'Tes cartes privées' })).toHaveTextContent('K♠9♠');
    expect(within(card).getByText(/Relancer : bon/)).toBeInTheDocument();
    expect(within(card).getByText(/Suivre : acceptable/)).toBeInTheDocument();
    expect(within(card).getByText(/Se coucher : erreur/)).toBeInTheDocument();
    expect(within(card).getByText('Essais refusés (1)')).toBeInTheDocument();
  });

  it('adds a generated situation on top and reports failures', async () => {
    const fetchMock = vi.spyOn(globalThis, 'fetch')
      .mockResolvedValueOnce(Response.json({ situations: [] }))
      .mockResolvedValueOnce(Response.json({ situation: { ...situation, source: 'repli', tentatives: 3 } }, { status: 201 }))
      .mockResolvedValueOnce(Response.json({ error: 'Thème inconnu.' }, { status: 400 }));
    render(<Banque />);
    expect(await screen.findByText('La banque est vide pour l’instant.')).toBeInTheDocument();

    await userEvent.click(screen.getByRole('button', { name: 'Générer une situation' }));
    expect(await screen.findByText('Repli : tirée par le code')).toBeInTheDocument();
    expect(JSON.parse(String(fetchMock.mock.calls[1][1]?.body))).toEqual({ theme: 'ouverture', niveau: 'debutant' });

    await userEvent.click(screen.getByRole('button', { name: 'Générer une situation' }));
    expect(await screen.findByRole('alert')).toHaveTextContent('Thème inconnu.');
  });
});
