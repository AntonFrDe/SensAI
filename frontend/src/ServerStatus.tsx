import { useEffect, useState } from 'react';
import { fetchStatus, switchModel, type ModelRole, type ModelStatus, type ServerStatusData } from './api';

const roles = { coach: 'Coach', opponent: 'Adversaire IA' };
const pickerLabels = { coach: 'Modèle du coach', opponent: 'Modèle de l’adversaire IA' };
const consequences = {
  coach: 'le coach ne pourra pas répondre',
  opponent: 'l’IA jouera avec sa règle de secours (check, sinon suivre)',
};

type ModelLineProps = {
  role: ModelRole; model: ModelStatus; available: string[]; switching: boolean; onSwitch: (name: string) => void;
};

function ModelLine({ role, model, available, switching, onSwitch }: ModelLineProps) {
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
      {available.length > 0 && <select aria-label={pickerLabels[role]} value={model.name} disabled={switching}
        onChange={event => onSwitch(event.target.value)}>
        {/* a missing model stays listed: it is the one in use until another is picked */}
        {(available.includes(model.name) ? available : [model.name, ...available]).map(name => (
          <option key={name} value={name}>{name}</option>
        ))}
      </select>}
    </li>
  );
}

export default function ServerStatus() {
  const [status, setStatus] = useState<ServerStatusData | null>(null);
  const [error, setError] = useState('');
  const [checking, setChecking] = useState(true);
  const [switching, setSwitching] = useState(false);
  const [switchError, setSwitchError] = useState('');

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

  async function change(role: ModelRole, name: string) {
    setSwitching(true);
    setSwitchError('');
    try {
      setStatus(await switchModel(role, name));
    } catch (cause) {
      setSwitchError(cause instanceof Error ? cause.message : 'Changement de modèle impossible.');
    } finally {
      setSwitching(false);
    }
  }

  return (
    <section className="server-status" aria-label="État des modèles" aria-busy={checking}>
      <h3>État de l’IA locale</h3>
      {checking && !status && <p>Vérification d’Ollama…</p>}
      {error && <p className="status-error" role="alert">{error} Lance <code>python3 server.py</code>.</p>}
      {status && !status.ollama && <p className="status-error" role="alert">
        Ollama ne répond pas : la partie reste jouable, mais {consequences.opponent} et {consequences.coach}. Lance <code>ollama serve</code>.
      </p>}
      {status?.ollama && <ul className="model-lines">
        {(['coach', 'opponent'] as const).map(role => (
          <ModelLine key={role} role={role} model={status.models[role]} available={status.available ?? []}
            switching={switching} onSwitch={name => void change(role, name)} />
        ))}
      </ul>}
      {switchError && <p className="status-error" role="alert">{switchError}</p>}
      <button type="button" className="link-button" disabled={checking} onClick={() => void check()}>
        {checking ? 'Vérification…' : 'Revérifier'}
      </button>
    </section>
  );
}
