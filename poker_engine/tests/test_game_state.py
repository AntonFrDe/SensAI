from poker_engine.card import Card, Suit
from poker_engine.game_state import GamePhase, GameState
from poker_engine.player import Player
import pytest

def test_game_state_creation():
    players = [
        Player("Alex", 1000),
        Player("Bob", 1000),
    ]

    game = GameState(players)

    assert game.players == players
    assert game.deck.remaining == 52
    assert game.community_cards == []
    assert game.pot == 0
    assert game.phase == GamePhase.PRE_FLOP
    assert game.current_player_index == 0

def test_current_player():
    alex = Player("Alex", 1000)
    bob = Player("Bob", 1000)

    game = GameState([alex, bob])

    assert game.current_player == alex

def test_next_player():
    alex = Player("Alex", 1000)
    bob = Player("Bob", 1000)

    game = GameState([alex, bob])

    game.next_player()

    assert game.current_player == bob

def test_next_player_wraps_around():
    alex = Player("Alex", 1000)
    bob = Player("Bob", 1000)

    game = GameState([alex, bob])

    game.next_player()
    game.next_player()

    assert game.current_player == alex

def test_add_community_card():
    game = GameState([
        Player("Alex", 1000),
        Player("Bob", 1000),
    ])

    card = Card("A", Suit.SPADES)

    game.add_community_card(card)

    assert game.community_cards == [card]
    assert game.community_card_count == 1

def test_reject_invalid_community_card():
    game = GameState([
        Player("Alex", 1000),
    ])

    with pytest.raises(TypeError):
        game.add_community_card("A of spades")

def test_next_phase():
    game = GameState([
        Player("Alex", 1000),
    ])

    assert game.phase == GamePhase.PRE_FLOP

    game.next_phase()
    assert game.phase == GamePhase.FLOP

    game.next_phase()
    assert game.phase == GamePhase.TURN

    game.next_phase()
    assert game.phase == GamePhase.RIVER

    game.next_phase()
    assert game.phase == GamePhase.SHOWDOWN

def test_phase_does_not_go_past_showdown():
    game = GameState([
        Player("Alex", 1000),
    ])

    for _ in range(10):
        game.next_phase()

    assert game.phase == GamePhase.SHOWDOWN

def test_game_requires_players():
    with pytest.raises(ValueError):
        GameState([])

def test_game_rejects_invalid_players():
    with pytest.raises(TypeError):
        GameState(["Alex", "Bob"])

def test_game_state_string():
    game = GameState([
        Player("Alex", 1000),
        Player("Bob", 1000),
    ])

    assert str(game) == (
        "Phase: pre_flop | "
        "Pot: 0 | "
        "Players: 2 | "
        "Community cards: 0"
    )

