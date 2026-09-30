from dataclasses import dataclass
from enum import IntEnum
from itertools import combinations

from .card import Card


class HandRank(IntEnum):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    STRAIGHT_FLUSH = 9


@dataclass(frozen=True)
class HandResult:
    rank: HandRank
    tiebreaker: tuple[int, ...]

    def __lt__(self, other):
        if self.rank != other.rank:
            return self.rank < other.rank

        return self.tiebreaker < other.tiebreaker


class HandEvaluator:

    @staticmethod
    def _rank_counts(cards):
        counts = {}

        for card in cards:
            counts[card.value] = counts.get(card.value, 0) + 1

        return counts

    @staticmethod
    def _straight_high_card(ranks):
        unique_ranks = sorted(set(ranks), reverse=True)

        if 14 in unique_ranks:
            unique_ranks.append(1)

        for i in range(len(unique_ranks) - 4):
            window = unique_ranks[i:i + 5]

            if window[0] - window[4] == 4:
                return window[0]

        return None

    @staticmethod
    def _evaluate_five(cards):
        ranks = sorted(
            (card.value for card in cards),
            reverse=True
        )

        counts = HandEvaluator._rank_counts(cards)

        is_flush = len({card.suit for card in cards}) == 1

        straight_high = HandEvaluator._straight_high_card(ranks)

        # Straight Flush
        if is_flush and straight_high is not None:
            return HandResult(
                HandRank.STRAIGHT_FLUSH,
                (straight_high,)
            )

        # Four of a Kind
        four = sorted(
            (
                rank
                for rank, count in counts.items()
                if count == 4
            ),
            reverse=True
        )

        if four:
            four_rank = four[0]

            kicker = max(
                rank
                for rank in ranks
                if rank != four_rank
            )

            return HandResult(
                HandRank.FOUR_OF_A_KIND,
                (four_rank, kicker)
            )

        # Full House
        trips = sorted(
            (
                rank
                for rank, count in counts.items()
                if count >= 3
            ),
            reverse=True
        )

        pairs = sorted(
            (
                rank
                for rank, count in counts.items()
                if count >= 2
            ),
            reverse=True
        )

        if trips:
            trip_rank = trips[0]

            remaining_pairs = [
                rank
                for rank in pairs
                if rank != trip_rank
            ]

            if remaining_pairs:
                pair_rank = remaining_pairs[0]

                return HandResult(
                    HandRank.FULL_HOUSE,
                    (trip_rank, pair_rank)
                )

        # Flush
        if is_flush:
            return HandResult(
                HandRank.FLUSH,
                tuple(ranks)
            )

        # Straight
        if straight_high is not None:
            return HandResult(
                HandRank.STRAIGHT,
                (straight_high,)
            )

        # Three of a Kind
        if trips:
            trip_rank = trips[0]

            kickers = sorted(
                (
                    rank
                    for rank in ranks
                    if rank != trip_rank
                ),
                reverse=True
            )

            return HandResult(
                HandRank.THREE_OF_A_KIND,
                (trip_rank, *kickers)
            )

        # Two Pair / One Pair
        pair_ranks = sorted(
            (
                rank
                for rank, count in counts.items()
                if count >= 2
            ),
            reverse=True
        )

        if len(pair_ranks) >= 2:
            high_pair = pair_ranks[0]
            low_pair = pair_ranks[1]

            kicker = max(
                rank
                for rank in ranks
                if rank != high_pair
                and rank != low_pair
            )

            return HandResult(
                HandRank.TWO_PAIR,
                (high_pair, low_pair, kicker)
            )

        if len(pair_ranks) == 1:
            pair_rank = pair_ranks[0]

            kickers = sorted(
                (
                    rank
                    for rank in ranks
                    if rank != pair_rank
                ),
                reverse=True
            )

            return HandResult(
                HandRank.ONE_PAIR,
                (pair_rank, *kickers)
            )

        # High Card
        return HandResult(
            HandRank.HIGH_CARD,
            tuple(ranks)
        )

    @classmethod
    def evaluate(cls, cards):
        if len(cards) < 5:
            raise ValueError(
                "At least 5 cards are required to evaluate a hand"
            )

        if len(cards) > 7:
            raise ValueError(
                "A Texas Hold'em hand cannot contain more than 7 cards"
            )

        results = [
            cls._evaluate_five(combo)
            for combo in combinations(cards, 5)
        ]

        return max(results)
