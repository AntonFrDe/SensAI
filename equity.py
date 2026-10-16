"""Équité d'une main de Texas Hold'em : chances de gagner selon le board et le nombre d'adversaires.

    python3 equity.py As Kh                           # avant le flop, 1 adversaire, avec la note
    python3 equity.py As Kh --board Ah 7c 2d -a 3     # au flop, contre 3 adversaires
    python3 equity.py --table                         # recalcule data/preflop_equity.json (~5 min)

Les adversaires ont des mains aléatoires : c'est la référence de comparaison. Le calcul contre les ranges
probables des adversaires (à venir) se branchera dans le tirage des mains adverses (`_random_deals`) et
s'affichera à côté de celui-ci, sans le remplacer.

Méthode :
- turn ou river en tête-à-tête : énumération exacte (au turn 1 035 × 44 = 45 540 issues, ~0,3 s) ;
- sinon : Monte Carlo, 10 000 tirages par défaut (~0,1 s, ±1 % au plus à 95 %, marge affichée) ;
- note avant le flop : lue dans data/preflop_equity.json, calculé une fois pour les 169 mains de départ.

Bibliothèque standard uniquement.
"""
import argparse
import json
import random
import sys
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path

Card = tuple[int, int]  # (valeur 2..14, couleur 0..3)

RANKS = "23456789TJQKA"
SUITS = "shdc"
SUIT_SYMBOLS = "♠♥♦♣"
DECK: list[Card] = [(rank, suit) for rank in range(2, 15) for suit in range(4)]
DATA = Path(__file__).parent / "data"
TABLE = DATA / "preflop_equity.json"
SAMPLES = 10_000
TABLE_SAMPLES = 20_000  # par main de départ et par nombre d'adversaires : ±0,7 % au plus à 95 %
MAX_TABLE_OPPONENTS = 5  # table 6-max, comme data/preflop_rfi.json
TABLE_SEED = 42  # tirages reproductibles : relancer --table redonne le même fichier

# Suites possibles en masque de bits (bit n = valeur n), de la plus haute à la roue A-2-3-4-5.
STRAIGHTS = [(0b11111 << (high - 4), high) for high in range(14, 5, -1)] + [((1 << 14) | 0b111100, 5)]


def parse_cards(text: str) -> list[Card]:
    """« As Kh », « AsKh », « A♠ K♥ », « 10d » → [(14, 0), (13, 1)]. Lève ValueError si illisible."""
    cleaned = "".join(text.split()).replace("️", "").replace("10", "T")
    if len(cleaned) % 2:
        raise ValueError(f"Cartes illisibles : {text!r} (exemples : As, Kh, 10d, Q♣)")
    cards = []
    for i in range(0, len(cleaned), 2):
        rank, suit = cleaned[i].upper(), cleaned[i + 1].lower()
        if rank not in RANKS or (suit not in SUITS and suit not in SUIT_SYMBOLS):
            raise ValueError(f"Carte inconnue : {cleaned[i:i + 2]!r} (exemples : As, Kh, 10d, Q♣)")
        cards.append((RANKS.index(rank) + 2, SUITS.index(suit) if suit in SUITS else SUIT_SYMBOLS.index(suit)))
    if len(set(cards)) != len(cards):
        raise ValueError(f"Carte en double : {text!r}")
    return cards


def show(cards: list[Card]) -> str:
    return " ".join(("10" if rank == 10 else RANKS[rank - 2]) + SUIT_SYMBOLS[suit] for rank, suit in cards)


def _straight_high(mask: int) -> int:
    return next((high for bits, high in STRAIGHTS if mask & bits == bits), 0)


