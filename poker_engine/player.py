from .card import Card


class Player:
    def __init__(self, name, chips):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Player name cannot be empty")

        if not isinstance(chips, (int, float)):
            raise ValueError("Chips must be a number")

        if chips < 0:
            raise ValueError("Chips cannot be negative")

        self.name = name
        self.chips = chips
        self.initial_chips = chips
        self.hand = []
        self.folded = False
        self.current_bet = 0

    @property
    def stack(self):
        return self.chips

    @property
    def hand_size(self):
        return len(self.hand)

    def receive_card(self, card):
        if not isinstance(card, Card):
            raise TypeError("Player can only receive a Card")

        if self.hand_size >= 2:
            raise RuntimeError("Player already has two cards")

        self.hand.append(card)

    def fold(self):
        self.folded = True

    def reset_hand(self):
        self.hand.clear()
        self.folded = False
        self.current_bet = 0

    def commit_chips(self, amount):
        if not isinstance(amount, (int, float)):
            raise ValueError("Amount must be a number")

        if amount < 0:
            raise ValueError("Amount cannot be negative")

        if amount > self.chips:
            amount = self.chips

        self.chips -= amount
        self.current_bet += amount

        return amount

    def is_active(self):
        return not self.folded and self.chips > 0

    def __str__(self):
        return f"{self.name} ({self.chips} chips)"
