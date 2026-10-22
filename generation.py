"""Banque de situations générées par le LLM : génération, vérification, repli et référence.

Le modèle propose une situation en JSON (schéma imposé à Ollama). Le code la vérifie, renvoie les erreurs
au modèle (3 essais au plus), puis tire une situation au hasard si rien ne passe. La bonne réponse vient de
preflop.py et odds.py, jamais du modèle.
"""
import json
import random
import sys
import threading
from datetime import datetime
from uuid import uuid4

import equity
import odds
import preflop
from llm import ROOT, LLMError, complete

THEMES = ("ouverture", "tirage")   # ceux que le modèle sait générer
QUI_GAGNE = "qui_gagne"   # quiz d'abattage (débutant) : tiré par le code seulement
DEFENSE = "defense_bb"   # défendre sa grosse blinde face à une ouverture (avancé) : tiré par le code seulement
TOUS_THEMES = (*THEMES, QUI_GAGNE, DEFENSE)
NIVEAUX = ("debutant", "intermediaire", "avance")
CARTES = [r + s for r in "AKQJT98765432" for s in "shdc"]  # les 52 codes
MAINS_DU_TIRAGE = ("Quinte", "Couleur", "Quinte flush", "Quinte flush royale")   # les seuls outs « propres »
POSITIONS = {"ouverture": ["UTG", "MP", "CO", "BTN", "SB"],  # la BB n'ouvre jamais
             "tirage": ["UTG", "MP", "CO", "BTN", "SB", "BB"]}
ACTIONS = {"ouverture": ["fold", "raise"], "tirage": ["fold", "call", "raise"],
           QUI_GAGNE: ["moi", "adversaire", "egalite"], DEFENSE: ["fold", "call", "raise"]}
LIBELLES = {"fold": "se coucher", "call": "suivre", "raise": "relancer",
            "moi": "tu gagnes", "adversaire": "ton adversaire gagne", "egalite": "égalité, pot partagé"}
QUESTIONS = {QUI_GAGNE: "Qui gagne ?"}   # sinon « Que fais-tu ? »
NOMS_POSITIONS = {"UTG": "sous le canon (UTG)", "MP": "en milieu de parole (MP)", "CO": "au cut-off (CO)",
                  "BTN": "au bouton (BTN)", "SB": "à la petite blinde (SB)", "BB": "à la grosse blinde (BB)"}
CHAMPS_MODELE = ("position", "cartes", "board", "pot", "a_payer")  # ce que le modèle écrit
CHAMPS = (*CHAMPS_MODELE, "historique")  # la situation finale, dans l'ordre du contrat
TAILLES_BOARD = {"ouverture": (0,), "tirage": (3, 4)}
MAX_TENTATIVES = 3
TEMPERATURE = 0.9  # de la variété : à 0, le modèle redonnerait toujours la même situation
ESSAIS_REPLI = 5_000
POT_AVANT_FLOP = 1.5  # les deux blindes
POTS_REPLI = (4, 6, 8, 10)
FRACTIONS_MISE = (0.33, 0.5, 0.75, 1)
OUVREURS = ("CO", "BTN", "SB")   # les ouvertures que la grosse blinde défend le plus souvent
OUVERTURE_BB = 2.5   # taille de l'ouverture, en blindes
ECHANTILLONS_DEFENSE = 4_000   # équité contre la range à ±1,5 point près
# Hors position, on ne touche pas toute son équité (on se couche sur certains boards) : environ 80 % en grosse
# blinde. Sans ce facteur, comparer l'équité brute à la cote du pot ferait suivre presque toutes les mains.
REALISATION_BB = 0.8
MARGE_DEFENSE = 0.03   # à moins de 3 points de la cote du pot, suivre ou se coucher se défendent tous les deux
RELANCE_DEFENSE = 0.55   # au-dessus, relancer (3-bet) est aussi acceptable
# Une petite mise rend « suivre » évident : au-delà du niveau débutant, l'adversaire mise au moins ~un tiers du pot
MISE_MIN = 0.3
MISE_TROP_PETITE = "mise trop petite pour ce niveau"
# Avec une paire, la décision ne se joue plus sur les outs seuls : la référence (outs contre cote du pot) serait fausse
MAIN_FAITE = "le joueur a déjà une paire"
PROMPT = ROOT / "prompts" / "generation.txt"
_verrou = threading.Lock()

