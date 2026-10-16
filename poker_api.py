"""Public poker state consumed by the frontend; the human occupies seat zero, the AI opponent seat one."""
import json
import random
from itertools import combinations
from pathlib import Path

import equity as eq
import odds
from poker_engine.card import RANK_VALUES
from poker_engine.game import Game
from poker_engine.game_state import GamePhase
from poker_engine.hand_evaluator import HandEvaluator
from poker_engine.player import Player

HUMAN, AI = 0, 1
BLIND_LEVELS = {"5/10": (5, 10), "10/20": (10, 20), "25/50": (25, 50)}
STACK_RANGE = (20, 500)
DEFAULT_OPTIONS = {"blinds": "10/20", "stackBigBlinds": 50}


def create_game(options: object = None) -> Game:
    if options is None:
        options = {}
    if not isinstance(options, dict):
        raise ValueError("Invalid game options.")
    level = options.get("blinds", DEFAULT_OPTIONS["blinds"])
    depth = options.get("stackBigBlinds", DEFAULT_OPTIONS["stackBigBlinds"])
    if level not in BLIND_LEVELS:
        raise ValueError("Unknown blind level.")
    if type(depth) is not int or not STACK_RANGE[0] <= depth <= STACK_RANGE[1]:
        raise ValueError(f"Starting stack must be between {STACK_RANGE[0]} and {STACK_RANGE[1]} big blinds.")
    small, big = BLIND_LEVELS[level]
    game = Game([Player("Vous", depth * big), Player("IA", depth * big)], small_blind=small, big_blind=big)
    game.start_hand()
    return game


def _cards(cards):
    return [{"rank": card.rank, "suit": card.suit.value} for card in cards]


def player_controls(game: Game, seat: int = HUMAN) -> dict:
    state = game.state
    player = state.players[seat]
    if state.phase is GamePhase.SHOWDOWN or state.current_player is not player or not player.can_act():
        return {"allowedActions": []}
    actions = ["fold"]
    actions.append("check" if player.current_bet == state.current_bet else "call")
    minimum = max(state.current_bet + state.last_raise_size, player.current_bet + 1) if state.current_bet else 1
    maximum = player.current_bet + player.chips
    if maximum >= minimum:
        actions.append("raise" if state.current_bet else "bet")
    to_call = min(state.current_bet - player.current_bet, player.chips)
    return {"allowedActions": actions, "minAmount": minimum, "maxAmount": maximum, "toCall": to_call}


def apply_action(game: Game, seat: int, action: object, amount: object = None) -> None:
    """Play a legal action for the seat, or raise ValueError before touching the game."""
    controls = player_controls(game, seat)
    if action not in controls["allowedActions"]:
        raise ValueError("Action unavailable on this turn.")
    method = getattr(game, "raise_bet" if action == "raise" else action)
    if action in ("bet", "raise"):
        if type(amount) is not int or not controls["minAmount"] <= amount <= controls["maxAmount"]:
            raise ValueError("Invalid bet amount.")
        method(amount)
    else:
        method()


def is_game_over(game: Game) -> bool:
    return game.state.phase is GamePhase.SHOWDOWN and any(p.chips == 0 for p in game.state.players)


def next_hand(game: Game) -> None:
    """Deal the next hand once the current one is over, swapping the dealer so the first speaker alternates."""
    if game.state.phase is not GamePhase.SHOWDOWN:
        raise ValueError("The current hand is not over.")
    if is_game_over(game):
        raise ValueError("Game over: a player has no chips left.")
    game.dealer_index = (game.dealer_index + 1) % len(game.state.players)
    game.start_hand()


def _public_history(events: list[dict]) -> list[dict]:
    street, entries = GamePhase.PRE_FLOP.value, []
    for event in events:
        if event["type"] == "street_dealt":
            street = event["street"]
        elif event["type"] == "action":
            entry = {"street": street, "player": event["player"], "action": event["action"]}
            amount = event.get("target_amount", event.get("amount"))
            if amount is not None:
                entry["amount"] = amount
            entries.append(entry)
    return entries


def best_hand(cards: list) -> dict | None:
    if len(cards) < 5:
        return None
    scored = ((HandEvaluator.evaluate(list(combo)), combo) for combo in combinations(cards, 5))
    result, five = max(scored, key=lambda pair: pair[0])
    return {"rank": result.rank.name.lower(), "cards": _cards(five)}


