from poker_engine.card import Card, Suit
from poker_engine.game import Game
from poker_engine.game_state import GamePhase
from poker_engine.hand_evaluator import HandEvaluator
from poker_engine.player import Player


def build_cards(*pairs):
    return [Card(rank, suit) for rank, suit in pairs]


def test_compare_hands_returns_correct_order():
    first_hand = build_cards(
        ("A", Suit.SPADES),
        ("A", Suit.HEARTS),
        ("K", Suit.CLUBS),
        ("Q", Suit.DIAMONDS),
        ("9", Suit.SPADES),
        ("4", Suit.HEARTS),
        ("2", Suit.CLUBS),
    )
    second_hand = build_cards(
        ("K", Suit.SPADES),
        ("K", Suit.HEARTS),
        ("Q", Suit.CLUBS),
        ("J", Suit.DIAMONDS),
        ("9", Suit.HEARTS),
        ("4", Suit.CLUBS),
        ("2", Suit.SPADES),
    )

    assert HandEvaluator.compare_hands(first_hand, second_hand) == 1
    assert HandEvaluator.compare_hands(second_hand, first_hand) == -1


def test_showdown_awards_entire_pot_to_best_hand():
    alice = Player("Alice", 0)
    bob = Player("Bob", 0)

    game = Game([alice, bob])
    game.state.phase = GamePhase.RIVER
    game.state.pot = 30
    game.state.community_cards = build_cards(
        ("2", Suit.CLUBS),
        ("5", Suit.CLUBS),
        ("9", Suit.CLUBS),
        ("J", Suit.DIAMONDS),
        ("Q", Suit.SPADES),
    )

    alice.hand = build_cards(
        ("A", Suit.CLUBS),
        ("K", Suit.CLUBS),
    )
    bob.hand = build_cards(
        ("A", Suit.DIAMONDS),
        ("A", Suit.SPADES),
    )

    game.end_hand()

    assert game.state.phase == GamePhase.SHOWDOWN
    assert game.state.pot == 0
    assert alice.chips == 30
    assert bob.chips == 0


def test_showdown_splits_pot_and_gives_odd_chip_to_player_closest_to_button():
    alice = Player("Alice", 0)
    bob = Player("Bob", 0)

    game = Game([alice, bob])
    game.dealer_index = 0
    game.state.dealer_index = 0
    game.state.phase = GamePhase.RIVER
    game.state.pot = 13
    game.state.community_cards = build_cards(
        ("10", Suit.SPADES),
        ("J", Suit.HEARTS),
        ("Q", Suit.CLUBS),
        ("K", Suit.DIAMONDS),
        ("A", Suit.SPADES),
    )

    alice.hand = build_cards(
        ("2", Suit.CLUBS),
        ("7", Suit.HEARTS),
    )
    bob.hand = build_cards(
        ("3", Suit.CLUBS),
        ("8", Suit.HEARTS),
    )

    game.end_hand()

    assert game.state.phase == GamePhase.SHOWDOWN
    assert game.state.pot == 0
    assert alice.chips == 6
    assert bob.chips == 7


def test_fold_win_awards_pot_to_remaining_player():
    alice = Player("Alice", 0)
    bob = Player("Bob", 0)
    charlie = Player("Charlie", 0)

    game = Game([alice, bob, charlie])
    game.state.phase = GamePhase.PRE_FLOP
    game.state.pot = 21
    alice.folded = True
    bob.folded = True
    charlie.folded = False

    game._advance_hand_if_round_complete()

    assert game.state.phase == GamePhase.SHOWDOWN
    assert game.state.pot == 0
    assert charlie.chips == 21
    assert alice.chips == 0
    assert bob.chips == 0