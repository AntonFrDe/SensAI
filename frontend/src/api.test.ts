import { describe, expect, it, vi } from 'vitest';
import { postGame, streamCoach, toCard } from './api';

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
