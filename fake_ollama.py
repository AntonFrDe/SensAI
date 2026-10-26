"""Fake Ollama for the tests: streams a canned chunked reply, records requests, counts concurrent streams."""
import json
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

CHUNKS = [
    {"message": {"content": "", "thinking": "hmm"}},
    {"message": {"content": "Hel"}},
    {"message": {"content": "lo"}},
    {"message": {"content": ""}, "done": True, "eval_count": 20, "eval_duration": 2_000_000_000},
]
# What the model answers when the request carries a JSON schema (the AI opponent's decision)
DECISION = [{"message": {"content": '{"action": "call"}'}}, {"message": {"content": ""}, "done": True}]
INSTALLED = ["ok", "missing", "a", "b", "c", "slow1", "slow2", "slow3"]


class FakeOllama(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"  # like the real Ollama: the stream is chunked, so tokens arrive live
    lock = threading.Lock()
    requests: list = []   # every /api/chat body received
    active = 0            # streams generating right now
    max_active = 0        # peak of `active`: what the RAM semaphore must keep low
    tool_call = None      # {"name": ..., "arguments": {...}}: asked for whenever tools are offered and none ran yet

    @classmethod
    def reset(cls):
        cls.requests, cls.active, cls.max_active, cls.tool_call = [], 0, 0, None

    @classmethod
    def chunks_for(cls, body: dict) -> list[dict]:
        if "format" in body:
            return DECISION
        if cls.tool_call and body.get("tools") and body["messages"][-1]["role"] != "tool":
            return [{"message": {"content": "", "tool_calls": [{"function": cls.tool_call}]}},
                    {"message": {"content": ""}, "done": True, "eval_count": 5, "eval_duration": 1_000_000_000}]
        return CHUNKS

    def do_GET(self):  # /api/tags
        data = json.dumps({"models": [{"name": n, "size": 1} for n in INSTALLED]}).encode()
        self.send_response(200)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        cls = FakeOllama
        if self.path == "/api/embed":
            body = {**body, "model": "missing"}
        else:
            with cls.lock:
                cls.requests.append(body)
        if body["model"] == "missing":
            data = json.dumps({"error": "model 'missing' not found"}).encode()
            self.send_response(404)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return
        self.send_response(200)
        self.send_header("Transfer-Encoding", "chunked")
        self.end_headers()
        with cls.lock:
            cls.active += 1
            cls.max_active = max(cls.max_active, cls.active)
        try:
            for chunk in cls.chunks_for(body):
                time.sleep(0.3 if body["model"].startswith("slow") else 0.05)
                line = json.dumps(chunk).encode() + b"\n"
                self.wfile.write(b"%x\r\n%s\r\n" % (len(line), line))
            self.wfile.write(b"0\r\n\r\n")
        except (BrokenPipeError, ConnectionResetError):
            pass  # the server closed the request: generation stops
        finally:
            with cls.lock:
                cls.active -= 1

    def log_message(self, *args):
        pass


class QuietServer(ThreadingHTTPServer):
    def handle_error(self, request, client_address):
        if not isinstance(sys.exc_info()[1], (ConnectionResetError, BrokenPipeError)):  # a client hanging up is expected
            super().handle_error(request, client_address)


def start(handler):
    srv = QuietServer(("127.0.0.1", 0), handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv.server_address[1]
