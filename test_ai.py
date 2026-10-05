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


if __name__ == "__main__":
        for name, test in list(globals().items()):
                if name.startswith("test_"):
                    test()
        print("FIN TESTs")