CONSIGNES_THEME = {
    "ouverture": "Avant le flop. Tout le monde s'est couché jusqu'au joueur, qui doit ouvrir (relancer) ou se "
                 "coucher. board vide, a_payer 0, pot 1.5 (les deux blindes). position parmi UTG, MP, CO, BTN, SB.",
    "tirage": "Au flop (board de 3 cartes) ou au turn (4 cartes). Le joueur n'a pas encore de main faite mais "
              "un tirage couleur ou quinte. Un adversaire vient de miser a_payer ; pot = pot avant la mise + la "
              "mise, donc a_payer est plus petit que pot.",
}
# Comment corriger chaque refus : le modèle réussit mieux quand on lui dit quoi changer, pas seulement ce qui ne va pas
AIDES = {
    "pas de tirage couleur ou quinte": "il faut 4 cartes de même couleur, ou 4 hauteurs qui se suivent, entre les "
                                       "2 cartes du joueur et le board, sans main déjà faite",
    "situation déjà dans la banque": "change les cartes du joueur ou le board",
    MAIN_FAITE: "ni paire en main, ni carte du joueur de la même hauteur qu'une carte du board",
    MISE_TROP_PETITE: "a_payer doit valoir au moins un tiers du pot d'avant la mise (pot - a_payer)",
}
CONSIGNES_NIVEAU = {
    "debutant": "décision nette : une main clairement à jouer ou clairement à jeter.",
    "intermediaire": "décision moins évidente : position précoce ou main limite ; au tirage, une mise d'au moins un "
                     "tiers du pot.",
    "avance": "décision serrée, proche de la limite ; au tirage, une mise d'au moins un tiers du pot.",
}


def schema(theme: str, position: str) -> dict:
    """Schéma JSON du format attendu par Ollama : la position est imposée par le code."""
    carte = {"type": "string", "enum": CARTES}
    board = TAILLES_BOARD[theme]
    return {
        "type": "object",
        "properties": {
            "position": {"type": "string", "enum": [position]},
            "cartes": {"type": "array", "items": carte, "minItems": 2, "maxItems": 2},
            "board": {"type": "array", "items": carte, "minItems": min(board), "maxItems": max(board)},
            "pot": {"type": "number"},
            "a_payer": {"type": "number"},
        },
        "required": list(CHAMPS_MODELE),
        "additionalProperties": False,
    }


def demande(theme: str, niveau: str, position: str) -> str:
    lignes = [f"Thème : {theme} — {CONSIGNES_THEME[theme]}",
              f"Niveau du joueur : {niveau} — {CONSIGNES_NIVEAU[niveau]}",
              f"Position imposée : {position}.",
              "Réponds avec le JSON seulement."]
    return "\n".join(lignes)


def cle(theme: str, sit: dict) -> str:
    """Identité d'une situation, pour repérer les doublons."""
    return f"{theme}|{sit['position']}|{' '.join(sorted(sit['cartes']))}|{' '.join(sit['board'])}"


def _codes(valeur) -> list:
    return valeur if isinstance(valeur, list) else []


def _nombre(valeur) -> bool:
    return isinstance(valeur, (int, float)) and not isinstance(valeur, bool)


def _cartes(codes: list[str]) -> list[equity.Card]:
    return equity.parse_cards(" ".join(codes))


