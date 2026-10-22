"""Évaluation du coach (EV1) : sur des situations tirées par le code, le débrief contredit-il la référence ?

    python3 evaluate_coach.py                          # 30 situations, coach et juge de config.json
    python3 evaluate_coach.py --nombre 6 --graine 1    # moins de situations, un autre tirage
    python3 evaluate_coach.py --modele llama3.2:3b     # un autre coach ; --juge pour un autre correcteur

Pour chaque situation, le joueur prend la mauvaise décision (le coach a quelque chose à expliquer), demande
« pourquoi ? », puis un juge d'une autre famille de modèle (config "judge_model", llama3.2:3b par défaut) coche
chaque fait de la référence : présent, absent ou contredit. Le score principal est la part des débriefs sans
contradiction. Le script remplit evaluation/coach_resultats.md et evaluation/coach_resultats.json.
"""
import argparse
import json
import random
import sys
import time
from datetime import datetime

import coach
import evaluate
import generation
import trainer
from llm import ROOT, LLMError, complete, load_config

FOLDER = ROOT / "evaluation"
NOMBRE = 30
GRAINE = 2026   # le même jeu de situations d'une fois sur l'autre, pour comparer deux modèles ou deux prompts
JUGE = "llama3.2:3b"   # une autre famille que le coach (qwen3) : il ne se corrige pas lui-même
QUESTION = "Pourquoi ? Explique-moi."
NIVEAU_DU_THEME = {"ouverture": "intermediaire", "tirage": "intermediaire", generation.QUI_GAGNE: "debutant"}
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


def evaluer(situation: dict, cfg: dict) -> dict:
    debut = time.monotonic()
    action = mauvaise_action(situation)
    reponse = debrief(situation, action, cfg)
    verdicts = juger(situation, reponse, cfg)
    return {
        "id": situation["id"], "theme": situation["theme"], "situation": generation.decrire(situation),
        "action": action, "reponse": reponse,
        "faits": [{"fait": fait, "verdict": v} for fait, v in zip(faits(situation), verdicts)],
        "contredit": "contredit" in verdicts, "illisible": "illisible" in verdicts,
        "secondes": round(time.monotonic() - debut, 1),
    }


def score(resultats: list[dict]) -> dict:
    juges = [r for r in resultats if not r["illisible"]]
    presents = [f["verdict"] == "présent" for r in juges for f in r["faits"]]
    return {"situations": len(resultats), "jugees": len(juges),
            "sans_contradiction": sum(not r["contredit"] for r in juges),
            "faits_presents": sum(presents), "faits": len(presents)}


def render(resultats: list[dict], coach_modele: str, juge: str) -> str:
    s = score(resultats)
    lignes = ["# Évaluation du coach (EV1)", "",
              f"Coach : `{coach_modele}` — juge : `{juge}` — {datetime.now():%Y-%m-%d %H:%M} — "
              f"**{s['sans_contradiction']}/{s['jugees']} débriefs sans contradiction**, "
              f"{s['faits_presents']}/{s['faits']} faits de la référence présents.", ""]
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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Évalue le débrief du coach contre la référence calculée.")
    parser.add_argument("--modele", help="coach (sinon celui de config.json)")
    parser.add_argument("--juge", help=f"correcteur (sinon judge_model de config.json, ou {JUGE})")
    parser.add_argument("--nombre", type=int, default=NOMBRE, help=f"situations (défaut : {NOMBRE})")
    parser.add_argument("--graine", type=int, default=GRAINE, help=f"tirage des situations (défaut : {GRAINE})")
    args = parser.parse_args(argv)
    cfg = load_config()
    cfg = {**cfg, **({"model": args.modele} if args.modele else {}), **({"judge_model": args.juge} if args.juge else {})}
    juge = cfg.get("judge_model", JUGE)

    resultats, tirees = [], situations(args.nombre, args.graine)
    try:
        for situation in tirees:
            resultat = evaluer(situation, cfg)
            resultats.append(resultat)
            marque = "?" if resultat["illisible"] else "✗" if resultat["contredit"] else " "
            print(f"[{marque}] {resultat['id']} {resultat['theme']} ({resultat['secondes']} s)", flush=True)
    except LLMError as e:
        print(e, file=sys.stderr)
    except KeyboardInterrupt:
        print("\nInterrompu.", file=sys.stderr)

    if resultats:
        (FOLDER / "coach_resultats.md").write_text(render(resultats, cfg["model"], juge), encoding="utf-8")
        payload = {"coach": cfg["model"], "juge": juge, "graine": args.graine,
                   "date": datetime.now().isoformat(timespec="seconds"), "score": score(resultats),
                   "resultats": resultats}
        (FOLDER / "coach_resultats.json").write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n",
                                                    encoding="utf-8")
        s = score(resultats)
        print(f"\n{s['sans_contradiction']}/{s['jugees']} sans contradiction → {FOLDER / 'coach_resultats.md'}")
    return 0 if len(resultats) == len(tirees) else 1


if __name__ == "__main__":
    sys.exit(main())
