import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it, vi } from 'vitest';
import CoachPanel from './CoachPanel';

function ndjson(...lines: object[]): Response {
  return new Response(lines.map(line => JSON.stringify(line)).join('\n') + '\n');
}

function bodyOf(call: unknown[]): unknown {
  return JSON.parse(String((call[1] as RequestInit).body));
}

describe('CoachPanel', () => {
  it('streams the first advice for the current decision', async () => {
    const fetchMock = vi.spyOn(globalThis, 'fetch').mockResolvedValue(ndjson({ token: 'Suivez, ' }, { token: 'la cote est bonne.' }, { done: {} }));
    render(<CoachPanel gameId="g1" available />);
    await userEvent.click(screen.getByRole('button', { name: 'Demander conseil' }));
    expect(await screen.findByText('Suivez, la cote est bonne.')).toBeInTheDocument();
    expect(bodyOf(fetchMock.mock.calls[0])).toEqual({ gameId: 'g1' });
  });

  it('sends follow-up questions with the conversation so far', async () => {
    const fetchMock = vi.spyOn(globalThis, 'fetch')
      .mockResolvedValueOnce(ndjson({ token: 'Suivez.' }))
      .mockResolvedValueOnce(ndjson({ token: 'Une relance isole votre adversaire.' }));
    render(<CoachPanel gameId="g1" available />);
    await userEvent.click(screen.getByRole('button', { name: 'Demander conseil' }));
    await userEvent.click(await screen.findByRole('button', { name: 'Et si je relance ?' }));
    expect(await screen.findByText('Une relance isole votre adversaire.')).toBeInTheDocument();
    expect(bodyOf(fetchMock.mock.calls[1])).toEqual({
      gameId: 'g1',
      messages: [{ role: 'assistant', content: 'Suivez.' }, { role: 'user', content: 'Et si je relance ?' }],
    });
    expect(screen.getAllByRole('listitem').map(item => item.textContent)).toEqual([
      'SensAISuivez.', 'VousEt si je relance ?', 'SensAIUne relance isole votre adversaire.',
    ]);
  });

  it('sends a typed question', async () => {
    const fetchMock = vi.spyOn(globalThis, 'fetch')
      .mockResolvedValueOnce(ndjson({ token: 'Couchez-vous.' }))
      .mockResolvedValueOnce(ndjson({ token: 'Avec AK, suivez.' }));
    render(<CoachPanel gameId="g1" available />);
    await userEvent.click(screen.getByRole('button', { name: 'Demander conseil' }));
    await userEvent.type(await screen.findByRole('textbox', { name: 'Votre question' }), 'Et avec AK ?');
    await userEvent.click(screen.getByRole('button', { name: 'Envoyer' }));
    expect(await screen.findByText('Avec AK, suivez.')).toBeInTheDocument();
    expect(bodyOf(fetchMock.mock.calls[1])).toMatchObject({ messages: [{}, { role: 'user', content: 'Et avec AK ?' }] });
  });

  it('shows the error and lets you ask again', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(ndjson({ error: 'Model "qwen" is not installed.' }));
    render(<CoachPanel gameId="g1" available />);
    await userEvent.click(screen.getByRole('button', { name: 'Demander conseil' }));
    expect(await screen.findByRole('alert')).toHaveTextContent('Model "qwen" is not installed.');
    expect(screen.getByRole('button', { name: 'Redemander' })).toBeEnabled();
    expect(screen.queryByRole('listitem')).not.toBeInTheDocument();
  });

  it('stops a long answer and keeps what was said', async () => {
    vi.spyOn(globalThis, 'fetch').mockImplementation(async (_input, init) => new Response(new ReadableStream({
      start(controller) {
        controller.enqueue(new TextEncoder().encode('{"token": "Le début"}\n'));
        init?.signal?.addEventListener('abort', () => controller.error(new DOMException('Aborted', 'AbortError')));
      },
    })));
    render(<CoachPanel gameId="g1" available />);
    await userEvent.click(screen.getByRole('button', { name: 'Demander conseil' }));
    expect(await screen.findByText('Le début')).toBeInTheDocument();
    await userEvent.click(screen.getByRole('button', { name: 'Arrêter' }));
    await waitFor(() => expect(screen.queryByRole('button', { name: 'Arrêter' })).not.toBeInTheDocument());
    expect(screen.getByText('Le début')).toBeInTheDocument();
    expect(screen.queryByRole('alert')).not.toBeInTheDocument();
  });

  it('waits for your turn', () => {
    render(<CoachPanel gameId="g1" available={false} />);
    expect(screen.getByText('Le coach répond quand c’est à vous de jouer.')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Demander conseil' })).toBeDisabled();
  });
});