def valider(brut, theme: str, niveau: str, deja_vues: set[str]) -> list[str]:
    """Erreurs en français de la situation brute du modèle, liste vide si elle est valide."""
    if not isinstance(brut, dict):
        return ["la réponse doit être un objet JSON"]
    manquants = [f"champ manquant : {c}" for c in CHAMPS_MODELE if c not in brut]
    if manquants:
        return manquants

    problemes = []
    cartes, board = brut["cartes"], brut["board"]
    if brut["position"] not in POSITIONS[theme]:
        problemes.append(f"position impossible pour ce thème : {brut['position']}")
    if not isinstance(cartes, list) or len(cartes) != 2:
        problemes.append("il faut exactement 2 cartes")
    problemes += [f"carte inconnue : {c}" for c in _codes(cartes) if c not in CARTES]
    if not isinstance(board, list) or len(board) not in TAILLES_BOARD[theme]:
        problemes.append(f"board de {len(_codes(board))} cartes impossible pour ce thème")
    problemes += [f"carte inconnue : {c}" for c in _codes(board) if c not in CARTES]
    tous = [c for c in _codes(cartes) + _codes(board) if c in CARTES]
    problemes += [f"carte en double : {c}" for c in dict.fromkeys(tous) if tous.count(c) > 1]

    pot, a_payer = brut["pot"], brut["a_payer"]
    if not (_nombre(pot) and _nombre(a_payer)):
        problemes.append("pot et a_payer doivent être des nombres")
    elif theme == "ouverture" and (pot != POT_AVANT_FLOP or a_payer != 0):
        problemes.append("avant le flop sans relance, pot 1.5 et a_payer 0")
    elif theme == "tirage" and not 0 < a_payer < pot:
        problemes.append("a_payer doit être positif et plus petit que pot")
    elif theme == "tirage" and niveau != "debutant" and a_payer < MISE_MIN * (pot - a_payer):
        problemes.append(MISE_TROP_PETITE)

    if problemes:
        return problemes

    if theme == "ouverture" and niveau == "debutant":
        cellule = preflop.hand_range("".join(cartes))[brut["position"]]
        if isinstance(cellule, tuple):
            problemes.append("main limite à cette position : trop ambiguë pour un débutant")
    if theme == "tirage":
        groupes = odds.outs(_cartes(cartes), _cartes(board))
        if "Couleur" not in groupes and "Quinte" not in groupes:
            problemes.append("pas de tirage couleur ou quinte")
        hauteurs = [c[0] for c in cartes]
        if hauteurs[0] == hauteurs[1] or any(c[0] in hauteurs for c in board):
            problemes.append(MAIN_FAITE)
    if cle(theme, brut) in deja_vues:
        problemes.append("situation déjà dans la banque")
    return problemes


def reference(sit: dict) -> dict:
    """La bonne réponse et les faits qui la justifient, calculés par le code."""
    if sit["theme"] == "ouverture":
        return _reference_ouverture(sit)
    if sit["theme"] == QUI_GAGNE:
        return _reference_qui_gagne(sit)
    if sit["theme"] == DEFENSE:
        return _reference_defense(sit)
    return _reference_tirage(sit)


def _reference_defense(sit: dict) -> dict:
    # graine tirée des cartes : la même situation donne toujours la même référence
    rng = random.Random(cle(DEFENSE, sit) + sit["ouvreur"])
    eq = equity.versus_range(_cartes(sit["cartes"]), preflop.opening_range(sit["ouvreur"]), ECHANTILLONS_DEFENSE,
                             rng).equity
    requis = odds.pot_odds(sit["pot"], sit["a_payer"])
    realisee = eq * REALISATION_BB
    if realisee < requis - MARGE_DEFENSE:
        bonnes, acceptables = ["fold"], []
    elif realisee < requis + MARGE_DEFENSE:
        bonnes, acceptables = [], ["call", "fold"]
    else:
        bonnes, acceptables = ["call"], ["raise"] if eq >= RELANCE_DEFENSE else []
    main = preflop.normalize_hand("".join(sit["cartes"]))
    faits = [f"Équité de {main} contre la range d'ouverture du {sit['ouvreur']} : {equity.pct(eq)}",
             f"Équité réalisée hors position (environ {round(REALISATION_BB * 100)} %) : {equity.pct(realisee)}",
             f"Cote du pot : il faut {equity.pct(requis)} d'équité "
             f"(payer {sit['a_payer']:g} pour un pot de {sit['pot']:g})",
             "Hypothèse : range d'ouverture 6-max 100bb ; la part d'équité réalisée hors position est une moyenne."]
    if eq >= RELANCE_DEFENSE:
        faits.insert(3, f"Au-dessus de {equity.pct(RELANCE_DEFENSE)} d'équité, relancer se défend aussi.")
    return {"bonnes": bonnes, "acceptables": acceptables, "faits": faits}


def _scores(sit: dict) -> tuple[tuple, tuple]:
    """La force de la meilleure main de 5 cartes du joueur et de son adversaire (la plus grande gagne)."""
    return (equity.evaluate7(_cartes(sit["cartes"] + sit["board"])),
            equity.evaluate7(_cartes(sit["adversaire"] + sit["board"])))


