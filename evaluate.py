"""Jeu d'évaluation : le modèle local répond aux questions, puis compare lui-même sa réponse à la référence.

    python3 evaluate.py                                  # les 87 questions, modèle de ai.py
    python3 evaluate.py --modele llama3.2:3b             # un autre modèle installé
    python3 evaluate.py --questions q01 q28              # seulement certaines questions
    python3 evaluate.py --reprendre                      # garde les questions déjà corrigées, fait le reste

Pour chaque question de evaluation/questions.jsonl :
1. le modèle répond, comme dans ai.py (même prompt système, même contexte injecté) ;
2. le même modèle reçoit la question, la réponse de référence et sa propre réponse, et rend en JSON
   les différences relevées et un verdict (réussi ou non).
Le script remplit evaluation/resultats.md (une ligne et une case cochée par question réussie) et
evaluation/resultats.json (réponses complètes). Seul le modèle local, via Ollama, est utilisé.
"""
import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path

import ai

FOLDER = Path(__file__).parent / "evaluation"
QUESTIONS = FOLDER / "questions.jsonl"

JUDGE = (
    "Tu es correcteur d'un examen de poker (Texas Hold'em). On te donne une question, la réponse d'un élève et une "
    "liste numérotée de faits attendus. Pour chaque fait, dis s'il est « présent » dans la réponse de l'élève (même "
    "formulé autrement ; chiffres à ±2 points près), « absent », ou « contredit » (l'élève affirme le contraire, "
    "même s'il le dit aussi ailleurs). Ne juge que ces faits : le reste de la réponse ne compte pas."
)
VERDICTS = ("présent", "absent", "contredit")
JUDGE_MODEL: str | None = None  # None : le modèle évalué se corrige lui-même ; --juge pour comparer des modèles


def verdict_format(facts: list[str]) -> dict:
    """Schéma JSON imposé au correcteur : un verdict par fait, ni plus ni moins."""
    keys = [str(n) for n in range(1, len(facts) + 1)]
    return {
        "type": "object",
        "properties": {key: {"type": "string", "enum": list(VERDICTS)} for key in keys},
        "required": keys,
    }


def load_questions(path: Path = QUESTIONS) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def judge(item: dict, answer: str) -> dict:
    """Le modèle vérifie chaque fait attendu (champ « faits ») dans sa réponse. Réussi si tous sont présents.

    Les faits sont écrits à la main dans questions.jsonl : laissé seul, le petit modèle découpait souvent la
    réponse de l'élève au lieu de la référence. Il ne fait que cocher, le script tranche.
    Renvoie {"reussi": bool, "differences": ["fait : absent" | "fait : contredit", ...]}.
    """
    facts = item["faits"]
    numbered = "\n".join(f"{n}. {fact}" for n, fact in enumerate(facts, 1))
    raw = ai.chat(
        [
            {"role": "system", "content": JUDGE},
            {"role": "user", "content": (
                f"Question : {item['question']}\n\nRéponse de l'élève :\n{answer}\n\nFaits attendus :\n{numbered}"
            )},
        ],
        format=verdict_format(facts),
        options={"temperature": 0},
        **({"model": JUDGE_MODEL} if JUDGE_MODEL else {}),
    )
    try:
        verdicts = json.loads(raw)
        found = [verdicts[str(n)] for n in range(1, len(facts) + 1)]
        if all(v in VERDICTS for v in found):
            missed = [f"{fact} : {v}" for fact, v in zip(facts, found) if v != "présent"]
            return {"reussi": not missed, "differences": missed}
    except (ValueError, KeyError, TypeError):
        pass
    return {"reussi": False, "differences": [f"Verdict illisible, compté comme échec : {raw[:200]!r}"]}


def evaluate(item: dict) -> dict:
    start = time.monotonic()
    answer = ai.ask(item["question"])
    return {
        **item,
        "reponse_modele": answer,
        **judge(item, answer),
        "secondes": round(time.monotonic() - start, 1),
    }


def cell(text: str) -> str:
    """Texte sûr dans une cellule de tableau Markdown."""
    return " ".join(text.split()).replace("|", "\\|")


