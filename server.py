"""Self-hosted web UI: static page + streaming chat and multi-model comparison, stdlib only.

    python3 server.py [--model M] [--host 0.0.0.0] [--port 8000]

Binds to localhost by default. There is no authentication: --host 0.0.0.0 gives anyone on
your network access to your models.

RAM guard: every generation, from chat or comparison, first takes a slot from a semaphore
(config "max_parallel_models", default 1). Models that cannot get a slot wait, paused, until
a running one finishes, so two multi-GB models never sit in RAM at the same time.
"""
import argparse
import functools
import json
import queue
import threading
import traceback
from collections.abc import Callable
from contextlib import closing
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from uuid import uuid4

from llm import ROOT, LLMError, list_models, load_config, stream_chat
from poker_api import player_controls, public_game_state
from poker_engine.game import Game
from poker_engine.player import Player

MAX_BODY = 1_000_000  # bytes
MAX_COMPARED = 8      # models per comparison
ROLES = ("user", "assistant")  # clients cannot inject "system" messages

Job = tuple[str, dict, list[dict]]  # (label, config for this model, messages)


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


def parse_requests(raw: bytes, installed: set[str]) -> list[tuple[str, list[dict]]]:
    """Body of /api/compare: {"requests": [{"model": ..., "messages": [...]}, ...]}."""
    reqs = parse_json(raw).get("requests")
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
        else:
            self._send_json(404, {"error": "Not found."})

    def do_POST(self) -> None:
        if self.path not in ("/api/chat", "/api/compare", "/api/games", "/api/actions"):
            return self._send_json(404, {"error": "Not found."})
        # Requiring JSON forces a CORS preflight, so other websites cannot drive your models.
        if self.headers.get("Content-Type", "").split(";")[0].strip() != "application/json":
            return self._send_json(415, {"error": "Content-Type must be application/json."})
        try:
            length = int(self.headers.get("Content-Length") or 0)
            if not 0 < length <= MAX_BODY:
                raise ValueError("Empty or oversized request.")
            raw = self.rfile.read(length)
            if self.path == "/api/actions":
                body = parse_json(raw)
                with self.games_lock:
                    game_id = body.get("gameId")
                    game = self.games.get(game_id) if isinstance(game_id, str) else None
                    if game is None:
                        return self._send_json(404, {"error": "Unknown game."})
                    controls = player_controls(game)
                    action = body.get("action")
                    if action not in controls["allowedActions"]:
                        raise ValueError("Action unavailable on your turn.")
                    method = getattr(game, "raise_bet" if action == "raise" else action)
                    if action in ("bet", "raise"):
                        amount = body.get("amount")
                        if type(amount) is not int or not controls["minAmount"] <= amount <= controls["maxAmount"]:
                            raise ValueError("Invalid bet amount.")
                        method(amount)
                    else:
                        method()
                    result = {"gameId": game_id, "state": public_game_state(game)}
                return self._send_json(200, result)
            if self.path == "/api/games":
                parse_json(raw)
                game = Game([Player("Vous", 1000), Player("IA", 1000)])
                game.start_hand()
                game_id = uuid4().hex
                with self.games_lock:
                    if len(self.games) >= 100:
                        return self._send_json(503, {"error": "Game session limit reached."})
                    self.games[game_id] = game
                return self._send_json(201, {"gameId": game_id, "state": public_game_state(game)})
            if self.path == "/api/chat":
                jobs = [(self.cfg["model"], self.cfg, parse_messages(raw))]
            else:
                installed = {m["name"] for m in list_models(self.cfg)}
                # keep_alive 0: each model leaves RAM as soon as it has answered
                jobs = [
                    (model, {**self.cfg, "model": model, "keep_alive": 0}, messages)
                    for model, messages in parse_requests(raw, installed)
                ]
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
    args = ap.parse_args()

    Handler.cfg = load_config()
    if args.model:
        Handler.cfg["model"] = args.model
    parallel = Handler.cfg.get("max_parallel_models", 1)
    Handler.slots = threading.BoundedSemaphore(parallel)
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"SensAI on http://{args.host}:{args.port}  (model: {Handler.cfg['model']}, {parallel} at a time)", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
