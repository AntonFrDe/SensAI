import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import OddsPanel from './OddsPanel';
import type { OddsSummary } from './api';

const facingBet: OddsSummary = {
  pot: 120, toCall: 40, potOdds: 0.25, equity: { win: 0.3, tie: 0.02, share: 0.31, exact: false },
  outs: { count: 9, byHand: { Couleur: 9 }, nextCard: 9 / 47, byRiver: 0.35 },
};

describe('OddsPanel', () => {
  beforeEach(() => localStorage.clear());

  it('computes the odds on demand and compares them', async () => {
    const fetchMock = vi.spyOn(globalThis, 'fetch').mockResolvedValue(Response.json({ odds: facingBet }));
    render(<OddsPanel gameId="g1" available />);
    expect(fetchMock).not.toHaveBeenCalled();
    await userEvent.click(screen.getByRole('button', { name: 'Afficher mes repères' }));
    expect(await screen.findByText('À payer : 40 jetons pour un pot de 120.')).toBeInTheDocument();
    expect(screen.getByText(/Cote du pot/)).toHaveTextContent(/il faut 25\s% d’équité pour suivre/);
    expect(screen.getByRole('meter', { name: 'Équité' })).toHaveAttribute('aria-valuenow', '31');
    expect(screen.getByText('Suivre est rentable à long terme contre une main au hasard.')).toBeInTheDocument();
    expect(screen.getByText(/outs/)).toHaveTextContent(/9 outs \(Couleur 9\) : 19\s% à la prochaine carte, 35\s% d’ici la river\./);
    expect(JSON.parse(String(fetchMock.mock.calls[0][1]?.body))).toEqual({ gameId: 'g1' });
  });

  it('warns when calling costs too much and when there is nothing to pay', async () => {
    vi.spyOn(globalThis, 'fetch')
      .mockResolvedValueOnce(Response.json({ odds: { ...facingBet, equity: { ...facingBet.equity, share: 0.12 } } }))
      .mockResolvedValueOnce(Response.json({ odds: { ...facingBet, toCall: 0, potOdds: null, outs: null } }));
    render(<OddsPanel gameId="g1" available />);
    await userEvent.click(screen.getByRole('button', { name: 'Afficher mes repères' }));
    expect(await screen.findByText(/Suivre coûte plus/)).toBeInTheDocument();
    await userEvent.click(screen.getByRole('button', { name: 'Recalculer' }));
    expect(await screen.findByText('Rien à payer : vous pouvez checker sans risque.')).toBeInTheDocument();
    expect(screen.getByText('Pot de 120 jetons, rien à payer.')).toBeInTheDocument();
  });

  it('computes by itself at each decision once asked to', async () => {
    const fetchMock = vi.spyOn(globalThis, 'fetch').mockImplementation(async () => Response.json({ odds: facingBet }));
    const { unmount } = render(<OddsPanel gameId="g1" available />);
    await userEvent.click(screen.getByRole('checkbox', { name: 'À chaque décision' }));
    expect(await screen.findByText('À payer : 40 jetons pour un pot de 120.')).toBeInTheDocument();
    unmount();
    render(<OddsPanel gameId="g1" available />);
    expect(await screen.findByText('À payer : 40 jetons pour un pot de 120.')).toBeInTheDocument();
    expect(fetchMock).toHaveBeenCalledTimes(2);
  });

  it('waits for your turn and reports errors', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(Response.json({ error: 'Odds are available on your turn.' }, { status: 400 }));
    const { rerender } = render(<OddsPanel gameId="g1" available={false} />);
    expect(screen.getByRole('button', { name: 'Afficher mes repères' })).toBeDisabled();
    rerender(<OddsPanel gameId="g1" available />);
    await userEvent.click(screen.getByRole('button', { name: 'Afficher mes repères' }));
    expect(await screen.findByRole('alert')).toHaveTextContent('Odds are available on your turn.');
  });
});
