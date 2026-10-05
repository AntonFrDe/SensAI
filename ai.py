"""Poser une question à un modèle local (Qwen) via Ollama, en ligne de commande.

    python3 ai.py "Explique le terme UTG au poker"

Le classement des combinaisons (data/hand_rankings.json) est injecté avant chaque question.
Bibliothèque standard uniquement (urllib) — aucune dépendance à installer.

Prérequis : Ollama tourne (`ollama serve`) avec le modèle installé
            (`ollama pull qwen3:4b-instruct-2507-q4_K_M`).
"""
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

import equity
import glossary
import odds

MODEL = "qwen3:4b-instruct-2507-q4_K_M"
OLLAMA = "http://localhost:11434/api/chat"
# 0 = réponses reproductibles (Ollama prend 0,7 pour ce modèle). Ne rend pas la réponse plus juste : sans le
# bon contexte, elle reste fausse, mais toujours de la même façon, ce qui permet de comparer avant/après.
TEMPERATURE = 0.0
NUM_CTX = 8192  # tokens : contexte injecté + question + réponse ; Ollama prend 4 096 par défaut
DATA = Path(__file__).parent / "data"
SYSTEM = "Tu es SensAI, un coach de poker. Réponds en Français, court et précis. Dans le cadre d'une question par rapport " \
           "a une partie (que faire a un moment donné), il faudra que tu normalize le resultat, avec - (Action à faire) \n - (Combien miser)\n - (Pourquoi) \n" \
         "Si le contexte contient des calculs (équité, outs, cote du pot), appuie ton conseil dessus et cite-les tels quels.\n"


def hand_rankings_context() -> str:
    """Le classement des 10 combinaisons (data/hand_rankings.json), une ligne par combinaison.

    Le fichier stocke un rang (1 = la meilleure). Le modèle, lui, reçoit une force (10 = la meilleure) :
    avec des rangs, il lit « 5 > 4 » et conclut qu'une couleur bat un full.
    """
    rankings = json.loads((DATA / "hand_rankings.json").read_text(encoding="utf-8"))
    top = len(rankings)
    lines = [
        f"- {r['fr']} ({r['en']}), force {top + 1 - r['rang']}/{top} : {r['description']} Exemple : {r['exemple']}"
        for r in rankings
    ]
    return (
        "Classement des combinaisons au poker, de la plus forte à la plus faible :\n"
        + "\n".join(lines)
        + "\nPlus la force est élevée, plus la combinaison est forte."
    )

def glossary_entries_in(question: str) -> list[glossary.Entry]:
    """Les entrées du glossaire dont le terme ou un alias apparaît dans la question, plus leurs renvois « voir X ».

    Le glossaire entier fait ~15 000 tokens : bien plus que le contexte de 4 096 tokens d'Ollama par défaut.
    """
    words = f" {glossary.normalize(question)} "
    found = [
        entry for entry in glossary.ENTRIES
        if any(len(key) > 1 and f" {key} " in words for key in map(glossary.normalize, (entry.term, *entry.aliases)))
    ]
    for entry in list(found):
        for target in filter(None, map(glossary.lookup, entry.see)):
            if target not in found:
                found.append(target)
    return found


def glossary_context(question: str | None = None) -> str:
    """Le glossaire de poker, une ligne textuelle par entrée : tout, ou seulement les termes de la question."""
    entries = glossary.ENTRIES if question is None else glossary_entries_in(question)
    lines = []
    for entry in entries:
        aliases = f" (alias : {', '.join(entry.aliases)})" if entry.aliases else ""
        if entry.definition:
            text = entry.definition.replace("\n", " ")
            if entry.see:
                text += f" Voir aussi : {', '.join(entry.see)}."
        else:
            text = f"Voir : {', '.join(entry.see)}."
        lines.append(f"- {entry.term}{aliases} : {text}")

    return "Glossaire de poker :\n" + "\n".join(lines) if lines else ""

def ambigu_context() -> str:
    line1  = "Si la question ne pointe pas vers une reponse rapide du tableau, il faut que tu fasse une association des elements pour essayer d'y repondre, et serialiser les donnée comme ci dessous \n"
    serial_ex = "-- Je n'ai pas de reponse precise pour cette question mais je peux essayer de deviner --\
                - Ce que je comprend de la question : (ton analyse de la question et comment t'en ai venue à selection l'une ou l'autre donnée en fonction\n \
                (LA REPONSE)"

    ambigue = "Si la question te semble embigu ou pointe vers deux ou plusieurs données de ton tableau menant a plusieur reponse differente il faudrait que tu redemande la questino en proposant des piste comme dans l'exemple ci-dessous\n"
    ambigue_ex = "- J'interprete ta question de plusieurs manière peux-tu reformuler ou selectionner l'une des proposition ci dessous : \n\
                1.(Reformulation de la question celon ta premiere interpretation)" \
                "2.(Deuxieme reformulation)" \
                "3. (Troisieme si nescssaire, pas plus)"

    return "CONTEXTE AMBIGU \n" ++ line1 ++ serial_ex ++ ambigue ++ ambigue_ex 

