"""Test sans Ollama : check construction du prompt sans modèle"""

import re
import ai

def test_context_gives_the_royal_flush_the_top_force():
        best = ai.find_context("peu importe").splitlines()[1]

        assert best.startswith("- Quinte flush royale (Royal flush), force 10/10")

        assert "As, Roi, Dame, Valet, 10" in best

def test_context_lists_the_ten_hands_from_strongest_to_weakest():
        forces = re.findall(r"force (\d+)/10", ai.find_context("peu importe"))

        assert forces == [str(n) for n in range (10, 0, -1)]


def test_glossary_context_serializes_entries_as_text():
        context = ai.glossary_context()

        assert isinstance(context, str)
        assert "- Acolyte : Traduction français hasardeuse du fameux Kicker." in context
        assert "- UTG : Voir : Under The Gun." in context


def test_only_the_glossary_terms_of_the_question_are_injected():
        context = ai.glossary_context("Que veut dire UTG ?")

        assert "- UTG : Voir : Under The Gun." in context
        assert "- Under The Gun" in context  # le renvoi est suivi
        assert "Acolyte" not in context
        assert ai.glossary_context("Bonjour") == ""
        assert len(ai.build_prompt("Que veut dire UTG ?")) < 4000  # le glossaire entier dépassait 50 000


def test_prompt_puts_the_context_before_the_question():
        question = "Quelle est la meilleur main ?"

        prompt = ai.build_prompt(question)

        assert prompt.index("Quinte flush royale") < prompt.index(question)

def test_situation_in_the_question_is_computed_and_injected():
        question = "J'ai Ah Kh, le flop est Qh 7h 2c, pot de 100 et je dois payer 50. Je suis ?"

        prompt = ai.build_prompt(question)

        assert "Outs : 15" in prompt and "33,3 %" in prompt
        assert prompt.index("Outs : 15") < prompt.index(question)


def test_question_without_cards_gets_no_calculation():
        assert ai.situation_context("Quelle est la meilleure main ? As-tu une idée ?") == ""
        assert "pas une situation valide" in ai.situation_context("Ah Ah sur Kd 2c")


def test_answers_use_temperature_zero_by_default():
        sent = {}
        real_chat = ai.chat
        ai.chat = lambda messages, **extra: sent.update(extra) or "ok"
        try:
                ai.ask("Que veut dire UTG ?")
        finally:
                ai.chat = real_chat

        assert ai.TEMPERATURE == 0 and sent["options"] == {"temperature": 0}


def test_preflop_hands_are_read_in_notation_and_in_words():
        assert ai.hands_in("Faut-il ouvrir 7-2 dépareillés (72o) depuis UTG ?") == ["72o"]
        assert ai.hands_in("As-Roi assortis contre une paire de 8") == ["AKs", "88"]
        assert ai.hands_in("paire de Rois contre paire de Dames") == ["KK", "QQ"]
        assert ai.hands_in("Mes cartes : Ah Kh.") == ["AKs"]
        assert ai.hands_in("J'ai Ah Kh, le flop est Qh 7h 2c") == []
        assert ai.hands_in("As-tu une idée ? J'ai AK.") == []


def test_preflop_context_gives_the_opening_range_and_the_equity():
        context = ai.preflop_context("Depuis quelles positions ouvre-t-on Roi-9 assortis (K9s) ?")

        assert "ouvrir depuis MP (hijack), CO (cut-off), BTN (bouton), SB (petite blinde)" in context
        assert "se coucher depuis UTG" in context
        assert "85,1 %" in ai.preflop_context("Équité d'une paire d'As ?")
        assert ai.preflop_context("Que veut dire UTG ?") == ""


def test_two_preflop_hands_get_their_head_to_head_equity():
        prompt = ai.build_prompt("Paire de Rois contre paire de Dames : quelles chances ?")

        assert "KK contre QQ : KK 81,9 %, QQ 18,1 %" in prompt
        assert prompt.index("KK contre QQ") < prompt.index("quelles chances")


def test_meaning_search_skips_short_messages_and_survives_a_missing_ollama():
        url, ai.EMBED_URL = ai.EMBED_URL, "http://localhost:1/api/embed"
        try:
            assert ai.glossary_entries_like("salut") == []
            assert ai.glossary_entries_like("quand je tire quatre cartes à la couleur") == []
            assert [e.term for e in ai.glossary_entries_for("Que veut dire UTG ?")][0] == "UTG"
            assert ai.embed_warned
        finally:
            ai.EMBED_URL = url


def test_the_advice_prompt_comes_from_its_file():
        assert ai.SYSTEM == (ai.Path(ai.__file__).parent / "prompts" / "conseil.txt").read_text(encoding="utf-8")
        assert ai.SYSTEM.startswith("Tu es SensAI, un coach de poker.")


if __name__ == "__main__":
        for name, test in list(globals().items()):
                if name.startswith("test_"):
                    test()
        print("FIN TESTs")
