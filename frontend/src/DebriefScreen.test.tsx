import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { afterEach, describe, expect, it, vi } from 'vitest';
import DebriefScreen from './DebriefScreen';
import type { TrainerSituation } from './api';

const situation: TrainerSituation = {
  id: 'd1',
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
  actions: [{ action: 'call', libelle: 'suivre' }],
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

afterEach(() => {
  vi.restoreAllMocks();
});

describe('DebriefScreen', () => {
  it('sends the number of the chosen answer to the control question', async () => {
    const fetchMock = vi.spyOn(globalThis, 'fetch')
      .mockResolvedValueOnce(streamOf(['{"question": {"question": "Combien d’outs ?", "choix": ["8", "9"]}}\n', '{"done": null}\n']))
      .mockResolvedValueOnce(streamOf(['{"token": "Exact."}\n', '{"done": null}\n']));
    render(
      <DebriefScreen sessionId="s1" situation={situation} verdict="bon" reference={{ bonnes: ['call'], acceptables: [], faits: [] }} onFini={vi.fn()} />,
    );
    await userEvent.click(screen.getByRole('button', { name: 'Pose-moi une question' }));
    await userEvent.click(await screen.findByRole('button', { name: '9' }));
    expect(await screen.findByText('Exact.')).toBeInTheDocument();
    const reponse = JSON.parse(String(fetchMock.mock.calls[1][1]?.body));
    expect(reponse).toEqual({ texte: '2' });
  });

  it('removes the empty answer bubble and shows the server error', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(streamOf(['{"error": "Ollama absent"}\n']));
    render(
      <DebriefScreen sessionId="s1" situation={situation} verdict="acceptable" reference={{ bonnes: [], acceptables: ['call'], faits: [] }} onFini={vi.fn()} />,
    );
    await userEvent.click(screen.getByRole('button', { name: 'Pourquoi ce verdict ?' }));
    expect(await screen.findByText('Ollama absent')).toBeInTheDocument();
    expect(document.querySelectorAll('.jt-dots')).toHaveLength(0);
  });
});
