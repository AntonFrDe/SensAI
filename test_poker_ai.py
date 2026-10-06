"""Coach and AI opponent without Ollama: prompts built from a real game, decisions validated. Run: python3 test_poker_ai.py"""
import json

import poker_ai
from poker_api import AI, HUMAN, apply_action, next_hand, player_controls, public_game_state
from poker_engine.card import Card, Suit
from poker_engine.game import Game
from poker_engine.player import Player

RAISE = {"allowedActions": ["fold", "call", "raise"], "minAmount": 40, "maxAmount": 1000}
BET = {"allowedActions": ["fold", "check", "bet"], "minAmount": 1, "maxAmount": 980}


def new_game():
    game = Game([Player("Vous", 1000), Player("IA", 1000)])
    game.start_hand()
    return game


def test_situation_is_read_back_as_cards_pot_and_amount_to_call():
    game = new_game()
    game.state.players[AI].hand[:] = [Card("A", Suit.HEARTS), Card("10", Suit.SPADES)]

    prompt = poker_ai.coach_prompt(poker_ai.situation(game, AI))

    assert "Main : A♥ 10♠ | board : aucun (avant le flop)" in prompt
    assert "Cote du pot : payer 10 pour un pot de 30" in prompt


def test_nothing_to_call_gives_no_pot_odds():
    game = new_game()
    apply_action(game, AI, "call")  # the small blind completes: the big blind can check

    seen = poker_ai.situation(game, HUMAN)

    assert "je peux checker" in seen
    assert "Cote du pot" not in poker_ai.coach_prompt(seen)


def test_opponent_request_lists_legal_actions_and_constrains_the_answer():
    game = new_game()

    _, prompt, schema = poker_ai.opponent_request(poker_ai.situation(game, AI), player_controls(game, AI))

    assert prompt.endswith("Actions possibles : fold, call, raise (montant total entre 40 et 1000). Choisis-en une.")
    assert schema["properties"]["action"]["enum"] == ["fold", "call", "raise"]
    assert "Cote du pot : payer 10" in prompt  # the action list did not change the amount to call


def test_legal_decision_is_kept_and_bet_amounts_are_clamped():
    assert poker_ai.parse_decision('{"action": "call"}', RAISE) == {"action": "call", "source": "llm"}
    assert poker_ai.parse_decision('{"action": "raise", "amount": 5000}', RAISE)["amount"] == 1000
    assert poker_ai.parse_decision('{"action": "raise", "amount": 3}', RAISE)["amount"] == 40
    assert poker_ai.parse_decision('{"action": "bet"}', BET)["amount"] == 1


def test_unusable_answer_falls_back_to_check_or_call():
    for reply in (None, "Hello", "[]", '{"amount": 50}', '{"action": "check"}'):
        assert poker_ai.parse_decision(reply, RAISE) == {"action": "call", "source": "fallback"}, reply
    assert poker_ai.parse_decision("not json", BET) == {"action": "check", "source": "fallback"}


def test_actions_are_refused_out_of_turn_or_out_of_bounds():
    game = new_game()  # the AI speaks first
    for seat, action, amount in ((HUMAN, "call", None), (AI, "check", None), (AI, "raise", 39), (AI, "raise", True)):
        try:
            apply_action(game, seat, action, amount)
        except ValueError:
            continue
        raise AssertionError(f"{action} {amount} accepted for seat {seat}")


def test_next_hand_waits_for_the_end_and_alternates_the_first_speaker():
    game = new_game()
    try:
        next_hand(game)
        raise AssertionError("a hand in progress was replaced")
    except ValueError:
        pass
    apply_action(game, AI, "fold")

    next_hand(game)

    assert public_game_state(game)["currentPlayer"] == "player"
    assert public_game_state(game)["awards"] == []


def test_opponent_cards_stay_hidden_until_a_showdown():
    game = new_game()
    assert public_game_state(game)["opponentCards"] == []
    apply_action(game, AI, "fold")
    state = public_game_state(game)
    assert state["opponentCards"] == []  # a fold shows nothing
    assert state["awards"] == [{"amount": 30, "winners": ["Vous"], "reason": "fold"}]

    game = new_game()
    apply_action(game, AI, "call")
    for _ in range(3):
        apply_action(game, HUMAN, "check")
        apply_action(game, AI, "check")
    apply_action(game, HUMAN, "check")
    state = public_game_state(game)
    assert state["phase"] == "showdown" and len(state["opponentCards"]) == 2
    json.dumps(state)  # what the frontend receives


if __name__ == "__main__":
    for name, test in list(globals().items()):
        if name.startswith("test_"):
            test()
            print("ok", name)
