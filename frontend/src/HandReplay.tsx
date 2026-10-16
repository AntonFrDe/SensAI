import { useEffect, useRef, useState, type KeyboardEvent } from 'react';
import CommunityCards from './CommunityCards';
import HandBadge from './HandBadge';
import { describeEntry } from './HandHistory';
import { phaseLabels } from './HandInfo';
import PlayingCard from './PlayingCard';
import { replaySteps, type PlayedHand } from './handLog';

export type HandReplayProps = { hand: PlayedHand; onClose: () => void };

const formatter = new Intl.NumberFormat('fr-FR');

function resultText(hand: PlayedHand): string {
  if (hand.net > 0) return `Vous gagnez ${formatter.format(hand.net)} jetons.`;
  if (hand.net < 0) return `Vous perdez ${formatter.format(-hand.net)} jetons.`;
  return 'Main sans gain ni perte.';
}

export default function HandReplay({ hand, onClose }: HandReplayProps) {
  const steps = replaySteps(hand);
  const [index, setIndex] = useState(0);
  const box = useRef<HTMLElement | null>(null);
  useEffect(() => box.current?.focus(), []);
  const step = steps[index];
  const last = steps.length - 1;
  const go = (next: number) => setIndex(Math.min(Math.max(next, 0), last));

  function onKeyDown(event: KeyboardEvent<HTMLElement>) {
    const moves: Record<string, number> = { ArrowRight: index + 1, ArrowLeft: index - 1, Home: 0, End: last };
    if (event.key === 'Escape') onClose();
    else if (event.key in moves) {
      event.preventDefault();
      go(moves[event.key]);
    }
  }

  return (
    <section ref={box} className="hand-replay" aria-label={`Revoir la main n°${hand.number}`} tabIndex={-1} onKeyDown={onKeyDown}>
      <header className="replay-head">
        <h3>Main n°{hand.number}</h3>
        <button type="button" className="link-button" onClick={onClose}>Fermer</button>
      </header>
      <p className="replay-street">{step.showdown ? 'Fin de la main' : phaseLabels[step.street]}</p>
      <div className="replay-table">
        <div className="cards" role="group" aria-label="Cartes de l’IA">
          {step.showdown && hand.opponentCards.length > 0
            ? hand.opponentCards.map(card => <PlayingCard key={card.rank + card.suit} card={card} />)
            : <><PlayingCard /><PlayingCard /></>}
        </div>
        <CommunityCards cards={step.board} />
        <div className="cards" role="group" aria-label="Vos cartes privées">
          {hand.playerCards.map(card => <PlayingCard key={card.rank + card.suit} card={card} />)}
        </div>
      </div>
      <p className="replay-action" aria-live="polite">
        {step.entry ? describeEntry(step.entry) : step.showdown ? resultText(hand) : 'Les cartes sont distribuées.'}
      </p>
      {step.showdown && <div className="replay-hands">
        {hand.playerHand && <span className="replay-owner">Vous <HandBadge hand={hand.playerHand} owner="Votre main" /></span>}
        {hand.opponentHand && <span className="replay-owner">IA <HandBadge hand={hand.opponentHand} owner="Main de l’IA" /></span>}
      </div>}
      <div className="replay-controls" role="group" aria-label="Navigation dans la main">
        <button type="button" onClick={() => go(0)} disabled={index === 0}>Début</button>
        <button type="button" onClick={() => go(index - 1)} disabled={index === 0}>Précédent</button>
        <span className="replay-count">Étape {index + 1} / {steps.length}</span>
        <button type="button" onClick={() => go(index + 1)} disabled={index === last}>Suivant</button>
        <button type="button" onClick={() => go(last)} disabled={index === last}>Fin</button>
      </div>
    </section>
  );
}
