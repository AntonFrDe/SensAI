"""Tests de evaluate.py avec un faux modèle : ni Ollama ni réseau.

    python3 test_evaluate.py
"""
import json

import ai
import evaluate


def fake_chat(messages, **extra):
    """Répond « quinte flush royale » à tout ; en correcteur, ne valide que si la référence parle de royale."""
    if "format" not in extra:
        return "La quinte flush royale."
    prompt = messages[-1]["content"]
    ok = "royale" in prompt.split("Faits attendus")[1]
    return json.dumps({str(n): "présent" if ok else "absent" for n in extra["format"]["required"]})


def test_question_file_is_complete():
    items = evaluate.load_questions()

    assert len(items) >= 30
    assert len({item["id"] for item in items}) == len(items)
    assert all(item[key].strip() for item in items for key in ("id", "theme", "question", "reponse"))
    assert all(item["faits"] and all(fact.strip() for fact in item["faits"]) for item in items)


def test_each_question_is_answered_then_judged_by_the_model():
    ai.chat = fake_chat
    items = [item for item in evaluate.load_questions() if item["id"] in ("q01", "q02")]

    results = [evaluate.evaluate(item) for item in items]

    assert [r["reussi"] for r in results] == [True, False]
    assert results[1]["differences"] == ["Non, la couleur ne bat pas le full : absent", "Le full bat la couleur : absent"]
    assert results[0]["reponse_modele"] == "La quinte flush royale."


def test_unreadable_or_empty_verdict_counts_as_a_failure():
    for verdict in ("je pense que oui", "{}", '{"1": "bof"}'):
        ai.chat = lambda messages, **extra: verdict if "format" in extra else "réponse"

        result = evaluate.evaluate(evaluate.load_questions()[0])

        assert result["reussi"] is False and "illisible" in result["differences"][0]


def test_report_has_one_checked_box_per_success():
    ai.chat = fake_chat
    items = evaluate.load_questions()[:3]
    results = [evaluate.evaluate(item) for item in items]

    report = evaluate.render(results, "faux-modele", total=5)

    rows = [line for line in report.splitlines() if line.startswith("| ☑") or line.startswith("| ☐")]
    assert len(rows) == 3 and rows[0].startswith("| ☑ | q01")
    assert "**1/3 réussies**" in report and "interrompue : 3 questions sur 5" in report


if __name__ == "__main__":
    for name, test in list(globals().items()):
        if name.startswith("test_"):
            test()
    print("OK")
