"""Profils des joueurs, un fichier JSON par pseudo dans profiles/ : niveau, résultats par thème, dernier débrief.

Bibliothèque standard uniquement. Un profil est un dict qu'on remplace, jamais modifié en place. Le module ne
s'appelle pas profile.py : ce nom masquerait le module profile de la bibliothèque standard (utilisé par cProfile).
"""
import json
import re
import sys
from datetime import datetime

from llm import ROOT

PSEUDO = re.compile(r"[a-z0-9_-]{1,32}")
VERDICTS = ("bon", "acceptable", "erreur")
MAX_FICHES = 20   # les plus récentes suffisent : le profil reste petit


def valider_pseudo(pseudo: str) -> str:
    """Le pseudo en minuscules ; ValueError s'il ne ferait pas un nom de fichier sûr."""
    pseudo = pseudo.strip().lower()
    if not PSEUDO.fullmatch(pseudo):
        raise ValueError("pseudo : 1 à 32 lettres sans accent, chiffres, - ou _")
    return pseudo


def _chemin(pseudo: str, cfg: dict):
    return ROOT / cfg.get("profiles_dir", "profiles") / f"{valider_pseudo(pseudo)}.json"


def nouveau(pseudo: str) -> dict:
    return {"pseudo": valider_pseudo(pseudo), "niveau": None, "resultats": {}, "dernier_debrief": None, "fiches": []}


def charger(pseudo: str, cfg: dict) -> dict:
    """Le profil enregistré, ou un profil neuf s'il n'existe pas ou est illisible."""
    chemin = _chemin(pseudo, cfg)
    if not chemin.exists():
        return nouveau(pseudo)
    try:
        return {**nouveau(pseudo), **json.loads(chemin.read_text(encoding="utf-8"))}
    except ValueError:
        print(f"Profil illisible ignoré : {chemin}", file=sys.stderr)
        return nouveau(pseudo)


def enregistrer(profil: dict, cfg: dict) -> None:
    chemin = _chemin(profil["pseudo"], cfg)
    chemin.parent.mkdir(parents=True, exist_ok=True)
    data = {**profil, "mis_a_jour": datetime.now().isoformat(timespec="seconds")}
    chemin.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def noter(profil: dict, theme: str, verdict: str) -> dict:
    """Le profil avec un verdict de plus pour ce thème."""
    compte = {v: 0 for v in VERDICTS} | profil["resultats"].get(theme, {})
    return {**profil, "resultats": {**profil["resultats"], theme: {**compte, verdict: compte[verdict] + 1}}}


def ajouter_fiche(profil: dict, fiche: dict) -> dict:
    """Le profil avec cette fiche de fin d'exercice en dernier, sans dépasser MAX_FICHES."""
    return {**profil, "fiches": [*profil["fiches"], fiche][-MAX_FICHES:]}


def taux_erreur(compte: dict) -> float:
    total = sum(compte.values())
    return compte["erreur"] / total if total else 0.0


def themes_faibles(profil: dict) -> list[str]:
    """Les thèmes où le joueur s'est trompé, du plus raté au moins raté."""
    rates = {theme: taux_erreur(compte) for theme, compte in profil["resultats"].items() if compte["erreur"]}
    return sorted(rates, key=rates.get, reverse=True)


def resume(profil: dict) -> str:
    """Les résultats en une ligne, pour le coach : « tirage : 1 bon, 0 acceptable, 3 erreurs ; … »."""
    parties = [f"{theme} : " + ", ".join(f"{compte[v]} {v}{'s' if compte[v] > 1 else ''}" for v in VERDICTS)
               for theme, compte in profil["resultats"].items()]
    return " ; ".join(parties) or "aucun exercice encore"
