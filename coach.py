"""Le coach du débrief : son contexte (situation, décision, verdict, référence) et la boucle d'appels d'outils
d'une réponse, sans rien afficher. Le CLI et le web la rendent chacun à leur façon.

Le code a déjà calculé la bonne réponse (generation.reference) : le coach l'explique, il ne la recalcule pas.
"""
from collections.abc import Iterator
from contextlib import closing

import generation
from llm import ROOT, stream_chat
from mcp_client import Toolbox

MAX_TOOL_ROUNDS = 5  # then the model must answer with what it has
PROMPT = ROOT / "prompts" / "coach.txt"
CONSIGNES_NIVEAU = {
    "debutant": "Il découvre le poker : explique chaque terme technique, une idée à la fois.",
    "intermediaire": "Il connaît les combinaisons et les positions : tu peux parler de range et de cote du pot.",
    "avance": "Il calcule ses cotes : va droit aux chiffres.",
}


def _actions(actions: list[str]) -> str:
    return ", ".join(generation.LIBELLES[a] for a in actions) or "aucune"


def contexte(situation: dict, niveau: str, action: str, verdict: str) -> str:
    """Ce que le coach sait de l'exercice : la situation, la décision du joueur, son verdict et la référence."""
    ref = situation["reference"]
    lignes = ["Situation de l'exercice :", generation.decrire(situation),
              f"Niveau du joueur : {niveau}. {CONSIGNES_NIVEAU[niveau]}",
              f"Décision du joueur : {generation.LIBELLES[action]}. Verdict : {verdict}.",
              "Référence calculée par le code (fais-lui confiance, ne la recalcule pas) :",
              f"- bonnes actions : {_actions(ref['bonnes'])}",
              f"- actions acceptables (situation limite) : {_actions(ref['acceptables'])}",
              *(f"- {fait}" for fait in ref["faits"])]
    return "\n".join(lignes)


def config(cfg: dict, situation: dict, niveau: str, action: str, verdict: str) -> dict:
    """La config du débrief : le prompt du coach suivi du contexte de l'exercice."""
    prompt = PROMPT.read_text(encoding="utf-8").strip()
    return {**cfg, "system_prompt": f"{prompt}\n\n{contexte(situation, niveau, action, verdict)}"}


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
