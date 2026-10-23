import { useEffect, useState } from 'react';
import { fetchGlossary, type GlossaryEntry } from './api';

function plain(text: string): string {
  return text.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
}

export default function GlossaryScreen() {
  const [entries, setEntries] = useState<GlossaryEntry[]>([]);
  const [query, setQuery] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    fetchGlossary()
      .then(list => { if (!cancelled) setEntries(list); })
      .catch(cause => { if (!cancelled) setError(cause instanceof Error ? cause.message : 'Glossaire indisponible.'); })
      .finally(() => { if (!cancelled) setLoading(false); });
    return () => { cancelled = true; };
  }, []);

  const needle = plain(query.trim());
  const shown = needle
    ? entries.filter(entry => [entry.term, ...entry.aliases].some(name => plain(name).includes(needle)))
    : entries;

  return (
    <section className="glossary" aria-label="Glossaire du poker">
      <h2>Glossaire du poker</h2>
      <label className="glossary-search">Chercher un terme
        <input type="search" value={query} onChange={event => setQuery(event.target.value)} placeholder="Ex. : kicker, flop, bouton" />
      </label>
      {error && <p role="alert">{error}</p>}
      {loading ? <p aria-live="polite">Chargement du glossaire…</p> : <>
        <p aria-live="polite">{shown.length} terme{shown.length > 1 ? 's' : ''}</p>
        <dl className="glossary-list">
          {shown.map(entry => (
            <div key={entry.term}>
              <dt>{entry.term}{entry.aliases.length > 0 && <small> ({entry.aliases.join(', ')})</small>}</dt>
              <dd>{entry.definition}</dd>
            </div>
          ))}
        </dl>
      </>}
    </section>
  );
}
