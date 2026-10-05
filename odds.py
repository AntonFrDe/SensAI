"""Outs, cote du pot et analyse complète d'une situation, à partir de equity.py.

    python3 odds.py Ah Kh --board Qh 7h 2c --pot 100 --payer 50

Les calculs sont faits ici, pas par le modèle : un LLM de 4 milliards de paramètres calcule mal.
`analyse()` renvoie un texte prêt à être injecté dans le prompt (voir ai.py).
"""
import argparse
import sys
from math import comb

import equity as eq


def outs(hero: list[eq.Card], board: list[eq.Card]) -> dict[str, list[eq.Card]]:
    """Cartes qui améliorent la combinaison au prochain tirage, groupées par combinaison obtenue.

    Une carte compte si elle fait monter la catégorie de la main (paire → deux paires, tirage → couleur…)
    et si cette catégorie vient de nos cartes : une carte qui ne fait que pairer le board ne compte pas.
    ponytail: ignore les outs « sales » (couleur qui donne aussi une couleur plus haute à l'adversaire) ;
    à affiner avec les ranges adverses.
    """
    if len(board) not in (3, 4):
        raise ValueError("Les outs se comptent au flop (3 cartes) ou au turn (4 cartes).")
    eq._check(hero, board, 1)  # même validation des cartes que equity()
    current = eq.evaluate7(hero + board)[0]
    groups: dict[str, list[eq.Card]] = {}
    for card in eq.DECK:
        if card in hero or card in board:
            continue
        improved = eq.evaluate7(hero + board + [card])[0]
        if improved > current and improved > eq.evaluate7(board + [card])[0]:
            groups.setdefault(eq.hand_name(hero + board + [card]), []).append(card)
    return groups


def hit_chance(n_outs: int, board_size: int) -> dict[str, float]:
    """Probabilité exacte de toucher un out : à la prochaine carte, et d'ici la river si on est au flop."""
    unseen = 52 - 2 - board_size
    chances = {"prochaine carte": n_outs / unseen}
    if board_size == 3:
        chances["d'ici la river"] = 1 - comb(unseen - n_outs, 2) / comb(unseen, 2)
    return chances


def pot_odds(pot: float, to_call: float) -> float:
    """Équité minimale pour que suivre soit rentable : à payer / (pot + à payer).

    `pot` = ce qu'il y a au milieu au moment de décider, mise adverse comprise.
    """
    if pot < 0 or to_call <= 0:
        raise ValueError("Le pot doit être positif et la somme à payer strictement positive.")
    return to_call / (pot + to_call)


def analyse(
    hero: list[eq.Card],
    board: list[eq.Card] = (),
    opponents: int = 1,
    pot: float | None = None,
    to_call: float | None = None,
) -> str:
    """Résumé chiffré de la situation, en français, pour le joueur ou pour le modèle."""
    hero, board = list(hero), list(board)
    result = eq.equity(hero, board, opponents)
    lines = [f"Main : {eq.show(hero)} | board : {eq.show(board) or 'aucun (avant le flop)'} | {opponents} adversaire(s)"]
    if board:
        lines.append(f"Combinaison actuelle : {eq.hand_name(hero + board)}")
    elif opponents <= eq.MAX_TABLE_OPPONENTS:
        rating = eq.preflop_rating(hero, opponents)
        lines.append(f"Note avant le flop : {rating['note']}/10 (top {eq.pct(rating['top'])} des mains de départ)")
    margin = "exact" if result.exact else f"±{eq.pct(result.margin)}"
    lines.append(
        f"Équité contre des mains aléatoires : {eq.pct(result.equity)} ({margin}) "
        f"— gagne {eq.pct(result.win)}, égalité {eq.pct(result.tie)}, perd {eq.pct(result.lose)}"
    )
    if len(board) in (3, 4):
        groups = outs(hero, board)
        total = sum(map(len, groups.values()))
        detail = ", ".join(f"{len(cards)} pour {name.lower()} ({eq.show(cards)})" for name, cards in groups.items())
        lines.append(f"Outs : {total}" + (f" — {detail}" if detail else ""))
        if total:
            chances = ", ".join(f"{when} {eq.pct(p)}" for when, p in hit_chance(total, len(board)).items())
            lines.append(f"Chance de toucher un out : {chances}")
    if pot is not None and to_call is not None:
        needed = pot_odds(pot, to_call)
        verdict = "rentable" if result.equity >= needed else "pas rentable"
        lines.append(
            f"Cote du pot : payer {to_call:g} pour un pot de {pot:g} → il faut au moins {eq.pct(needed)} d'équité. "
            f"Avec {eq.pct(result.equity)}, suivre est {verdict} à long terme (sans compter les mises futures)."
        )
    lines.append(
        "Attention : l'équité est calculée contre des mains au hasard ; face à une mise, l'adversaire a en "
        "général une main plus forte que le hasard, donc l'équité réelle est plus basse."
    )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Outs, cote du pot et équité d'une main de Texas Hold'em.")
    parser.add_argument("main", nargs="+", help="tes 2 cartes, ex. Ah Kh")
    parser.add_argument("-b", "--board", nargs="*", default=[], help="0, 3, 4 ou 5 cartes")
    parser.add_argument("-a", "--adversaires", type=int, default=1)
    parser.add_argument("--pot", type=float, help="pot au moment de décider, mise adverse comprise")
    parser.add_argument("--payer", type=float, help="somme à payer pour suivre")
    args = parser.parse_args(argv)
    try:
        hero, board = eq.parse_cards(" ".join(args.main)), eq.parse_cards(" ".join(args.board))
        print(analyse(hero, board, args.adversaires, args.pot, args.payer))
    except ValueError as error:
        print(f"Erreur : {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
