import { useEffect, useRef, useState } from 'react';
import Banque from './Banque';
import CoachPanel from './CoachPanel';
import PokerTable from './PokerTable';
import SessionStats from './SessionStats';
import { useSessionStats } from './sessionStats';
import { postGame, type Award, type GameResponse, type GameState, type OpponentAction } from './api';
import { handLabels } from './HandBadge';
import './styles.css';

const verbs = { fold: 'se couche', check: 'checke', call: 'suit', bet: 'mise', raise: 'relance à' };

function describeMove({ action, amount, source }: OpponentAction): string {
  const fallback = source === 'fallback' ? ' (règle de secours : réponse du modèle inutilisable)' : '';
  return `L’IA ${verbs[action]}${amount === undefined ? '' : ` ${amount}`}${fallback}.`;
}

function describeAward({ amount, winners, reason }: Award, hands?: GameState['hands']): string {
  const hand = reason === 'showdown' ? hands?.[winners[0] === 'Vous' ? 'player' : 'opponent'] : null;
  const withHand = hand ? ` avec : ${handLabels[hand.rank].toLowerCase()}` : '';
  if (winners.length > 1) return `Égalité : pot de ${amount} jetons partagé${withHand}.`;
  const who = winners[0] === 'Vous' ? 'Vous remportez' : 'L’IA remporte';
  return `${who} ${amount} jetons${reason === 'fold' ? ' (adversaire couché)' : withHand}.`;
}

export default function App() {
  const [view, setView] = useState<'home' | 'game' | 'banque'>('home');
  const [game, setGame] = useState<GameResponse | null>(null);
  const [version, setVersion] = useState(0);  // remounts the coach: its advice is about one table state
  const [busy, setBusy] = useState<'' | 'player' | 'opponent'>('');
  const [error, setError] = useState('');
  const [opponentMove, setOpponentMove] = useState('');
  const inFlight = useRef(false);
  const stats = useSessionStats(game);

  async function send(path: string, body: object, by: 'player' | 'opponent') {
    if (inFlight.current) return;
    inFlight.current = true;
    setBusy(by);
    setError('');
    try {
      const result = await postGame(path, body);
      setGame(result);
      setVersion(previous => previous + 1);
      setView('game');
      setOpponentMove(result.opponentAction ? describeMove(result.opponentAction) : '');  // stale once you act
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : 'Connexion au serveur impossible.');
    } finally {
      inFlight.current = false;
      setBusy('');
    }
  }

  const state = game?.state;
  const opponentToPlay = state?.currentPlayer === 'opponent' && state.phase !== 'showdown';
  useEffect(() => {
    // The server only moves the AI when asked: ask as soon as it is its turn, once per state.
    if (game && opponentToPlay && !busy && !error) void send('/api/opponent', { gameId: game.gameId }, 'opponent');
  }, [game, opponentToPlay, busy, error]);

  return (
    <main>
      <h1>SensAI Poker</h1>
      {error && <p role="alert">{error} {opponentToPlay && <button type="button" onClick={() => setError('')}>Relancer l’IA</button>}</p>}
      {view === 'banque' ? <Banque onBack={() => setView('home')} /> : view === 'home' || !game || !state ? <section aria-label="Accueil">
        <h2>Entraînez-vous au Texas Hold’em</h2>
        <p>Affrontez une IA et apprenez à comprendre vos décisions.</p>
        <button type="button" disabled={busy !== ''} onClick={() => void send('/api/games', {}, 'player')}>
          {busy ? 'Distribution…' : 'Jouer'}
        </button>
        <button type="button" onClick={() => setView('banque')}>Banque de situations</button>
      </section> : <section aria-label="Partie">
        <h2>Table de poker</h2>
        <div className="game-layout">
          <PokerTable {...state}
            opponentNote={busy === 'opponent' ? 'L’IA réfléchit…' : opponentMove}
            controls={{
              ...state.controls,
              onAction: busy ? undefined : (action, amount) => {
                void send('/api/actions', { gameId: game.gameId, action, amount }, 'player');
              },
            }} />
          <div className="side-panel">
            <CoachPanel key={version} gameId={game.gameId} available={!busy && state.controls.allowedActions.length > 0} />
            <SessionStats session={stats.session} lifetime={stats.lifetime} onResetLifetime={stats.resetLifetime} />
          </div>
        </div>
        {state.phase === 'showdown' && <section className="result" aria-label="Résultat de la main" aria-live="polite">
          {state.awards.map((award, index) => <p key={index}>{describeAward(award, state.hands)}</p>)}
          {state.gameOver && <p>Partie terminée : un joueur n’a plus de jetons.</p>}
          <button type="button" disabled={busy !== ''} onClick={() => state.gameOver
            ? void send('/api/games', {}, 'player')
            : void send('/api/next-hand', { gameId: game.gameId }, 'player')}>
            {state.gameOver ? 'Nouvelle partie' : 'Main suivante'}
          </button>
        </section>}
        <button type="button" disabled={busy !== ''} onClick={() => setView('home')}>Retour à l’accueil</button>
      </section>}
    </main>
  );
}
