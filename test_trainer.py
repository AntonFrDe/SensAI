"""Tests du parcours (trainer.py) : niveau, situation, décision, verdict, puis débrief contre le faux Ollama.

    python3 test_trainer.py
"""
import json
import random
import tempfile
from pathlib import Path

import generation
import profils
import trainer
from fake_ollama import FakeOllama, start
from llm import LLMError

OLLAMA = f"http://127.0.0.1:{start(FakeOllama)}"
CFG = {"model": "ok", "ollama_url": OLLAMA, "num_ctx": 1024, "system_prompt": "test",
       "banque_file": "/nonexistent/banque.jsonl"}   # situations drawn by the code only


def session(niveau="intermediaire", seed=0):   # fold is legal in all its themes
    s = trainer.Session(CFG, rng=random.Random(seed))
    s.choisir_niveau(niveau)
    return s


def raises(fn, *args):
    try:
        fn(*args)
    except ValueError:
        return True
    return False


def test_choisir_niveau_by_number_or_name():
    s = trainer.Session({})
    assert s.choisir_niveau("1") == "debutant"
    assert s.choisir_niveau(" Avance ") == "avance"
    assert raises(s.choisir_niveau, "4") and raises(s.choisir_niveau, "expert")
    assert s.niveau == "avance"   # a refused answer keeps the level


def test_niveau_libre_takes_the_level_the_model_gives():
    original = trainer.coach.complete
    trainer.coach.complete = lambda messages, cfg: '{"niveau": "intermediaire", "raison": "Tu connais les positions."}'
    try:
        s = trainer.Session(CFG)
        assert s.niveau_libre("je joue le vendredi entre amis")["raison"] == "Tu connais les positions."
    finally:
        trainer.coach.complete = original
    assert s.niveau == "intermediaire"


def test_noter_follows_the_reference():
    reference = {"bonnes": ["call"], "acceptables": ["fold"]}
    assert [trainer.noter(reference, a) for a in ("call", "fold", "raise")] == ["bon", "acceptable", "erreur"]


def test_each_level_gets_the_themes_it_is_ready_for():
    for niveau, themes in trainer.THEMES_PAR_NIVEAU.items():
        s = session(niveau)
        assert {s.nouvelle_situation()["theme"] for _ in range(10)} <= set(themes)


def test_a_situation_is_never_given_twice_in_a_session():
    s = session()
    cles = [generation.cle(sit["theme"], sit) for sit in (s.nouvelle_situation() for _ in range(30))]
    assert len(set(cles)) == 30 and s.numero == 30


def test_the_generated_bank_comes_first():
    generee = {**generation.tirer("tirage", "avance", random.Random(1)), "source": "llm"}
    autre_niveau = {**generation.tirer("tirage", "intermediaire", random.Random(2)), "source": "llm"}
    with tempfile.TemporaryDirectory() as tmp:
        banque = Path(tmp) / "banque.jsonl"
        banque.write_text("".join(json.dumps(s) + "\n" for s in (generee, autre_niveau)))
        s = trainer.Session({**CFG, "banque_file": str(banque)}, rng=random.Random(0))
        s.choisir_niveau("avance")   # draws (from the bank) and big blind defenses (drawn by the code)
        tirages = [sit for sit in (s.nouvelle_situation() for _ in range(8)) if sit["theme"] == "tirage"]
    assert tirages[0] == generee
    assert all(sit["source"] == "code" for sit in tirages[1:])   # the bank has nothing left for this level


def test_vue_situation_hides_the_reference():
    situation = generation.tirer("tirage", "avance", random.Random(3))
    vue = trainer.vue_situation(situation)
    assert "reference" not in vue and "source" not in vue
    assert vue["texte"] == generation.decrire(situation) and vue["question"] == "Que fais-tu ?"
    assert vue["actions"][1] == {"action": "call", "libelle": "suivre"}
    quiz = trainer.vue_situation(generation.tirer("qui_gagne", "debutant", random.Random(3)))
    assert quiz["question"] == "Qui gagne ?" and len(quiz["adversaire"]) == 2


def test_decider_gives_the_verdict_of_the_reference():
    s = session()
    situation = s.nouvelle_situation()
    bonne = (situation["reference"]["bonnes"] or situation["reference"]["acceptables"])[0]
    assert s.decider(bonne) in ("bon", "acceptable")
    assert s.action == bonne


def test_decider_refuses_an_impossible_action():
    s = session("debutant")
    s.nouvelle_situation()
    assert raises(s.decider, "call")   # nothing to call before the flop, nor in a showdown quiz
    assert s.action is None


def test_nothing_happens_before_its_step():
    s = trainer.Session({})
    assert raises(s.nouvelle_situation) and raises(s.decider, "fold")


def test_a_new_situation_forgets_the_previous_decision():
    s = session()
    s.nouvelle_situation()
    s.decider("fold")
    s.nouvelle_situation()
    assert s.action is None and s.verdict is None


def test_the_profile_keeps_the_level_and_the_results():
    with tempfile.TemporaryDirectory() as tmp:
        cfg = {**CFG, "profiles_dir": tmp}
        s = trainer.Session(cfg, rng=random.Random(0), profil=profils.nouveau("amine"))
        s.choisir_niveau("2")
        theme = s.nouvelle_situation()["theme"]
        s.decider("fold")
        relu = profils.charger("amine", cfg)
        assert relu["niveau"] == "intermediaire"
        assert sum(relu["resultats"][theme].values()) == 1

        retour = trainer.Session(cfg, profil=relu)
        assert retour.niveau == "intermediaire"   # a known player skips the level question