# « Ah », « 10d », « Q♣ » : valeur en majuscule, couleur en minuscule, pour ne pas lire « as » ou « je » comme des cartes.
CARD = re.compile(r"(?<!\w)(?:10|[2-9TJQKA])[shdc♠♥♦♣](?!\w)")
AMOUNT = r"\D{0,20}?(\d+(?:[.,]\d+)?)"
POT = re.compile(r"\bpot\b" + AMOUNT, re.I)
TO_CALL = re.compile(r"\b(?:payer|suivre|call(?:er)?|mise|misé)" + AMOUNT, re.I)
OPPONENTS = re.compile(r"(\d+)\s*adversaires?", re.I)


def situation_context(question: str) -> str:
    """Équité, outs et cote du pot calculés par odds.py, si la question décrit une main.

    Convention : les 2 premières cartes citées sont les nôtres, les suivantes le board (0, 3, 4 ou 5).
    « pot 100 » = ce qu'il y a au milieu, mise adverse comprise ; « payer 50 » = la somme à suivre.
    """
    cards = CARD.findall(question)
    if len(cards) < 2:
        return ""
    pot, to_call, opponents = POT.search(question), TO_CALL.search(question), OPPONENTS.search(question)
    try:
        return "Calculs exacts pour cette main (fais-leur confiance, ne les recalcule pas) :\n" + odds.analyse(
            equity.parse_cards(" ".join(cards[:2])),
            equity.parse_cards(" ".join(cards[2:])),
            int(opponents.group(1)) if opponents else 1,
            float(pot.group(1).replace(",", ".")) if pot and to_call else None,
            float(to_call.group(1).replace(",", ".")) if pot and to_call else None,
        )
    except ValueError as error:  # cartes en double, board de 2 cartes... : le modèle doit le signaler
        return f"Les cartes de la question ne forment pas une situation valide : {error}"


def find_context(question: str) -> str:
    """Cherche dans data/ ce qui aide à répondre, et le renvoie en texte pour le modèle.

    Le classement des combinaisons et le glossaire, puis les calculs de la main si la question en décrit une.
    """
    parts = (hand_rankings_context(), glossary_context(question), situation_context(question))
    return "\n\n".join(part for part in parts if part)


def build_prompt(question: str) -> str:
    """Assemble le message envoyé au modèle : le contexte trouvé dans la doc, puis la question."""
    context = find_context(question)
    if not context:
        return question
    return f"Contexte (extrait de la documentation) :\n{context}\n\nQuestion : {question}"


def ask(question: str) -> str:
    """Envoie la question à Ollama et renvoie la réponse du modèle. C'EST L'APPEL À L'IA."""
    return chat([
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": build_prompt(question)},
    ], options={"temperature": TEMPERATURE})


class OllamaError(Exception):
    """Erreur d'Ollama, avec un message lisible pour l'utilisateur."""


def chat(messages: list[dict], options: dict | None = None, **extra) -> str:
    """Un appel à Ollama, sans streaming. `extra` complète la requête (ex. `format` pour une sortie JSON)."""
    payload = {
        "model": MODEL,
        "stream": False,  # on attend la réponse entière (plus simple à lire qu'en streaming)
        "messages": messages,
        "options": {"num_ctx": NUM_CTX, **(options or {})},
        **extra,
    }
    request = urllib.request.Request(
        OLLAMA, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(request) as response:
            return json.load(response)["message"]["content"].strip()
    except urllib.error.HTTPError as e:
        raise OllamaError(_http_error(e)) from None
    except urllib.error.URLError:
        raise OllamaError("Ollama injoignable. Lance-le avec : ollama serve") from None


def _http_error(e: urllib.error.HTTPError) -> str:
    """Le message d'Ollama lui-même ; il est parfois un JSON dans le JSON (dépassement de contexte)."""
    if e.code == 404:
        return f"Modèle « {MODEL} » absent. Installe-le : ollama pull {MODEL}"
    message = e.read().decode(errors="replace")
    for _ in range(2):
        try:
            message = json.loads(message)["error"]
            message = message["message"] if isinstance(message, dict) else message
        except (ValueError, KeyError, TypeError):
            break
    return f"Erreur Ollama (HTTP {e.code}) : {message}"


def main() -> int:
    if len(sys.argv) < 2:
        print('Usage : python3 ai.py "ta question"', file=sys.stderr)
        return 2
    try:
        print(ask(" ".join(sys.argv[1:])))
    except OllamaError as e:
        print(e, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
