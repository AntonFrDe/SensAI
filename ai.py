"""Poser une question à un modèle local (Qwen) via Ollama, en ligne de commande.

    python3 ai.py "Explique le terme UTG au poker"

Le classement des combinaisons (data/hand_rankings.json) est injecté avant chaque question.
Bibliothèque standard uniquement (urllib) — aucune dépendance à installer.

Prérequis : Ollama tourne (`ollama serve`) avec le modèle installé
            (`ollama pull qwen3:4b-instruct-2507-q4_K_M`).
"""
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

MODEL = "qwen3:4b-instruct-2507-q4_K_M"
OLLAMA = "http://localhost:11434/api/chat"
DATA = Path(__file__).parent / "data"
SYSTEM = "Tu es SensAI, un coach de poker. Réponds en Français, court et précis. Dans le cadre d'une question par rapport " \
           "a une partie (que faire a un moment donné), il faudra que tu normalize le resultat, avec - (Action à faire) \n - (Combien miser)\n - (Pourquoi) \n"


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


def find_context(question: str) -> str:
    """Cherche dans data/ ce qui aide à répondre, et le renvoie en texte pour le modèle.

    Pour l'instant : le classement des combinaisons, injecté à chaque question (10 lignes).
    À venir : les définitions du glossaire pour les termes présents dans la question.
    """
    return hand_rankings_context()


def build_prompt(question: str) -> str:
    """Assemble le message envoyé au modèle : le contexte trouvé dans la doc, puis la question."""
    context = find_context(question)
    if not context:
        return question  # pas de doc branchée : le modèle répond avec ce qu'il sait déjà
    return f"Contexte (extrait de la documentation) :\n{context}\n\nQuestion : {question}"


def ask(question: str) -> str:
    """Envoie la question à Ollama et renvoie la réponse du modèle. C'EST L'APPEL À L'IA."""
    
    payload = {
        "model": MODEL,
        "stream": False,  # on attend la réponse entière (plus simple à lire qu'en streaming)
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": build_prompt(question)},
        ],
    }
    request = urllib.request.Request(
        OLLAMA, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(request) as response:
        return json.load(response)["message"]["content"].strip()


def main() -> int:
    if len(sys.argv) < 2:
        print('Usage : python3 ai.py "ta question"', file=sys.stderr)
        return 2
    try:
        print(ask(" ".join(sys.argv[1:])))
    except urllib.error.HTTPError as e:  # ex. 404 : modèle pas installé
        print(f"Erreur Ollama (HTTP {e.code}). Modèle « {MODEL} » installé ? → ollama pull {MODEL}", file=sys.stderr)
        return 1
    except urllib.error.URLError:  # Ollama éteint / injoignable
        print("Ollama injoignable. Lance-le avec : ollama serve", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
