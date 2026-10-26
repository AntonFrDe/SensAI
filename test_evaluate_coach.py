"""Tests de evaluate_coach.py avec un faux modèle : ni Ollama ni réseau.

    python3 test_evaluate_coach.py
"""
import json
import tempfile
from pathlib import Path

import evaluate_coach
import generation

CFG = {"model": "coach", "judge_model": "juge", "system_prompt": "test"}


def with_model(reply, fn, *args):
    """Run fn while llm.complete answers with reply(messages, cfg); returns (result, every call made)."""
    calls = []

    def fake(messages, cfg):
        calls.append((messages, cfg))
        return reply(messages, cfg)

    original = evaluate_coach.complete
    evaluate_coach.complete = fake
    try:
        return fn(*args), calls
    finally:
        evaluate_coach.complete = original


def test_situations_are_different_and_cycle_through_the_themes():
    tirees = evaluate_coach.situations(9, 1)
    assert [s["theme"] for s in tirees[:len(generation.TOUS_THEMES)]] == list(generation.TOUS_THEMES)
    assert len({generation.cle(s["theme"], s) for s in tirees}) == 9
    assert [s["id"] for s in evaluate_coach.situations(3, 1)] != [s["id"] for s in tirees[:3]]   # ids are fresh
    assert [s["cartes"] for s in evaluate_coach.situations(3, 1)] == [s["cartes"] for s in tirees[:3]]


def test_the_player_takes_a_wrong_decision_when_there_is_one():
    for situation in evaluate_coach.situations(9, 2):
        action = evaluate_coach.mauvaise_action(situation)
        reference = situation["reference"]
        assert action not in reference["bonnes"] or not set(situation["actions"]) - set(reference["bonnes"])


def test_faits_start_with_the_right_answer_and_drop_the_framing():
    situation = evaluate_coach.situations(1, 3)[0]   # an opening
    attendus = evaluate_coach.faits(situation)
    assert attendus[0].startswith("La bonne réponse est : ")
    assert not any(f.startswith("Référence :") for f in attendus)


def test_evaluer_asks_the_coach_then_the_judge():
    situation = evaluate_coach.situations(2, 4)[1]   # a draw: several facts

    def reply(messages, cfg):
        if "format" not in cfg:
            return "Suis : 9 outs."
        keys = cfg["format"]["required"]
        return json.dumps({k: "contredit" if k == "1" else "présent" for k in keys})

    result, calls = with_model(reply, evaluate_coach.evaluer, situation, CFG)
    (coach_messages, coach_cfg), (_, judge_cfg) = calls
    assert coach_cfg["model"] == "coach" and coach_cfg["tools"] == [] and "Verdict : erreur." in coach_cfg["system_prompt"]
    assert coach_messages == [{"role": "user", "content": evaluate_coach.QUESTION}]
    assert judge_cfg["model"] == "juge" and judge_cfg["temperature"] == 0
    assert result["contredit"] and not result["illisible"] and result["reponse"] == "Suis : 9 outs."


def test_an_unreadable_verdict_is_not_counted():
    situation = evaluate_coach.situations(1, 5)[0]
    result, _ = with_model(lambda m, cfg: "pas du json", evaluate_coach.evaluer, situation, CFG)
    assert result["illisible"] and not result["contredit"]
    assert evaluate_coach.score([result])["jugees"] == 0


def test_render_gives_the_score_and_each_situation():
    situation = evaluate_coach.situations(1, 6)[0]
    result, _ = with_model(lambda m, cfg: json.dumps({k: "présent" for k in cfg["format"]["required"]})
                           if "format" in cfg else "Couche-toi.", evaluate_coach.evaluer, situation, CFG)
    page = evaluate_coach.render([result], "coach", "juge")
    assert "**1/1 débriefs sans contradiction**" in page and f"### {situation['id']}" in page


def test_present_par_code_finds_the_action_and_the_numbers():
    assert evaluate_coach.present_par_code("La bonne réponse est : suivre ou se coucher.", "Tu peux te coucher.") is False
    assert evaluate_coach.present_par_code("La bonne réponse est : suivre ou se coucher.", "Il faut Se coucher.")
    fait = "Cote du pot : il faut 30,0 % d'équité (payer 6 pour un pot de 14)"
    assert evaluate_coach.present_par_code(fait, "payer 6 bb dans un pot de 14 bb, soit 30.0 %")
    assert not evaluate_coach.present_par_code(fait, "payer 6 bb pour 14 bb, soit 33 %")
    assert evaluate_coach.present_par_code("Ta meilleure main : Couleur", "une couleur") is None
    equite = "Équité de 42o contre la range d'ouverture du SB : 31,8 %"
    assert evaluate_coach.present_par_code(equite, "Avec 4♥ 2♣, ton équité est de 31,8 %.")
    realisee = "Équité réalisée hors position (environ 80 %) : 25,4 %"
    assert evaluate_coach.present_par_code(realisee, "tu réalises 25,4 % hors position")
    assert evaluate_coach.present_par_code("99 : ouvrir partout", "99 s'ouvre partout") is None



def test_failed_situations_are_kept_once_for_the_next_run():
    tirees = evaluate_coach.situations(3, 1)
    ok = {"contredit": False, "faits": [{"code": True}]}
    contredit = {"contredit": True, "faits": [{"code": True}]}
    manque = {"contredit": False, "faits": [{"code": None}, {"code": False}]}
    assert [evaluate_coach.rate(r) for r in (ok, contredit, manque)] == [False, False, True]
    with tempfile.TemporaryDirectory() as tmp:
        chemin = Path(tmp) / "ratees.jsonl"
        assert evaluate_coach.lire_ratees(chemin) == []
        assert evaluate_coach.garder_ratees(tirees, [ok, contredit, manque], chemin) == 1
        assert evaluate_coach.garder_ratees(tirees, [manque, manque, manque], chemin) == 2
        assert [s["id"] for s in evaluate_coach.lire_ratees(chemin)] == [tirees[i]["id"] for i in (2, 0, 1)]


def test_the_readme_line_gets_the_last_score_and_its_date():
    payload = {"date": "2026-10-26T10:00:00", "coach": "c", "juge": "j",
               "score": {"situations": 4, "jugees": 3, "sans_contradiction": 2, "faits_retrouves_par_code": 5,
                         "faits_verifiables": 6}}
    with tempfile.TemporaryDirectory() as tmp:
        chemin = Path(tmp) / "README.md"
        chemin.write_text("# T\n\nDernier score enregistré : ancien.\nSuite.\n", encoding="utf-8")
        assert evaluate_coach.maj_readme(payload, chemin)
        lignes = chemin.read_text(encoding="utf-8").splitlines()
        assert lignes[2].startswith("Dernier score enregistré : 2026-10-26, coach `c`, juge `j`, 4 situations")
        assert "**2/3 débriefs sans contradiction**, 5/6 faits" in lignes[2] and lignes[3] == "Suite."
        assert not evaluate_coach.maj_readme(payload, chemin)


if __name__ == "__main__":
    for name, test in list(globals().items()):
        if name.startswith("test_"):
            test()
            print("ok", name)
