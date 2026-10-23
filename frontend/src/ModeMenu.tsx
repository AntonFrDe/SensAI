import { useEffect, useId, useRef, useState } from 'react';
import { IconLayoutGrid } from '@tabler/icons-react';
import { modeOf, modes, type View } from './navigation';

export type ModeMenuProps = { current: View; onSelect: (view: View) => void };

export default function ModeMenu({ current, onSelect }: ModeMenuProps) {
  const [open, setOpen] = useState(false);
  const wrap = useRef<HTMLDivElement>(null);
  const toggle = useRef<HTMLButtonElement>(null);
  const listId = useId();
  const active = modeOf(current);

  useEffect(() => {
    if (!open) return undefined;
    function closeOnOutsideClick(event: MouseEvent) {
      if (wrap.current && !wrap.current.contains(event.target as Node)) setOpen(false);
    }
    function closeOnEscape(event: KeyboardEvent) {
      if (event.key !== 'Escape') return;
      setOpen(false);
      toggle.current?.focus();
    }
    document.addEventListener('mousedown', closeOnOutsideClick);
    document.addEventListener('keydown', closeOnEscape);
    return () => {
      document.removeEventListener('mousedown', closeOnOutsideClick);
      document.removeEventListener('keydown', closeOnEscape);
    };
  }, [open]);

  function choose(view: View) {
    setOpen(false);
    onSelect(view);
  }

  return (
    <div className="jt-menu" ref={wrap}>
      <button ref={toggle} type="button" className="jt-pill jt-menu-toggle" aria-expanded={open} aria-controls={listId}
        onClick={() => setOpen(!open)}>
        <IconLayoutGrid size={17} aria-hidden="true" />Plus
      </button>
      <nav id={listId} className="jt-menu-list" aria-label="Autres modes" hidden={!open}>
        {modes.map(({ view, label }) => (
          <button key={view} type="button" className="jt-menu-item" aria-current={view === active ? 'page' : undefined}
            onClick={() => choose(view)}>
            {label}
          </button>
        ))}
      </nav>
    </div>
  );
}
