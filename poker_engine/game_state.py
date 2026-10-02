from enum import Enum

from .card import Card
from .deck import Deck
from .player import Player


class GamePhase(Enum):
    PRE_FLOP = "pre_flop"
    FLOP = "flop"
    TURN = "turn"
    RIVER = "river"
    SHOWDOWN = "showdown"


class GameState:
    def __init__(self, players):
        if not isinstance(players, list):
            raise TypeError("Players must be a list")

        if len(players) == 0:
            raise ValueError("At least one player is required")

        for player in players:
            if not isinstance(player, Player):
                raise TypeError("All players must be Player objects")

        self.players = players
        self.deck = Deck()

        self.community_cards = []
        self.pot = 0
        self.hand_history = []

        self.phase = GamePhase.PRE_FLOP

        self.current_player_index = 0
        self.dealer_index = 0

        self.current_bet = 0
        self.last_raise_size = 0

    @property
    def current_player(self):
        if not self.players:
            return None

        return self.players[self.current_player_index]

    @property
    def community_card_count(self):
        return len(self.community_cards)

    def next_player(self):
        if not self.players:
            return None

        self.current_player_index = (
            self.current_player_index + 1
        ) % len(self.players)

        return self.current_player

    def next_phase(self):
        if self.phase == GamePhase.PRE_FLOP:
            self.phase = GamePhase.FLOP

        elif self.phase == GamePhase.FLOP:
            self.phase = GamePhase.TURN

        elif self.phase == GamePhase.TURN:
            self.phase = GamePhase.RIVER

        elif self.phase == GamePhase.RIVER:
            self.phase = GamePhase.SHOWDOWN

        return self.phase

    def add_community_card(self, card):
        if not isinstance(card, Card):
            raise TypeError("Community card must be a Card")

        if self.community_card_count >= 5:
            raise RuntimeError(
                "There cannot be more than five community cards"
            )

        self.community_cards.append(card)

    def __str__(self):
        return (
            f"Phase: {self.phase.value} | "
            f"Pot: {self.pot} | "
            f"Players: {len(self.players)} | "
            f"Community cards: {self.community_card_count}"
        )
