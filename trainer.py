"""Le parcours d'entraînement : niveau → situation → décision → verdict → débrief.

Aucune entrée-sortie ici : main.py (terminal) et, plus tard, server.py (web) ne font que l'afficher.
"""
import random

import generation

NIVEAUX = {
    "debutant": "Je découvre (je connais à peine les règles)",
    "intermediaire": "Je joue un peu (je connais les combinaisons et les positions)",
    "avance": "Je joue souvent (je calcule mes cotes)",
}
THEMES_PAR_NIVEAU = {"debutant": ("ouverture",), "intermediaire": ("ouverture", "tirage"), "avance": ("tirage",)}


def noter(reference: dict, action: str) -> str:
    """« bon » si l'action est parmi les meilleures, « acceptable » si la référence est mixte, « erreur » sinon."""
    if action in reference["bonnes"]:
        return "bon"
    if action in reference["acceptables"]:
        return "acceptable"
    return "erreur"


class Session:
    """Une session d'un joueur. Les situations se tirent sans le modèle : elles arrivent tout de suite."""

    def __init__(self, cfg: dict, rng: random.Random | None = None):
        self.cfg = cfg
        self.rng = rng or random.Random()
        self.niveau: str | None = None
        self.situation: dict | None = None
        self.action: str | None = None
        self.verdict: str | None = None
        self.vues: set[str] = set()   # situations déjà jouées, pour ne pas les redonner
        self.numero = 0

    def choisir_niveau(self, choix: str) -> str:
        """Le niveau d'après son numéro (« 1 ») ou son nom (« debutant ») ; ValueError sinon."""
        noms = list(NIVEAUX)
        choix = choix.strip().lower()
        if choix.isdigit() and 1 <= int(choix) <= len(noms):
            choix = noms[int(choix) - 1]
        if choix not in NIVEAUX:
            raise ValueError(f"niveau inconnu : {choix!r}")
        self.niveau = choix
        return choix

    def nouvelle_situation(self) -> dict:
        """Une situation d'un thème du niveau, jamais vue dans la session ; oublie la décision précédente."""
        if self.niveau is None:
            raise ValueError("choisis d'abord un niveau")
        theme = self.rng.choice(THEMES_PAR_NIVEAU[self.niveau])
        situation = generation.tirer(theme, self.niveau, self.rng, self.vues)
        self.vues = {*self.vues, generation.cle(theme, situation)}
        self.situation, self.action, self.verdict = situation, None, None
        self.numero += 1
        return situation

    def decider(self, action: str) -> str:
        """Note l'action du joueur d'après la référence de la situation et renvoie le verdict."""
        if self.situation is None:
            raise ValueError("aucune situation en cours")
        if action not in self.situation["actions"]:
            raise ValueError(f"action impossible ici : {action!r}")
        self.action, self.verdict = action, noter(self.situation["reference"], action)
        return self.verdict
