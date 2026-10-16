"""Public game state sent to the frontend, without Ollama. Run: python3 test_poker_api.py"""
import random

from poker_api import (
    AI, HUMAN, apply_action, best_hand, create_game, hand_rankings, next_hand, odds_summary, player_controls,
    public_game_state,
)
from poker_engine.card import Card, Suit
from poker_engine.game import Game
from poker_engine.player import Player


def new_game(human_chips: int = 1000, ai_chips: int = 1000) -> Game:
    game = Game([Player("Vous", human_chips), Player("IA", ai_chips)])
    game.start_hand()
    return game


def test_controls_give_the_amount_to_call():
    game = new_game()
    first = AI if game.state.current_player is game.state.players[AI] else HUMAN

    controls = player_controls(game, first)

    assert controls["allowedActions"] == ["fold", "call", "raise"]
    assert controls["toCall"] == 10 and controls["minAmount"] == 40


def test_nothing_to_call_once_the_blinds_are_matched():
    game = new_game()
    first = AI if game.state.current_player is game.state.players[AI] else HUMAN
    apply_action(game, first, "call")

    controls = player_controls(game, 1 - first)

    assert "check" in controls["allowedActions"] and controls["toCall"] == 0


def test_amount_to_call_is_capped_by_the_stack():
    game = new_game()
    first = AI if game.state.current_player is game.state.players[AI] else HUMAN
    stacks = [1000, 1000]
    stacks[1 - first] = 300
    game = new_game(*stacks)
    apply_action(game, first, "raise", 1000)
    short = game.state.players[1 - first]

    assert short.current_bet + short.chips == 300
    assert player_controls(game, 1 - first)["toCall"] == short.chips


def test_controls_are_empty_when_it_is_not_your_turn():
    game = new_game()
    waiting = HUMAN if game.state.current_player is game.state.players[AI] else AI

    assert player_controls(game, waiting) == {"allowedActions": []}
    assert public_game_state(game)["controls"] == player_controls(game, HUMAN)


def test_seats_show_dealer_blinds_and_street_bets():
    game = new_game()

    state = public_game_state(game)
    seats = state["seats"]

    assert state["blinds"] == {"small": 10, "big": 20}
    assert {seats["player"]["blind"], seats["opponent"]["blind"]} == {"small", "big"}
    assert [seats["player"]["dealer"], seats["opponent"]["dealer"]].count(True) == 1
    small = next(seat for seat in seats.values() if seat["blind"] == "small")
    assert small["bet"] == 10 and small["stack"] == 990
    assert seats["player"]["name"] == "Vous" and seats["opponent"]["name"] == "IA"


def test_seats_flag_folded_and_all_in_players():
    game = new_game()
    first = AI if game.state.current_player is game.state.players[AI] else HUMAN
    raiser, folder = ("opponent", "player") if first == AI else ("player", "opponent")
    apply_action(game, first, "raise", player_controls(game, first)["maxAmount"])

    assert public_game_state(game)["seats"][raiser]["allIn"]

    apply_action(game, 1 - first, "fold")
    seats = public_game_state(game)["seats"]

    assert seats[folder]["folded"] and not seats[folder]["allIn"]
    assert not seats[raiser]["allIn"] and seats[raiser]["stack"] > 0


def test_dealer_moves_with_the_next_hand():
    game = new_game()
    dealer_before = public_game_state(game)["seats"]["player"]["dealer"]
    first = AI if game.state.current_player is game.state.players[AI] else HUMAN
    apply_action(game, first, "fold")
    next_hand(game)

    assert public_game_state(game)["seats"]["player"]["dealer"] is not dealer_before


def cards(*codes: str) -> list[Card]:
    suits = {"s": Suit.SPADES, "h": Suit.HEARTS, "d": Suit.DIAMONDS, "c": Suit.CLUBS}
    return [Card(code[:-1], suits[code[-1]]) for code in codes]


def test_best_hand_names_the_rank_and_keeps_the_five_best_cards():
    hand = best_hand(cards("Ah", "As", "Kh", "7h", "2h", "9c", "3h"))

    assert hand["rank"] == "flush"
    assert hand["cards"] == [{"rank": r, "suit": "hearts"} for r in ("A", "K", "7", "2", "3")]


