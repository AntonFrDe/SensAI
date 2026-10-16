import sys
import tempfile
import threading
from http.server import ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import server
from fake_ollama import FakeOllama, start
from llm import load_config


def main() -> None:
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8791
    ollama = f"http://127.0.0.1:{start(FakeOllama)}"
    bank = str(Path(tempfile.mkdtemp()) / "banque.jsonl")
    server.Handler.cfg = {**load_config(), "model": "ok", "opponent_model": "ok", "ollama_url": ollama, "banque_file": bank}
    server.Handler.slots = threading.BoundedSemaphore(1)
    server.Handler.log_message = lambda *args: None
    ThreadingHTTPServer(("127.0.0.1", port), server.Handler).serve_forever()


if __name__ == "__main__":
    main()
