"""Le coach du débrief : son contexte (situation, décision, verdict, référence) et la boucle d'appels d'outils
d'une réponse, sans rien afficher. Le CLI et le web la rendent chacun à leur façon.

Le code a déjà calculé la bonne réponse (generation.reference) : le coach l'explique, il ne la recalcule pas.
"""
import json
from collections.abc import Iterator
from contextlib import closing

import generation
import preflop
import profils
from llm import ROOT, complete, stream_chat
from mcp_client import Toolbox

MAX_TOOL_ROUNDS = 5  # then the model must answer with what it has
PROMPT = ROOT / "prompts" / "coach.txt"
PROMPT_NIVEAU = ROOT / "prompts" / "niveau.txt"
PROMPT_FICHE = ROOT / "prompts" / "fiche.txt"
QUESTION = "poser_question"   # outil local (X4) : il faut l'interface du joueur, donc pas de serveur MCP
OUTIL_QUESTION = {"type": "function", "function": {
    "name": QUESTION,
    "description": "Pose au joueur une question de contrôle à choix, pour vérifier qu'il a compris (par exemple "
                   "« Combien d'outs as-tu ici ? »). Il répond en choisissant. Une seule question à la fois ; "
                   "attends sa réponse avant de continuer.",
    "parameters": {"type": "object", "required": ["question", "choix"], "properties": {
        "question": {"type": "string", "description": "La question, en français, adressée au joueur (tu)."},
        "choix": {"type": "array", "items": {"type": "string"}, "minItems": 2, "maxItems": 4,
                  "description": "De 2 à 4 réponses courtes, dont une seule juste."},
    }},
}}
CONSIGNES_NIVEAU = {
    "debutant": "Il découvre le poker : explique chaque terme technique, une idée à la fois.",
    "intermediaire": "Il connaît les combinaisons et les positions : tu peux parler de range et de cote du pot.",
    "avance": "Il calcule ses cotes : va droit aux chiffres.",
}


SORTES = {"s": "assorties (même couleur)", "o": "dépareillées (couleurs différentes)", "": "une paire"}


def main_de_depart(cartes: list[str]) -> str:
    """« J5o : cartes dépareillées (couleurs différentes) » : le nom de la main, que le modèle lit souvent mal."""
    main = preflop.normalize_hand("".join(cartes))
    return f"{main} : {SORTES[main[2:]]}"


def schema_niveau() -> dict:
    """Sortie structurée (T5) du classement d'une réponse libre : {niveau, raison}."""
    return {"type": "object",
            "properties": {"niveau": {"type": "string", "enum": list(CONSIGNES_NIVEAU)},
                           "raison": {"type": "string"}},
            "required": ["niveau", "raison"], "additionalProperties": False}


def lire_json(reponse: str, schema: dict) -> dict:
    """La réponse du modèle si elle suit le schéma (champs requis, chaînes, valeurs permises) ; ValueError sinon.

    Ollama impose le schéma en général, mais un modèle peut encore renvoyer un JSON coupé ou vide.
    """
    try:
        data = json.loads(reponse)
    except ValueError:
        raise ValueError("la réponse n'est pas du JSON") from None
    if not isinstance(data, dict):
        raise ValueError("la réponse doit être un objet JSON")
    for champ, regle in schema["properties"].items():
        valeur = data.get(champ)
        if regle["type"] == "string" and not (isinstance(valeur, str) and valeur.strip()):
            raise ValueError(f"champ manquant ou vide : {champ}")
        if "enum" in regle and valeur not in regle["enum"]:
            raise ValueError(f"valeur impossible pour {champ} : {valeur!r}")
    return {champ: data[champ] for champ in schema["properties"]}


def classer_niveau(texte: str, cfg: dict) -> dict:
    """Le niveau d'un joueur d'après sa réponse libre : {niveau, raison}. ValueError si la réponse est inutilisable."""
    schema = schema_niveau()
    niveau_cfg = {**cfg, "system_prompt": PROMPT_NIVEAU.read_text(encoding="utf-8").strip(), "format": schema,
                  "temperature": 0, "tools": []}
    return lire_json(complete([{"role": "user", "content": texte}], niveau_cfg), schema)


def _actions(actions: list[str]) -> str:
    return ", ".join(generation.LIBELLES[a] for a in actions) or "aucune"


