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


def test_fiche_is_checked_against_its_schema():
    debrief = [{"role": "user", "content": "pourquoi ?"},
               {"role": "assistant", "content": "", "tool_calls": [{"function": {"name": "x"}}]},
               {"role": "tool", "tool_name": "x", "content": "résultat"},
               {"role": "assistant", "content": "Parce que K9s s'ouvre au bouton."}]
    seen = []

    def fake(messages, cfg):
        seen.append((messages, cfg))
        return '{"a_retenir": "K9s s\'ouvre au bouton.", "theme_a_revoir": "ouverture"}'

    original = coach.complete
    coach.complete = fake
    try:
        result = coach.fiche(SITUATION, "debutant", "fold", "erreur", debrief, CFG)
    finally:
        coach.complete = original
    assert result == {"a_retenir": "K9s s'ouvre au bouton.", "theme_a_revoir": "ouverture"}
    messages, cfg = seen[0]
    assert [m["content"] for m in messages] == ["pourquoi ?", "Parce que K9s s'ouvre au bouton.",
                                               "Écris la fiche de fin d'exercice."]
    assert cfg["format"] == coach.schema_retenir() and "Verdict : erreur." in cfg["system_prompt"]
    assert raises(coach.lire_json, '{"a_retenir": "x", "theme_a_revoir": "bluff"}', coach.schema_fiche())


def test_the_theme_to_review_follows_the_verdict_not_the_model():
    original = coach.complete
    coach.complete = lambda messages, cfg: '{"a_retenir": "Ouvre K9s au bouton.", "theme_a_revoir": "defense_bb"}'
    try:
        themes = {verdict: coach.fiche(SITUATION, "debutant", "raise", verdict, [], CFG)["theme_a_revoir"]
                  for verdict in ("bon", "acceptable", "erreur")}
    finally:
        coach.complete = original
    assert themes == {"bon": "aucun", "acceptable": "ouverture", "erreur": "ouverture"}


def test_lire_question_wants_a_question_and_two_to_four_choices():
    assert coach.lire_question({"question": " Outs ? ", "choix": ["9", " 15 "]}) == {"question": "Outs ?",
                                                                                     "choix": ["9", "15"]}
    assert raises(coach.lire_question, {"question": "Outs ?", "choix": ["9"]})
    assert raises(coach.lire_question, {"question": "", "choix": ["9", "15"]})
    assert raises(coach.lire_question, "Outs ?")


def test_a_question_on_outs_must_offer_the_computed_count():
    assert coach.lire_question({"question": "Combien d'outs ?", "choix": ["15", "9"]}, 9)["choix"] == ["15", "9"]
    assert coach.lire_question({"question": "Quelle main ?", "choix": ["paire", "brelan"]}, 9)
    assert raises(coach.lire_question, {"question": "Combien d'outs ?", "choix": ["19", "15"]}, 9)
    assert coach.outs_de({"faits": ["Outs : 9 (9 pour couleur)", "Cote du pot : 25 %"]}) == 9
    assert coach.outs_de({"faits": ["K9s : ouverture"]}) is None


def test_a_question_to_the_player_ends_the_turn():
    FakeOllama.reset()
    FakeOllama.tool_call = {"name": "poser_question", "arguments": {"question": "Outs ?", "choix": ["9", "15"]}}
    toolbox = FakeToolbox()
    events = list(coach.repondre([], "pourquoi ?", {**CFG, "tools": [coach.OUTIL_QUESTION]}, toolbox))
    assert ("question", {"question": "Outs ?", "choix": ["9", "15"]}) in events
    assert toolbox.calls == [] and len(FakeOllama.requests) == 1   # no MCP call, no second round
    turn, _ = events[-1][1]
    assert [m["role"] for m in turn] == ["user", "assistant", "tool"]


def test_a_broken_question_goes_back_to_the_model():
    FakeOllama.reset()
    FakeOllama.tool_call = {"name": "poser_question", "arguments": {"question": "Outs ?"}}
    events = list(coach.repondre([], "pourquoi ?", {**CFG, "tools": [coach.OUTIL_QUESTION]}, FakeToolbox()))
    assert not any(kind == "question" for kind, _ in events)
    assert FakeOllama.requests[1]["messages"][-1]["content"].startswith("Erreur : il faut de 2 à 4 choix")



def test_a_question_without_the_computed_outs_goes_back_to_the_model():
    FakeOllama.reset()
    FakeOllama.tool_call = {"name": "poser_question", "arguments": {"question": "Combien d'outs ?", "choix": ["4", "8"]}}
    cfg = {**CFG, "tools": [coach.OUTIL_QUESTION], "outs": 9}
    events = list(coach.repondre([], "pourquoi ?", cfg, FakeToolbox()))
    assert not any(kind == "question" for kind, _ in events)
    assert "les 9 outs de la référence" in FakeOllama.requests[1]["messages"][-1]["content"]
    assert "outs" not in FakeOllama.requests[0]


if __name__ == "__main__":
    for name, test in list(globals().items()):
        if name.startswith("test_"):
            test()
            print("ok", name)