def evaluate7(cards: list[Card]) -> tuple[int, ...]:
    """Force de la meilleure main de 5 parmi 5 à 7 cartes, en un seul passage.

    Renvoie un tuple comparable : (catégorie 1 = carte haute … 9 = quinte flush, départages…).
    Même convention que poker_engine/hand_evaluator.py, environ 50 fois plus rapide :
    il ne teste pas les 21 combinaisons de 5 cartes.
    """
    counts = [0] * 15
    suits = [0, 0, 0, 0]
    mask = 0
    for rank, suit in cards:
        counts[rank] += 1
        suits[suit] += 1
        mask |= 1 << rank
    flush = next((suit for suit in range(4) if suits[suit] >= 5), -1)
    if flush >= 0:
        flush_ranks = sorted((rank for rank, suit in cards if suit == flush), reverse=True)
        high = _straight_high(sum(1 << rank for rank in flush_ranks))
        if high:
            return (9, high)
    quads, trips, pairs, singles = [], [], [], []
    for rank in range(14, 1, -1):
        group = (None, singles, pairs, trips, quads)[counts[rank]]
        if group is not None:
            group.append(rank)
    if quads:
        return (8, quads[0], max(rank for rank in range(14, 1, -1) if counts[rank] and rank != quads[0]))
    if trips and (len(trips) > 1 or pairs):
        return (7, trips[0], max(trips[1] if len(trips) > 1 else 0, pairs[0] if pairs else 0))
    if flush >= 0:
        return (6, *flush_ranks[:5])
    high = _straight_high(mask)
    if high:
        return (5, high)
    if trips:
        return (4, trips[0], *singles[:2])
    if len(pairs) >= 2:
        return (3, pairs[0], pairs[1], max(singles + pairs[2:], default=0))
    if pairs:
        return (2, pairs[0], *singles[:3])
    return (1, *singles[:5])


def hand_name(cards: list[Card]) -> str:
    """Nom français de la combinaison, tiré de data/hand_rankings.json (ex. « Paire », « Full »)."""
    score = evaluate7(cards)
    rang = 1 if score == (9, 14) else 11 - score[0]
    rankings = json.loads((DATA / "hand_rankings.json").read_text(encoding="utf-8"))
    return next(entry["fr"] for entry in rankings if entry["rang"] == rang)


@dataclass(frozen=True)
class Equity:
    win: float  # seul gagnant
    tie: float  # gagnant à égalité, pot partagé
    lose: float
    equity: float  # part du pot gagnée en moyenne (égalités partagées)
    samples: int  # nombre d'issues calculées
    exact: bool

    @property
    def margin(self) -> float:
        """Marge à 95 % sur l'équité (0 si le calcul est exact)."""
        return 0.0 if self.exact else 1.96 * (self.equity * (1 - self.equity) / self.samples) ** 0.5


def _check(hero: list[Card], board: list[Card], opponents: int) -> None:
    if len(hero) != 2:
        raise ValueError("Il faut exactement 2 cartes en main.")
    if len(board) not in (0, 3, 4, 5):
        raise ValueError("Le board a 0, 3, 4 ou 5 cartes.")
    known = [*hero, *board]
    if any(card not in DECK for card in known) or len(set(known)) != len(known):
        raise ValueError("Carte invalide, ou présente à la fois en main et sur le board.")
    if not 1 <= opponents <= 9:
        raise ValueError("Il faut entre 1 et 9 adversaires.")


def _random_deals(deck: list[Card], missing: int, opponents: int, samples: int, rng: random.Random):
    """Tire le reste du board et les mains adverses, au hasard. Les ranges adverses remplaceront ce tirage."""
    for _ in range(samples):
        draw = rng.sample(deck, missing + 2 * opponents)
        yield draw[:missing], [draw[missing + 2 * i: missing + 2 * i + 2] for i in range(opponents)]


def _all_deals(deck: list[Card], missing: int):
    """Toutes les mains adverses et toutes les fins de board possibles (tête-à-tête)."""
    for opponent in combinations(deck, 2):
        rest = [card for card in deck if card not in opponent]
        for runout in combinations(rest, missing):
            yield list(runout), [list(opponent)]