def _reference_qui_gagne(sit: dict) -> dict:
    moi, lui = _scores(sit)
    bonne = "moi" if moi > lui else "adversaire" if lui > moi else "egalite"
    faits = [f"Ta meilleure main : {equity.hand_name(_cartes(sit['cartes'] + sit['board']))}",
             f"Celle de ton adversaire : {equity.hand_name(_cartes(sit['adversaire'] + sit['board']))}"]
    if bonne == "egalite":
        faits.append("Mêmes cinq meilleures cartes : le pot est partagé.")
    elif moi[0] == lui[0]:
        faits.append("Même combinaison : on départage par la hauteur des cartes, puis par le kicker.")
    faits.append("Règle : chacun garde ses 5 meilleures cartes parmi ses 2 cartes et les 5 du board.")
    return {"bonnes": [bonne], "acceptables": [], "faits": faits}


def _reference_ouverture(sit: dict) -> dict:
    cellules = preflop.hand_range("".join(sit["cartes"]))
    cellule = cellules[sit["position"]]
    if isinstance(cellule, tuple):
        bonnes, acceptables = [], ["raise", "fold"]
    else:
        bonnes, acceptables = [cellule], []

    parties = []
    for libelle, pred in (("ouvrir en", lambda c: c == "raise"),
                          ("limite en", lambda c: isinstance(c, tuple)),
                          ("se coucher en", lambda c: c == "fold")):
        found = [pos for pos, c in cellules.items() if pred(c)]
        if found:
            parties.append(f"{libelle} {', '.join(found)}")
    main = preflop.normalize_hand("".join(sit["cartes"]))
    faits = [f"{main} : {' ; '.join(parties)}", "Référence : ranges d'ouverture 6-max, 100 blindes."]
    return {"bonnes": bonnes, "acceptables": acceptables, "faits": faits}


def _reference_tirage(sit: dict) -> dict:
    tous = odds.outs(_cartes(sit["cartes"]), _cartes(sit["board"]))
    groupes = {nom: cartes for nom, cartes in tous.items() if nom in MAINS_DU_TIRAGE}
    total = sum(map(len, groupes.values()))
    chances = odds.hit_chance(total, len(sit["board"]))
    une = chances["prochaine carte"]
    deux = chances.get("d'ici la river")
    requis = odds.pot_odds(sit["pot"], sit["a_payer"])
    if une >= requis:
        bonnes, acceptables = ["call"], []
    elif deux is not None and deux >= requis:
        bonnes, acceptables = [], ["call", "fold"]
    else:
        bonnes, acceptables = ["fold"], []

    detail = ", ".join(f"{len(cartes)} pour {nom.lower()}" for nom, cartes in groupes.items())
    faits = [f"Outs : {total}" + (f" ({detail})" if detail else ""),
             f"Chance de toucher à la prochaine carte : {equity.pct(une)}"]
    if len(groupes) < len(tous):
        faits.insert(1, "Les cartes qui ne donnent qu'une paire, une double paire ou un brelan ne comptent pas : "
                        "elles ne suffisent souvent pas à gagner le coup.")
    if deux is not None:
        faits.append(f"Chance de toucher d'ici la river : {equity.pct(deux)}")
    faits += [f"Cote du pot : il faut {equity.pct(requis)} d'équité "
              f"(payer {sit['a_payer']:g} pour un pot de {sit['pot']:g})",
              "Hypothèse : sans gains implicites ni semi-bluff."]
    return {"bonnes": bonnes, "acceptables": acceptables, "faits": faits}


def _au_hasard(theme: str, rng: random.Random) -> dict:
    position = rng.choice(POSITIONS[theme])
    if theme == "ouverture":
        return {"position": position, "cartes": rng.sample(CARTES, 2), "board": [], "pot": POT_AVANT_FLOP,
                "a_payer": 0}
    taille_board = rng.choice((3, 4))
    cartes = rng.sample(CARTES, 2 + taille_board)
    pot_avant = rng.choice(POTS_REPLI)
    mise = round(pot_avant * rng.choice(FRACTIONS_MISE), 1)
    return {"position": position, "cartes": cartes[:2], "board": cartes[2:], "pot": round(pot_avant + mise, 1),
            "a_payer": mise}


def repli(theme: str, niveau: str, rng: random.Random, deja_vues: set[str]) -> dict:
    """Situation tirée au hasard, relancée jusqu'à être valide."""
    for _ in range(ESSAIS_REPLI):
        brut = _au_hasard(theme, rng)
        if not valider(brut, theme, niveau, deja_vues):
            return brut
    raise RuntimeError("Aucune situation de repli valide.")


