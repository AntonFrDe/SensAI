import { useEffect, useRef, useState } from 'react';
import { streamCoach } from './api';

/** Advice on the current decision. Remount it (new `key`) when the table changes: the advice would be stale. */
export default function CoachPanel({ gameId, available }: { gameId: string; available: boolean }) {
  const [advice, setAdvice] = useState('');
  const [status, setStatus] = useState<'idle' | 'loading' | 'done' | 'error'>('idle');
  const controller = useRef<AbortController | null>(null);
  useEffect(() => () => controller.current?.abort(), []);

  async function ask() {
    controller.current = new AbortController();
    setAdvice('');
    setStatus('loading');
    try {
      await streamCoach(gameId, text => setAdvice(previous => previous + text), controller.current.signal);
      setStatus('done');
    } catch (cause) {
      if (controller.current.signal.aborted) return;
      setAdvice(cause instanceof Error ? cause.message : 'Le coach est indisponible.');
      setStatus('error');
    }
  }

  return (
    <aside className="coach" aria-label="Coach SensAI">
      <h3>Coach SensAI</h3>
      {status === 'idle' ? <p>{available ? 'Un doute ? Demandez un conseil sur cette décision.' : 'Le coach répond quand c’est à vous de jouer.'}</p>
        : <p className={status === 'error' ? 'coach-error' : 'coach-advice'} aria-live="polite" aria-busy={status === 'loading'}>
          {advice || 'SensAI analyse la situation…'}
        </p>}
      <button type="button" disabled={!available || status === 'loading'} onClick={() => void ask()}>
        {status === 'loading' ? 'Analyse en cours…' : status === 'idle' ? 'Demander conseil' : 'Redemander'}
      </button>
    </aside>
  );
}
