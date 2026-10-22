"""Le parcours d'entraînement : niveau → situation → décision → verdict → débrief.

Aucune entrée-sortie ici : main.py (terminal) et, plus tard, server.py (web) ne font que l'afficher.
"""
import random
from collections.abc import Iterator
from contextlib import closing

import coach
import generation
import profils
from mcp_client import Toolbox

NIVEAUX = {
    "debutant": "Je découvre (je connais à peine les règles)",
    "intermediaire": "Je joue un peu (je connais les combinaisons et les positions)",
    "avance": "Je joue souvent (je calcule mes cotes)",
}
THEMES_PAR_NIVEAU = {"debutant": ("ouverture",), "intermediaire": ("ouverture", "tirage"), "avance": ("tirage",)}
POIDS_ERREUR = 2   # un thème toujours raté pèse 1 + 2 = 3 fois plus qu'un thème réussi


def noter(reference: dict, action: str) -> str:
    """« bon » si l'action est parmi les meilleures, « acceptable » si la référence est mixte, « erreur » sinon."""
    if action in reference["bonnes"]:
        return "bon"
    if action in reference["acceptables"]:
        return "acceptable"
    return "erreur"


class Session:
    """Une session d'un joueur. Les situations ne demandent pas d'appel au modèle : elles arrivent tout de suite."""

    def __init__(self, cfg: dict, toolbox: Toolbox | None = None, rng: random.Random | None = None,
                 profil: dict | None = None):
        self.cfg = cfg
        self.toolbox = toolbox or Toolbox({})
        self.rng = rng or random.Random()
        self.profil = profil   # None : session anonyme, rien n'est enregistré
        self.niveau: str | None = profil["niveau"] if profil else None
        self.situation: dict | None = None
        self.action: str | None = None
        self.verdict: str | None = None
        self.debrief: list[dict] = []   # replaced, never edited in place
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
        self._garder(niveau=choix)
        return choix

    def niveau_libre(self, texte: str) -> dict:
        """Le niveau d'après une réponse en toutes lettres, classée par le modèle (T5) : {niveau, raison}.

        ValueError si la réponse du modèle est inutilisable : on repose alors la question par choix fermé.
        """
        classement = coach.classer_niveau(texte, self.cfg)
        self.choisir_niveau(classement["niveau"])
        return classement

    def choisir_theme(self) -> str:
        """Un thème du niveau ; un thème raté revient plus souvent (jusqu'à 3 fois plus s'il est toujours raté)."""
        themes = THEMES_PAR_NIVEAU[self.niveau]
        resultats = self.profil["resultats"] if self.profil else {}
        poids = [1 + POIDS_ERREUR * profils.taux_erreur(resultats[t]) if t in resultats else 1 for t in themes]
        return self.rng.choices(themes, poids)[0]

    def nouvelle_situation(self) -> dict:
        """Une situation d'un thème du niveau, jamais vue dans la session ; oublie la décision précédente.

        D'abord celles de la banque générée par le modèle, puis des situations tirées par le code.
        """
        if self.niveau is None:
            raise ValueError("choisis d'abord un niveau")
        theme = self.choisir_theme()
        banque = [s for s in generation.lire_banque(self.cfg)
                  if s["theme"] == theme and s["niveau"] == self.niveau and generation.cle(theme, s) not in self.vues]
        situation = self.rng.choice(banque) if banque else generation.tirer(theme, self.niveau, self.rng, self.vues)
        self.vues = {*self.vues, generation.cle(theme, situation)}
        self.situation, self.action, self.verdict, self.debrief = situation, None, None, []
        self.numero += 1
        return situation

    def decider(self, action: str) -> str:
        """Note l'action du joueur d'après la référence de la situation et renvoie le verdict."""
        if self.situation is None:
            raise ValueError("aucune situation en cours")
        if action not in self.situation["actions"]:
            raise ValueError(f"action impossible ici : {action!r}")
        self.action, self.verdict = action, noter(self.situation["reference"], action)
        if self.profil:
            self.profil = profils.noter(self.profil, self.situation["theme"], self.verdict)
            self._garder(dernier_debrief=self._debrief_en_cours())
        return self.verdict

    def discuter(self, texte: str) -> Iterator[tuple[str, object]]:
        """Le débrief en streaming (les événements de coach.repondre), une fois la décision prise.

        Le tour n'entre dans l'historique du débrief que si le modèle a répondu jusqu'au bout.
        """
        if self.action is None:
            raise ValueError("décide d'abord : le débrief vient après la décision")
        return self._debrief(texte)

    def _debrief(self, texte: str) -> Iterator[tuple[str, object]]:
        cfg = coach.config(self.cfg, self.situation, self.niveau, self.action, self.verdict, self.profil)
        with closing(coach.repondre(self.debrief, texte, cfg, self.toolbox)) as events:
            for kind, data in events:
                if kind == "fin" and data[0][-1]["content"]:
                    self.debrief = [*self.debrief, *data[0]]
                    self._garder(dernier_debrief=self._debrief_en_cours())
                yield kind, data

    def _debrief_en_cours(self) -> dict:
        return {"situation": self.situation, "action": self.action, "verdict": self.verdict, "debrief": self.debrief}

    def reprendre(self) -> dict:
        """Recharge le dernier débrief du profil (situation, décision, verdict, messages) pour le continuer."""
        dernier = self.profil and self.profil.get("dernier_debrief")
        if not dernier:
            raise ValueError("aucun débrief à reprendre")
        self.situation, self.action, self.verdict = dernier["situation"], dernier["action"], dernier["verdict"]
        self.debrief = dernier["debrief"]
        self.vues = {*self.vues, generation.cle(self.situation["theme"], self.situation)}
        return dernier

    def _garder(self, **champs) -> None:
        """Met à jour le profil et l'enregistre, si la session en a un."""
        if self.profil:
            self.profil = {**self.profil, **champs}
            profils.enregistrer(self.profil, self.cfg)

    def oublier(self) -> None:
        """Oublie le débrief en cours, pas la situation."""
        self.debrief = []
