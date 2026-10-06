from poker_engine.game import Game
from poker_engine.game_state import GamePhase
from poker_engine.player import Player


def create_game():
    players = [
        Player("Alice", 1000),
        Player("Bob", 1000),
    ]

    game = Game(players, small_blind=10, big_blind=20)
    game.start_hand()

    return game, players


def test_betting_round_completion_advances_through_all_streets():
    game, players = create_game()

    game.call()
    game.check()

    assert game.state.phase == GamePhase.FLOP
    assert game.state.community_card_count == 3
    assert game.state.current_bet == 0
    assert all(player.current_bet == 0 for player in players)
    assert all(player.acted_this_round is False for player in players)

    game.check()
    game.check()

    assert game.state.phase == GamePhase.TURN
    assert game.state.community_card_count == 4
    assert game.state.current_bet == 0
    assert all(player.acted_this_round is False for player in players)

    game.check()
    game.check()

    assert game.state.phase == GamePhase.RIVER
    assert game.state.community_card_count == 5
    assert game.state.current_bet == 0
    assert all(player.acted_this_round is False for player in players)

    game.check()
    game.check()

    assert game.state.phase == GamePhase.SHOWDOWN

def test_second_hand_keeps_the_blinds_in_the_pot_and_charges_the_right_call():
    game, players = create_game()
    game.fold()  # Bob wins the blinds: his stack is now above where he started
    game.dealer_index = 1
    game.start_hand()

    assert game.state.pot == 30
    assert sum(player.chips for player in players) + game.state.pot == 2000

    small_blind = game.current_player
    chips_before = small_blind.chips
    game.call()

    assert chips_before - small_blind.chips == 10
