"""Self-hosted web UI: static page + streaming chat and multi-model comparison, stdlib only.

    python3 server.py [--model M] [--host 0.0.0.0] [--port 8000]

Binds to localhost by default. There is no authentication: --host 0.0.0.0 gives anyone on
your network access to your models.

Trainer routes (/api/sessions...): the same path as the CLI, on trainer.py; see README.md, « API de
l'entraîneur ».

RAM guard: every generation, from chat or comparison, first takes a slot from a semaphore
(config "max_parallel_models", default 1). Models that cannot get a slot wait, paused, until
a running one finishes, so two multi-GB models never sit in RAM at the same time.
"""
import argparse
import functools
import json
import queue
import random
import re
import sys
import threading
import traceback
from collections.abc import Callable
from contextlib import closing
from datetime import date
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit
from uuid import uuid4

import ai
import generation
import glossary
import poker_ai
import profils
import trainer
from llm import ROOT, LLMError, list_models, load_config, stream_chat
from mcp_client import Toolbox
from poker_api import (
    AI, HUMAN, apply_action, create_game, hand_rankings, next_hand, odds_summary, player_controls, public_game_state,
)
from poker_engine.game import Game

MAX_BODY = 1_000_000  # bytes
MAX_COMPARED = 8      # models per comparison
MAX_COACH_FOLLOW_UPS = 20
ROLES = ("user", "assistant")  # clients cannot inject "system" messages

Job = tuple[str, dict, list[dict]]  # (label, config for this model, messages)
GAME_ROUTES = ("/api/games", "/api/actions", "/api/opponent", "/api/next-hand", "/api/odds", "/api/state")
BANQUE_ROUTE = "/api/banque"
NOTES_ROUTE = "/api/notes"
MAX_NOTE = 200
# The trainer: POST /api/sessions, then /api/sessions/<id>/<step> (see docs/REFONTE.md, section 5)
SESSION_ROUTE = re.compile(r"/api/sessions(?:/([0-9a-f]{32})/(niveau|situations|decision|messages|fiche|reprendre))?")
MAX_SESSIONS = 100
MAX_TEXT = 2_000  # characters of a message to the coach


class UnknownGame(Exception):
    """The request names no live game: answered with a 404."""


class UnknownSession(Exception):
    """The request names no live trainer session: answered with a 404."""


def session_summary(session: trainer.Session) -> dict:
    """What the web page needs to start: the level (or the levels to choose from) and the profile, if any."""
    profil = session.profil
    return {
        "niveau": session.niveau,
        "niveaux": [{"niveau": niveau, "libelle": libelle} for niveau, libelle in trainer.NIVEAUX.items()],
        "profil": profil and {"pseudo": profil["pseudo"], "resultats": profil["resultats"],
                              "exercices": profils.nombre_exercices(profil),
                              "themesARevoir": profils.themes_faibles(profil),
                              "reprise": bool(profil["dernier_debrief"])},
    }


def clean_messages(messages: object) -> list[dict]:
    """Validate a message list and return a clean copy, or raise ValueError with a user-facing reason."""
    valid = isinstance(messages, list) and messages and all(
        isinstance(m, dict) and m.get("role") in ROLES and isinstance(m.get("content"), str) for m in messages
    )
    if not valid:
        raise ValueError("Invalid messages.")
    if messages[-1]["role"] != "user" or not messages[-1]["content"].strip():
        raise ValueError("Empty message.")
    return [{"role": m["role"], "content": m["content"]} for m in messages]


def model_status(cfg: dict) -> dict:
    names = {"coach": cfg["model"], "opponent": cfg.get("opponent_model", cfg["model"])}
    try:
        installed = {m["name"] for m in list_models(cfg)}
        status = {"ollama": True}
    except LLMError as e:
        installed, status = set(), {"ollama": False, "error": str(e)}
    status["models"] = {role: {"name": name, "installed": name in installed} for role, name in names.items()}
    return status


