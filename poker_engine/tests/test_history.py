from poker_engine.game import Game
from poker_engine.game_state import GamePhase
from poker_engine.player import Player


def create_game():
    players = [
        Player("Alice", 1000),
        Player("Bob", 1000),
    ]

    game = Game(players)
    game.start_hand()

    return game


def test_hand_history_records_hand_start_blinds_action_and_payout():
    game = create_game()

    assert [entry["type"] for entry in game.history] == [
        "hand_started",
        "blinds_posted",
    ]

    game.fold()

    assert game.state.phase == GamePhase.SHOWDOWN
    assert [entry["type"] for entry in game.history] == [
        "hand_started",
        "blinds_posted",
        "action",
        "pot_awarded",
    ]
    assert game.history[-1]["reason"] == "fold"
    assert game.history[-1]["winners"] == ["Alice"]


def test_hand_history_resets_when_new_hand_starts():
    game = create_game()

    game.fold()
    assert len(game.history) == 4

    game.start_hand()

    assert [entry["type"] for entry in game.history] == [
        "hand_started",
        "blinds_posted",
    ]