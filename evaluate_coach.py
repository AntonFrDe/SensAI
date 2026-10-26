"""Évaluation du coach (EV1) : sur des situations tirées par le code, le débrief contredit-il la référence ?

    python3 evaluate_coach.py                          # 30 situations, coach et juge de config.json
    python3 evaluate_coach.py --nombre 6 --graine 1    # moins de situations, un autre tirage
    python3 evaluate_coach.py --modele llama3.2:3b     # un autre coach ; --juge pour un autre correcteur
    python3 evaluate_coach.py --ratees                 # rejoue les situations déjà ratées (evaluation/coach_ratees.jsonl)

Pour chaque situation, le joueur prend la mauvaise décision (le coach a quelque chose à expliquer), demande
« pourquoi ? », puis un juge d'une autre famille de modèle (config "judge_model", llama3.2:3b par défaut) coche
chaque fait de la référence : présent, absent ou contredit. Le score principal est la part des débriefs sans
contradiction. Le script remplit evaluation/coach_resultats.md et evaluation/coach_resultats.json, ajoute les
situations ratées à evaluation/coach_ratees.jsonl et écrit le dernier score dans le README.
"""
import argparse
import json
import random
import re
import sys
import time
from datetime import datetime

import coach
import evaluate
import generation
import trainer
from llm import ROOT, LLMError, complete, load_config

FOLDER = ROOT / "evaluation"
RATEES = FOLDER / "coach_ratees.jsonl"
README = ROOT / "README.md"
DERNIER = "Dernier score enregistré : "
NOMBRE = 30
GRAINE = 2026   # le même jeu de situations d'une fois sur l'autre, pour comparer deux modèles ou deux prompts
JUGE = "llama3.2:3b"   # une autre famille que le coach (qwen3) : il ne se corrige pas lui-même
QUESTION = "Pourquoi ? Explique-moi."
NIVEAU_DU_THEME = {"ouverture": "intermediaire", "tirage": "intermediaire", generation.QUI_GAGNE: "debutant",
                   generation.DEFENSE: "avance"}
NOMBRE_RE = re.compile(r"\d+(?:[.,]\d+)?")
CADRE_RE = re.compile(r"\b[2-9TJQKA]{2}[so]?(?= contre| :)|\(environ [^)]*\)")
BONNE_REPONSE = "La bonne réponse est : "
HORS_FAITS = ("Référence :", "Hypothèse :", "Règle :")   # le cadre de la référence, pas un fait à expliquer


def situations(nombre: int, graine: int) -> list[dict]:
    """`nombre` situations différentes, les thèmes à tour de rôle."""
    rng, vues, tirees = random.Random(graine), set(), []
    for n in range(nombre):
        theme = generation.TOUS_THEMES[n % len(generation.TOUS_THEMES)]
        situation = generation.tirer(theme, NIVEAU_DU_THEME[theme], rng, vues)
        vues = {*vues, generation.cle(theme, situation)}
        tirees.append(situation)
    return tirees


def mauvaise_action(situation: dict) -> str:
    """Une action notée « erreur » s'il y en a une, sinon la première : le coach doit corriger le joueur."""
    erreurs = [a for a in situation["actions"] if trainer.noter(situation["reference"], a) == "erreur"]
    return (erreurs or situation["actions"])[0]


def faits(situation: dict) -> list[str]:
    """Ce que le débrief doit dire : la bonne réponse, puis les faits chiffrés de la référence."""
    reference = situation["reference"]
    bonnes = reference["bonnes"] or reference["acceptables"]
    attendu = " ou ".join(generation.LIBELLES[a] for a in bonnes)
    return [f"La bonne réponse est : {attendu}.",
            *(fait for fait in reference["faits"] if not fait.startswith(HORS_FAITS))]


def debrief(situation: dict, action: str, cfg: dict) -> str:
    """La réponse du coach à « pourquoi ? », sans outils : on mesure son explication de la référence."""
    verdict = trainer.noter(situation["reference"], action)
    coach_cfg = {**coach.config(cfg, situation, situation["niveau"], action, verdict), "tools": []}
    return complete([{"role": "user", "content": QUESTION}], coach_cfg)


def juger(situation: dict, reponse: str, cfg: dict) -> list[str]:
    """Le verdict du juge pour chaque fait ; « illisible » partout si sa réponse ne suit pas le schéma."""
    attendus = faits(situation)
    numerotes = "\n".join(f"{n}. {fait}" for n, fait in enumerate(attendus, 1))
    juge_cfg = {**cfg, "model": cfg.get("judge_model", JUGE), "system_prompt": evaluate.JUDGE,
                "format": evaluate.verdict_format(attendus), "temperature": 0, "tools": []}
    question = f"Situation : {generation.decrire(situation)}\nLe joueur demande : {QUESTION}"
    brut = complete([{"role": "user", "content": (
        f"Question : {question}\n\nRéponse de l'élève :\n{reponse}\n\nFaits attendus :\n{numerotes}")}], juge_cfg)
    try:
        verdicts = json.loads(brut)
        found = [verdicts[str(n)] for n in range(1, len(attendus) + 1)]
        if all(v in evaluate.VERDICTS for v in found):
            return found
    except (ValueError, KeyError, TypeError):
        pass
    return ["illisible"] * len(attendus)


