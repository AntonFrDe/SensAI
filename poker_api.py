"""Public poker state consumed by the frontend; the human occupies seat zero."""
from poker_engine.game import Game


def _cards(cards):
    return [{"rank": card.rank, "suit": card.suit.value} for card in cards]


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
    }
