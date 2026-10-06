"""SensAI's poker tools as an MCP server (stdio, JSON-RPC 2.0), standard library only.

    python3 mcp_server.py          # speaks MCP on stdin/stdout; any MCP client can use it

Tools: hand_odds (equity, outs, pot odds), define_term (glossary), preflop_open (opening ranges),
hand_rankings (the 10 poker hands). Nothing but protocol messages may be written to stdout.
"""
import json
import sys

import ai
import equity
import glossary
import odds
import preflop

PROTOCOL_VERSIONS = ("2025-06-18", "2025-03-26", "2024-11-05")  # newest first
ACTIONS = {"raise": "ouvrir (relancer)", "fold": "se coucher"}


def hand_odds(args: dict) -> str:
    pot, to_call = args.get("pot"), args.get("to_call")
    return odds.analyse(
        equity.parse_cards(args["hand"]),
        equity.parse_cards(args.get("board", "")),
        int(args.get("opponents", 1)),
        float(pot) if pot is not None and to_call is not None else None,
        float(to_call) if pot is not None and to_call is not None else None,
    )


def define_term(args: dict) -> str:
    entry = glossary.lookup(args["term"])
    definition = glossary.define(args["term"])
    if definition is None:
        return f"« {args['term']} » n'est pas dans le glossaire."
    return f"{entry.term} : {definition}"


def preflop_open(args: dict) -> str:
    cell = preflop.normalize_hand(args["hand"])
    lines = [
        f"- {position} : " + (ACTIONS[action] if isinstance(action, str) else "mixte (relancer ou se coucher)")
        for position, action in preflop.hand_range(cell).items()
    ]
    return f"Ouverture de {cell} en 6-max 100bb, si personne n'a encore relancé :\n" + "\n".join(lines)


CARDS = (
    "Cartes en notation courte : valeur puis couleur, ex. « As Kh ». Valeurs : 2-9, T ou 10, J (valet), Q (dame), "
    "K (roi), A (as). Couleurs : h (cœur), d (carreau), c (trèfle), s (pique). Ex. « dame de cœur » = Qh."
)
TOOLS = {
    "hand_odds": (
        "Calcule l'équité d'une main de Texas Hold'em contre des mains aléatoires, ses outs et, si pot et "
        "to_call sont donnés, si suivre est rentable (cote du pot). " + CARDS,
        {
            "type": "object",
            "properties": {
                "hand": {"type": "string", "description": "Les 2 cartes du joueur, ex. « Ah Kh »."},
                "board": {"type": "string", "description": "0, 3, 4 ou 5 cartes communes, ex. « Qh 7h 2c »."},
                "opponents": {"type": "integer", "minimum": 1, "maximum": 9, "description": "Nombre d'adversaires."},
                "pot": {"type": "number", "description": "Jetons au milieu, mise adverse comprise."},
                "to_call": {"type": "number", "description": "Somme à payer pour suivre."},
            },
            "required": ["hand"],
        },
        hand_odds,
    ),
    "define_term": (
        "Donne la définition d'un terme de poker (glossaire français : UTG, check-raise, river, nuts...).",
        {"type": "object", "properties": {"term": {"type": "string"}}, "required": ["term"]},
        define_term,
    ),
    "preflop_open": (
        "Dit, pour chaque position (UTG, MP, CO, BTN, SB), s'il faut ouvrir une main de départ quand personne "
        "n'a encore relancé (table 6-max, 100 big blinds).",
        {
            "type": "object",
            "properties": {"hand": {"type": "string", "description": "« AKs » (assorties), « AKo », « 77 » ou « AsKd »."}},
            "required": ["hand"],
        },
        preflop_open,
    ),
    "hand_rankings": (
        "Classement officiel des 10 combinaisons du poker, de la plus forte à la plus faible.",
        {"type": "object", "properties": {}},
        lambda args: ai.hand_rankings_context(),
    ),
}


def handle(message: dict) -> dict | None:
    """The response to one JSON-RPC message, or None for a notification."""
    method, params, msg_id = message.get("method"), message.get("params") or {}, message.get("id")
    if msg_id is None:
        return None  # notifications (notifications/initialized...) need no answer
    if method == "initialize":
        asked = params.get("protocolVersion")
        result = {
            "protocolVersion": asked if asked in PROTOCOL_VERSIONS else PROTOCOL_VERSIONS[0],
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "sensai-poker", "version": "1.0.0"},
        }
    elif method == "ping":
        result = {}
    elif method == "tools/list":
        result = {"tools": [
            {"name": name, "description": description, "inputSchema": schema}
            for name, (description, schema, _) in TOOLS.items()
        ]}
    elif method == "tools/call":
        tool = TOOLS.get(params.get("name"))
        if tool is None:
            return _error(msg_id, -32602, f"Unknown tool: {params.get('name')}")
        try:
            text, is_error = tool[2](params.get("arguments") or {}), False
        except (KeyError, TypeError, ValueError) as e:  # bad arguments: the model can read this and retry
            text, is_error = f"Arguments invalides : {e}", True
        result = {"content": [{"type": "text", "text": text}], "isError": is_error}
    else:
        return _error(msg_id, -32601, f"Method not found: {method}")
    return {"jsonrpc": "2.0", "id": msg_id, "result": result}


def _error(msg_id, code: int, message: str) -> dict:
    return {"jsonrpc": "2.0", "id": msg_id, "error": {"code": code, "message": message}}


def main() -> None:
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            message = json.loads(line)
            response = handle(message) if isinstance(message, dict) else _error(None, -32600, "Invalid request")
        except ValueError:
            response = _error(None, -32700, "Parse error")
        if response is not None:
            print(json.dumps(response, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
