"""Ollama HTTP client shared by the web UI and the CLI. Stateless: the caller owns the history."""
import json
from collections.abc import Iterator
from pathlib import Path

import requests

ROOT = Path(__file__).parent


class LLMError(Exception):
    """A failure that is safe to show to the user (model missing, server down...)."""


def load_config(path: Path = ROOT / "config.json") -> dict:
    cfg = json.loads(Path(path).read_text())
    cfg["system_prompt"] = (ROOT / cfg["system_prompt_file"]).read_text().strip()
    return cfg


def stream_chat(messages: list[dict], cfg: dict) -> Iterator[tuple[str, object]]:
    """Yield ("thinking" | "token", text) as the model produces them, ("tool_calls", calls) when it asks for
    tools instead of answering, then ("done", stats)."""
    payload = {
        "model": cfg["model"],
        "stream": True,
        "options": {"num_ctx": cfg["num_ctx"]},
        "messages": [{"role": "system", "content": cfg["system_prompt"]}, *messages],
    }
    if "keep_alive" in cfg:  # 0 = unload the model from RAM as soon as it has answered
        payload["keep_alive"] = cfg["keep_alive"]
    if "format" in cfg:  # a JSON schema the answer must follow (Ollama structured output)
        payload["format"] = cfg["format"]
    if cfg.get("tools"):  # functions the model may call (Ollama tool calling)
        payload["tools"] = cfg["tools"]
    try:
        with requests.post(f"{cfg['ollama_url']}/api/chat", json=payload, stream=True, timeout=(5, 300)) as r:
            if r.status_code >= 400:
                raise LLMError(_http_error(r, cfg["model"]))
            for line in r.iter_lines():
                if not line:
                    continue
                chunk = json.loads(line)
                if "error" in chunk:
                    raise LLMError(chunk["error"])
                msg = chunk.get("message", {})
                if msg.get("thinking"):
                    yield "thinking", msg["thinking"]
                if msg.get("content"):
                    yield "token", msg["content"]
                if msg.get("tool_calls"):
                    yield "tool_calls", msg["tool_calls"]
                if chunk.get("done"):
                    n, ns = chunk.get("eval_count", 0), chunk.get("eval_duration", 0)
                    yield "done", {"tokens": n, "tok_s": round(n / ns * 1e9, 1) if ns else None}
    except requests.ConnectionError:
        raise _unreachable(cfg) from None
    except requests.Timeout:
        raise LLMError("Ollama took too long to answer.") from None
    except requests.RequestException as e:
        raise LLMError(f"Connection to Ollama lost: {e}") from None


def list_models(cfg: dict) -> list[dict]:
    """Models installed in Ollama, as [{"name": ..., "size": bytes}]."""
    try:
        r = requests.get(f"{cfg['ollama_url']}/api/tags", timeout=5)
        r.raise_for_status()
        return [{"name": m["name"], "size": m["size"]} for m in r.json()["models"]]
    except (requests.RequestException, KeyError, ValueError):
        raise _unreachable(cfg) from None


def _unreachable(cfg: dict) -> LLMError:
    return LLMError(f"Cannot reach Ollama at {cfg['ollama_url']}. Is it running? (ollama serve)")


def _http_error(r: requests.Response, model: str) -> str:
    if r.status_code == 404:
        return f'Model "{model}" is not installed. Run: ollama pull {model}'
    try:
        return r.json()["error"]
    except (ValueError, KeyError):
        return f"Ollama returned HTTP {r.status_code}."
