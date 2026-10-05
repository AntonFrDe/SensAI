"""Tests de odds.py, sans Ollama.

    python3 test_odds.py
"""
import equity as eq
import odds


def cards(text):
    return eq.parse_cards(text)


def count(groups):
    return {name: len(found) for name, found in groups.items()}


def test_flush_draw_with_two_overcards_has_15_outs():
    assert count(odds.outs(cards("Ah Kh"), cards("Qh 7h 2c"))) == {"Couleur": 9, "Paire": 6}


def test_open_ended_and_gutshot_straight_draws():
    assert count(odds.outs(cards("8h 9d"), cards("7c 6s 2h")))["Quinte"] == 8
    assert count(odds.outs(cards("As Kd"), cards("Qh Jc 2s 3d")))["Quinte"] == 4


def test_card_that_only_pairs_the_board_is_not_an_out():
    groups = odds.outs(cards("Ah Kh"), cards("Qh 7h 2c"))

    paired = [card for found in groups.values() for card in found if card[0] in (12, 7, 2)]
    assert paired and all(card in groups["Couleur"] for card in paired)  # seuls les cœurs comptent


def test_overpair_does_not_improve_when_the_board_pairs():
    assert count(odds.outs(cards("As Ad"), cards("Kc 7d 2s"))) == {"Brelan": 2}


def test_outs_need_a_flop_or_a_turn():
    for board in ("", "Qh 7h 2c 3d 4s"):
        try:
            odds.outs(cards("Ah Kh"), cards(board))
        except ValueError:
            continue
        raise AssertionError(f"board {board!r} aurait dû être refusé")


def test_hit_chance_matches_the_known_figures():
    flop = odds.hit_chance(9, 3)  # tirage couleur au flop
    turn = odds.hit_chance(9, 4)

    assert round(flop["prochaine carte"], 3) == round(9 / 47, 3)
    assert round(flop["d'ici la river"], 3) == 0.35
    assert round(turn["prochaine carte"], 3) == round(9 / 46, 3) and len(turn) == 1


def test_pot_odds():
    assert odds.pot_odds(100, 50) == 50 / 150
    for pot, to_call in ((100, 0), (-1, 10)):
        try:
            odds.pot_odds(pot, to_call)
        except ValueError:
            continue
        raise AssertionError(f"pot {pot} / payer {to_call} aurait dû être refusé")


def test_analyse_gives_outs_and_the_call_verdict():
    text = odds.analyse(cards("Ah Kh"), cards("Qh 7h 2c"), pot=100, to_call=50)

    assert "Outs : 15" in text
    assert "33,3 %" in text and "rentable" in text


def test_analyse_before_the_flop_gives_the_rating():
    assert "Note avant le flop : 10/10" in odds.analyse(cards("As Ah"))


if __name__ == "__main__":
    for name, test in list(globals().items()):
        if name.startswith("test_"):
            test()
    print("OK")
