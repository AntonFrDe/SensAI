"""MCP client over stdio (JSON-RPC 2.0), standard library only: start the servers listed in the config, list their
tools in Ollama's format, and route the model's tool calls to the right server.

config.json:
    "mcp_servers": {
        "poker": {"command": ["python3", "mcp_server.py"]},
        "fichiers": {"command": ["npx", "-y", "@modelcontextprotocol/server-filesystem", "notes"],
                     "tools": ["read_text_file", "write_file", "list_directory"],   # optional allow-list
                     "hint": "Notes de jeu de l'utilisateur."}   # optional, put before each tool's description
    }
"""
import json
import subprocess

from llm import ROOT

PROTOCOL_VERSION = "2025-06-18"


class MCPError(Exception):
    """A server that cannot start or answer: the message is safe to show."""


class MCPServer:
    """One server process. Requests are sequential: one call at a time, as the chat loop needs."""

    def __init__(self, name: str, command: list[str]):
        self.name = name
        try:
            self.proc = subprocess.Popen(
                command, cwd=ROOT, text=True, encoding="utf-8", bufsize=1,
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
            )
        except OSError as e:
            raise MCPError(f"{name} : impossible de lancer {command[0]!r} ({e.strerror})") from None
        self._next_id = 0
        self.request("initialize", {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {},
            "clientInfo": {"name": "sensai-cli", "version": "1.0.0"},
        })
        self._send({"jsonrpc": "2.0", "method": "notifications/initialized"})

    def request(self, method: str, params: dict) -> dict:
        # ponytail: no timeout, a hung server blocks the turn until Ctrl-C; add a reader thread if it happens
        self._next_id += 1
        self._send({"jsonrpc": "2.0", "id": self._next_id, "method": method, "params": params})
        while line := self.proc.stdout.readline():
            try:
                message = json.loads(line)
            except ValueError:
                continue  # a stray log line on stdout
            if "method" in message:  # a request or notification from the server
                if "id" in message:  # we offer no client capability (roots, sampling...): refuse politely
                    self._send({"jsonrpc": "2.0", "id": message["id"],
                                "error": {"code": -32601, "message": "Not supported by this client"}})
                continue
            if message.get("id") != self._next_id:
                continue
            if "error" in message:
                raise MCPError(f"{self.name} : {message['error'].get('message', 'erreur inconnue')}")
            return message["result"]
        raise MCPError(f"{self.name} : le serveur s'est arrêté")

    def _send(self, message: dict) -> None:
        try:
            self.proc.stdin.write(json.dumps(message) + "\n")
            self.proc.stdin.flush()
        except (BrokenPipeError, OSError):
            raise MCPError(f"{self.name} : le serveur s'est arrêté") from None

    def close(self) -> None:
        if self.proc.poll() is None:
            self.proc.stdin.close()
            try:
                self.proc.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self.proc.kill()


class Toolbox:
    """Every tool of every configured server, under its own name (the first server wins on a clash)."""

    def __init__(self, servers: dict[str, dict]):
        self.servers: list[MCPServer] = []
        self.routes: dict[str, MCPServer] = {}
        self.specs: list[dict] = []   # Ollama's "tools" format
        self.warnings: list[str] = []
        for name, settings in servers.items():
            try:
                server = MCPServer(name, settings["command"])
                self.servers.append(server)
                tools = server.request("tools/list", {}).get("tools", [])
            except MCPError as e:
                self.warnings.append(str(e))
                continue
            allowed, hint = settings.get("tools"), settings.get("hint")
            for tool in tools:
                if (allowed is not None and tool["name"] not in allowed) or tool["name"] in self.routes:
                    continue
                self.routes[tool["name"]] = server
                self.specs.append({"type": "function", "function": {
                    "name": tool["name"],
                    "description": f"{hint} {tool.get('description', '')}" if hint else tool.get("description", ""),
                    "parameters": tool.get("inputSchema", {"type": "object", "properties": {}}),
                }})

    def call(self, name: str, arguments: object) -> str:
        """The tool's text result. Failures come back as text too, so the model can explain or retry."""
        server = self.routes.get(name)
        if server is None:
            return f"Erreur : l'outil {name!r} n'existe pas."
        try:
            result = server.request("tools/call", {"name": name, "arguments": arguments if isinstance(arguments, dict) else {}})
        except MCPError as e:
            return f"Erreur : {e}"
        text = "\n".join(part["text"] for part in result.get("content", []) if part.get("type") == "text")
        return f"Erreur : {text}" if result.get("isError") else text

    def close(self) -> None:
        for server in self.servers:
            server.close()
