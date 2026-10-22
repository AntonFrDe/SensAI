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


if __name__ == "__main__":
    for name, test in list(globals().items()):
        if name.startswith("test_"):
            test()
            print("ok", name)
