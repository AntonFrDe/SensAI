"""Tests du parcours (trainer.py) : niveau, situation, décision, verdict, puis débrief contre le faux Ollama.

    python3 test_trainer.py
"""
import json
import random
import tempfile
from pathlib import Path

import generation
import trainer
from fake_ollama import FakeOllama, start
from llm import LLMError

OLLAMA = f"http://127.0.0.1:{start(FakeOllama)}"
CFG = {"model": "ok", "ollama_url": OLLAMA, "num_ctx": 1024, "system_prompt": "test",
       "banque_file": "/nonexistent/banque.jsonl"}   # situations drawn by the code only


def session(niveau="debutant", seed=0):
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


def test_noter_follows_the_reference():
    reference = {"bonnes": ["call"], "acceptables": ["fold"]}
    assert [trainer.noter(reference, a) for a in ("call", "fold", "raise")] == ["bon", "acceptable", "erreur"]


def test_each_level_gets_the_themes_it_is_ready_for():
    for niveau, themes in trainer.THEMES_PAR_NIVEAU.items():
        s = session(niveau)
        assert {s.nouvelle_situation()["theme"] for _ in range(10)} <= set(themes)


def test_a_situation_is_never_given_twice_in_a_session():
    s = session()
    cles = [generation.cle("ouverture", s.nouvelle_situation()) for _ in range(30)]
    assert len(set(cles)) == 30 and s.numero == 30


def test_the_generated_bank_comes_first():
    generee = {**generation.tirer("ouverture", "debutant", random.Random(1)), "source": "llm"}
    autre_niveau = {**generation.tirer("ouverture", "avance", random.Random(2)), "source": "llm"}
    with tempfile.TemporaryDirectory() as tmp:
        banque = Path(tmp) / "banque.jsonl"
        banque.write_text("".join(json.dumps(s) + "\n" for s in (generee, autre_niveau)))
        s = trainer.Session({**CFG, "banque_file": str(banque)}, rng=random.Random(0))
        s.choisir_niveau("debutant")
        first, second = s.nouvelle_situation(), s.nouvelle_situation()
    assert first == generee
    assert second["source"] == "code"   # the bank has nothing left for this level


def test_decider_gives_the_verdict_of_the_reference():
    s = session()
    situation = s.nouvelle_situation()
    bonne = (situation["reference"]["bonnes"] or situation["reference"]["acceptables"])[0]
    assert s.decider(bonne) in ("bon", "acceptable")
    assert s.action == bonne


def test_decider_refuses_an_impossible_action():
    s = session()
    s.nouvelle_situation()
    assert raises(s.decider, "call")   # nothing to call before the flop when everyone has folded
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


def test_a_failed_answer_stays_out_of_the_debrief():
    s = trainer.Session({**CFG, "model": "missing"}, rng=random.Random(0))
    s.choisir_niveau("1")
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
