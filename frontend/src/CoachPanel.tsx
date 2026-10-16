import { useEffect, useRef, useState, type FormEvent } from 'react';
import { streamCoach, type CoachMessage } from './api';

export type CoachPanelProps = { gameId: string; available: boolean };

const suggestions = ['Pourquoi ce choix ?', 'Et si je relance ?', 'Quelle est ma cote du pot ?'];
const speakers = { user: 'Vous', assistant: 'SensAI' };

function appendToLast(messages: CoachMessage[], text: string): CoachMessage[] {
  const last = messages[messages.length - 1];
  return [...messages.slice(0, -1), { ...last, content: last.content + text }];
}

function withoutEmptyAnswer(messages: CoachMessage[]): CoachMessage[] {
  const last = messages[messages.length - 1];
  return last?.role === 'assistant' && !last.content ? messages.slice(0, -1) : messages;
}

/** Advice on the current decision. Remount it (new `key`) when the table changes: the advice would be stale. */
export default function CoachPanel({ gameId, available }: CoachPanelProps) {
  const [messages, setMessages] = useState<CoachMessage[]>([]);
  const [status, setStatus] = useState<'idle' | 'loading' | 'done' | 'error'>('idle');
  const [error, setError] = useState('');
  const [draft, setDraft] = useState('');
  const controller = useRef<AbortController | null>(null);
  const list = useRef<HTMLOListElement | null>(null);
  useEffect(() => () => controller.current?.abort(), []);
  useEffect(() => {
    if (list.current) list.current.scrollTop = list.current.scrollHeight;
  }, [messages]);

  async function ask(question?: string) {
    const history: CoachMessage[] = question && messages.length > 0 ? [...messages, { role: 'user', content: question }] : [];
    const current = new AbortController();
    controller.current = current;
    setMessages([...history, { role: 'assistant', content: '' }]);
    setStatus('loading');
    setError('');
    setDraft('');
    try {
      await streamCoach(gameId, text => setMessages(previous => appendToLast(previous, text)), current.signal, history);
      setStatus('done');
    } catch (cause) {
      setMessages(previous => withoutEmptyAnswer(previous));
      if (current.signal.aborted) {
        setStatus('done');
        return;
      }
      setError(cause instanceof Error ? cause.message : 'Le coach est indisponible.');
      setStatus('error');
    }
  }

  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (draft.trim()) void ask(draft.trim());
  }

  const loading = status === 'loading';
  const canFollowUp = available && !loading && messages.length > 0;
  return (
    <aside className="coach" aria-label="Coach SensAI">
      <h3>Coach SensAI</h3>
      {messages.length === 0 && !loading && <p>
        {available ? 'Un doute ? Demandez un conseil sur cette décision.' : 'Le coach répond quand c’est à vous de jouer.'}
      </p>}
      {messages.length > 0 && <ol ref={list} className="coach-messages" aria-live="polite" aria-busy={loading}>
        {messages.map((message, index) => (
          <li key={index} className={`coach-message ${message.role}`}>
            <span className="speaker">{speakers[message.role]}</span>
            <p>{message.content || 'SensAI analyse la situation…'}</p>
          </li>
        ))}
      </ol>}
      {error && <p className="coach-error" role="alert">{error}</p>}
      {loading
        ? <button type="button" onClick={() => controller.current?.abort()}>Arrêter</button>
        : messages.length === 0 && <button type="button" disabled={!available} onClick={() => void ask()}>
          {status === 'error' ? 'Redemander' : 'Demander conseil'}
        </button>}
      {canFollowUp && <>
        <div className="coach-suggestions" role="group" aria-label="Questions suggérées">
          {suggestions.map(suggestion => (
            <button key={suggestion} type="button" className="suggestion" onClick={() => void ask(suggestion)}>{suggestion}</button>
          ))}
        </div>
        <form className="coach-form" onSubmit={submit}>
          <label>Votre question
            <input value={draft} maxLength={500} onChange={event => setDraft(event.target.value)} placeholder="Et si j’avais eu…" />
          </label>
          <button type="submit" disabled={!draft.trim()}>Envoyer</button>
        </form>
        <button type="button" className="link-button" onClick={() => void ask()}>Nouveau conseil</button>
      </>}
    </aside>
  );
}