def glossary_entries() -> list[dict]:
    entries = ((entry, glossary.define(entry.term)) for entry in glossary.ENTRIES)
    return [{"term": entry.term, "aliases": list(entry.aliases), "definition": text} for entry, text in entries if text]


def session_note(body: dict, today: date) -> str:
    counts = [body.get(key) for key in ("hands", "won", "net")]
    if any(type(value) is not int for value in counts) or not 0 <= counts[1] <= counts[0] <= 10_000:
        raise ValueError("Invalid session numbers.")
    remark = body.get("remark", "")
    if not isinstance(remark, str) or len(remark) > MAX_NOTE:
        raise ValueError(f"The remark must be text of at most {MAX_NOTE} characters.")
    hands, won, net = counts
    plural = {"mains": "s" if hands > 1 else "", "gagnées": "s" if won > 1 else ""}
    line = (f"- {today.isoformat()} : partie web, {hands} main{plural['mains']}, {won} gagnée{plural['gagnées']}, "
            f"bilan {net:+d} jetons.")
    remark = " ".join(remark.split())
    return f"{line} {remark}" if remark else line


def parse_json(raw: bytes) -> dict:
    try:
        body = json.loads(raw)
    except ValueError:
        raise ValueError("Invalid JSON.") from None
    if not isinstance(body, dict):
        raise ValueError("Invalid request.")
    return body


def parse_messages(raw: bytes) -> list[dict]:
    """Body of /api/chat: {"messages": [...]}."""
    return clean_messages(parse_json(raw).get("messages"))


def as_coach(messages: list[dict]) -> list[dict]:
    """The conversation with the documentation's context added to its last question."""
    return [*messages[:-1], {"role": "user", "content": ai.build_prompt(messages[-1]["content"])}]


def compare_jobs(body: dict, installed: set[str], cfg: dict) -> list[Job]:
    """Body of /api/compare: {"requests": [{"model": ..., "messages": [...]}, ...], "coach"?: true}.

    With "coach", every model answers as SensAI the poker coach, with the documentation's context.
    """
    parsed = parse_requests(body, installed)
    coach = body.get("coach") is True
    # keep_alive 0: with several models, each leaves RAM as soon as it has answered; a lone one stays warm
    unload = {"keep_alive": 0} if len(parsed) > 1 else {}
    system = {"system_prompt": ai.SYSTEM} if coach else {}
    return [(model, {**cfg, "model": model, **unload, **system}, as_coach(messages) if coach else messages)
            for model, messages in parsed]


def parse_requests(body: dict, installed: set[str]) -> list[tuple[str, list[dict]]]:
    reqs = body.get("requests")
    if not isinstance(reqs, list) or not 1 <= len(reqs) <= MAX_COMPARED:
        raise ValueError(f"Expected between 1 and {MAX_COMPARED} requests.")
    parsed = []
    for r in reqs:
        model = r.get("model") if isinstance(r, dict) else None
        if model not in installed:
            raise ValueError(f"Model {model!r} is not installed.")
        parsed.append((model, clean_messages(r.get("messages"))))
    if len({m for m, _ in parsed}) != len(parsed):
        raise ValueError("Each model can only appear once.")
    return parsed


