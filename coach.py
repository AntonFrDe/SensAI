"""Le coach : la boucle d'appels d'outils d'une réponse, sans rien afficher. Le CLI et le web la rendent chacun à
leur façon.
"""
from collections.abc import Iterator
from contextlib import closing

from llm import stream_chat
from mcp_client import Toolbox

MAX_TOOL_ROUNDS = 5  # then the model must answer with what it has


def repondre(history: list[dict], text: str, cfg: dict, toolbox: Toolbox) -> Iterator[tuple[str, object]]:
    """Stream the reply to `text`, running the tools the model asks for on the way.

    Yields ("thinking" | "token", text) as the model writes, ("outil", (name, arguments)) before each tool runs,
    then ("fin", (turn, stats)): the turn's messages (user, tool calls and results, final answer). LLMError
    propagates; closing the generator stops Ollama's generation.
    """
    turn = [{"role": "user", "content": text}]
    stats = None
    for round_ in range(MAX_TOOL_ROUNDS + 1):
        round_cfg = cfg if round_ < MAX_TOOL_ROUNDS else {**cfg, "tools": []}
        reply, calls = "", []
        with closing(stream_chat([*history, *turn], round_cfg)) as chunks:
            for kind, data in chunks:
                if kind == "tool_calls":
                    calls = [*calls, *data]
                elif kind == "done":
                    stats = data
                else:
                    reply += data if kind == "token" else ""
                    yield kind, data
        turn = [*turn, {"role": "assistant", "content": reply, **({"tool_calls": calls} if calls else {})}]
        if not calls:
            break
        for call in calls:
            name, arguments = call["function"]["name"], call["function"].get("arguments", {})
            yield "outil", (name, arguments)
            turn = [*turn, {"role": "tool", "tool_name": name, "content": toolbox.call(name, arguments)}]
    yield "fin", (turn, stats)