def equity(
    hero: list[Card],
    board: list[Card] = (),
    opponents: int = 1,
    samples: int = SAMPLES,
    rng: random.Random | None = None,
    exact: bool | None = None,
) -> Equity:
    """Chances de `hero` contre `opponents` mains aléatoires, avec le board connu (0, 3, 4 ou 5 cartes).

    `exact=None` choisit seul : énumération exacte en tête-à-tête au turn et à la river, Monte Carlo sinon.
    """
    hero, board = list(hero), list(board)
    _check(hero, board, opponents)
    feasible = opponents == 1 and len(board) >= 4
    if exact and not feasible:
        raise ValueError("Calcul exact possible seulement en tête-à-tête, au turn ou à la river.")
    exact = feasible if exact is None else exact
    if not exact and samples < 1:
        raise ValueError("Il faut au moins 1 tirage.")
    deck = [card for card in DECK if card not in hero and card not in board]
    missing = 5 - len(board)
    deals = _all_deals(deck, missing) if exact else _random_deals(deck, missing, opponents, samples, rng or random.Random())
    wins = ties = total = 0
    share = 0.0
    for runout, hands in deals:
        full_board = board + runout
        best = evaluate7(hero + full_board)
        tied = 1
        for hand in hands:
            score = evaluate7(hand + full_board)
            if score > best:
                tied = 0
                break
            tied += score == best
        total += 1
        if tied:
            wins += tied == 1
            ties += tied > 1
            share += 1 / tied
    return Equity(wins / total, ties / total, (total - wins - ties) / total, share / total, total, exact)


def hand_class(hero: list[Card]) -> str:
    """Classe de main de départ : « AKs » (assortie), « AKo » (dépareillée), « QQ » (paire)."""
    (high, high_suit), (low, low_suit) = sorted(hero, reverse=True)
    name = RANKS[high - 2] + RANKS[low - 2]
    return name if high == low else name + ("s" if high_suit == low_suit else "o")


def class_combos(name: str) -> list[list[Card]]:
    """Les mains d'une classe de départ : « QQ » en a 6, « AKs » 4, « AKo » 12. Lève ValueError si illisible."""
    if len(name) not in (2, 3) or name[0] not in RANKS or name[1] not in RANKS:
        raise ValueError(f"Main de départ illisible : {name!r} (exemples : AKs, 72o, QQ)")
    high, low, kind = RANKS.index(name[0]) + 2, RANKS.index(name[1]) + 2, name[2:]
    if high < low or (high == low) != (kind == "") or kind not in ("", "s", "o"):
        raise ValueError(f"Main de départ illisible : {name!r} (exemples : AKs, 72o, QQ)")
    if high == low:
        return [[(high, a), (high, b)] for a, b in combinations(range(4), 2)]
    return [[(high, a), (low, b)] for a in range(4) for b in range(4) if (a == b) == (kind == "s")]


def versus(first: str, second: str, samples: int = SAMPLES, rng: random.Random | None = None) -> Equity:
    """Équité avant le flop d'une classe de départ contre une autre (« AKs » contre « 88 »).

    Les couleurs sont tirées au hasard parmi les combinaisons compatibles, puis le board : Monte Carlo.
    """
    deals = [(a, b) for a in class_combos(first) for b in class_combos(second) if not set(a) & set(b)]
    if not deals:
        raise ValueError(f"{first} et {second} ne peuvent pas être distribuées ensemble.")
    if samples < 1:
        raise ValueError("Il faut au moins 1 tirage.")
    rng = rng or random.Random()
    wins = ties = 0
    for _ in range(samples):
        hero, villain = rng.choice(deals)
        board = rng.sample([card for card in DECK if card not in hero and card not in villain], 5)
        mine, theirs = evaluate7(hero + board), evaluate7(villain + board)
        wins += mine > theirs
        ties += mine == theirs
    return Equity(wins / samples, ties / samples, (samples - wins - ties) / samples,
                  (wins + ties / 2) / samples, samples, False)


