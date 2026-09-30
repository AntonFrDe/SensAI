from .deck import Deck
from .game_state import GamePhase, GameState


class Game:
    def __init__(
        self,
        players,
        small_blind=10,
        big_blind=20,
    ):
        if not isinstance(players, list):
            raise TypeError("Players must be a list")

        if len(players) < 2:
            raise ValueError("At least two players are required")

        if small_blind <= 0:
            raise ValueError("Small blind must be positive")

        if big_blind <= small_blind:
            raise ValueError(
                "Big blind must be greater than small blind"
            )

        self.state = GameState(players)

        self.small_blind = small_blind
        self.big_blind = big_blind

        self.dealer_index = 0

    @property
    def current_player(self):
        return self.state.current_player

    @property
    def current_bet(self):
        return self.state.current_bet

    def start_hand(self):
        had_previous_hand = self.state.phase == GamePhase.SHOWDOWN

        for player in self.state.players:
            player.reset_hand()

        self.state.deck = Deck()
        self.state.deck.shuffle()

        self.state.community_cards.clear()

        # Nouvelle main = nouveau pot
        self.state.pot = 0

        self.state.phase = GamePhase.PRE_FLOP
        self.state.current_bet = 0
        self.state.last_raise_size = self.big_blind

        self.state.dealer_index = self.dealer_index

        self._deal_private_cards()
        self._post_blinds()
        self._set_pre_flop_first_player()

        if had_previous_hand:
            self.state.pot = 0

    def _deal_private_cards(self):
        for _ in range(2):
            for player in self.state.players:
                self._deal_private_card(player)

    def _deal_private_card(self, player):
        player.receive_card(
            self.state.deck.draw()
        )

    def _post_blinds(self):
        small_blind_index = (
            self.dealer_index + 1
        ) % len(self.state.players)

        big_blind_index = (
            self.dealer_index + 2
        ) % len(self.state.players)

        small_blind_player = self.state.players[
            small_blind_index
        ]

        big_blind_player = self.state.players[
            big_blind_index
        ]

        self._put_chips(
            small_blind_player,
            self.small_blind
        )

        self._put_chips(
            big_blind_player,
            self.big_blind
        )

        self.state.current_bet = (
            big_blind_player.current_bet
        )

    def _set_pre_flop_first_player(self):
        first_player = (
            self.dealer_index + 3
        ) % len(self.state.players)

        self.state.current_player_index = first_player

    def _burn_card(self):
        self.state.deck.draw()

    def _deal_community_card(self):
        card = self.state.deck.draw()
        self.state.add_community_card(card)

    def _put_chips(self, player, amount):
        committed = player.commit_chips(amount)
        self.state.pot += committed
        return committed

    def _normalize_current_bet(self, player):
        if player.chips + player.current_bet > player.initial_chips:
            player.current_bet = 0

    def _next_player(self):
        start_index = self.state.current_player_index

        while True:
            self.state.next_player()

            player = self.current_player

            if player.is_active():
                return

            if self.state.current_player_index == start_index:
                return

    def _require_current_player(self, player):
        if player != self.current_player:
            raise RuntimeError(
                "Only the current player can act"
            )

    def fold(self):
        player = self.current_player

        player.fold()

        self._next_player()

    def check(self):
        player = self.current_player

        if player.current_bet != self.state.current_bet:
            raise RuntimeError(
                "Cannot check while facing a bet"
            )

        self._next_player()

    def call(self):
        player = self.current_player

        self._normalize_current_bet(player)

        amount = (
            self.state.current_bet
            - player.current_bet
        )

        if amount <= 0:
            raise RuntimeError(
                "Nothing to call"
            )

        self._put_chips(player, amount)

        self._next_player()

    def bet(self, amount):
        player = self.current_player

        self._normalize_current_bet(player)

        if self.state.current_bet != 0:
            raise RuntimeError(
                "Cannot bet when there is already a bet"
            )

        if amount <= 0:
            raise ValueError(
                "Bet must be positive"
            )

        self._put_chips(player, amount)

        self.state.current_bet = player.current_bet
        self.state.last_raise_size = amount

        self._next_player()

    def raise_bet(self, target_amount):
        player = self.current_player

        self._normalize_current_bet(player)

        if self.state.current_bet == 0:
            raise RuntimeError(
                "Cannot raise without an existing bet"
            )

        minimum_raise = (
            self.state.current_bet
            + self.state.last_raise_size
        )

        if target_amount < minimum_raise:
            raise ValueError(
                f"Minimum raise is {minimum_raise}"
            )

        if target_amount <= player.current_bet:
            raise ValueError(
                "Raise must be greater than player's current bet"
            )

        amount_to_add = (
            target_amount
            - player.current_bet
        )

        if amount_to_add > player.chips:
            raise ValueError(
                "Player does not have enough chips"
            )

        self._put_chips(
            player,
            amount_to_add
        )

        self.state.last_raise_size = (
            target_amount
            - self.state.current_bet
        )

        self.state.current_bet = target_amount

        self._next_player()

    def all_in(self):
        player = self.current_player

        self._normalize_current_bet(player)

        if player.chips <= 0:
            raise RuntimeError(
                "Player is already all-in"
            )

        amount = player.chips

        previous_current_bet = self.state.current_bet

        self._put_chips(
            player,
            amount
        )

        if player.current_bet > previous_current_bet:
            self.state.last_raise_size = (
                player.current_bet
                - previous_current_bet
            )

            self.state.current_bet = (
                player.current_bet
            )

        self._next_player()

    def deal_flop(self):
        if self.state.phase != GamePhase.PRE_FLOP:
            raise RuntimeError(
                "Flop can only be dealt during pre-flop"
            )

        self._burn_card()

        for _ in range(3):
            self._deal_community_card()

        self.state.next_phase()

        self._prepare_post_flop_round()

    def deal_turn(self):
        if self.state.phase != GamePhase.FLOP:
            raise RuntimeError(
                "Turn can only be dealt after the flop"
            )

        self._burn_card()
        self._deal_community_card()

        self.state.next_phase()

        self._prepare_post_flop_round()

    def deal_river(self):
        if self.state.phase != GamePhase.TURN:
            raise RuntimeError(
                "River can only be dealt after the turn"
            )

        self._burn_card()
        self._deal_community_card()

        self.state.next_phase()

        self._prepare_post_flop_round()

    def _prepare_post_flop_round(self):
        self.state.current_bet = 0
        self.state.last_raise_size = self.big_blind

        for player in self.state.players:
            player.current_bet = 0

        first_player = (
            self.dealer_index + 1
        ) % len(self.state.players)

        self.state.current_player_index = (
            self._find_next_active_player(first_player)
        )

    def _find_next_active_player(self, start_index):
        index = start_index

        for _ in range(len(self.state.players)):
            player = self.state.players[index]

            if player.is_active():
                return index

            index = (
                index + 1
            ) % len(self.state.players)

        return start_index

    def end_hand(self):
        if self.state.phase != GamePhase.RIVER:
            raise RuntimeError(
                "A hand can only end after the river"
            )

        self.state.next_phase()
