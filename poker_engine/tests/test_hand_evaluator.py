from poker_engine.card import Card, Suit
from poker_engine.hand_evaluator import HandEvaluator, HandRank


def test_pair_of_aces():
    cards = [
        Card("A", Suit.SPADES),
        Card("A", Suit.HEARTS),
        Card("K", Suit.CLUBS),
        Card("7", Suit.DIAMONDS),
        Card("2", Suit.SPADES),
    ]

    result = HandEvaluator.evaluate(cards)

    assert result.rank == HandRank.ONE_PAIR
    assert result.tiebreaker == (14, 13, 7, 2)

def test_straight():
    cards = [
        Card("10", Suit.SPADES),
        Card("J", Suit.HEARTS),
        Card("Q", Suit.CLUBS),
        Card("K", Suit.DIAMONDS),
        Card("A", Suit.SPADES),
    ]

    result = HandEvaluator.evaluate(cards)

    assert result.rank == HandRank.STRAIGHT
    assert result.tiebreaker == (14,)

def test_wheel_straight():
    cards = [
        Card("A", Suit.SPADES),
        Card("2", Suit.HEARTS),
        Card("3", Suit.CLUBS),
        Card("4", Suit.DIAMONDS),
        Card("5", Suit.SPADES),
    ]

    result = HandEvaluator.evaluate(cards)

    assert result.rank == HandRank.STRAIGHT
    assert result.tiebreaker == (5,)

def test_full_house():
    cards = [
        Card("A", Suit.SPADES),
        Card("A", Suit.HEARTS),
        Card("A", Suit.CLUBS),
        Card("K", Suit.DIAMONDS),
        Card("K", Suit.SPADES),
    ]

    result = HandEvaluator.evaluate(cards)

    assert result.rank == HandRank.FULL_HOUSE
    assert result.tiebreaker == (14, 13)

def test_four_of_a_kind():
    cards = [
        Card("A", Suit.SPADES),
        Card("A", Suit.HEARTS),
        Card("A", Suit.CLUBS),
        Card("A", Suit.DIAMONDS),
        Card("K", Suit.SPADES),
    ]

    result = HandEvaluator.evaluate(cards)

    assert result.rank == HandRank.FOUR_OF_A_KIND
    assert result.tiebreaker == (14, 13)

def test_straight_flush():
    cards = [
        Card("10", Suit.SPADES),
        Card("J", Suit.SPADES),
        Card("Q", Suit.SPADES),
        Card("K", Suit.SPADES),
        Card("A", Suit.SPADES),
    ]

    result = HandEvaluator.evaluate(cards)

    assert result.rank == HandRank.STRAIGHT_FLUSH
    assert result.tiebreaker == (14,)

def test_best_five_cards_from_seven():
    cards = [
        Card("A", Suit.SPADES),
        Card("K", Suit.SPADES),
        Card("Q", Suit.SPADES),
        Card("J", Suit.SPADES),
        Card("10", Suit.SPADES),
        Card("3", Suit.DIAMONDS),
        Card("2", Suit.CLUBS),
    ]

    result = HandEvaluator.evaluate(cards)

    assert result.rank == HandRank.STRAIGHT_FLUSH
    assert result.tiebreaker == (14,)

assert (
    HandEvaluator.evaluate([
        Card("A", Suit.SPADES),
        Card("A", Suit.HEARTS),
        Card("K", Suit.CLUBS),
        Card("7", Suit.DIAMONDS),
        Card("2", Suit.SPADES),
    ])
    >
    HandEvaluator.evaluate([
        Card("K", Suit.SPADES),
        Card("K", Suit.HEARTS),
        Card("Q", Suit.CLUBS),
        Card("7", Suit.DIAMONDS),
        Card("2", Suit.SPADES),
    ])
)