def _nombres(texte: str) -> set[float]:
    return {float(n.replace(",", ".")) for n in NOMBRE_RE.findall(texte)}


def present_par_code(fait: str, reponse: str) -> bool | None:
    """Vérification sans modèle : la bonne action est nommée, ou tous les nombres du fait sont dans la réponse.

    None si le fait n'a ni action ni nombre à chercher. Ne voit pas les contradictions : c'est le rôle du juge.
    """
    if fait.startswith(BONNE_REPONSE):
        actions = fait.removeprefix(BONNE_REPONSE).rstrip(".").split(" ou ")
        return any(action.lower() in reponse.lower() for action in actions)
    nombres = _nombres(CADRE_RE.sub("", fait)) - {6, 100}   # « 6-max, 100 blindes » : le cadre, pas un résultat
    return nombres <= _nombres(reponse) if nombres else None


def evaluer(situation: dict, cfg: dict) -> dict:
    debut = time.monotonic()
    action = mauvaise_action(situation)
    reponse = debrief(situation, action, cfg)
    verdicts = juger(situation, reponse, cfg)
    return {
        "id": situation["id"], "theme": situation["theme"], "situation": generation.decrire(situation),
        "action": action, "reponse": reponse,
        "faits": [{"fait": fait, "verdict": v, "code": present_par_code(fait, reponse)}
                  for fait, v in zip(faits(situation), verdicts)],
        "contredit": "contredit" in verdicts, "illisible": "illisible" in verdicts,
        "secondes": round(time.monotonic() - debut, 1),
    }


def score(resultats: list[dict]) -> dict:
    juges = [r for r in resultats if not r["illisible"]]
    presents = [f["verdict"] == "présent" for r in juges for f in r["faits"]]
    verifies = [f["code"] for r in resultats for f in r["faits"] if f.get("code") is not None]
    return {"situations": len(resultats), "jugees": len(juges),
            "sans_contradiction": sum(not r["contredit"] for r in juges),
            "faits_presents": sum(presents), "faits": len(presents),
            "faits_retrouves_par_code": sum(verifies), "faits_verifiables": len(verifies)}


def render(resultats: list[dict], coach_modele: str, juge: str) -> str:
    s = score(resultats)
    lignes = ["# Évaluation du coach (EV1)", "",
              f"Coach : `{coach_modele}` — juge : `{juge}` — {datetime.now():%Y-%m-%d %H:%M} — "
              f"**{s['sans_contradiction']}/{s['jugees']} débriefs sans contradiction**, "
              f"{s['faits_presents']}/{s['faits']} faits de la référence présents selon le juge ; "
              f"**{s['faits_retrouves_par_code']}/{s['faits_verifiables']} retrouvés par le code** (bonne action "
              "nommée, chiffres cités).", ""]
    if s["jugees"] < s["situations"]:
        lignes += [f"{s['situations'] - s['jugees']} verdicts illisibles, non comptés.", ""]
    lignes += ["Fichier généré par `python3 evaluate_coach.py` : ne pas modifier à la main. Le joueur prend la "
               "mauvaise décision, demande « pourquoi ? », un juge d'une autre famille de modèle coche les faits.",
               "", "| Contredit | # | Thème | Décision | Faits absents ou contredits |", "|:---:|---|---|---|---|"]
    for r in resultats:
        manques = " ; ".join(f"{f['fait']} : {f['verdict']}" for f in r["faits"] if f["verdict"] != "présent")
        marque = "?" if r["illisible"] else "✗" if r["contredit"] else "—"
        lignes.append(f"| {marque} | {r['id']} | {r['theme']} | {generation.LIBELLES[r['action']]} | "
                      f"{evaluate.cell(manques) or '—'} |")
    lignes += ["", "## Détail"]
    for r in resultats:
        lignes += ["", f"### {r['id']} — {r['theme']}", "", *(f"> {l}" for l in r["situation"].splitlines()), "",
                   f"Décision : {generation.LIBELLES[r['action']]}", "", "**Débrief du coach :**", "",
                   *(f"> {l}" for l in r["reponse"].splitlines() or [""]), "", f"*{r['secondes']} s*"]
    return "\n".join(lignes) + "\n"


def enregistrer(resultats: list[dict], cfg: dict, juge: str, graine: int) -> None:
    """Écrit les deux fichiers de résultats ; appelé après chaque situation, un arrêt garde ce qui est fait."""
    (FOLDER / "coach_resultats.md").write_text(render(resultats, cfg["model"], juge), encoding="utf-8")
    payload = {"coach": cfg["model"], "juge": juge, "graine": graine,
               "date": datetime.now().isoformat(timespec="seconds"), "score": score(resultats),
               "resultats": resultats}
    (FOLDER / "coach_resultats.json").write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n",
                                                encoding="utf-8")


