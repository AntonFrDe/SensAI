"""Tests de coach.py : le contexte du débrief et la boucle d'outils, contre le faux Ollama.

    python3 test_coach.py
"""
import coach
from fake_ollama import FakeOllama, start

OLLAMA = f"http://127.0.0.1:{start(FakeOllama)}"
CFG = {"model": "ok", "ollama_url": OLLAMA, "num_ctx": 1024, "system_prompt": "test"}
SITUATION = {"theme": "ouverture", "position": "BTN", "cartes": ["Kd", "9d"], "board": [], "pot": 1.5,
             "a_payer": 0, "historique": "Tout le monde s'est couché jusqu'à toi (BTN).",
             "reference": {"bonnes": ["raise"], "acceptables": [],
                           "faits": ["K9s : ouvrir en MP, CO, BTN, SB ; se coucher en UTG"]}}


def with_model(answer, fn, *args):
    """Run fn with coach.complete answering `answer`; returns (result, the config the model got)."""
    seen = []

    def fake(messages, cfg):
        seen.append(cfg)
        return answer

    original = coach.complete
    coach.complete = fake
    try:
        return fn(*args), seen[0]
    finally:
        coach.complete = original


def raises(fn, *args):
    try:
        fn(*args)
    except ValueError:
        return True
    return False


class FakeToolbox:
    def __init__(self):
        self.calls = []

    def call(self, name, arguments):
        self.calls.append((name, arguments))
        return "résultat"


def test_contexte_gives_the_decision_the_verdict_and_the_reference():
    texte = coach.contexte(SITUATION, "debutant", "fold", "erreur")
    assert "Tu as K♦ 9♦." in texte and "Main de départ : K9s : assorties (même couleur)." in texte
    assert "Décision du joueur : se coucher. Verdict : erreur." in texte
    assert "- bonnes actions : relancer" in texte and "acceptables (situation limite) : aucune" in texte
    assert "- K9s : ouvrir en MP, CO, BTN, SB ; se coucher en UTG" in texte
    assert coach.CONSIGNES_NIVEAU["debutant"] in texte


def test_contexte_adds_the_past_results_of_a_known_player():
    profil = {"pseudo": "amine", "niveau": "debutant", "dernier_debrief": None,
              "resultats": {"ouverture": {"bon": 1, "acceptable": 0, "erreur": 2}}}
    texte = coach.contexte(SITUATION, "debutant", "fold", "erreur", profil)
    assert "Résultats passés du joueur (amine) : ouverture : 1 bon, 0 acceptable, 2 erreurs." in texte
    assert texte.endswith("Thèmes à revoir : ouverture.")
    assert "Résultats passés" not in coach.contexte(SITUATION, "debutant", "fold", "erreur")


def test_main_de_depart_names_the_kind_of_hand():
    assert coach.main_de_depart(["5h", "Js"]) == "J5o : dépareillées (couleurs différentes)"
    assert coach.main_de_depart(["Qc", "Qd"]) == "QQ : une paire"


def test_config_puts_the_context_after_the_coach_prompt():
    cfg = coach.config(CFG, SITUATION, "avance", "raise", "bon")
    assert cfg["system_prompt"].startswith("Tu es SensAI, un coach de poker")
    assert cfg["system_prompt"].endswith("- K9s : ouvrir en MP, CO, BTN, SB ; se coucher en UTG")
    assert CFG["system_prompt"] == "test"   # the caller's config is left as it was


def test_repondre_streams_then_gives_the_turn():
    FakeOllama.reset()
    events = list(coach.repondre([], "salut", CFG, FakeToolbox()))
    assert "".join(data for kind, data in events if kind == "token") == "Hello"
    kind, (turn, stats) = events[-1]
    assert kind == "fin" and stats["tokens"] == 20
    assert turn == [{"role": "user", "content": "salut"}, {"role": "assistant", "content": "Hello"}]


def test_repondre_runs_the_tools_the_model_asks_for():
    FakeOllama.reset()
    FakeOllama.tool_call = {"name": "preflop_open", "arguments": {"hand": "K9s"}}
    toolbox = FakeToolbox()
    events = list(coach.repondre([], "et K9o ?", {**CFG, "tools": [{"type": "function"}]}, toolbox))
    assert ("outil", ("preflop_open", {"hand": "K9s"})) in events
    assert toolbox.calls == [("preflop_open", {"hand": "K9s"})]
    turn, _ = events[-1][1]
    assert [m["role"] for m in turn] == ["user", "assistant", "tool", "assistant"]
    assert turn[2] == {"role": "tool", "tool_name": "preflop_open", "content": "résultat"}


def test_classer_niveau_reads_the_structured_answer():
    result, cfg = with_model('{"niveau": "avance", "raison": "Tu calcules tes outs."}',
                             coach.classer_niveau, "je compte mes outs à chaque main", CFG)
    assert result == {"niveau": "avance", "raison": "Tu calcules tes outs."}
    assert cfg["format"] == coach.schema_niveau() and cfg["temperature"] == 0 and cfg["tools"] == []
    assert cfg["system_prompt"].startswith("Tu classes un joueur de poker")


def test_lire_json_refuses_what_breaks_the_schema():
    schema = coach.schema_niveau()
    assert raises(coach.lire_json, "", schema) and raises(coach.lire_json, "[]", schema)
    assert raises(coach.lire_json, '{"niveau": "expert", "raison": "x"}', schema)
    assert raises(coach.lire_json, '{"niveau": "avance", "raison": "  "}', schema)
    assert coach.lire_json('{"niveau": "avance", "raison": "x", "en_trop": 1}', schema) == {"niveau": "avance",
                                                                                           "raison": "x"}


def test_classer_niveau_against_ollama_refuses_an_answer_off_schema():
    FakeOllama.reset()
    assert raises(coach.classer_niveau, "je joue un peu", CFG)   # the fake model answers {"action": "call"}
    assert "format" in FakeOllama.requests[0]


if __name__ == "__main__":
    for name, test in list(globals().items()):
        if name.startswith("test_"):
            test()
            print("ok", name)