RANKINGS_FILE = Path(__file__).parent / "data" / "hand_rankings.json"
EXAMPLE_RANKS = {"As": "A", "Roi": "K", "Dame": "Q", "Valet": "J"}
EXAMPLE_SUITS = {"♠": "spades", "♥": "hearts", "♦": "diamonds", "♣": "clubs"}


def _example_card(text: str) -> dict:
    rank, suit = text[:-1], text[-1]
    if suit not in EXAMPLE_SUITS or EXAMPLE_RANKS.get(rank, rank) not in RANK_VALUES:
        raise ValueError(f"Unreadable example card: {text}")
    return {"rank": EXAMPLE_RANKS.get(rank, rank), "suit": EXAMPLE_SUITS[suit]}


def hand_rankings() -> list[dict]:
    rows = json.loads(RANKINGS_FILE.read_text(encoding="utf-8"))
    return [
        {"rank": row["rang"], "name": row["fr"], "description": row["description"],
         "cards": [_example_card(card) for card in row["exemple"].split()]}
        for row in sorted(rows, key=lambda row: row["rang"])
    ]


ODDS_SAMPLES = 3000
SUIT_INDEX = {"spades": 0, "hearts": 1, "diamonds": 2, "clubs": 3}


def _equity_cards(cards: list) -> list[eq.Card]:
    return [(RANK_VALUES[card.rank], SUIT_INDEX[card.suit.value]) for card in cards]


def odds_summary(game: Game, seat: int = HUMAN, rng: random.Random | None = None) -> dict:
    if not player_controls(game, seat)["allowedActions"]:
        raise ValueError("Odds are available on your turn.")
    state = game.state
    player = state.players[seat]
    hero, board = _equity_cards(player.hand), _equity_cards(state.community_cards)
    to_call = player_controls(game, seat)["toCall"]
    result = eq.equity(hero, board, samples=ODDS_SAMPLES, rng=rng or random.Random())
    summary = {
        "pot": state.pot,
        "toCall": to_call,
        "potOdds": odds.pot_odds(state.pot, to_call) if to_call > 0 else None,
        "equity": {"win": result.win, "tie": result.tie, "share": result.equity, "exact": result.exact},
        "outs": None,
    }
    if len(board) in (3, 4):
        groups = odds.outs(hero, board)
        count = sum(len(cards) for cards in groups.values())
        summary["outs"] = {
            "count": count,
            "byHand": {name: len(cards) for name, cards in groups.items()},
            "nextCard": odds.hit_chance(count, len(board))["prochaine carte"],
            "byRiver": odds.hit_chance(count, len(board)).get("d'ici la river"),
        }
    return summary


def _blind_roles(events: list[dict]) -> dict[str, str]:
    for event in events:
        if event["type"] == "blinds_posted":
            return {event["small_blind"]: "small", event["big_blind"]: "big"}
    return {}


def _seat(game: Game, seat: int, roles: dict[str, str]) -> dict:
    player = game.state.players[seat]
    return {
        "name": player.name,
        "stack": player.chips,
        "bet": player.current_bet,
        "folded": player.folded,
        "allIn": player.chips == 0 and not player.folded,
        "dealer": game.state.dealer_index == seat,
        "blind": roles.get(player.name),
    }


def public_game_state(game: Game) -> dict:
    state = game.state
    player, opponent = state.players
    revealed = state.phase is GamePhase.SHOWDOWN and not player.folded and not opponent.folded
    roles = _blind_roles(state.hand_history)
    return {
        "playerCards": _cards(player.hand),
        "opponentCards": _cards(opponent.hand) if revealed else [],
        "communityCards": _cards(state.community_cards),
        "pot": state.pot,
        "playerStack": player.chips,
        "opponentStack": opponent.chips,
        "currentPlayer": "player" if state.current_player is player else "opponent",
        "phase": state.phase.value,
        "currentBet": state.current_bet,
        "controls": player_controls(game),
        "awards": [
            {"amount": e["amount"], "winners": e["winners"], "reason": e["reason"]}
            for e in state.hand_history if e["type"] == "pot_awarded"
        ],
        "history": _public_history(state.hand_history),
        "hands": {
            "player": best_hand(player.hand + state.community_cards),
            "opponent": best_hand(opponent.hand + state.community_cards) if revealed else None,
        },
        "seats": {"player": _seat(game, HUMAN, roles), "opponent": _seat(game, AI, roles)},
        "blinds": {"small": game.small_blind, "big": game.big_blind},
        "gameOver": is_game_over(game),
    }
