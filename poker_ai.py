"""The LLM's side of a game: the coach's advice for the human, and the AI opponent's decisions.

The situation is written in the notation `ai.situation_context` reads (« Ah Kh », « pot 130 », « payer 20 »),
so the web coach and the AI opponent get the same context as the CLI: hand rankings, glossary, equity, pot odds.
"""
import json

import ai
from poker_engine.game import Game

SUITS = {"clubs": "c", "diamonds": "d", "hearts": "h", "spades": "s"}
PHASES = {"pre_flop": "préflop", "flop": "flop", "turn": "turn", "river": "river", "showdown": "abattage"}
OPPONENT_SYSTEM = (
    "Tu es l'adversaire de l'utilisateur dans une partie de Texas Hold'em en tête-à-tête, et tu joues pour gagner. "
    "Décide ton action à partir de tes cartes et des calculs fournis. "
    'Réponds uniquement en JSON : {"action": "<une des actions possibles>", "amount": <montant total, '
    "seulement pour bet ou raise>}."
)


def notation(cards) -> str:
    return " ".join(card.rank + SUITS[card.suit.value] for card in cards)


def situation(game: Game, seat: int) -> str:
    """The hand seen from a seat: its own cards first, then the board, the pot and what it has to pay."""
    state = game.state
    player, opponent = state.players[seat], state.players[1 - seat]
    to_call = state.current_bet - player.current_bet
    return "\n".join([
        f"Texas Hold'em en tête-à-tête contre 1 adversaire, phase : {PHASES[state.phase.value]}.",
        f"Mes cartes : {notation(player.hand)}.",
        f"Board : {notation(state.community_cards) or 'aucune carte'}.",
        f"Pot {state.pot}, " + (f"je dois payer {to_call}." if to_call > 0 else "je peux checker."),
        f"Mon tapis : {player.chips}. Tapis adverse : {opponent.chips}.",
    ])


def coach_prompt(seen: str) -> str:
    return ai.build_prompt(f"{seen}\nQue dois-je faire ?")


def opponent_request(seen: str, controls: dict) -> tuple[str, str, dict]:
    """(system prompt, user prompt, JSON schema for Ollama's `format`) asking the AI for one legal action."""
    allowed = controls["allowedActions"]
    actions = ", ".join(
        f"{a} (montant total entre {controls['minAmount']} et {controls['maxAmount']})" if a in ("bet", "raise") else a
        for a in allowed
    )
    # The legal actions go after the prompt: « call » or « mise » in them would mislead situation_context.
    prompt = f"{ai.build_prompt(seen)}\n\nActions possibles : {actions}. Choisis-en une."
    schema = {
        "type": "object",
        "properties": {"action": {"type": "string", "enum": allowed}, "amount": {"type": "integer"}},
        "required": ["action"],
    }
    return OPPONENT_SYSTEM, prompt, schema


def parse_decision(reply: str | None, controls: dict) -> dict:
    """The model's action if it is legal, bet amounts clamped to the allowed range; otherwise the fallback rule."""
    try:
        choice = json.loads(reply)
        action = choice["action"]
    except (TypeError, ValueError, KeyError):
        return fallback(controls)
    if action not in controls["allowedActions"]:
        return fallback(controls)
    if action not in ("bet", "raise"):
        return {"action": action, "source": "llm"}
    amount = choice.get("amount")
    if type(amount) is not int:
        amount = controls["minAmount"]
    return {"action": action, "amount": min(max(amount, controls["minAmount"]), controls["maxAmount"]), "source": "llm"}


def fallback(controls: dict) -> dict:
    """Never folds for free, never bets: check when possible, otherwise call."""
    return {"action": "check" if "check" in controls["allowedActions"] else "call", "source": "fallback"}
