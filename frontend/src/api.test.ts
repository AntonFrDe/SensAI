import { describe, expect, it, vi } from 'vitest';
import {
  creerSession, decider, ecrireFiche, envoyerDebrief, nouvelleSituation, postGame, streamCoach, toCard, type DebriefEvent,
} from './api';

function streamOf(chunks: string[]): ReadableStream<Uint8Array> {
  const encoder = new TextEncoder();
  return new ReadableStream({
    start(controller) {
      chunks.forEach(chunk => controller.enqueue(encoder.encode(chunk)));
      controller.close();
    },
  });
}

describe('toCard', () => {
  it('reads ranks, tens and suits', () => {
    expect(toCard('Kd')).toEqual({ rank: 'K', suit: 'diamonds' });
    expect(toCard('Th')).toEqual({ rank: '10', suit: 'hearts' });
    expect(toCard('2c')).toEqual({ rank: '2', suit: 'clubs' });
  });
});

describe('postGame', () => {
  it('posts JSON and returns the game', async () => {
    const fetchMock = vi.spyOn(globalThis, 'fetch').mockResolvedValue(Response.json({ gameId: 'g1', state: {} }));
    await expect(postGame('/api/actions', { gameId: 'g1', action: 'fold' })).resolves.toEqual({ gameId: 'g1', state: {} });
    const [path, init] = fetchMock.mock.calls[0];
    expect(path).toBe('/api/actions');
    expect(init?.method).toBe('POST');
    expect(JSON.parse(String(init?.body))).toEqual({ gameId: 'g1', action: 'fold' });
  });

  it('turns a server error into a readable message', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(Response.json({ error: 'Unknown game.' }, { status: 404 }));
    await expect(postGame('/api/actions', {})).rejects.toThrow('Unknown game.');
  });
});

describe('streamCoach', () => {
  it('joins tokens even when a line is split across chunks', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(new Response(streamOf([
      '{"token": "Sui', 'vez"}\n{"thinking": "..."}\n', '{"token": " ici"}\n{"done": true}\n',
    ])));
    const tokens: string[] = [];
    await streamCoach('g1', token => tokens.push(token), new AbortController().signal);
    expect(tokens.join('')).toBe('Suivez ici');
  });

  it('stops on an error event from the model', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(new Response(streamOf(['{"error": "Model missing"}\n'])));
    await expect(streamCoach('g1', () => {}, new AbortController().signal)).rejects.toThrow('Model missing');
  });

  it('reports a refused request', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(Response.json({ error: 'Advice is available on your turn.' }, { status: 400 }));
    await expect(streamCoach('g1', () => {}, new AbortController().signal)).rejects.toThrow('Advice is available on your turn.');
  });
});

describe('trainer api', () => {
  it('creates a session with the pseudo only when there is one', async () => {
    const fetchMock = vi.spyOn(globalThis, 'fetch').mockResolvedValue(Response.json({ sessionId: 's1', niveau: null, niveaux: [], profil: null }, { status: 201 }));
    await creerSession('sam');
    expect(JSON.parse(String(fetchMock.mock.calls[0][1]?.body))).toEqual({ pseudo: 'sam' });
    await creerSession();
    expect(JSON.parse(String(fetchMock.mock.calls[1][1]?.body))).toEqual({});
  });

  it('returns the situation from the situations route', async () => {
    const situation = { id: 'a1', theme: 'ouverture', texte: 'Table 6 joueurs', actions: [{ action: 'fold', libelle: 'se coucher' }] };
    const fetchMock = vi.spyOn(globalThis, 'fetch').mockResolvedValue(Response.json({ numero: 1, situation }, { status: 201 }));
    await expect(nouvelleSituation('s1')).resolves.toEqual(situation);
    expect(fetchMock.mock.calls[0][0]).toBe('/api/sessions/s1/situations');
  });

  it('sends the chosen action and returns the verdict', async () => {
    const fetchMock = vi.spyOn(globalThis, 'fetch').mockResolvedValue(Response.json({ verdict: 'bon', reference: { bonnes: ['raise'], acceptables: [], faits: [] } }));
    await expect(decider('s1', 'raise')).resolves.toMatchObject({ verdict: 'bon' });
    expect(JSON.parse(String(fetchMock.mock.calls[0][1]?.body))).toEqual({ action: 'raise' });
  });

  it('turns a refused step into a readable message', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(Response.json({ error: 'Décide d’abord.' }, { status: 400 }));
    await expect(ecrireFiche('s1')).rejects.toThrow('Décide d’abord.');
  });

  it('reads the debrief events of the NDJSON stream, in order', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(new Response(streamOf([
      '{"queued": true}\n{"thinking": "..."}\n{"outil": {"name": "calc", "arguments": {}}}\n',
      '{"token": "Bien"}\n{"question": {"question": "Combien ?", "choix": ["1", "2"]}}\n{"done": null}\n',
    ])));
    const events: DebriefEvent[] = [];
    await envoyerDebrief('s1', 'bonjour', event => events.push(event), new AbortController().signal);
    expect(events).toEqual([
      { type: 'queued' },
      { type: 'thinking' },
      { type: 'outil', nom: 'calc' },
      { type: 'token', texte: 'Bien' },
      { type: 'question', question: 'Combien ?', choix: ['1', '2'], bonne: null },
      { type: 'done' },
    ]);
  });

  it('passes a model error of the stream to the caller', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(new Response(streamOf(['{"error": "Ollama absent"}'])));
    const events: DebriefEvent[] = [];
    await envoyerDebrief('s1', 'bonjour', event => events.push(event));
    expect(events).toEqual([{ type: 'error', message: 'Ollama absent' }]);
  });
});