def rate(resultat: dict) -> bool:
    return any(f.get("code") is False for f in resultat["faits"])


def lire_ratees(chemin=RATEES) -> list[dict]:
    if not chemin.exists():
        return []
    return [json.loads(ligne) for ligne in chemin.read_text(encoding="utf-8").splitlines() if ligne.strip()]


def garder_ratees(tirees: list[dict], resultats: list[dict], chemin=RATEES) -> int:
    connues = {situation["id"] for situation in lire_ratees(chemin)}
    nouvelles = [situation for situation, resultat in zip(tirees, resultats)
                 if rate(resultat) and situation["id"] not in connues]
    if nouvelles:
        with chemin.open("a", encoding="utf-8") as fichier:
            fichier.writelines(json.dumps(situation, ensure_ascii=False) + "\n" for situation in nouvelles)
    return len(nouvelles)


def ligne_score(payload: dict) -> str:
    s = payload["score"]
    return (f"{DERNIER}{payload['date'][:10]}, coach `{payload['coach']}`, juge `{payload['juge']}`, "
            f"{s['situations']} situations : **{s['sans_contradiction']}/{s['jugees']} débriefs sans contradiction**, "
            f"{s['faits_retrouves_par_code']}/{s['faits_verifiables']} faits retrouvés par le code.")


def maj_readme(payload: dict, chemin=README) -> bool:
    texte = chemin.read_text(encoding="utf-8")
    nouveau = re.sub(rf"^{DERNIER}.*$", lambda _: ligne_score(payload), texte, count=1, flags=re.MULTILINE)
    chemin.write_text(nouveau, encoding="utf-8")
    return nouveau != texte


def relire() -> int:
    """Recalcule la vérification par le code et la page à partir de coach_resultats.json, sans appeler de modèle."""
    payload = json.loads((FOLDER / "coach_resultats.json").read_text(encoding="utf-8"))
    resultats = [{**r, "faits": [{**f, "code": present_par_code(f["fait"], r["reponse"])} for f in r["faits"]]}
                 for r in payload["resultats"]]
    (FOLDER / "coach_resultats.md").write_text(render(resultats, payload["coach"], payload["juge"]), encoding="utf-8")
    payload = {**payload, "score": score(resultats), "resultats": resultats}
    (FOLDER / "coach_resultats.json").write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n",
                                                encoding="utf-8")
    maj_readme(payload)
    print(json.dumps(payload["score"], ensure_ascii=False))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Évalue le débrief du coach contre la référence calculée.")
    parser.add_argument("--modele", help="coach (sinon celui de config.json)")
    parser.add_argument("--juge", help=f"correcteur (sinon judge_model de config.json, ou {JUGE})")
    parser.add_argument("--nombre", type=int, default=NOMBRE, help=f"situations (défaut : {NOMBRE})")
    parser.add_argument("--graine", type=int, default=GRAINE, help=f"tirage des situations (défaut : {GRAINE})")
    parser.add_argument("--relire", action="store_true",
                        help="recalculer la vérification par le code sur les résultats enregistrés, sans modèle")
    parser.add_argument("--ratees", action="store_true", help=f"rejouer les situations ratées ({RATEES.name})")
    args = parser.parse_args(argv)
    if args.relire:
        return relire()
    cfg = load_config()
    cfg = {**cfg, **({"model": args.modele} if args.modele else {}), **({"judge_model": args.juge} if args.juge else {})}
    juge = cfg.get("judge_model", JUGE)

    tirees = lire_ratees() if args.ratees else situations(args.nombre, args.graine)
    if not tirees:
        print(f"Aucune situation ratée dans {RATEES}.", file=sys.stderr)
        return 1
    resultats = []
    try:
        for situation in tirees:
            resultat = evaluer(situation, cfg)
            resultats.append(resultat)
            enregistrer(resultats, cfg, juge, args.graine)
            marque = "?" if resultat["illisible"] else "✗" if resultat["contredit"] else " "
            print(f"[{marque}] {resultat['id']} {resultat['theme']} ({resultat['secondes']} s)", flush=True)
    except LLMError as e:
        print(e, file=sys.stderr)
    except KeyboardInterrupt:
        print("\nInterrompu.", file=sys.stderr)

    if resultats:
        s = score(resultats)
        print(f"\n{s['sans_contradiction']}/{s['jugees']} sans contradiction → {FOLDER / 'coach_resultats.md'}")
        print(f"{garder_ratees(tirees, resultats)} situations ratées ajoutées à {RATEES}")
    if resultats and len(resultats) == len(tirees):
        maj_readme(json.loads((FOLDER / "coach_resultats.json").read_text(encoding="utf-8")))
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