def test_best_hand_finds_the_wheel_and_the_pair():
    assert best_hand(cards("Ah", "2s", "3d", "4c", "5h", "Kc", "Kd"))["rank"] == "straight"
    assert best_hand(cards("Qh", "Qs", "3d", "8c", "Jh"))["rank"] == "one_pair"


def test_no_hand_before_the_flop():
    assert best_hand(cards("Ah", "As")) is None


def test_opponent_hand_stays_hidden_until_the_showdown():
    game = new_game()
    assert public_game_state(game)["hands"] == {"player": None, "opponent": None}

    first = AI if game.state.current_player is game.state.players[AI] else HUMAN
    apply_action(game, first, "call")
    apply_action(game, 1 - first, "check")
    hands = public_game_state(game)["hands"]

    assert game.state.phase.value == "flop" and len(hands["player"]["cards"]) == 5
    assert hands["opponent"] is None

def test_default_game_keeps_the_classic_table():
    state = public_game_state(create_game())

    assert state["blinds"] == {"small": 10, "big": 20}
    assert sum(seat["stack"] + seat["bet"] for seat in state["seats"].values()) == 2000


def test_game_options_set_blinds_and_stack_depth():
    game = create_game({"blinds": "25/50", "stackBigBlinds": 200})
    state = public_game_state(game)

    assert state["blinds"] == {"small": 25, "big": 50}
    assert {seat["stack"] + seat["bet"] for seat in state["seats"].values()} == {10_000}


def test_invalid_game_options_are_refused():
    for options in ([], {"blinds": "1/2"}, {"stackBigBlinds": 19}, {"stackBigBlinds": 501}, {"stackBigBlinds": "100"},
                    {"stackBigBlinds": True}):
        try:
            create_game(options)
        except ValueError:
            continue
        raise AssertionError(f"accepted {options}")


def to_act(game) -> int:
    return AI if game.state.current_player is game.state.players[AI] else HUMAN


def test_odds_give_pot_odds_when_facing_a_bet():
    game = new_game()
    game.state.players[to_act(game)].hand[:] = cards("Ah", "Ad")

    summary = odds_summary(game, to_act(game), random.Random(7))

    assert summary["toCall"] == 10 and summary["pot"] == 30
    assert summary["potOdds"] == 10 / 40
    assert 0.8 < summary["equity"]["share"] < 0.9 and summary["outs"] is None


def test_odds_count_outs_on_the_flop():
    game = new_game()
    apply_action(game, to_act(game), "call")
    apply_action(game, to_act(game), "check")
    seat = to_act(game)
    game.state.players[seat].hand[:] = cards("Ah", "Kh")
    game.state.community_cards[:] = cards("Qh", "7h", "2c")

    summary = odds_summary(game, seat, random.Random(7))

    assert summary["potOdds"] is None
    assert summary["outs"]["byHand"] == {"Couleur": 9, "Paire": 6} and summary["outs"]["count"] == 15
    assert summary["outs"]["nextCard"] == 15 / 47 and summary["outs"]["byRiver"] > 0.5


def test_odds_are_refused_out_of_turn():
    game = new_game()
    try:
        odds_summary(game, 1 - to_act(game))
    except ValueError:
        return
    raise AssertionError("odds given out of turn")


def test_hand_rankings_come_with_readable_example_cards():
    rankings = hand_rankings()

    assert [row["rank"] for row in rankings] == sorted(row["rank"] for row in rankings)
    assert rankings[0]["name"] == "Quinte flush royale"
    assert rankings[0]["cards"][0] == {"rank": "A", "suit": "spades"}
    assert all(len(row["cards"]) == 5 for row in rankings)


def test_each_example_is_the_hand_it_illustrates():
    names = {"Quinte flush royale": "straight_flush", "Quinte flush": "straight_flush", "Carré": "four_of_a_kind",
             "Full": "full_house", "Couleur": "flush", "Quinte": "straight", "Brelan": "three_of_a_kind",
             "Double paire": "two_pair", "Paire": "one_pair", "Carte haute": "high_card", "Hauteur": "high_card"}
    suits = {"spades": "s", "hearts": "h", "diamonds": "d", "clubs": "c"}
    for row in hand_rankings():
        codes = [card["rank"] + suits[card["suit"]] for card in row["cards"]]
        assert best_hand(cards(*codes))["rank"] == names[row["name"]], row["name"]


if __name__ == "__main__":
    for name, test in list(globals().items()):
        if name.startswith("test_"):
            test()
            print("ok", name)