def tirer(theme: str, niveau: str, rng: random.Random, deja_vues: set[str] = frozenset()) -> dict:
    """Situation tirée par le code, tout de suite : sans appel au modèle et sans l'ajouter à la banque."""
    if theme == QUI_GAGNE:
        return _tirer_qui_gagne(niveau, rng, deja_vues)
    if theme == DEFENSE:
        return _tirer_defense(niveau, rng, deja_vues)
    return _situation(repli(theme, niveau, rng, deja_vues), theme, niveau, "code", 0, [])


def _tirer_defense(niveau: str, rng: random.Random, deja_vues: set[str]) -> dict:
    """Le CO, le bouton ou la petite blinde ouvre à 2,5 bb, les autres se couchent : tu es à la grosse blinde."""
    for _ in range(ESSAIS_REPLI):
        ouvreur = rng.choice(OUVREURS)
        sit = {"theme": DEFENSE, "position": "BB", "ouvreur": ouvreur, "cartes": rng.sample(CARTES, 2), "board": [],
               # la petite blinde (0,5) est dans l'ouverture si c'est elle qui ouvre
               "pot": OUVERTURE_BB + (1 if ouvreur == "SB" else 1.5), "a_payer": OUVERTURE_BB - 1}
        if cle(DEFENSE, sit) in deja_vues:
            continue
        sit = {"id": uuid4().hex[:8], "niveau": niveau, **sit,
               "historique": f"Tout le monde se couche jusqu'au {ouvreur}, qui relance à {OUVERTURE_BB:g} bb ; "
                             f"les autres se couchent."}
        return {**sit, "actions": list(ACTIONS[DEFENSE]), "reference": reference(sit), "source": "code",
                "tentatives": 0, "erreurs": [], "cree_le": datetime.now().isoformat(timespec="seconds")}
    raise RuntimeError("Aucune défense de grosse blinde valide.")


def _tirer_qui_gagne(niveau: str, rng: random.Random, deja_vues: set[str]) -> dict:
    """Un abattage : tes cartes, celles de l'adversaire et un board complet. Pour un débutant, deux combinaisons
    différentes : départager deux mêmes combinaisons par le kicker viendra plus tard."""
    for _ in range(ESSAIS_REPLI):
        codes = rng.sample(CARTES, 9)
        sit = {"theme": QUI_GAGNE, "position": rng.choice(POSITIONS["tirage"]), "cartes": codes[:2],
               "adversaire": codes[2:4], "board": codes[4:], "pot": 0, "a_payer": 0}
        moi, lui = _scores(sit)
        if (niveau == "debutant" and moi[0] == lui[0]) or cle(QUI_GAGNE, sit) in deja_vues:
            continue
        sit = {"id": uuid4().hex[:8], "niveau": niveau, **sit,
               "historique": f"Le coup est fini : abattage. Ton adversaire montre "
                             f"{equity.show(_cartes(sit['adversaire']))}."}
        return {**sit, "actions": list(ACTIONS[QUI_GAGNE]), "reference": reference(sit), "source": "code",
                "tentatives": 0, "erreurs": [], "cree_le": datetime.now().isoformat(timespec="seconds")}
    raise RuntimeError("Aucun abattage valide.")


def _chemin(cfg: dict):
    return ROOT / cfg.get("banque_file", "data/situations_generees.jsonl")


def lire_banque(cfg: dict) -> list[dict]:
    """Les situations de la banque, dans l'ordre du fichier."""
    chemin = _chemin(cfg)
    if not chemin.exists():
        return []
    situations = []
    for ligne in chemin.read_text(encoding="utf-8").splitlines():
        if not ligne.strip():
            continue
        try:
            situations.append(json.loads(ligne))
        except ValueError:
            print(f"Ligne illisible ignorée dans {chemin} : {ligne[:60]!r}", file=sys.stderr)
    return situations


def ajouter(situation: dict, cfg: dict) -> None:
    chemin = _chemin(cfg)
    ligne = json.dumps(situation, ensure_ascii=False)
    with _verrou:
        chemin.parent.mkdir(parents=True, exist_ok=True)
        with chemin.open("a", encoding="utf-8") as f:
            f.write(ligne + "\n")


