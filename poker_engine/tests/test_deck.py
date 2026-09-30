from poker_engine.card import Card, Suit
from poker_engine.deck import Deck
import pytest


def test_deck_has_52_cards():
    deck = Deck()

    assert deck.remaining == 52


def test_deck_has_unique_cards():
    deck = Deck()

    assert len(set(deck.cards)) == 52


def test_card_value():
    assert Card("2", Suit.CLUBS).value == 2
    assert Card("10", Suit.CLUBS).value == 10
    assert Card("J", Suit.CLUBS).value == 11
    assert Card("Q", Suit.CLUBS).value == 12
    assert Card("K", Suit.CLUBS).value == 13
    assert Card("A", Suit.CLUBS).value == 14


def test_card_string():
    card = Card("A", Suit.SPADES)

    assert str(card) == "A of spades"


def test_draw_removes_one_card():
    deck = Deck()

    card = deck.draw()

    assert deck.remaining == 51
    assert isinstance(card, Card)


def test_draw_many():
    deck = Deck()

    cards = deck.draw_many(5)

    assert len(cards) == 5
    assert deck.remaining == 47


def test_draw_many_too_many_cards():
    deck = Deck()

    with pytest.raises(RuntimeError):
        deck.draw_many(53)


def test_draw_many_invalid_amount():
    deck = Deck()

    with pytest.raises(ValueError):
        deck.draw_many(0)


def test_draw_many_negative_amount():
    deck = Deck()

    with pytest.raises(ValueError):
        deck.draw_many(-1)

def test_invalid_rank():
    with pytest.raises(ValueError):
        Card("X", Suit.SPADES)


def test_invalid_suit():
    with pytest.raises(ValueError):
        Card("A", "spades")
