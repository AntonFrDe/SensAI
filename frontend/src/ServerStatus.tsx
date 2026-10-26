import { useEffect, useState } from 'react';
import { fetchStatus, type ModelStatus, type ServerStatusData } from './api';

const roles = { coach: 'Coach', opponent: 'Adversaire IA' };
const consequences = {
  coach: 'le coach ne pourra pas répondre',
  opponent: 'l’IA jouera avec sa règle de secours (check, sinon suivre)',
};

function ModelLine({ role, model }: { role: keyof typeof roles; model: ModelStatus }) {
  const [copied, setCopied] = useState(false);
  const command = `ollama pull ${model.name}`;

  async function copy() {
    try {
      await navigator.clipboard.writeText(command);
      setCopied(true);
    } catch {
      setCopied(false);
    }
  }

  return (
    <li className={model.installed ? 'ok' : 'missing'}>
      <span aria-hidden="true">{model.installed ? '✓' : '!'}</span>
      <span>{roles[role]} : <code>{model.name}</code> {model.installed ? 'installé' : `absent, ${consequences[role]}`}</span>
      {!model.installed && <button type="button" className="link-button" onClick={() => void copy()}>
        {copied ? 'Commande copiée' : `Copier « ${command} »`}
      </button>}
    </li>
  );
}

export default function ServerStatus() {
  const [status, setStatus] = useState<ServerStatusData | null>(null);
  const [error, setError] = useState('');
  const [checking, setChecking] = useState(true);

  async function check() {
    setChecking(true);
    setError('');
    try {
      setStatus(await fetchStatus());
    } catch (cause) {
      setStatus(null);
      setError(cause instanceof Error ? cause.message : 'Serveur SensAI injoignable.');
    } finally {
      setChecking(false);
    }
  }

  useEffect(() => {
    void check();
  }, []);

  return (
    <section className="server-status" aria-label="État des modèles" aria-busy={checking}>
      <h3>État de l’IA locale</h3>
      {checking && !status && <p>Vérification d’Ollama…</p>}
      {error && <p className="status-error" role="alert">{error} Lance <code>python3 server.py</code>.</p>}
      {status && !status.ollama && <p className="status-error" role="alert">
        Ollama ne répond pas : la partie reste jouable, mais {consequences.opponent} et {consequences.coach}. Lance <code>ollama serve</code>.
      </p>}
      {status?.ollama && <ul className="model-lines">
        <ModelLine role="coach" model={status.models.coach} />
        <ModelLine role="opponent" model={status.models.opponent} />
      </ul>}
      <button type="button" className="link-button" disabled={checking} onClick={() => void check()}>
        {checking ? 'Vérification…' : 'Revérifier'}
      </button>
    </section>
  );
}
