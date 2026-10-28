import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it, vi } from 'vitest';
import ServerStatus from './ServerStatus';

describe('ServerStatus', () => {
  it('lists the installed and missing models with the command to install them', async () => {
    const writeText = vi.fn().mockResolvedValue(undefined);
    Object.defineProperty(navigator, 'clipboard', { value: { writeText }, configurable: true });
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(Response.json({
      ollama: true,
      models: { coach: { name: 'qwen2.5:3b', installed: true }, opponent: { name: 'qwen3:1.7b', installed: false } },
    }));
    render(<ServerStatus />);
    expect(await screen.findByText(/Coach :/)).toHaveTextContent('Coach : qwen2.5:3b installé');
    expect(screen.getByText(/Adversaire IA :/)).toHaveTextContent('absent, l’IA jouera avec sa règle de secours');
    await userEvent.click(screen.getByRole('button', { name: 'Copier « ollama pull qwen3:1.7b »' }));
    expect(writeText).toHaveBeenCalledWith('ollama pull qwen3:1.7b');
    expect(screen.getByRole('button', { name: 'Commande copiée' })).toBeInTheDocument();
  });

  it('switches the coach to another installed model', async () => {
    const both = (coach: string) => Response.json({
      ollama: true, available: ['llama3.2:3b', 'qwen3:4b'],
      models: { coach: { name: coach, installed: true }, opponent: { name: 'qwen3:4b', installed: true } },
    });
    const fetchMock = vi.spyOn(globalThis, 'fetch').mockResolvedValueOnce(both('qwen3:4b')).mockResolvedValueOnce(both('llama3.2:3b'));
    render(<ServerStatus />);
    await userEvent.selectOptions(await screen.findByRole('combobox', { name: 'Modèle du coach' }), 'llama3.2:3b');
    expect(await screen.findByText(/Coach :/)).toHaveTextContent('Coach : llama3.2:3b installé');
    expect(fetchMock.mock.calls[1][0]).toBe('/api/models');
    expect(JSON.parse(String((fetchMock.mock.calls[1][1] as RequestInit).body))).toEqual({ role: 'coach', name: 'llama3.2:3b' });
    expect(screen.getByRole('combobox', { name: 'Modèle de l’adversaire IA' })).toHaveValue('qwen3:4b');
  });

  it('says why a switch failed and keeps the current model', async () => {
    vi.spyOn(globalThis, 'fetch')
      .mockResolvedValueOnce(Response.json({
        ollama: true, available: ['a', 'b'],
        models: { coach: { name: 'a', installed: true }, opponent: { name: 'a', installed: true } },
      }))
      .mockResolvedValueOnce(Response.json({ error: "Model 'b' is not installed." }, { status: 400 }));
    render(<ServerStatus />);
    await userEvent.selectOptions(await screen.findByRole('combobox', { name: 'Modèle du coach' }), 'b');
    expect(await screen.findByRole('alert')).toHaveTextContent("Model 'b' is not installed.");
    expect(screen.getByRole('combobox', { name: 'Modèle du coach' })).toHaveValue('a');
  });

  it('explains what still works when ollama is down', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(Response.json({
      ollama: false, error: 'Cannot reach Ollama.',
      models: { coach: { name: 'a', installed: false }, opponent: { name: 'a', installed: false } },
    }));
    render(<ServerStatus />);
    expect(await screen.findByRole('alert')).toHaveTextContent(/la partie reste jouable.*ollama serve/);
    expect(screen.queryByRole('list')).not.toBeInTheDocument();
  });

  it('reports a missing backend and checks again on demand', async () => {
    const fetchMock = vi.spyOn(globalThis, 'fetch')
      .mockRejectedValueOnce(new TypeError('Failed to fetch'))
      .mockResolvedValueOnce(Response.json({
        ollama: true, models: { coach: { name: 'a', installed: true }, opponent: { name: 'a', installed: true } },
      }));
    render(<ServerStatus />);
    expect(await screen.findByRole('alert')).toHaveTextContent(/Failed to fetch.*python3 server\.py/);
    await userEvent.click(screen.getByRole('button', { name: 'Revérifier' }));
    expect(await screen.findAllByText(/installé/)).toHaveLength(2);
    expect(screen.queryByRole('alert')).not.toBeInTheDocument();
    expect(fetchMock).toHaveBeenCalledTimes(2);
  });
});