class Handler(BaseHTTPRequestHandler):
    games: dict[str, Game] = {}
    games_lock = threading.Lock()
    thinking: set[str] = set()  # games whose AI opponent is deciding: one decision at a time per game
    sessions: dict[str, trainer.Session] = {}
    busy: set[str] = set()  # sessions handling a request: one at a time per session
    toolbox = Toolbox({})  # the MCP tools of the debrief, shared by every session; set by main()
    cfg: dict = None  # set by main()
    slots = threading.BoundedSemaphore(1)  # replaced by main() from "max_parallel_models"

    def do_GET(self) -> None:
        if self.path == "/":
            self._send(200, (ROOT / "web" / "index.html").read_bytes(), "text/html; charset=utf-8")
        elif self.path == "/api/models":
            try:
                models = list_models(self.cfg)
            except LLMError as e:
                return self._send_json(502, {"error": str(e)})
            self._send_json(200, {"default": self.cfg["model"], "models": models})
        elif urlsplit(self.path).path == "/api/glossary":
            self._glossary(parse_qs(urlsplit(self.path).query).get("term", [None])[0])
        elif self.path == "/api/hand-rankings":
            self._send_json(200, {"rankings": hand_rankings()})
        elif self.path == "/api/status":
            self._send_json(200, model_status(self.cfg))
        elif self.path == BANQUE_ROUTE:
            situations = generation.lire_banque(self.cfg)
            self._send_json(200, {"situations": list(reversed(situations))})
        else:
            self._send_json(404, {"error": "Not found."})

    def do_POST(self) -> None:
        route = SESSION_ROUTE.fullmatch(self.path)
        if not route and self.path not in ("/api/chat", "/api/compare", "/api/coach", BANQUE_ROUTE, NOTES_ROUTE,
                                           *GAME_ROUTES):
            return self._send_json(404, {"error": "Not found."})
        # Requiring JSON forces a CORS preflight, so other websites cannot drive your models.
        if self.headers.get("Content-Type", "").split(";")[0].strip() != "application/json":
            return self._send_json(415, {"error": "Content-Type must be application/json."})
        try:
            length = int(self.headers.get("Content-Length") or 0)
            if not 0 < length <= MAX_BODY:
                raise ValueError("Empty or oversized request.")
            raw = self.rfile.read(length)
            if route and route[2] == "messages":
                return self._messages(route[1], parse_json(raw))
            if route:
                return self._send_json(*self._session_route(route[1], route[2], parse_json(raw)))
            if self.path in GAME_ROUTES:
                return self._send_json(*self._game_route(parse_json(raw)))
            if self.path == BANQUE_ROUTE:
                return self._send_json(*self._banque_route(parse_json(raw)))
            if self.path == NOTES_ROUTE:
                return self._send_json(*self._notes_route(parse_json(raw)))
            if self.path == "/api/coach":
                jobs = [self._coach_job(parse_json(raw))]
            elif self.path == "/api/chat":
                jobs = [(self.cfg["model"], self.cfg, parse_messages(raw))]
            else:
                jobs = compare_jobs(parse_json(raw), {m["name"] for m in list_models(self.cfg)}, self.cfg)
        except UnknownGame:
            return self._send_json(404, {"error": "Unknown game."})
        except UnknownSession:
            return self._send_json(404, {"error": "Unknown session."})
        except (ValueError, RuntimeError) as e:
            return self._send_json(400, {"error": str(e)})
        except LLMError as e:
            return self._send_json(502, {"error": str(e)})

        self.send_response(200)
        self.send_header("Content-Type", "application/x-ndjson")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()  # HTTP/1.0: the body ends when the connection closes
        try:
            self.run_jobs(jobs, functools.partial(self._emit_event, tagged=self.path == "/api/compare"))
        except (BrokenPipeError, ConnectionResetError):
            pass  # the browser hit Stop or closed the tab

    def _glossary(self, term: str | None) -> None:
        if term is None:
            return self._send_json(200, {"entries": glossary_entries()})
        entry, definition = glossary.lookup(term), glossary.define(term)
        if entry is None or definition is None:
            return self._send_json(404, {"error": "Unknown term."})
        self._send_json(200, {"term": entry.term, "definition": definition})

    def _game(self, body: dict) -> tuple[str, Game]:
        """The game named by the request. Call with games_lock held."""
        game_id = body.get("gameId")
        game = self.games.get(game_id) if isinstance(game_id, str) else None
        if game is None:
            raise UnknownGame
        return game_id, game

    def _game_route(self, body: dict) -> tuple[int, dict]:
        if self.path == "/api/games":
            game = create_game(body.get("options"))
            game_id = uuid4().hex
            with self.games_lock:
                if len(self.games) >= 100:
                    return 503, {"error": "Game session limit reached."}
                self.games[game_id] = game
            return 201, {"gameId": game_id, "state": public_game_state(game)}
        if self.path == "/api/opponent":
            return self._opponent_turn(body)
        with self.games_lock:
            game_id, game = self._game(body)
            if self.path == "/api/state":
                return 200, {"gameId": game_id, "state": public_game_state(game)}
            if self.path == "/api/odds":
                return 200, {"gameId": game_id, "odds": odds_summary(game)}
            if self.path == "/api/actions":
                apply_action(game, HUMAN, body.get("action"), body.get("amount"))
            else:
                next_hand(game)
            return 200, {"gameId": game_id, "state": public_game_state(game)}

    def _claim(self, session_id: str) -> trainer.Session:
        """The session named by the URL, reserved for this request; _release() frees it."""
        with self.games_lock:
            session = self.sessions.get(session_id)
            if session is None:
                raise UnknownSession
            if session_id in self.busy:
                raise ValueError("La session traite déjà une demande.")
            self.busy.add(session_id)
            return session

    def _release(self, session_id: str) -> None:
        with self.games_lock:
            self.busy.discard(session_id)

    def _session_route(self, session_id: str | None, step: str | None, body: dict) -> tuple[int, dict]:
        if step is None:
            return self._new_session(body)
        session = self._claim(session_id)
        try:
            if step == "niveau":
                return 200, self._level(session, body.get("reponse"))
            if step == "situations":
                situation = session.nouvelle_situation()
                return 201, {"numero": session.numero, "situation": trainer.vue_situation(situation)}
            if step == "decision":
                verdict = session.decider(body.get("action"))
                return 200, {"verdict": verdict, "reference": session.situation["reference"]}
            if step == "fiche":
                with self.slots:  # a model call: one RAM slot
                    return 200, {"fiche": session.ecrire_fiche()}
            last = session.reprendre()
            return 200, {"situation": trainer.vue_situation(last["situation"]), "action": last["action"],
                         "verdict": last["verdict"], "reference": last["situation"]["reference"],
                         "debrief": [{"role": m["role"], "content": m["content"]} for m in last["debrief"]
                                     if m["role"] in ROLES and m["content"]]}
        finally:
            self._release(session_id)

    def _new_session(self, body: dict) -> tuple[int, dict]:
        pseudo = body.get("pseudo")
        if pseudo is not None and not isinstance(pseudo, str):
            raise ValueError("Le pseudo doit être un texte.")
        seed = body.get("graine")
        if seed is not None and type(seed) is not int:
            raise ValueError("La graine doit être un entier.")
        profil = profils.charger(pseudo, self.cfg) if pseudo else None
        session = trainer.Session({**self.cfg, "tools": self.toolbox.specs}, self.toolbox, random.Random(seed), profil)
        session_id = uuid4().hex
        with self.games_lock:
            if len(self.sessions) >= MAX_SESSIONS:
                return 503, {"error": "Session limit reached."}
            self.sessions[session_id] = session
        return 201, {"sessionId": session_id, **session_summary(session)}

    def _level(self, session: trainer.Session, answer: object) -> dict:
        """The level from its number or name; otherwise the model classifies the plain-words answer (T5)."""
        if not isinstance(answer, str) or not answer.strip():
            raise ValueError("Réponse vide.")
        try:
            return {"niveau": session.choisir_niveau(answer), "raison": None}
        except ValueError:
            if answer.strip().isdigit():
                raise
        with self.slots:
            try:
                return session.niveau_libre(answer)
            except ValueError:
                raise ValueError("Réponse non comprise : choisis un des niveaux proposés.") from None

    def _messages(self, session_id: str, body: dict) -> None:
        """The debrief, streamed as NDJSON: queued, thinking, token, outil, question, then done or error."""
        text = body.get("texte")
        if not isinstance(text, str) or not text.strip():
            return self._send_json(400, {"error": "Message vide."})
        if len(text) > MAX_TEXT:
            return self._send_json(400, {"error": f"Message trop long (plus de {MAX_TEXT} caractères)."})
        session = self._claim(session_id)
        try:
            try:
                events = session.discuter(session.reponse(text.strip()))
            except ValueError as e:
                return self._send_json(400, {"error": str(e)})
            self.send_response(200)
            self.send_header("Content-Type", "application/x-ndjson")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            try:
                self._stream_debrief(events)
            except (BrokenPipeError, ConnectionResetError):
                pass  # the browser hit Stop or closed the tab
        finally:
            self._release(session_id)

    def _stream_debrief(self, events) -> None:
        if not self.slots.acquire(blocking=False):
            self._emit({"queued": True})
            self.slots.acquire()  # paused here until a running model releases its slot
        try:
            with closing(events):  # closing stops Ollama's generation
                for kind, data in events:
                    if kind == "outil":
                        self._emit({"outil": {"name": data[0], "arguments": data[1]}})
                    elif kind == "fin":
                        self._emit({"done": data[1]})
                    else:
                        self._emit({kind: data})
        except LLMError as e:
            self._emit({"error": str(e)})
        finally:
            self.slots.release()

    def _notes_route(self, body: dict) -> tuple[int, dict]:
        line = session_note(body, date.today())
        path = ROOT / self.cfg.get("notes_file", "notes/sessions.md")
        with self.games_lock:
            existing = path.read_text(encoding="utf-8") if path.exists() else "# Notes de jeu\n"
            path.write_text(existing.rstrip("\n") + "\n" + line + "\n", encoding="utf-8")
        return 201, {"line": line, "file": self.cfg.get("notes_file", "notes/sessions.md")}

    def _banque_route(self, body: dict) -> tuple[int, dict]:
        """One generated situation, one model call at a time (RAM guard)."""
        if body.get("theme") not in generation.THEMES:
            return 400, {"error": "Thème inconnu."}
        if body.get("niveau") not in generation.NIVEAUX:
            return 400, {"error": "Niveau inconnu."}
        with self.slots:
            return 201, {"situation": generation.generer(body["theme"], body["niveau"], self.cfg)}

    def _opponent_turn(self, body: dict) -> tuple[int, dict]:
        """One decision of the AI opponent. The model runs outside games_lock, so other games keep playing."""
        with self.games_lock:
            game_id, game = self._game(body)
            controls = player_controls(game, AI)
            if not controls["allowedActions"] or game_id in self.thinking:
                raise ValueError("It is not the AI's turn.")
            self.thinking.add(game_id)
            seen = poker_ai.situation(game, AI)
        try:
            system, prompt, schema = poker_ai.opponent_request(seen, controls)
            try:
                # a small model plays, the main one keeps the analysis (coach, generation)
                model = self.cfg.get("opponent_model", self.cfg["model"])
                cfg = {**self.cfg, "model": model, "think": False, "system_prompt": system, "format": schema}
                reply = self._complete(cfg, prompt)
            except LLMError as e:  # the hand goes on with the fallback rule
                print(f"AI opponent: {e}", file=sys.stderr)
                reply = None
            with self.games_lock:
                decision = poker_ai.parse_decision(reply, player_controls(game, AI))
                apply_action(game, AI, decision["action"], decision.get("amount"))
                return 200, {"gameId": game_id, "state": public_game_state(game), "opponentAction": decision}
        finally:
            with self.games_lock:
                self.thinking.discard(game_id)

    def _coach_job(self, body: dict) -> Job:
        """The coach's advice on the human's current decision, streamed like a chat answer."""
        with self.games_lock:
            _, game = self._game(body)
            if not player_controls(game)["allowedActions"]:
                raise ValueError("Advice is available on your turn.")
            seen = poker_ai.situation(game, HUMAN)
        prompt = poker_ai.coach_prompt(seen)
        follow_ups = clean_messages(body["messages"]) if body.get("messages") is not None else []
        if follow_ups and follow_ups[0]["role"] != "assistant":
            raise ValueError("Follow-up questions must answer the coach.")
        if len(follow_ups) > MAX_COACH_FOLLOW_UPS:
            raise ValueError("Conversation too long.")
        messages = [{"role": "user", "content": prompt}, *follow_ups]
        return self.cfg["model"], {**self.cfg, "system_prompt": ai.SYSTEM}, messages

    def _complete(self, cfg: dict, prompt: str) -> str:
        """A whole answer, generated once a RAM slot is free."""
        with self.slots:
            chunks = stream_chat([{"role": "user", "content": prompt}], cfg)
            return "".join(data for kind, data in chunks if kind == "token")

    def run_jobs(self, jobs: list[Job], emit: Callable[[str, str, object], None]) -> None:
        """Run every job in its own thread; each waits for a free RAM slot. Events reach `emit` as they happen:
        "queued" (waiting for a slot), "started", then "thinking"/"token" chunks, "done" or "error"."""
        events: queue.Queue = queue.Queue()
        cancel = threading.Event()

        def worker(name: str, cfg: dict, messages: list[dict]) -> None:
            try:
                if not self.slots.acquire(blocking=False):
                    events.put((name, "queued", True))
                    self.slots.acquire()  # paused here until a running model releases its slot
                try:
                    if cancel.is_set():  # the client left while we were waiting
                        return
                    events.put((name, "started", True))
                    with closing(stream_chat(messages, cfg)) as chunks:  # closing stops Ollama's generation
                        for kind, data in chunks:
                            if cancel.is_set():
                                return
                            events.put((name, kind, data))
                finally:
                    self.slots.release()
            except LLMError as e:
                events.put((name, "error", str(e)))
            except Exception:
                traceback.print_exc()
                events.put((name, "error", "Internal error."))
            finally:
                events.put((name, "end", None))

        for job in jobs:
            threading.Thread(target=worker, args=job, daemon=True).start()
        pending = len(jobs)
        try:
            while pending:
                name, kind, data = events.get()
                if kind == "end":
                    pending -= 1
                else:
                    emit(name, kind, data)
        finally:
            cancel.set()  # on disconnect: running models stop, waiting ones give up

    def _emit_event(self, name: str, kind: str, data: object, tagged: bool) -> None:
        self._emit({"model": name, kind: data} if tagged else {kind: data})

    def _emit(self, obj: dict) -> None:
        self.wfile.write(json.dumps(obj).encode() + b"\n")
        self.wfile.flush()

    def _send(self, code: int, body: bytes, ctype: str) -> None:
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")  # no clickjacking of the chat page
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, code: int, obj: dict) -> None:
        self._send(code, json.dumps(obj).encode(), "application/json")


def main() -> None:
    ap = argparse.ArgumentParser(description="SensAI web UI")
    ap.add_argument("--model", help="override the model from config.json")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--no-tools", action="store_true", help="no MCP server for the trainer's debrief")
    args = ap.parse_args()

    Handler.cfg = load_config()
    if args.model:
        Handler.cfg["model"] = args.model
    ai.EMBED_URL = f"{Handler.cfg['ollama_url']}/api/embed"
    Handler.toolbox = Toolbox({} if args.no_tools else Handler.cfg.get("mcp_servers", {}))
    for warning in Handler.toolbox.warnings:  # a broken tool server must not stop the server
        print(f"Outils indisponibles, {warning}", file=sys.stderr)
    parallel = Handler.cfg.get("max_parallel_models", 1)
    Handler.slots = threading.BoundedSemaphore(parallel)
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"SensAI on http://{args.host}:{args.port}  (model: {Handler.cfg['model']}, {parallel} at a time)", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        Handler.toolbox.close()


if __name__ == "__main__":
    main()
