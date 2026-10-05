from .deck import Deck
from .game_state import GamePhase, GameState
from .hand_evaluator import HandEvaluator

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

    @property
    def history(self):
        return self.state.hand_history

    def start_hand(self):
        had_previous_hand = self.state.phase == GamePhase.SHOWDOWN

        for player in self.state.players:
            player.reset_hand()

        self.state.deck = Deck()
        self.state.deck.shuffle()

        self.state.community_cards.clear()
        self.state.hand_history.clear()

        # Nouvelle main = nouveau pot
        self.state.pot = 0

        self.state.phase = GamePhase.PRE_FLOP
        self.state.current_bet = 0
        self.state.last_raise_size = self.big_blind

        self.state.dealer_index = self.dealer_index

        self._record_history(
            "hand_started",
            dealer=self._player_name(self.state.players[self.dealer_index]),
            phase=self.state.phase.value,
        )

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

    def _player_name(self, player):
        return player.name

    def _player_names(self, players):
        return [player.name for player in players]

    def _record_history(self, event_type, **payload):
        self.state.hand_history.append(
            {
                "type": event_type,
                **payload,
            }
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

        self._record_history(
            "blinds_posted",
            small_blind=self._player_name(small_blind_player),
            small_blind_amount=self.small_blind,
            big_blind=self._player_name(big_blind_player),
            big_blind_amount=self.big_blind,
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

            if player.can_act():
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

        player.acted_this_round = True
        player.fold()

        self._record_history(
            "action",
            action="fold",
            player=self._player_name(player),
        )

        self._next_player()
        self._advance_hand_if_round_complete()

    def check(self):
        player = self.current_player

        if player.current_bet != self.state.current_bet:
            raise RuntimeError(
                "Cannot check while facing a bet"
            )

        player.acted_this_round = True

        self._record_history(
            "action",
            action="check",
            player=self._player_name(player),
        )

        self._next_player()
        self._advance_hand_if_round_complete()

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

        player.acted_this_round = True

        self._record_history(
            "action",
            action="call",
            player=self._player_name(player),
            amount=amount,
        )

        self._next_player()
        self._advance_hand_if_round_complete()

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

        player.acted_this_round = True

        self._record_history(
            "action",
            action="bet",
            player=self._player_name(player),
            amount=amount,
        )

        self._next_player()
        self._advance_hand_if_round_complete()

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

        player.acted_this_round = True

        self._record_history(
            "action",
            action="raise",
            player=self._player_name(player),
            amount=amount_to_add,
            target_amount=target_amount,
        )

        self._next_player()
        self._advance_hand_if_round_complete()

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

        player.acted_this_round = True

        if player.current_bet > previous_current_bet:
            self.state.last_raise_size = (
                player.current_bet
                - previous_current_bet
            )

            self.state.current_bet = (
                player.current_bet
            )

        self._record_history(
            "action",
            action="all_in",
            player=self._player_name(player),
            amount=amount,
        )

        self._next_player()
        self._advance_hand_if_round_complete()

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
        self._record_history(
            "street_dealt",
            street="flop",
            community_cards=self.state.community_card_count,
        )
        self._advance_hand_if_round_complete()

    def deal_turn(self):
        if self.state.phase != GamePhase.FLOP:
            raise RuntimeError(
                "Turn can only be dealt after the flop"
            )

        self._burn_card()
        self._deal_community_card()

        self.state.next_phase()

        self._prepare_post_flop_round()
        self._record_history(
            "street_dealt",
            street="turn",
            community_cards=self.state.community_card_count,
        )
        self._advance_hand_if_round_complete()

    def deal_river(self):
        if self.state.phase != GamePhase.TURN:
            raise RuntimeError(
                "River can only be dealt after the turn"
            )

        self._burn_card()
        self._deal_community_card()

        self.state.next_phase()

        self._prepare_post_flop_round()
        self._record_history(
            "street_dealt",
            street="river",
            community_cards=self.state.community_card_count,
        )
        self._advance_hand_if_round_complete()

    def _prepare_post_flop_round(self):
        self.state.current_bet = 0
        self.state.last_raise_size = self.big_blind

        for player in self.state.players:
            player.current_bet = 0
            player.acted_this_round = False

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
        self._resolve_showdown()

    def _showdown_contenders(self):
        return [
            player
            for player in self.state.players
            if not player.folded
        ]

    def _player_hand_result(self, player):
        return HandEvaluator.evaluate(
            player.hand + self.state.community_cards
        )

    def _best_showdown_players(self):
        contenders = self._showdown_contenders()

        if len(contenders) <= 1:
            return contenders

        best_result = None
        best_players = []

        for player in contenders:
            result = self._player_hand_result(player)

            if best_result is None or result > best_result:
                best_result = result
                best_players = [player]

            elif result == best_result:
                best_players.append(player)

        return best_players

    def _best_players_among(self, players):
        if not players:
            return []

        best_result = None
        best_players = []

        for player in players:
            result = self._player_hand_result(player)

            if best_result is None or result > best_result:
                best_result = result
                best_players = [player]

            elif result == best_result:
                best_players.append(player)

        return best_players

    def _ordered_players_from_button(self, players):
        if not players:
            return []

        ordered_players = []
        target_players = set(players)
        index = (self.dealer_index + 1) % len(self.state.players)

        for _ in range(len(self.state.players)):
            player = self.state.players[index]

            if player in target_players:
                ordered_players.append(player)

            index = (index + 1) % len(self.state.players)

        return ordered_players

    def _award_amount(self, amount, winners):
        if amount <= 0 or not winners:
            return

        share, remainder = divmod(amount, len(winners))

        for index, player in enumerate(
            self._ordered_players_from_button(winners)
        ):
            player.chips += share

            if index < remainder:
                player.chips += 1

    def _record_pot_award(self, amount, winners, eligible_players, reason):
        self._record_history(
            "pot_awarded",
            reason=reason,
            amount=amount,
            winners=self._player_names(winners),
            eligible_players=self._player_names(eligible_players),
        )

    def _build_side_pots(self):
        contributions = [
            player.contributed_this_hand
            for player in self.state.players
            if player.contributed_this_hand > 0
        ]

        if not contributions:
            return []

        levels = sorted(set(contributions))
        pots = []
        previous_level = 0
        dead_money = 0

        for level in levels:
            players_at_level = [
                player
                for player in self.state.players
                if player.contributed_this_hand >= level
            ]

            amount = (level - previous_level) * len(players_at_level)
            eligible_players = [
                player
                for player in players_at_level
                if not player.folded
            ]

            previous_level = level

            if not eligible_players:
                dead_money += amount
                continue

            pots.append((amount, eligible_players))

        if pots:
            amount, eligible_players = pots[-1]
            pots[-1] = (amount + dead_money, eligible_players)

        return pots

    def _resolve_showdown(self):
        contenders = self._showdown_contenders()

        if len(contenders) <= 1:
            self._award_amount(self.state.pot, contenders)
            self._record_pot_award(
                self.state.pot,
                contenders,
                contenders,
                "fold",
            )
            self.state.pot = 0
            return

        if not any(
            player.contributed_this_hand > 0
            for player in self.state.players
        ):
            winners = self._best_players_among(contenders)
            self._award_amount(self.state.pot, winners)
            self._record_pot_award(
                self.state.pot,
                winners,
                contenders,
                "showdown",
            )
            self.state.pot = 0
            return

        for amount, eligible_players in self._build_side_pots():
            winners = self._best_players_among(eligible_players)
            self._award_amount(amount, winners)
            self._record_pot_award(
                amount,
                winners,
                eligible_players,
                "showdown",
            )

        self.state.pot = 0

    def _advance_hand_if_round_complete(self):
        if not self.is_betting_round_complete():
            return False

        contenders = [
            player
            for player in self.state.players
            if not player.folded
        ]

        if len(contenders) <= 1:
            self.state.phase = GamePhase.SHOWDOWN
            self._resolve_showdown()
            return True

        if self.state.phase == GamePhase.PRE_FLOP:
            self.deal_flop()

        elif self.state.phase == GamePhase.FLOP:
            self.deal_turn()

        elif self.state.phase == GamePhase.TURN:
            self.deal_river()

        elif self.state.phase == GamePhase.RIVER:
            self.end_hand()

        return True

    def is_betting_round_complete(self):
        active_players = [
            player
            for player in self.state.players
            if not player.folded
        ]

        players_who_can_act = [
            player
            for player in active_players
            if player.chips > 0
        ]

        if len(active_players) <= 1:
            return True

        for player in players_who_can_act:
            if player.current_bet != self.state.current_bet:
                return False

        for player in players_who_can_act:
            if not player.acted_this_round:
                return False

        return True
