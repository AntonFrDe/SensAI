from poker_engine.card import Card, Suit
from poker_engine.player import Player
import pytest


def test_player_creation():
    player = Player("Alex", 1000)

    assert player.name == "Alex"
    assert player.chips == 1000
    assert player.hand == []
    assert player.folded is False


def test_player_receives_card():
    player = Player("Alex", 1000)
    card = Card("A", Suit.SPADES)

    player.receive_card(card)

    assert player.hand == [card]
    assert player.hand_size == 1


def test_player_receives_two_cards():
    player = Player("Alex", 1000)

    card1 = Card("A", Suit.SPADES)
    card2 = Card("K", Suit.HEARTS)

    player.receive_card(card1)
    player.receive_card(card2)

    assert player.hand == [card1, card2]
    assert player.hand_size == 2


def test_player_rejects_invalid_card():
    player = Player("Alex", 1000)

    with pytest.raises(TypeError):
        player.receive_card("A of spades")


def test_player_folds():
    player = Player("Alex", 1000)

    player.fold()

    assert player.folded is True


def test_player_reset_hand():
    player = Player("Alex", 1000)

    player.receive_card(Card("A", Suit.SPADES))
    player.receive_card(Card("K", Suit.HEARTS))
    player.fold()

    player.reset_hand()

    assert player.hand == []
    assert player.hand_size == 0
    assert player.folded is False


def test_player_string():
    player = Player("Alex", 1000)

    assert str(player) == "Alex (1000 chips)"

def test_player_rejects_empty_name():
    with pytest.raises(ValueError):
        Player("", 1000)


def test_player_rejects_negative_chips():
    with pytest.raises(ValueError):
        Player("Alex", -100)


def test_player_rejects_invalid_chips_type():
    with pytest.raises(ValueError):
        Player("Alex", "1000")