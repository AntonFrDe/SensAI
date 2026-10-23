import type { MouseEvent, ReactNode, RefObject } from 'react';

export type JetonShellProps = {
  label: string;
  shellRef?: RefObject<HTMLElement | null>;
  onClickCapture?: (event: MouseEvent<HTMLElement>) => void;
  children: ReactNode;
};

export default function JetonShell({ label, shellRef, onClickCapture, children }: JetonShellProps) {
  return (
    <section className="jt-app" ref={shellRef} onClickCapture={onClickCapture} aria-label={label}>
      <span className="jt-blob jt-blob-1" />
      <span className="jt-blob jt-blob-2" />
      <span className="jt-blob jt-blob-3" />
      <span className="jt-suit jt-suit-1" aria-hidden="true">♠</span>
      <span className="jt-suit jt-suit-2" aria-hidden="true">♥</span>
      <span className="jt-suit jt-suit-3" aria-hidden="true">♣</span>
      <span className="jt-suit jt-suit-4" aria-hidden="true">♦</span>
      {children}
    </section>
  );
}