def contexte(situation: dict, niveau: str, action: str, verdict: str, profil: dict | None = None) -> str:
    """Ce que le coach sait de l'exercice : la situation, la décision du joueur, son verdict et la référence ;
    et, s'il a un profil, ses résultats passés."""
    ref = situation["reference"]
    lignes = ["Situation de l'exercice :", generation.decrire(situation),
              *([f"Main de départ : {main_de_depart(situation['cartes'])}."]
                if situation["theme"] == "ouverture" else []),
              f"Niveau du joueur : {niveau}. {CONSIGNES_NIVEAU[niveau]}",
              f"Décision du joueur : {generation.LIBELLES[action]}. Verdict : {verdict}.",
              "Référence calculée par le code (fais-lui confiance, ne la recalcule pas) :",
              f"- bonnes actions : {_actions(ref['bonnes'])}",
              f"- actions acceptables (situation limite) : {_actions(ref['acceptables'])}",
              *(f"- {fait}" for fait in ref["faits"])]
    if profil:
        faibles = profils.themes_faibles(profil)
        lignes += [f"Résultats passés du joueur ({profil['pseudo']}) : {profils.resume(profil)}.",
                   f"Thèmes à revoir : {', '.join(faibles) or 'aucun'}."]
    return "\n".join(lignes)


def schema_fiche() -> dict:
    """Sortie structurée (T5) de la fiche de fin d'exercice : {a_retenir, theme_a_revoir}."""
    return {"type": "object",
            "properties": {"a_retenir": {"type": "string"},
                           "theme_a_revoir": {"type": "string", "enum": [*generation.TOUS_THEMES, "aucun"]}},
            "required": ["a_retenir", "theme_a_revoir"], "additionalProperties": False}


def fiche(situation: dict, niveau: str, action: str, verdict: str, debrief: list[dict], cfg: dict) -> dict:
    """La fiche de fin d'exercice, écrite par le modèle et vérifiée ; ValueError si elle est inutilisable."""
    schema = schema_fiche()
    prompt = PROMPT_FICHE.read_text(encoding="utf-8").strip()
    fiche_cfg = {**cfg, "system_prompt": f"{prompt}\n\n{contexte(situation, niveau, action, verdict)}",
                 "format": schema, "temperature": 0, "tools": []}
    echanges = [m for m in debrief if m["role"] in ("user", "assistant") and m["content"]]   # sans les outils
    demande = {"role": "user", "content": "Écris la fiche de fin d'exercice."}
    return lire_json(complete([*echanges, demande], fiche_cfg), schema)


def config(cfg: dict, situation: dict, niveau: str, action: str, verdict: str, profil: dict | None = None) -> dict:
    """La config du débrief : le prompt du coach suivi du contexte de l'exercice, et l'outil poser_question."""
    prompt = PROMPT.read_text(encoding="utf-8").strip()
    return {**cfg, "system_prompt": f"{prompt}\n\n{contexte(situation, niveau, action, verdict, profil)}",
            "tools": [*cfg.get("tools", []), OUTIL_QUESTION]}


def lire_question(arguments: object) -> dict:
    """{question, choix} d'un appel à poser_question ; ValueError s'il ne fait pas une question à choix."""
    if not isinstance(arguments, dict):
        raise ValueError("arguments attendus : question et choix")
    question, choix = arguments.get("question"), arguments.get("choix")
    if not (isinstance(question, str) and question.strip()):
        raise ValueError("question vide")
    if not (isinstance(choix, list) and 2 <= len(choix) <= 4 and all(isinstance(c, str) and c.strip() for c in choix)):
        raise ValueError("il faut de 2 à 4 choix, chacun un texte")
    return {"question": question.strip(), "choix": [c.strip() for c in choix]}


def repondre(history: list[dict], text: str, cfg: dict, toolbox: Toolbox) -> Iterator[tuple[str, object]]:
    """Stream the reply to `text`, running the tools the model asks for on the way.

    Yields ("thinking" | "token", text) as the model writes, ("outil", (name, arguments)) before each tool runs,
    ("question", {question, choix}) when the model asks the player a question (X4): the turn then stops there, the
    player's choice is the next message. Then ("fin", (turn, stats)): the turn's messages (user, tool calls and
    results, final answer). LLMError propagates; closing the generator stops Ollama's generation.
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
        asked = False
        for call in calls:
            name, arguments = call["function"]["name"], call["function"].get("arguments", {})
            if name == QUESTION:
                try:
                    question = lire_question(arguments)
                except ValueError as e:
                    result = f"Erreur : {e}"
                else:
                    asked = True
                    yield "question", question
                    result = "Question affichée au joueur : sa réponse sera le prochain message."
            else:
                yield "outil", (name, arguments)
                result = toolbox.call(name, arguments)
            turn = [*turn, {"role": "tool", "tool_name": name, "content": result}]
        if asked:
            break
    yield "fin", (turn, stats)
