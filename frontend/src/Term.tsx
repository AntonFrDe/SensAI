import { useId, useState, type KeyboardEvent, type ReactNode } from 'react';
import { defineTerm } from './api';

export type TermProps = { term: string; children: ReactNode };

export default function Term({ term, children }: TermProps) {
  const [open, setOpen] = useState(false);
  const [definition, setDefinition] = useState<string | null>(null);
  const [error, setError] = useState('');
  const id = useId();

  async function toggle() {
    if (open) {
      setOpen(false);
      return;
    }
    setOpen(true);
    if (definition !== null) return;
    try {
      setDefinition((await defineTerm(term)).definition);
      setError('');
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : 'Glossaire indisponible.');
    }
  }

  function onKeyDown(event: KeyboardEvent<HTMLSpanElement>) {
    if (event.key === 'Escape' && open) {
      event.stopPropagation();
      setOpen(false);
    }
  }

  return (
    <span className="term" onKeyDown={onKeyDown}>
      <button type="button" className="term-button" aria-expanded={open} aria-controls={id}
        title="Voir la définition" onClick={() => void toggle()}>{children}</button>
      {open && <span id={id} className="term-popover" role="note" aria-label={`Définition : ${term}`}>
        {definition ?? (error || 'Chargement de la définition…')}
      </span>}
    </span>
  );
}
