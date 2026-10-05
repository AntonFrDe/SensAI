from poker_engine.game import Game
from poker_engine.player import Player


def create_game():
    players = [
        Player("Alice", 1000),
        Player("Bob", 1000),
        Player("Charlie", 1000),
    ]

    game = Game(players)
    game.start_hand()

    return game, players


def test_betting_round_is_not_complete_before_players_act():
    game, players = create_game()

    assert game.is_betting_round_complete() is False


def test_betting_round_is_complete_when_all_players_have_acted():
    game, players = create_game()

    for player in players:
        player.current_bet = game.current_bet
        player.acted_this_round = True

    assert game.is_betting_round_complete() is True


def test_betting_round_is_not_complete_if_one_player_has_not_acted():
    game, players = create_game()

    for player in players:
        player.current_bet = game.current_bet
        player.acted_this_round = True

    players[2].acted_this_round = False

    assert game.is_betting_round_complete() is False


def test_folded_player_is_ignored():
    game, players = create_game()

    players[0].fold()
    players[0].acted_this_round = True

    for player in players[1:]:
        player.current_bet = game.current_bet
        player.acted_this_round = True

    assert game.is_betting_round_complete() is True


def test_all_in_player_is_ignored():
    game, players = create_game()

    players[0].chips = 0
    players[0].current_bet = game.current_bet

    for player in players[1:]:
        player.current_bet = game.current_bet
        player.acted_this_round = True

    assert game.is_betting_round_complete() is True


def test_betting_round_is_not_complete_if_player_has_not_matched_bet():
    game, players = create_game()

    for player in players:
        player.acted_this_round = True

    players[0].current_bet = game.current_bet
    players[1].current_bet = game.current_bet
    players[2].current_bet = game.current_bet - 10

    assert game.is_betting_round_complete() is False


def test_reset_hand_resets_acted_state():
    game, players = create_game()

    player = players[0]

    player.acted_this_round = True

    player.reset_hand()

    assert player.acted_this_round is False
