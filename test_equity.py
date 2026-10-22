"""Tests de equity.py, sans Ollama.

    python3 test_equity.py
"""
import random
from itertools import combinations

import equity as eq


def cards(text):
    return eq.parse_cards(text)


def test_parse_accepts_letters_symbols_and_10():
    assert cards("As Kh") == cards("A♠ K♥") == [(14, 0), (13, 1)]
    assert cards("10d Tc") == [(10, 2), (10, 3)]


def test_parse_rejects_unknown_and_duplicate_cards():
    for bad in ("Ax", "1h", "As As", "A"):
        try:
            cards(bad)
        except ValueError:
            continue
        raise AssertionError(f"{bad!r} aurait dû être refusé")


def test_evaluate_known_hands():
    assert eq.evaluate7(cards("As Ks Qs Js Ts 2h 3d")) == (9, 14)       # quinte flush royale
    assert eq.evaluate7(cards("As 2h 3d 4c 5s 9h Jd")) == (5, 5)        # roue A-2-3-4-5
    assert eq.evaluate7(cards("As Ah 9d 9c 5s 5h 3d")) == (3, 14, 9, 5)  # 3 paires : la 3e sert de kicker
    assert eq.evaluate7(cards("As Ah Ad 9c 9s 9h 3d")) == (7, 14, 9)    # 2 brelans = full
    assert eq.evaluate7(cards("Ah Qh 9h 7h 5h 6c 8d")) == (6, 14, 12, 9, 7, 5)  # couleur > quinte
    assert eq.evaluate7(cards("Kh Kd Ks Kc")) == (8, 13, 0)             # carré sans kicker (4 cartes)


def test_seven_cards_equal_best_of_the_21_five_card_hands():
    rng = random.Random(0)
    for _ in range(2000):
        hand = rng.sample(eq.DECK, 7)
        assert eq.evaluate7(hand) == max(eq.evaluate7(list(five)) for five in combinations(hand, 5))


def test_same_results_as_the_engine_hand_evaluator():
    from poker_engine.card import Card, Suit
    from poker_engine.hand_evaluator import HandEvaluator

    names = {10: "10", 11: "J", 12: "Q", 13: "K", 14: "A"}
    rng = random.Random(4)
    for _ in range(2000):
        hand = rng.sample(eq.DECK, 7)
        engine = HandEvaluator.evaluate([Card(names.get(r, str(r)), list(Suit)[s]) for r, s in hand])
        assert eq.evaluate7(hand) == (int(engine.rank), *engine.tiebreaker)


def test_hand_name_uses_the_hand_rankings_data():
    assert eq.hand_name(cards("As Ks Qs Js Ts")) == "Quinte flush royale"
    assert eq.hand_name(cards("As Kd Ah 7c 2d")) == "Paire"


def test_board_that_plays_is_an_exact_split():
    # Quinte flush royale sur le board : tout le monde partage.
    result = eq.equity(cards("2c 3d"), cards("As Ks Qs Js Ts"))

    assert result.exact
    assert result.tie == 1.0 and result.equity == 0.5


def test_turn_heads_up_is_exact_and_matches_monte_carlo():
    hero, turn = cards("As Ks"), cards("Ah 7c 2d 9s")

    exact = eq.equity(hero, turn)
    sampled = eq.equity(hero, turn, samples=20_000, rng=random.Random(1), exact=False)

    assert exact.exact and exact.samples == 1035 * 44  # C(46, 2) mains adverses × 44 rivers
    assert abs(exact.equity - sampled.equity) < 0.01


def test_preflop_aces_heads_up_close_to_known_85_percent():
    result = eq.equity(cards("As Ah"), samples=20_000, rng=random.Random(2))

    assert abs(result.equity - 0.852) < 0.01
    assert abs(result.win + result.tie + result.lose - 1) < 1e-9


def test_more_opponents_lower_the_equity():
    hero = cards("As Ks")

    one, four = (eq.equity(hero, opponents=n, samples=5_000, rng=random.Random(3)) for n in (1, 4))

    assert four.equity < one.equity


def test_invalid_situations_are_refused():
    for hero, board, opponents in (("As", "", 1), ("As Kh", "Ah 7c", 1), ("As Kh", "As 7c 2d", 1), ("As Kh", "", 0)):
        try:
            eq.equity(cards(hero), cards(board), opponents)
        except ValueError:
            continue
        raise AssertionError(f"situation {hero!r} / {board!r} / {opponents} aurait dû être refusée")
    try:
        eq.equity(cards("As Kh"), samples=0)
    except ValueError:
        return
    raise AssertionError("0 tirage aurait dû être refusé")


def test_hand_class_names():
    assert eq.hand_class(cards("Ks As")) == "AKs"
    assert eq.hand_class(cards("Ad Kh")) == "AKo"
    assert eq.hand_class(cards("Qc Qd")) == "QQ"


def test_preflop_rating_from_the_table():
    aces = eq.preflop_rating(cards("As Ah"), opponents=1)
    seven_deuce = eq.preflop_rating(cards("7s 2h"), opponents=1)

    assert aces["note"] == 10 and aces["top"] < 0.01
    assert seven_deuce["note"] == 1 and seven_deuce["top"] > 0.9


def test_class_combos_counts_and_rejects_bad_names():
    assert len(eq.class_combos("QQ")) == 6 and len(eq.class_combos("AKs")) == 4 and len(eq.class_combos("AKo")) == 12
    assert all(eq.hand_class(hand) == "AKs" for hand in eq.class_combos("AKs"))
    for bad in ("AK", "AAs", "KAs", "XYo", "AKx"):
        try:
            eq.class_combos(bad)
        except ValueError:
            continue
        raise AssertionError(f"{bad!r} aurait dû être refusée")


def test_versus_matches_known_preflop_matchups():
    kings = eq.versus("KK", "QQ", 20_000, random.Random(42))
    flip = eq.versus("AKs", "88", 20_000, random.Random(42))

    assert abs(kings.equity - 0.82) < 0.015
    assert abs(flip.equity - 0.48) < 0.015  # « coin flip » : la paire est légèrement favorite


if __name__ == "__main__":
    for name, test in list(globals().items()):
        if name.startswith("test_"):
            test()
    print("OK")
