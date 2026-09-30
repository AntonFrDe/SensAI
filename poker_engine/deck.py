import random

from .card import Card, Suit


class Deck:
    RANKS = [
        "2", "3", "4", "5", "6", "7",
        "8", "9", "10", "J", "Q", "K", "A"
    ]

    SUITS = [
        Suit.CLUBS,
        Suit.DIAMONDS,
        Suit.HEARTS,
        Suit.SPADES
    ]

    def __init__(self):
        self.cards = []

        for suit in self.SUITS:
            for rank in self.RANKS:
                self.cards.append(Card(rank, suit))

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        if not self.cards:
            raise RuntimeError("Cannot draw from an empty deck")
    
        return self.cards.pop()

    def draw_many(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be greater than 0")

        if amount > self.remaining:
            raise RuntimeError("Not enough cards in the deck")
    
        cards = []

        for _ in range(amount):
            cards.append(self.draw())

        return cards

    @property
    def remaining(self):
        return len(self.cards)
