import { useEffect, useRef, useState, type KeyboardEvent } from 'react';

export type GuidedTourProps = { onClose: () => void };
export type TourStep = { title: string; text: string; target: string };

export const tourSteps: TourStep[] = [
  {
    title: 'Vos cartes et le board',
    text: 'Vos deux cartes privées sont en bas, les cartes communes au centre. Dès le flop, SensAI nomme votre main et met ses cinq cartes en évidence.',
    target: '.seat-box.bottom',
  },
  {
    title: 'Vos actions',
    text: 'Seules les actions permises sont actives. Les montants rapides (½ pot, pot, tapis) et les touches F, C, R et T vont plus vite.',
    target: '.actions',
  },
  {
    title: 'Le coach et les repères',
    text: 'Demandez conseil au coach et posez des questions de suite. « Repères » donne la cote du pot, l’équité et les outs, calculées par le code.',
    target: '.side-panel',
  },
  {
    title: 'Après chaque main',
    text: 'Revoyez une main étape par étape, suivez la courbe de votre tapis et ajoutez un bilan à vos notes de jeu.',
    target: '.hand-log',
  },
];

export const tourDoneKey = 'sensai-tour-done';

export default function GuidedTour({ onClose }: GuidedTourProps) {
  const [index, setIndex] = useState(0);
  const heading = useRef<HTMLHeadingElement | null>(null);
  const step = tourSteps[index];
  const last = index === tourSteps.length - 1;

  useEffect(() => {
    heading.current?.focus();
    const target = document.querySelector(step.target);
    target?.classList.add('tour-target');
    target?.scrollIntoView?.({ block: 'nearest', behavior: 'smooth' });
    return () => target?.classList.remove('tour-target');
  }, [step.target]);

  function finish() {
    localStorage.setItem(tourDoneKey, 'true');
    onClose();
  }

  function onKeyDown(event: KeyboardEvent<HTMLDivElement>) {
    if (event.key === 'Escape') finish();
  }

  return (
    <div className="guided-tour" role="dialog" aria-modal="false" aria-labelledby="tour-title" onKeyDown={onKeyDown}>
      <p className="tour-count">Étape {index + 1} sur {tourSteps.length}</p>
      <h3 id="tour-title" ref={heading} tabIndex={-1}>{step.title}</h3>
      <p>{step.text}</p>
      <div className="tour-actions">
        <button type="button" className="link-button" onClick={finish}>Passer la visite</button>
        <button type="button" disabled={index === 0} onClick={() => setIndex(index - 1)}>Précédent</button>
        <button type="button" className="primary" onClick={() => (last ? finish() : setIndex(index + 1))}>
          {last ? 'Terminer' : 'Suivant'}
        </button>
      </div>
    </div>
  );
}