def render(results: list[dict], model: str, total: int) -> str:
    passed = sum(r["reussi"] for r in results)
    lines = [
        "# Résultats de l'évaluation",
        "",
        f"Modèle : `{model}` — température {ai.TEMPERATURE:g} — {datetime.now():%Y-%m-%d %H:%M} — "
        f"**{passed}/{len(results)} réussies** ({passed / len(results):.0%})" if results else "Aucun résultat.",
    ]
    if len(results) < total:
        lines.append(f"\nÉvaluation interrompue : {len(results)} questions sur {total}.")
    lines += [
        "",
        "Fichier généré par `python3 evaluate.py` : ne pas modifier à la main. Le verdict est donné par le modèle "
        "lui-même, à relire.",
        "",
        "| Réussi | # | Thème | Question | Différences relevées par le modèle |",
        "|:---:|---|---|---|---|",
    ]
    for r in results:
        box = "☑" if r["reussi"] else "☐"
        lines.append(f"| {box} | {r['id']} | {r['theme']} | {cell(r['question'])} | {cell(' ; '.join(r['differences'])) or '—'} |")
    lines += ["", "## Détail"]
    for r in results:
        lines += [
            "",
            f"### {'☑' if r['reussi'] else '☐'} {r['id']} — {r['question']}",
            "",
            f"**Référence :** {r['reponse']}",
            "",
            "**Réponse du modèle :**",
            "",
            *(f"> {line}" for line in r["reponse_modele"].splitlines() or [""]),
            "",
            f"*{r['secondes']} s*",
        ]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Évalue le modèle local sur le jeu de questions de poker.")
    parser.add_argument("--modele", default=ai.MODEL, help=f"modèle Ollama (défaut : {ai.MODEL})")
    parser.add_argument("--temperature", type=float, default=ai.TEMPERATURE,
                        help=f"température des réponses (défaut : {ai.TEMPERATURE} ; 0.7 = réglage d'Ollama)")
    parser.add_argument("--questions", nargs="*", help="identifiants à évaluer, ex. q01 q28")
    parser.add_argument("--juge", help="modèle correcteur, le même pour tous les modèles comparés (défaut : le modèle évalué)")
    parser.add_argument("--reprendre", action="store_true",
                        help="garde les résultats de resultats.json (même modèle et température) et fait le reste")
    args = parser.parse_args(argv)
    ai.MODEL, ai.TEMPERATURE = args.modele, args.temperature
    global JUDGE_MODEL
    JUDGE_MODEL = args.juge
    items = load_questions()
    if args.questions:
        items = [item for item in items if item["id"] in args.questions]
        if not items:
            print("Aucune question ne correspond.", file=sys.stderr)
            return 2

    results = previous_results(items) if args.reprendre else []
    done = {r["id"] for r in results}
    try:
        for item in items:
            if item["id"] in done:
                continue
            result = evaluate(item)
            results.append(result)
            save(results, len(items))  # après chaque question : un Ollama qui tombe ne fait rien perdre
            print(f"[{'x' if result['reussi'] else ' '}] {item['id']} {item['question']}", flush=True)
    except ai.OllamaError as e:
        print(e, file=sys.stderr)
    except KeyboardInterrupt:
        print("\nInterrompu.", file=sys.stderr)

    if results:
        passed = sum(r["reussi"] for r in results)
        print(f"\n{passed}/{len(results)} réussies → {FOLDER / 'resultats.md'}")
    return 0 if len(results) == len(items) else 1


def previous_results(items: list[dict], folder: Path = FOLDER) -> list[dict]:
    """Les résultats déjà enregistrés pour ces questions, s'ils viennent du même modèle et de la même température."""
    try:
        saved = json.loads((folder / "resultats.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    if (saved.get("modele"), saved.get("temperature")) != (ai.MODEL, ai.TEMPERATURE):
        return []
    ids = {item["id"] for item in items}
    return [r for r in saved.get("resultats", []) if r.get("id") in ids]


def save(results: list[dict], total: int, folder: Path = FOLDER) -> None:
    (folder / "resultats.md").write_text(render(results, ai.MODEL, total), encoding="utf-8")
    payload = {"modele": ai.MODEL, "temperature": ai.TEMPERATURE, "date": datetime.now().isoformat(timespec="seconds"),
               "resultats": results}
    (folder / "resultats.json").write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
