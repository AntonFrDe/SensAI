"""SensAI in the terminal: chat with a local Ollama model, answers streamed as they are written.

    python3 main.py [--model M] [--config config.json] [--no-tools]

Commands: /reset forgets the conversation, /tools lists the tools, /quit (or Ctrl-D) leaves, Ctrl-C stops an answer.
The model can call the tools of the MCP servers listed under "mcp_servers" in the config (see mcp_client.py).
"""
import argparse
import json
import sys
from collections.abc import Iterator
from contextlib import closing

import coach
from llm import ROOT, LLMError, list_models, load_config
from mcp_client import Toolbox

DIM, RED, RESET = "\033[2m", "\033[31m", "\033[0m"


def style(text: str, code: str, stream) -> str:
    """Colour only when writing to a terminal, so pipes and files stay clean."""
    return f"{code}{text}{RESET}" if stream.isatty() else text


def fail(message: str) -> None:
    print(style(f"Erreur : {message}", RED, sys.stderr), file=sys.stderr)


def note(message: str) -> None:
    print(style(message, DIM, sys.stdout), flush=True)


def ensure_model(cfg: dict) -> None:
    """Stop early, with a useful message, if Ollama is down or the model is not installed."""
    names = [m["name"] for m in list_models(cfg)]
    accepted = {cfg["model"], cfg["model"] + ":latest"}  # Ollama resolves a bare name to :latest
    if not accepted & set(names):
        raise LLMError(
            f"Modèle \"{cfg['model']}\" introuvable. Installés : {', '.join(names) or 'aucun'}. "
            f"Pour l'installer : ollama pull {cfg['model']}"
        )


def answer(history: list[dict], text: str, cfg: dict, toolbox: Toolbox) -> list[dict] | None:
    """Print the reply to `text` as it streams, with the tools it runs on the way."""
    return show(coach.repondre(history, text, cfg, toolbox))


def show(events: Iterator[tuple[str, object]]) -> list[dict] | None:
    """Print the events of coach.repondre as they come.

    Returns the turn's messages (user, tool calls and results, final answer), or None if it failed or was cut.
    """
    turn, stats, thinking, line = None, None, False, ""
    try:
        with closing(events) as events:  # closing stops Ollama's generation
            for kind, data in events:
                if kind == "thinking" and not thinking:
                    thinking = True
                    note("[réflexion…]")
                elif kind == "token":
                    line += data
                    print(data, end="", flush=True)
                elif kind == "outil":
                    if line:
                        print()
                    thinking, line = False, ""
                    name, arguments = data
                    note(f"[outil] {name}({json.dumps(arguments, ensure_ascii=False)})")
                elif kind == "fin":
                    turn, stats = data
    except LLMError as e:
        print()  # end a half-printed answer's line
        fail(str(e))
        return None
    except KeyboardInterrupt:
        print("\n(interrompu)")
        return None
    if not turn[-1]["content"]:
        fail("le modèle n'a rien répondu.")
        return None
    speed = f" · {stats['tok_s']} tok/s" if stats and stats["tok_s"] else ""
    print("\n" + style(f"({stats['tokens'] if stats else '?'} tokens{speed})", DIM, sys.stdout))
    return turn


def read_line() -> str | None:
    """The next line typed, stripped; None at the end of the input (Ctrl-D). Ctrl-C asks again."""
    while True:
        try:
            return input("> ").strip()
        except EOFError:
            print()
            return None
        except KeyboardInterrupt:
            print("\n(Ctrl-D ou /quit pour quitter)")


def list_tools(toolbox: Toolbox) -> None:
    for spec in toolbox.specs:
        print(f"- {spec['function']['name']} ({toolbox.routes[spec['function']['name']].name})")
    if not toolbox.specs:
        print("Aucun outil.")


def chat_loop(cfg: dict, toolbox: Toolbox) -> int:
    history: list[dict] = []  # replaced, never edited in place
    tools = f" · {len(toolbox.specs)} outils (/tools)" if toolbox.specs else ""
    print(f"SensAI · {cfg['model']}{tools} · /reset : oublier la conversation · /quit : quitter")
    while True:
        text = read_line()
        if text is None:
            return 0
        if not text:
            print("Message vide : écris quelque chose.")
        elif text in ("/quit", "/exit"):
            return 0
        elif text == "/reset":
            history = []
            print("Conversation oubliée.")
        elif text == "/tools":
            list_tools(toolbox)
        elif (turn := answer(history, text, cfg, toolbox)) is not None:
            history = [*history, *turn]


def main() -> int:
    ap = argparse.ArgumentParser(description="SensAI : chat en ligne de commande avec un modèle Ollama local")
    ap.add_argument("--model", help="modèle à utiliser (sinon celui de la config)")
    ap.add_argument("--config", default=str(ROOT / "config.json"), help="fichier de configuration (défaut : config.json)")
    ap.add_argument("--no-tools", action="store_true", help="ne lancer aucun serveur MCP")
    args = ap.parse_args()

    try:
        cfg = load_config(args.config)
        if args.model:
            cfg = {**cfg, "model": args.model}
        ensure_model(cfg)
    except (OSError, ValueError, KeyError) as e:
        fail(f"Configuration illisible ({args.config}) : {e!r}")
        return 1
    except LLMError as e:
        fail(str(e))
        return 1

    toolbox = Toolbox({} if args.no_tools else cfg.get("mcp_servers", {}))
    try:
        for warning in toolbox.warnings:  # a broken tool server must not stop the chat
            fail(f"outils indisponibles, {warning}")
        return chat_loop({**cfg, "tools": toolbox.specs}, toolbox)
    finally:
        toolbox.close()


if __name__ == "__main__":
    sys.exit(main())