def historique(theme: str, sit: dict) -> str:
    """Ce qui s'est passé avant la décision, écrit par le code (le modèle n'écrit pas ce texte)."""
    if theme == "ouverture":
        if sit["position"] == "UTG":
            return "Tu parles en premier (UTG)."
        return f"Tout le monde s'est couché jusqu'à toi ({sit['position']})."
    rue = "Au flop" if len(sit["board"]) == 3 else "Au turn"
    avant = round(sit["pot"] - sit["a_payer"], 1)
    return f"{rue}, ton adversaire mise {sit['a_payer']:g} bb dans un pot de {avant:g} bb."


def decrire(sit: dict) -> str:
    """La situation telle que le joueur la lit, écrite par un gabarit : aucun chiffre ne passe par le modèle."""
    quiz = sit.get("theme") == QUI_GAGNE   # la position ne compte pas à l'abattage
    lignes = ["Table 6 joueurs, quiz d'abattage." if quiz else
              f"Table 6 joueurs, 100 blindes · tu es {NOMS_POSITIONS[sit['position']]}.",
              f"{sit['historique']} Tu as {equity.show(_cartes(sit['cartes']))}."]
    if quiz:
        lignes.append(f"Board : {equity.show(_cartes(sit['board']))}.")
    elif sit.get("theme") == DEFENSE:
        lignes.append(f"Avant le flop · pot {sit['pot']:g} bb, à payer {sit['a_payer']:g} bb.")
    elif sit["board"]:
        lignes.append(f"Board : {equity.show(_cartes(sit['board']))} · pot {sit['pot']:g} bb, "
                      f"à payer {sit['a_payer']:g} bb.")
    return "\n".join(lignes)


def _situation(brut: dict, theme: str, niveau: str, source: str, tentatives: int, erreurs: list) -> dict:
    valeurs = {**{c: brut[c] for c in CHAMPS_MODELE}, "historique": historique(theme, brut)}
    base = {"id": uuid4().hex[:8], "theme": theme, "niveau": niveau, **{c: valeurs[c] for c in CHAMPS}}
    return {
        **base,
        "actions": list(ACTIONS[theme]),
        "reference": reference(base),
        "source": source,
        "tentatives": tentatives,
        "erreurs": erreurs,
        "cree_le": datetime.now().isoformat(timespec="seconds"),
    }


def refus(problemes: list[str]) -> str:
    """Le message renvoyé au modèle : ce qui ne va pas et, quand on sait, comment le corriger."""
    aides = [f"{p} : {AIDES[p]}" for p in problemes if p in AIDES]
    conseil = f" Pour corriger : {'; '.join(aides)}." if aides else ""
    return f"Situation refusée : {'; '.join(problemes)}.{conseil} Corrige et renvoie le JSON complet."


def generer(theme: str, niveau: str, cfg: dict) -> dict:
    """Demande une situation au modèle, la vérifie, la corrige ou la remplace, puis l'ajoute à la banque."""
    banque = lire_banque(cfg)
    deja_vues = {cle(s["theme"], s) for s in banque}
    position = random.choice(POSITIONS[theme])
    gen_cfg = {**cfg, "system_prompt": PROMPT.read_text(encoding="utf-8").strip(),
               "format": schema(theme, position), "temperature": TEMPERATURE}
    messages = [{"role": "user", "content": demande(theme, niveau, position)}]

    erreurs, tentatives = [], 0
    sit = None
    while tentatives < MAX_TENTATIVES:
        tentatives += 1
        try:
            reponse = complete(messages, gen_cfg)
        except LLMError as e:
            erreurs.append([f"modèle indisponible : {e}"])
            break
        try:
            brut = json.loads(reponse)
        except ValueError:
            problemes = ["la réponse n'est pas du JSON"]
        else:
            problemes = valider(brut, theme, niveau, deja_vues)
        if not problemes:
            sit = _situation(brut, theme, niveau, "llm", tentatives, erreurs)
            break
        erreurs.append(problemes)
        messages = [*messages,
                    {"role": "assistant", "content": reponse},
                    {"role": "user", "content": refus(problemes)}]

    if sit is None:
        brut = repli(theme, niveau, random.Random(), deja_vues)
        sit = _situation(brut, theme, niveau, "repli", tentatives, erreurs)
    ajouter(sit, cfg)
    return sit
