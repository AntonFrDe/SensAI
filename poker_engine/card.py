from dataclasses import dataclass
from enum import Enum


class Suit(Enum):
    CLUBS = "clubs"
    DIAMONDS = "diamonds"
    HEARTS = "hearts"
    SPADES = "spades"


RANK_VALUES = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14,
}


@dataclass(frozen=True)
class Card:
    rank: str
    suit: Suit

    def __post_init__(self):
        if self.rank not in RANK_VALUES:
            raise ValueError(f"Invalid rank: {self.rank}")

        if not isinstance(self.suit, Suit):
            raise ValueError(f"Invalid suit: {self.suit}")

    @property
    def value(self):
        return RANK_VALUES[self.rank]

    def __str__(self):
        return f"{self.rank} of {self.suit.value}"
