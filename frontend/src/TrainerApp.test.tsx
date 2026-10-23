import { act, render, screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import TrainerApp from './TrainerApp';
import { BADGES } from './progress';

const situation = {
  id: 'ab12',
  theme: 'ouverture',
  niveau: 'debutant',
  position: 'BTN',
  cartes: ['Kd', '9d'],
  board: [],
  pot: 1.5,
  a_payer: 1,
  historique: 'Tout le monde s’est couché jusqu’à toi (BTN).',
  texte: 'Table 6 joueurs, 100 blindes · tu es au bouton (BTN).\nTout le monde s’est couché jusqu’à toi (BTN). Tu as K♦ 9♦.\nAvant le flop · pot 1,5 bb, à payer 1 bb.',
  question: 'Que fais-tu ?',
  actions: [{ action: 'fold', libelle: 'se coucher' }, { action: 'raise', libelle: 'relancer' }],
};

const session = {
  sessionId: 's1',
  niveau: null,
  niveaux: [
    { niveau: 'debutant', libelle: 'Je découvre (je connais à peine les règles)' },
    { niveau: 'intermediaire', libelle: 'Je joue un peu (je connais les combinaisons)' },
    { niveau: 'avance', libelle: 'Je joue souvent (je calcule mes cotes)' },
  ],
  profil: { pseudo: 'sam', resultats: {}, exercices: 0, themesARevoir: [], reprise: false },
};

function streamOf(lignes: string[]): Response {
  const encoder = new TextEncoder();
  return new Response(new ReadableStream({
    start(controller) {
      lignes.forEach(ligne => controller.enqueue(encoder.encode(ligne)));
      controller.close();
    },
  }));
}

function routerFetch(extra: Record<string, () => Response> = {}) {
  const routes: Record<string, () => Response> = {
    'POST /api/sessions': () => Response.json(session, { status: 201 }),
    'POST /api/sessions/s1/niveau': () => Response.json({ niveau: 'debutant', raison: null }),
    'POST /api/sessions/s1/situations': () => Response.json({ numero: 1, situation }, { status: 201 }),
    'POST /api/sessions/s1/decision': () => Response.json({
      verdict: 'bon', reference: { bonnes: ['raise'], acceptables: [], faits: ['Ta main bat la plupart de celles des blindes.'] },
    }),
    'POST /api/sessions/s1/messages': () => streamOf(['{"queued": true}\n', '{"token": "Bien "}\n{"token": "joué"}\n', '{"done": null}\n']),
    'POST /api/sessions/s1/fiche': () => Response.json({ fiche: { a_retenir: 'Ouvre plus souvent au bouton.', theme_a_revoir: 'Ouverture' } }),
    ...extra,
  };
  return vi.spyOn(globalThis, 'fetch').mockImplementation(async (url, init) => {
    const cle = `${init?.method ?? 'GET'} ${String(url)}`;
    const route = routes[cle];
    if (!route) return Response.json({ error: `Route inconnue : ${cle}` }, { status: 404 });
    return route();
  });
}

beforeEach(() => {
  localStorage.clear();
  localStorage.setItem('sensai-trainer-pseudo', 'sam');
});

afterEach(() => {
  vi.restoreAllMocks();
});

describe('TrainerApp', () => {
  it('walks through a level, a situation, the verdict, the debrief and the summary', async () => {
    const fetchMock = routerFetch();
    render(<TrainerApp onNavigate={vi.fn()} />);

    await userEvent.click(await screen.findByRole('button', { name: /Je découvre/ }));
    expect(await screen.findByText(/Table 6 joueurs, 100 blindes/)).toBeInTheDocument();
    expect(screen.getByText('Pot 1,5 bb')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Se coucher/ })).toBeEnabled();

    await userEvent.click(screen.getByRole('button', { name: /Relancer/ }));
    expect(await screen.findByText('Bon coup !')).toBeInTheDocument();
    expect(screen.getByText(/la référence dit/)).toBeInTheDocument();
    expect(screen.getByText('Ta main bat la plupart de celles des blindes.')).toBeInTheDocument();
    expect(screen.getByText(/Hypothèse : ranges d’ouverture/)).toBeInTheDocument();

    await userEvent.click(screen.getByRole('button', { name: /Discuter avec Jeton/ }));
    expect(await screen.findByText(/La référence préfère : relancer/)).toBeInTheDocument();
    await userEvent.type(screen.getByRole('textbox', { name: 'Ton message à Jeton' }), 'Pourquoi ?');
    await userEvent.click(screen.getByRole('button', { name: 'Envoyer' }));
    expect(await screen.findByText('Pourquoi ?')).toBeInTheDocument();
    expect(await screen.findByText('Bien joué')).toBeInTheDocument();
    await waitFor(() => expect(screen.getByRole('button', { name: 'Envoyer' })).toBeEnabled());

    await userEvent.click(screen.getByRole('button', { name: /Terminer l’exercice/ }));
    expect(await screen.findByText('Ouvre plus souvent au bouton.')).toBeInTheDocument();
    expect(screen.getByText('Exercice terminé !')).toBeInTheDocument();

    const messages = fetchMock.mock.calls.find(([url]) => String(url).endsWith('/messages'));
    expect(JSON.parse(String(messages?.[1]?.body))).toEqual({ texte: 'Pourquoi ?' });
    const progression = JSON.parse(localStorage.getItem('sensai-trainer-progress') ?? '{}');
    expect(progression).toMatchObject({ xp: 20, bons: 1, exercices: 1, combo: 1 });
    expect(progression.badges).toEqual([BADGES.roiDuBouton]);
  });

  it('sends the pseudo once when none is stored, then opens the session with it', async () => {
    localStorage.clear();
    const fetchMock = routerFetch();
    render(<TrainerApp onNavigate={vi.fn()} />);
    await userEvent.type(await screen.findByRole('textbox', { name: 'Ton pseudo' }), 'Sam');
    await userEvent.click(screen.getByRole('button', { name: 'C’est moi' }));
    expect(await screen.findByRole('button', { name: /Je découvre/ })).toBeInTheDocument();
    const creation = fetchMock.mock.calls.find(([url]) => url === '/api/sessions');
    expect(JSON.parse(String(creation?.[1]?.body))).toEqual({ pseudo: 'Sam' });
    expect(localStorage.getItem('sensai-trainer-pseudo')).toBe('Sam');
  });

  it('refuses an invalid pseudo before calling the server', async () => {
    localStorage.clear();
    const fetchMock = routerFetch();
    render(<TrainerApp onNavigate={vi.fn()} />);
    await userEvent.type(await screen.findByRole('textbox', { name: 'Ton pseudo' }), 'Élise');
    await userEvent.click(screen.getByRole('button', { name: 'C’est moi' }));
    expect(screen.getByText(/Pseudo : 1 à 32 lettres sans accent/)).toBeInTheDocument();
    expect(fetchMock).not.toHaveBeenCalled();
  });

  it('shows a readable error when a decision is refused and keeps the situation', async () => {
    routerFetch({
      'POST /api/sessions/s1/decision': () => Response.json({ error: 'action impossible ici' }, { status: 400 }),
    });
    render(<TrainerApp onNavigate={vi.fn()} />);
    await userEvent.click(await screen.findByRole('button', { name: /Je découvre/ }));
    await userEvent.click(await screen.findByRole('button', { name: /Relancer/ }));
    expect(await screen.findByText('action impossible ici')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Relancer/ })).toBeEnabled();
  });

  it('plays the decision with the keyboard shortcut of the action', async () => {
    const fetchMock = routerFetch();
    render(<TrainerApp onNavigate={vi.fn()} />);
    await userEvent.click(await screen.findByRole('button', { name: /Je découvre/ }));
    await screen.findByRole('button', { name: /Relancer/ });
    await act(async () => {
      document.dispatchEvent(new KeyboardEvent('keydown', { key: 'r' }));
    });
    expect(await screen.findByText('Bon coup !')).toBeInTheDocument();
    const decision = fetchMock.mock.calls.find(([url]) => String(url).endsWith('/decision'));
    expect(JSON.parse(String(decision?.[1]?.body))).toEqual({ action: 'raise' });
  });

  it('lists the steps and keeps the later ones closed until a decision exists', async () => {
    routerFetch();
    render(<TrainerApp onNavigate={vi.fn()} />);
    const etapes = await screen.findByRole('navigation', { name: 'Étapes de l’exercice' });
    expect(within(etapes).getByRole('button', { name: 'Niveau' })).toBeEnabled();
    expect(within(etapes).getByRole('button', { name: 'Correction' })).toBeDisabled();
    expect(within(etapes).getByRole('button', { name: 'Fiche' })).toBeDisabled();
  });
});
