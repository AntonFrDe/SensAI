"""Public game state sent to the frontend, without Ollama. Run: python3 test_poker_api.py"""
from poker_api import AI, HUMAN, apply_action, player_controls, public_game_state
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


if __name__ == "__main__":
    for name, test in list(globals().items()):
        if name.startswith("test_"):
            test()
            print("ok", name)
