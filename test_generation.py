"""Tests de generation.py, sans Ollama : le faux modèle renvoie des réponses écrites à la main.

    python3 test_generation.py
"""
import json
import random
import tempfile
from pathlib import Path

import generation
from llm import LLMError

OUVERTURE = {"position": "BTN", "cartes": ["Kd", "9d"], "board": [], "pot": 1.5, "a_payer": 0,
             "historique": "Tout le monde s'est couché jusqu'à toi."}
TIRAGE = {"position": "BTN", "cartes": ["Ah", "5h"], "board": ["Kh", "7h", "2c"], "pot": 6, "a_payer": 2,
          "historique": "Au flop, ton adversaire mise 2 bb."}


def sit(theme: str, **champs) -> dict:
    """Situation complète pour reference() : le thème et les champs donnés."""
    base = OUVERTURE if theme == "ouverture" else TIRAGE
    return {**base, "theme": theme, **champs}


def valider(brut, theme="tirage", niveau="intermediaire", deja_vues=frozenset()):
    return generation.valider(brut, theme, niveau, set(deja_vues))


def simuler(theme, niveau, reponses, banque):
    """generer() avec un faux modèle qui renvoie les réponses données, dans l'ordre (une exception est levée)."""
    appels = []

    def faux(messages, cfg):
        appels.append((messages, cfg))
        reponse = reponses[len(appels) - 1]
        if isinstance(reponse, Exception):
            raise reponse
        return reponse

    original = generation.complete
    generation.complete = faux
    try:
        sit_generee = generation.generer(theme, niveau, {"banque_file": str(banque)})
    finally:
        generation.complete = original
    return sit_generee, appels


def test_ouverture_reference_follows_the_ranges():
    assert generation.reference(sit("ouverture", position="UTG", cartes=["Kd", "9d"]))["bonnes"] == ["fold"]
    assert generation.reference(sit("ouverture", position="BTN", cartes=["Kd", "9d"]))["bonnes"] == ["raise"]
    mixte = generation.reference(sit("ouverture", position="UTG", cartes=["2c", "2d"]))
    assert mixte["acceptables"] == ["raise", "fold"] and mixte["bonnes"] == []


def test_tirage_reference_compares_the_pot_odds():
    flush = generation.reference(sit("tirage"))
    assert flush["bonnes"] == ["call"] and any("25,0 %" in fait for fait in flush["faits"])

    limite = generation.reference(sit("tirage", cartes=["8h", "9d"], board=["7c", "6s", "2h"], pot=10, a_payer=8))
    assert limite["acceptables"] == ["call", "fold"] and limite["bonnes"] == []

    perdu = generation.reference(sit("tirage", board=["Kh", "7h", "2c", "Qd"], pot=10, a_payer=9))
    assert perdu["bonnes"] == ["fold"]


def test_valider_reports_each_kind_of_mistake():
    doublon = {**TIRAGE, "cartes": ["Ah", "Ah"]}
    assert "carte en double : Ah" in valider(doublon)

    inconnue = {**TIRAGE, "cartes": ["Zz", "5h"]}
    assert "carte inconnue : Zz" in valider(inconnue)

    sans_pot = {k: v for k, v in TIRAGE.items() if k != "pot"}
    assert valider(sans_pot) == ["champ manquant : pot"]

    avec_board = {**OUVERTURE, "board": ["Kh"]}
    assert "board de 1 cartes impossible pour ce thème" in valider(avec_board, "ouverture")

    tout_paye = {**TIRAGE, "a_payer": 6}
    assert "a_payer doit être positif et plus petit que pot" in valider(tout_paye)

    mixte = {**OUVERTURE, "cartes": ["2c", "2d"], "position": "UTG", "pot": 1.5, "a_payer": 0}
    assert "main limite à cette position : trop ambiguë pour un débutant" in valider(mixte, "ouverture", "debutant")

    sans_tirage = {**TIRAGE, "cartes": ["2c", "3d"], "board": ["As", "Kh", "9c"], "pot": 6, "a_payer": 2}
    assert "pas de tirage couleur ou quinte" in valider(sans_tirage)

    assert "situation déjà dans la banque" in valider(TIRAGE, deja_vues={generation.cle("tirage", TIRAGE)})

    assert valider("texte") == ["la réponse doit être un objet JSON"]


def test_historique_is_written_by_the_code():
    ouverture_utg = {"position": "UTG", "board": [], "pot": 1.5, "a_payer": 0}
    assert generation.historique("ouverture", ouverture_utg) == "Tu parles en premier (UTG)."
    assert generation.historique("tirage", TIRAGE) == "Au flop, ton adversaire mise 2 bb dans un pot de 4 bb."


def test_repli_gives_a_valid_situation_for_every_theme():
    for seed in range(30):
        for theme in generation.THEMES:
            for niveau in generation.NIVEAUX:
                brut = generation.repli(theme, niveau, random.Random(seed), set())
                assert valider(brut, theme, niveau) == [], (seed, theme, niveau, brut)


def test_generer_retries_after_a_refused_answer():
    doublon = json.dumps({**OUVERTURE, "cartes": ["Kd", "Kd"]})
    valide = json.dumps(OUVERTURE)
    with tempfile.TemporaryDirectory() as tmp:
        banque = Path(tmp) / "banque.jsonl"

        situation, appels = simuler("ouverture", "avance", [doublon, valide], banque)

        assert situation["source"] == "llm" and situation["tentatives"] == 2
        assert len(situation["erreurs"]) == 1
        messages, cfg = appels[-1]
        assert "Situation refusée" in messages[-1]["content"]
        assert "format" in cfg and cfg["temperature"] == generation.TEMPERATURE
        assert len(generation.lire_banque({"banque_file": str(banque)})) == 1
        assert situation["historique"] == "Tout le monde s'est couché jusqu'à toi (BTN)."


def test_generer_falls_back_when_the_model_is_down():
    with tempfile.TemporaryDirectory() as tmp:
        banque = Path(tmp) / "banque.jsonl"

        situation, _ = simuler("tirage", "debutant", [LLMError("hors ligne")], banque)

        assert situation["source"] == "repli" and situation["tentatives"] == 1
        assert valider(situation, "tirage", "debutant", deja_vues=()) == []


def test_lire_banque_on_a_missing_file_is_empty():
    with tempfile.TemporaryDirectory() as tmp:
        assert generation.lire_banque({"banque_file": str(Path(tmp) / "absent.jsonl")}) == []


if __name__ == "__main__":
    for name, test in list(globals().items()):
        if name.startswith("test_"):
            test()
            print("ok", name)
