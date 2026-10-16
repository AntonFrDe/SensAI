import { fireEvent, render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it, vi } from 'vitest';
import GlossaryScreen from './GlossaryScreen';
import Term from './Term';

describe('Term', () => {
  it('fetches the definition once and toggles it', async () => {
    const fetchMock = vi.spyOn(globalThis, 'fetch').mockResolvedValue(Response.json({ term: 'Kicker', definition: 'Carte d’accompagnement.' }));
    render(<p>Votre <Term term="kicker">kicker</Term> compte.</p>);
    const button = screen.getByRole('button', { name: 'kicker' });
    await userEvent.click(button);
    expect(await screen.findByRole('note', { name: 'Définition : kicker' })).toHaveTextContent('Carte d’accompagnement.');
    expect(button).toHaveAttribute('aria-expanded', 'true');
    await userEvent.click(button);
    expect(screen.queryByRole('note')).not.toBeInTheDocument();
    await userEvent.click(button);
    expect(screen.getByRole('note')).toHaveTextContent('Carte d’accompagnement.');
    expect(fetchMock).toHaveBeenCalledOnce();
    expect(String(fetchMock.mock.calls[0][0])).toBe('/api/glossary?term=kicker');
  });

  it('closes on Escape and explains a missing term', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(Response.json({ error: 'Unknown term.' }, { status: 404 }));
    render(<Term term="inconnu-xyz">inconnu</Term>);
    await userEvent.click(screen.getByRole('button', { name: 'inconnu' }));
    expect(await screen.findByText('Terme absent du glossaire.')).toBeInTheDocument();
    fireEvent.keyDown(screen.getByRole('button', { name: 'inconnu' }), { key: 'Escape' });
    expect(screen.queryByRole('note')).not.toBeInTheDocument();
  });
});

describe('GlossaryScreen', () => {
  it('filters the entries by term or alias, ignoring accents', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(Response.json({ entries: [
      { term: 'Bouton', aliases: ['Dealer button'], definition: 'Marque le donneur.' },
      { term: 'Équité', aliases: [], definition: 'Part du pot qui vous revient en moyenne.' },
      { term: 'Flop', aliases: [], definition: 'Les trois premières cartes communes.' },
    ] }));
    const onBack = vi.fn();
    render(<GlossaryScreen onBack={onBack} />);
    expect(await screen.findByText('3 termes')).toBeInTheDocument();
    await userEvent.type(screen.getByRole('searchbox', { name: 'Chercher un terme' }), 'equi');
    expect(screen.getByText('1 terme')).toBeInTheDocument();
    expect(screen.getByText('Part du pot qui vous revient en moyenne.')).toBeInTheDocument();
    await userEvent.clear(screen.getByRole('searchbox'));
    await userEvent.type(screen.getByRole('searchbox'), 'dealer');
    expect(screen.getByText('Marque le donneur.')).toBeInTheDocument();
    await userEvent.click(screen.getByRole('button', { name: '← Accueil' }));
    expect(onBack).toHaveBeenCalledOnce();
  });

  it('reports an unavailable glossary', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(Response.json({}, { status: 500 }));
    render(<GlossaryScreen onBack={vi.fn()} />);
    expect(await screen.findByRole('alert')).toHaveTextContent('Glossaire indisponible.');
  });
});
