"""Public poker state consumed by the frontend; the human occupies seat zero, the AI opponent seat one."""
from poker_engine.game import Game
from poker_engine.game_state import GamePhase

HUMAN, AI = 0, 1


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


def public_game_state(game: Game) -> dict:
    state = game.state
    player, opponent = state.players
    revealed = state.phase is GamePhase.SHOWDOWN and not player.folded and not opponent.folded
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
        "gameOver": is_game_over(game),
    }
