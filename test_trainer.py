"""Tests du parcours (trainer.py) : niveau, situation, décision, verdict, puis débrief contre le faux Ollama.

    python3 test_trainer.py
"""
import random

import generation
import trainer


def session(niveau="debutant", seed=0):
    s = trainer.Session({}, random.Random(seed))
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


if __name__ == "__main__":
    for name, test in list(globals().items()):
        if name.startswith("test_"):
            test()
            print("ok", name)
