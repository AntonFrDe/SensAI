import { useEffect, useRef, useState } from 'react';
import Banque from './Banque';
import CoachPanel from './CoachPanel';
import PokerTable from './PokerTable';
import SessionStats from './SessionStats';
import { usePreferences } from './preferences';
import { rememberGame, useSavedGame } from './savedGame';
import { useSessionStats } from './sessionStats';
import {
  defaultTableOptions, postGame, type Award, type GameResponse, type GameState, type OpponentAction, type TableOptions,
} from './api';
import GameRecords from './GameRecords';
import { useGameRecords } from './gameRecords';
import GameSummary from './GameSummary';
import GlossaryScreen from './GlossaryScreen';
import GuidedTour, { tourDoneKey } from './GuidedTour';
import HandLog from './HandLog';
import HandRankings from './HandRankings';
import { useHandLog } from './handLog';
import HomeScreen from './HomeScreen';
import JetonShell from './JetonShell';
import OddsPanel from './OddsPanel';
import PageHeader from './PageHeader';
import type { View } from './navigation';
import TrainerApp from './TrainerApp';
import { handLabels } from './HandBadge';
import { ACTION_NAMES } from './pokerTerms';
import './styles.css';

const optionsKey = 'sensai-table-options';

function loadOptions(): TableOptions {
  try {
    const saved = JSON.parse(localStorage.getItem(optionsKey) ?? 'null');
    return saved && typeof saved.stackBigBlinds === 'number' ? { ...defaultTableOptions, ...saved } : defaultTableOptions;
  } catch {
    return defaultTableOptions;
  }
}


function describeMove({ action, amount, source }: OpponentAction): string {
  const fallback = source === 'fallback' ? ' (règle de secours : réponse du modèle inutilisable)' : '';
  const name = action === 'raise' ? `${ACTION_NAMES.raise} à` : ACTION_NAMES[action];
  return `L’IA : ${name}${amount === undefined ? '' : ` ${amount}`}${fallback}.`;
}

function describeAward({ amount, winners, reason }: Award, hands?: GameState['hands']): string {
  const hand = reason === 'showdown' ? hands?.[winners[0] === 'Vous' ? 'player' : 'opponent'] : null;
  const withHand = hand ? ` avec : ${handLabels[hand.rank].toLowerCase()}` : '';
  if (winners.length > 1) return `Égalité : pot de ${amount} jetons partagé${withHand}.`;
  const who = winners[0] === 'Vous' ? 'Tu remportes' : 'L’IA remporte';
  const fold = winners[0] === 'Vous' ? ' (l’IA a fold)' : ' (tu as fold)';
  return `${who} ${amount} jetons${reason === 'fold' ? fold : withHand}.`;
}

export default function App() {
  const [view, setView] = useState<View>('trainer');
  const [game, setGame] = useState<GameResponse | null>(null);
  const [version, setVersion] = useState(0);  // remounts the coach: its advice is about one table state
  const [busy, setBusy] = useState<'' | 'player' | 'opponent'>('');
  const [error, setError] = useState('');
  const [opponentMove, setOpponentMove] = useState('');
  const inFlight = useRef(false);
  const stats = useSessionStats(game);
  const playedHands = useHandLog(game);
  const [records, clearRecords] = useGameRecords(game);
  const [options, setOptions] = useState<TableOptions>(loadOptions);
  const [savedGame, forgetSavedGame] = useSavedGame();
  const [preferences, setPreferences] = usePreferences();
  const [touring, setTouring] = useState(false);

  function offerTour() {
    if (localStorage.getItem(tourDoneKey) !== 'true') setTouring(true);
  }

  useEffect(() => {
    if (game) rememberGame(game.gameId);
  }, [game?.gameId]);

  function resumeGame() {
    if (game) {
      setView('game');
      return;
    }
    if (!savedGame) return;
    setGame(savedGame);
    setVersion(previous => previous + 1);
    setView('game');
    forgetSavedGame();
    offerTour();
  }

  function startGame(chosen: TableOptions) {
    setOptions(chosen);
    localStorage.setItem(optionsKey, JSON.stringify(chosen));
    offerTour();
    void send('/api/games', { options: chosen }, 'player');
  }

  async function send(path: string, body: object, by: 'player' | 'opponent') {
    if (inFlight.current) return;
    inFlight.current = true;
    setBusy(by);
    setError('');
    try {
      const result = await postGame(path, body);
      setGame(result);
      setVersion(previous => previous + 1);
      setView(current => (current === 'setup' ? 'game' : current));
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

  if (view === 'trainer') return <TrainerApp onNavigate={setView} />;

  let page = null;
  let atTable = false;
  if (view === 'banque') page = <Banque />;
  else if (view === 'glossary') page = <GlossaryScreen />;
  else if (view === 'rankings') page = <HandRankings />;
  else if (view === 'records') page = <GameRecords records={records} onClear={clearRecords} />;
  else if (view === 'setup' || !game || !state) {
    page = <HomeScreen options={options} busy={busy !== ''} onPlay={startGame}
      savedGame={game ? (game.state.gameOver ? null : game) : savedGame} onResume={resumeGame}
      preferences={preferences} onPreferencesChange={setPreferences} />;
  } else {
    atTable = true;
    page = <section className="game-page" aria-label="Partie">
        <h2 className="sr-only">Table de poker</h2>
        <div className="game-layout">
          <div className="table-column">
            <PokerTable {...state}
              opponentNote={opponentMove} opponentThinking={busy === 'opponent'}
              controls={{
                ...state.controls,
                onAction: busy ? undefined : (action, amount) => {
                  void send('/api/actions', { gameId: game.gameId, action, amount }, 'player');
                },
              }} />
            {state.phase === 'showdown' && <section className="result" aria-label="Résultat de la main" aria-live="polite">
              {state.awards.map((award, index) => <p key={index}>{describeAward(award, state.hands)}</p>)}
              {state.gameOver && <GameSummary hands={playedHands} playerWon={state.seats.opponent.stack === 0} />}
              <button type="button" disabled={busy !== ''} onClick={() => state.gameOver
                ? startGame(options)
                : void send('/api/next-hand', { gameId: game.gameId }, 'player')}>
                {state.gameOver ? 'Nouvelle partie' : 'Main suivante'}
              </button>
            </section>}
            <div className="game-footer">
              <button type="button" disabled={busy !== ''} onClick={() => setView('trainer')}>Retour à l’entraîneur</button>
              <button type="button" className="link-button" onClick={() => setTouring(true)}>Visite guidée</button>
            </div>
          </div>
          <div className="side-panel">
            <CoachPanel key={version} gameId={game.gameId} available={!busy && state.controls.allowedActions.length > 0} />
            <OddsPanel key={`odds-${version}`} gameId={game.gameId} available={!busy && state.controls.allowedActions.length > 0} />
            <SessionStats session={stats.session} lifetime={stats.lifetime} onResetLifetime={stats.resetLifetime} />
            <HandLog hands={playedHands} />
          </div>
        </div>
        {touring && <GuidedTour onClose={() => setTouring(false)} />}
      </section>;
  }

  return (
    <JetonShell label="SensAI">
      <div className={atTable ? 'jt-wrap jt-wrap-wide' : 'jt-wrap'}>
        <PageHeader view={view} onNavigate={setView} />
        <main className="jt-page">
          {error && <p role="alert">{error} {opponentToPlay && <button type="button" onClick={() => setError('')}>Relancer l’IA</button>}</p>}
          {page}
        </main>
      </div>
    </JetonShell>
  );
}
