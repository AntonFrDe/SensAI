"""Public poker state consumed by the frontend; the human occupies seat zero."""
from poker_engine.game import Game


def _cards(cards):
    return [{"rank": card.rank, "suit": card.suit.value} for card in cards]


def player_controls(game: Game) -> dict:
    state = game.state
    player = state.players[0]
    if state.phase.value == "showdown" or state.current_player is not player or not player.can_act():
        return {"allowedActions": []}
    actions = ["fold"]
    actions.append("check" if player.current_bet == state.current_bet else "call")
    minimum = max(state.current_bet + state.last_raise_size, player.current_bet + 1) if state.current_bet else 1
    maximum = player.current_bet + player.chips
    if maximum >= minimum:
        actions.append("raise" if state.current_bet else "bet")
    return {"allowedActions": actions, "minAmount": minimum, "maxAmount": maximum}


def public_game_state(game: Game) -> dict:
    state = game.state
    player, opponent = state.players
    return {
        "playerCards": _cards(player.hand),
        "communityCards": _cards(state.community_cards),
        "pot": state.pot,
        "playerStack": player.chips,
        "opponentStack": opponent.chips,
        "currentPlayer": "player" if state.current_player is player else "opponent",
        "phase": state.phase.value,
        "currentBet": state.current_bet,
        "controls": player_controls(game),
        "history": [
            {key: value for key, value in event.items() if key in ("player", "action", "amount", "target_amount")}
            for event in state.hand_history if event["type"] == "action"
        ],
    }
