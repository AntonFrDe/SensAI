import type { MouseEvent, ReactNode, RefObject } from 'react';

export type JetonShellProps = {
  shellRef?: RefObject<HTMLDivElement | null>;
  onClickCapture?: (event: MouseEvent<HTMLElement>) => void;
  children: ReactNode;
};

export default function JetonShell({ shellRef, onClickCapture, children }: JetonShellProps) {
  return (
    <div className="jt-app" ref={shellRef} onClickCapture={onClickCapture}>
      <span className="jt-blob jt-blob-1" aria-hidden="true" />
      <span className="jt-blob jt-blob-2" aria-hidden="true" />
      <span className="jt-blob jt-blob-3" aria-hidden="true" />
      <span className="jt-suit jt-suit-1" aria-hidden="true">♠</span>
      <span className="jt-suit jt-suit-2" aria-hidden="true">♥</span>
      <span className="jt-suit jt-suit-3" aria-hidden="true">♣</span>
      <span className="jt-suit jt-suit-4" aria-hidden="true">♦</span>
      {children}
    </div>
  );
}