def test_a_missed_theme_comes_back_more_often():
    rate = {**profils.nouveau("amine"), "niveau": "intermediaire",
            "resultats": {"tirage": {"bon": 0, "acceptable": 0, "erreur": 4}}}
    s = trainer.Session(CFG, rng=random.Random(0), profil=rate)
    tirages = sum(s.choisir_theme() == "tirage" for _ in range(1000))
    assert 700 < tirages < 800   # 3 chances in 4


def debrief(s, texte):
    return "".join(data for kind, data in s.discuter(texte) if kind == "token")


def test_the_debrief_knows_the_situation_and_keeps_its_history():
    FakeOllama.reset()
    s = session()
    situation = s.nouvelle_situation()
    s.decider("fold")
    assert debrief(s, "pourquoi ?") == "Hello"
    debrief(s, "et au bouton ?")

    first, second = FakeOllama.requests
    system = first["messages"][0]["content"]
    assert system.startswith("Tu es SensAI, un coach de poker") and situation["reference"]["faits"][0] in system
    assert f"Verdict : {s.verdict}." in system
    assert [m["content"] for m in second["messages"][1:]] == ["pourquoi ?", "Hello", "et au bouton ?"]


def test_a_numbered_answer_to_the_coach_question_is_sent_in_words():
    FakeOllama.reset()
    FakeOllama.tool_call = {"name": "poser_question", "arguments": {"question": "Outs ?", "choix": ["9", "15"]}}
    s = session()
    s.nouvelle_situation()
    s.decider("fold")
    debrief(s, "pourquoi ?")
    assert s.question == {"question": "Outs ?", "choix": ["9", "15"]}
    assert "poser_question" in {t["function"]["name"] for t in FakeOllama.requests[0]["tools"]}
    assert s.reponse("2") == "Je réponds : 15" and s.reponse("3") == "3" and s.reponse("neuf") == "neuf"
    FakeOllama.tool_call = None
    debrief(s, s.reponse("2"))
    assert s.question is None
    assert FakeOllama.requests[-1]["messages"][-1]["content"] == "Je réponds : 15"


def test_no_debrief_before_the_decision():
    s = session()
    s.nouvelle_situation()
    assert raises(s.discuter, "pourquoi ?")


def test_a_new_situation_or_oublier_clears_the_debrief():
    s = session()
    s.nouvelle_situation()
    s.decider("fold")
    debrief(s, "pourquoi ?")
    s.oublier()
    assert s.debrief == [] and s.action == "fold"
    debrief(s, "pourquoi ?")
    s.nouvelle_situation()
    assert s.debrief == []


def test_reprendre_brings_back_the_last_debrief_of_the_profile():
    FakeOllama.reset()
    with tempfile.TemporaryDirectory() as tmp:
        cfg = {**CFG, "profiles_dir": tmp}
        s = trainer.Session(cfg, rng=random.Random(0), profil=profils.nouveau("amine"))
        s.choisir_niveau("2")
        situation = s.nouvelle_situation()
        s.decider("fold")
        debrief(s, "pourquoi ?")

        retour = trainer.Session(cfg, profil=profils.charger("amine", cfg))
        retour.reprendre()
        assert retour.situation == situation and retour.action == "fold"
        debrief(retour, "et au bouton ?")
    assert [m["content"] for m in FakeOllama.requests[-1]["messages"][1:]] == ["pourquoi ?", "Hello", "et au bouton ?"]


def test_reprendre_without_a_debrief_is_refused():
    assert raises(session().reprendre)
    assert raises(trainer.Session(CFG, profil=profils.nouveau("amine")).reprendre)


def test_ecrire_fiche_keeps_the_card_in_the_profile():
    original = trainer.coach.complete
    trainer.coach.complete = lambda messages, cfg: '{"a_retenir": "Se coucher.", "theme_a_revoir": "aucun"}'
    try:
        with tempfile.TemporaryDirectory() as tmp:
            cfg = {**CFG, "profiles_dir": tmp}
            s = trainer.Session(cfg, rng=random.Random(0), profil=profils.nouveau("amine"))
            s.choisir_niveau("2")
            s.nouvelle_situation()
            assert raises(s.ecrire_fiche)   # not before the decision
            s.decider("fold")
            assert s.ecrire_fiche() == {"a_retenir": "Se coucher.", "theme_a_revoir": "aucun"}
            (gardee,) = profils.charger("amine", cfg)["fiches"]
    finally:
        trainer.coach.complete = original
    assert gardee["theme"] == s.situation["theme"] and gardee["verdict"] == s.verdict


def test_a_failed_answer_stays_out_of_the_debrief():
    s = trainer.Session({**CFG, "model": "missing"}, rng=random.Random(0))
    s.choisir_niveau("2")
    s.nouvelle_situation()
    s.decider("fold")
    try:
        debrief(s, "pourquoi ?")
    except LLMError:
        pass
    assert s.debrief == []


if __name__ == "__main__":
    for name, test in list(globals().items()):
        if name.startswith("test_"):
            test()
            print("ok", name)