def build_table(samples: int = TABLE_SAMPLES) -> dict:
    """Équité et percentile des 169 mains de départ, pour 1 à MAX_TABLE_OPPONENTS adversaires."""
    classes: dict[str, tuple[list[Card], int]] = {}  # classe → (main représentative, nombre de combos)
    for hero in combinations(DECK, 2):
        name = hand_class(list(hero))
        representative, combos = classes.get(name, (list(hero), 0))
        classes[name] = (representative, combos + 1)
    table: dict = {"samples": samples, "seed": TABLE_SEED}
    for opponents in range(1, MAX_TABLE_OPPONENTS + 1):
        rng = random.Random(TABLE_SEED + opponents)
        equities = {name: equity(hand, opponents=opponents, samples=samples, rng=rng).equity for name, (hand, _) in classes.items()}
        above, rows = 0, {}
        for name in sorted(equities, key=equities.get, reverse=True):
            combos = classes[name][1]
            rows[name] = {"equity": round(equities[name], 4), "top": round((above + combos / 2) / 1326, 4)}
            above += combos
        table[str(opponents)] = rows
    return table


def preflop_rating(hero: list[Card], opponents: int = 1) -> dict:
    """Note avant le flop, lue dans data/preflop_equity.json.

    `top` : part des 1 326 mains de départ qui font mieux (0,03 = top 3 %).
    `note` : décile, de 10 (top 10 %) à 1 (les 10 % les plus faibles).
    """
    if not TABLE.exists():
        raise FileNotFoundError(f"{TABLE} absent : lance « python3 equity.py --table ».")
    table = json.loads(TABLE.read_text(encoding="utf-8"))
    if str(opponents) not in table:
        raise ValueError(f"La table couvre 1 à {MAX_TABLE_OPPONENTS} adversaires.")
    entry = table[str(opponents)][hand_class(hero)]
    return {**entry, "note": 10 - min(int(entry["top"] * 10), 9)}


def pct(value: float) -> str:
    return f"{value * 100:.1f} %".replace(".", ",")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Équité d'une main de Texas Hold'em contre des mains aléatoires.")
    parser.add_argument("main", nargs="*", help="tes 2 cartes, ex. As Kh")
    parser.add_argument("-b", "--board", nargs="*", default=[], help="0, 3, 4 ou 5 cartes, ex. Ah 7c 2d")
    parser.add_argument("-a", "--adversaires", type=int, default=1)
    parser.add_argument("-n", "--tirages", type=int, default=SAMPLES)
    parser.add_argument("--table", action="store_true", help=f"recalcule data/{TABLE.name}")
    args = parser.parse_args(argv)
    if args.table:
        TABLE.write_text(json.dumps(build_table(), indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"{TABLE} écrit.")
        return 0
    try:
        hero, board = parse_cards(" ".join(args.main)), parse_cards(" ".join(args.board))
        result = equity(hero, board, args.adversaires, args.tirages)
    except ValueError as error:
        print(f"Erreur : {error}", file=sys.stderr)
        return 2
    print(f"Main {show(hero)} | board {show(board) or '—'} | {args.adversaires} adversaire(s)")
    if board:
        print(f"Combinaison : {hand_name(hero + board)}")
    count = f"{result.samples:,}".replace(",", " ")
    method = f"exact, {count} issues" if result.exact else f"Monte Carlo, {count} tirages, ±{pct(result.margin)}"
    print(f"Contre des mains aléatoires ({method}) :")
    print(f"  gagne {pct(result.win)}   égalité {pct(result.tie)}   perd {pct(result.lose)}   équité {pct(result.equity)}")
    if not board:
        try:
            rating = preflop_rating(hero, args.adversaires)
            print(f"Note avant le flop : {rating['note']}/10 (top {pct(rating['top'])} des mains de départ)")
        except (FileNotFoundError, ValueError) as error:
            print(f"Note avant le flop indisponible : {error}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
