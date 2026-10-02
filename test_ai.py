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

def test_prompt_puts_the_context_before_the_question():
        question = "Quelle est la meilleur main ?"

        prompt = ai.build_prompt(question)

        assert prompt.index("Quinte flush royale") < prompt.index(question)

if __name__ == "__main__":
        for name, test in list(globals().items()):
                if name.startswith("test_"):
                    test()
        print("FIN TESTs")