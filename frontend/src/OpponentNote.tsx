import { useEffect, useState } from 'react';

export type OpponentNoteProps = { thinking: boolean; note?: string };

const slowAfter = 20;

export default function OpponentNote({ thinking, note }: OpponentNoteProps) {
  const [seconds, setSeconds] = useState(0);

  useEffect(() => {
    setSeconds(0);
    if (!thinking) return;
    const timer = window.setInterval(() => setSeconds(previous => previous + 1), 1000);
    return () => window.clearInterval(timer);
  }, [thinking]);

  if (!thinking) return <p className="ai-note" aria-live="polite">{note}</p>;
  return (
    <p className="ai-note thinking" aria-live="polite">
      <span className="thinking-dots" aria-hidden="true"><span /><span /><span /></span>
      L’IA réfléchit…<span className="elapsed"> {seconds} s</span>
      {seconds >= slowAfter && <small className="slow-hint"> Sur processeur, une décision prend souvent 15 à 40 s.</small>}
    </p>
  );
}
