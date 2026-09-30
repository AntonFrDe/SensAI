import pytest

from poker_engine.game import Game
from poker_engine.game_state import GamePhase
from poker_engine.player import Player


def create_game():
    players = [
        Player("Alex", 1000),
        Player("Bob", 1000),
        Player("Charlie", 1000),
    ]

    return Game(
        players,
        small_blind=10,
        big_blind=20,
    )


def test_start_hand_posts_blinds():
    game = create_game()

    game.start_hand()

    players = game.state.players

    assert players[0].current_bet == 0
    assert players[1].current_bet == 10
    assert players[2].current_bet == 20

    assert players[1].stack == 990
    assert players[2].stack == 980

    assert game.state.pot == 30
    assert game.state.current_bet == 20


def test_start_hand_gives_two_cards():
    game = create_game()

    game.start_hand()

    for player in game.state.players:
        assert player.hand_size == 2


def test_check_is_allowed_when_no_bet_is_facing():
    game = create_game()

    game.start_hand()

    player = game.current_player

    player.current_bet = 20
    game.state.current_bet = 20

    game.check()

    assert game.current_player != player


def test_check_is_not_allowed_when_facing_bet():
    game = create_game()

    game.start_hand()

    game.state.current_bet = 50

    with pytest.raises(RuntimeError):
        game.check()


def test_call_pays_difference():
    game = create_game()

    game.start_hand()

    player = game.current_player

    player.current_bet = 20
    game.state.current_bet = 50

    game.call()

    assert player.current_bet == 50
    assert player.stack == 950
    assert game.state.pot == 80


def test_bet():
    game = create_game()

    game.start_hand()

    player = game.current_player

    game.state.current_bet = 0
    player.current_bet = 0

    game.bet(100)

    assert player.current_bet == 100
    assert player.stack == 900
    assert game.state.current_bet == 100
    assert game.state.pot == 130


def test_raise():
    game = create_game()

    game.start_hand()

    player = game.current_player

    player.current_bet = 20
    game.state.current_bet = 20
    game.state.last_raise_size = 20

    game.raise_bet(60)

    assert player.current_bet == 60
    assert player.stack == 940
    assert game.state.current_bet == 60
    assert game.state.last_raise_size == 40


def test_raise_below_minimum_is_rejected():
    game = create_game()

    game.start_hand()

    player = game.current_player

    player.current_bet = 20
    game.state.current_bet = 20
    game.state.last_raise_size = 20

    with pytest.raises(ValueError):
        game.raise_bet(30)


def test_all_in():
    game = create_game()

    game.start_hand()

    player = game.current_player

    player.current_bet = 20
    game.state.current_bet = 20

    game.all_in()

    assert player.stack == 0
    assert player.current_bet == 1000
    assert game.state.current_bet == 1000
    assert game.state.pot == 1030


def test_fold():
    game = create_game()

    game.start_hand()

    player = game.current_player

    game.fold()

    assert player.folded is True
    assert game.current_player != player


def test_flop_resets_betting_round():
    game = create_game()

    game.start_hand()
    game.deal_flop()

    assert game.state.phase == GamePhase.FLOP
    assert game.state.community_card_count == 3
    assert game.state.current_bet == 0

    for player in game.state.players:
        assert player.current_bet == 0


def test_turn_resets_betting_round():
    game = create_game()

    game.start_hand()
    game.deal_flop()
    game.deal_turn()

    assert game.state.phase == GamePhase.TURN
    assert game.state.community_card_count == 4
    assert game.state.current_bet == 0


def test_river_resets_betting_round():
    game = create_game()

    game.start_hand()
    game.deal_flop()
    game.deal_turn()
    game.deal_river()

    assert game.state.phase == GamePhase.RIVER
    assert game.state.community_card_count == 5
    assert game.state.current_bet == 0


def test_end_hand():
    game = create_game()

    game.start_hand()
    game.deal_flop()
    game.deal_turn()
    game.deal_river()

    game.end_hand()

    assert game.state.phase == GamePhase.SHOWDOWN


def test_only_current_player_can_act():
    game = create_game()

    game.start_hand()

    current_player = game.current_player

    other_player = next(
        player
        for player in game.state.players
        if player != current_player
    )

    with pytest.raises(RuntimeError):
        game._require_current_player(other_player)
