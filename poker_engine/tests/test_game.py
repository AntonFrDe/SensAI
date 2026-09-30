from poker_engine.game import Game
from poker_engine.game_state import GamePhase
from poker_engine.player import Player
import pytest

def test_game_creation():
    alex = Player("Alex", 1000)
    bob = Player("Bob", 1000)

    game = Game([alex, bob])

    assert game.state.players == [alex, bob]
    assert game.state.phase == GamePhase.PRE_FLOP
    assert game.state.deck.remaining == 52

def test_start_hand_deals_two_cards_to_each_player():
    alex = Player("Alex", 1000)
    bob = Player("Bob", 1000)

    game = Game([alex, bob])

    game.start_hand()

    assert alex.hand_size == 2
    assert bob.hand_size == 2

def test_start_hand_removes_correct_number_of_cards():
    alex = Player("Alex", 1000)
    bob = Player("Bob", 1000)

    game = Game([alex, bob])

    game.start_hand()

    assert game.state.deck.remaining == 48

def test_players_receive_unique_cards():
    alex = Player("Alex", 1000)
    bob = Player("Bob", 1000)

    game = Game([alex, bob])

    game.start_hand()

    cards = alex.hand + bob.hand

    assert len(cards) == 4
    assert len(set(cards)) == 4

def test_deal_flop():
    game = Game([
        Player("Alex", 1000),
        Player("Bob", 1000),
    ])

    game.start_hand()
    game.deal_flop()

    assert game.state.phase == GamePhase.FLOP
    assert game.state.community_card_count == 3

def test_deal_flop_removes_four_cards():
    game = Game([
        Player("Alex", 1000),
        Player("Bob", 1000),
    ])

    game.start_hand()
    game.deal_flop()

    assert game.state.deck.remaining == 44

def test_deal_turn():
    game = Game([
        Player("Alex", 1000),
        Player("Bob", 1000),
    ])

    game.start_hand()
    game.deal_flop()
    game.deal_turn()

    assert game.state.phase == GamePhase.TURN
    assert game.state.community_card_count == 4

def test_deal_turn_removes_two_cards():
    game = Game([
        Player("Alex", 1000),
        Player("Bob", 1000),
    ])

    game.start_hand()
    game.deal_flop()
    game.deal_turn()

    assert game.state.deck.remaining == 42

def test_deal_river():
    game = Game([
        Player("Alex", 1000),
        Player("Bob", 1000),
    ])

    game.start_hand()
    game.deal_flop()
    game.deal_turn()
    game.deal_river()

    assert game.state.phase == GamePhase.RIVER
    assert game.state.community_card_count == 5

def test_deal_river_removes_two_cards():
    game = Game([
        Player("Alex", 1000),
        Player("Bob", 1000),
    ])

    game.start_hand()
    game.deal_flop()
    game.deal_turn()
    game.deal_river()

    assert game.state.deck.remaining == 40

def test_end_hand():
    game = Game([
        Player("Alex", 1000),
        Player("Bob", 1000),
    ])

    game.start_hand()
    game.deal_flop()
    game.deal_turn()
    game.deal_river()
    game.end_hand()

    assert game.state.phase == GamePhase.SHOWDOWN

def test_cannot_deal_turn_before_flop():
    game = Game([
        Player("Alex", 1000),
        Player("Bob", 1000),
    ])

    game.start_hand()

    with pytest.raises(RuntimeError):
        game.deal_turn()

def test_cannot_deal_river_before_turn():
    game = Game([
        Player("Alex", 1000),
        Player("Bob", 1000),
    ])

    game.start_hand()
    game.deal_flop()

    with pytest.raises(RuntimeError):
        game.deal_river()

def test_cannot_end_hand_before_river():
    game = Game([
        Player("Alex", 1000),
        Player("Bob", 1000),
    ])

    game.start_hand()

    with pytest.raises(RuntimeError):
        game.end_hand()

def test_start_new_hand_resets_state():
    alex = Player("Alex", 1000)
    bob = Player("Bob", 1000)

    game = Game([alex, bob])

    game.start_hand()
    game.deal_flop()
    game.deal_turn()
    game.deal_river()
    game.end_hand()

    game.start_hand()

    assert game.state.phase == GamePhase.PRE_FLOP
    assert game.state.community_card_count == 0
    assert game.state.pot == 0
    assert alex.hand_size == 2
    assert bob.hand_size == 2
    assert game.state.deck.remaining == 48

