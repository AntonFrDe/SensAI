"""Preflop open-raise (RFI) ranges, 6-max 100bb. Data provenance: data/SOURCE.md."""
import json
from pathlib import Path

RANKS = "AKQJT98765432"
SUITS = "shdc"

_raw = json.loads((Path(__file__).parent / "data" / "preflop_rfi.json").read_text())
# mixed cells are read-only tuples so callers cannot corrupt the shared data
_RANGES = {
    pos: {h: tuple(a) if isinstance(a, list) else a for h, a in chart.items()}
    for pos, chart in _raw.items()
}


def _bad(hand: str) -> ValueError:
    return ValueError(f"invalid hand {hand!r}: expected 'AKs', 'AKo', '77' or exact cards like 'AsKd'")


def normalize_hand(hand: str) -> str:
    """'AKs' | 'kao' | '77' | 'AsKd' -> canonical 13x13 cell name: 'AKs', 'AKo', '77'."""
    h = hand.strip()
    if len(h) == 4:  # exact cards: "AsKd"
        (r1, s1), (r2, s2) = (h[0].upper(), h[1].lower()), (h[2].upper(), h[3].lower())
        if (r1, s1) == (r2, s2) or s1 not in SUITS or s2 not in SUITS:
            raise _bad(hand)
        kind = "" if r1 == r2 else "s" if s1 == s2 else "o"
    elif len(h) in (2, 3):  # cell name: pair has no suffix, other hands need s/o
        r1, r2, kind = h[0].upper(), h[1].upper(), h[2:].lower()
        if kind not in ("", "s", "o") or (r1 == r2) != (kind == ""):
            raise _bad(hand)
    else:
        raise _bad(hand)
    if r1 not in RANKS or r2 not in RANKS:
        raise _bad(hand)
    hi, lo = sorted((r1, r2), key=RANKS.index)
    return hi + lo + kind


def hand_range(hand: str) -> dict[str, str | tuple[str, str]]:
    """Action of the hand's cell for each opening position, e.g. {'UTG': 'raise', 'BTN': ('raise', 'fold'), ...}.

    'raise' = open, ('raise', 'fold') = mixed/marginal, 'fold' = not in range.
    MP is the hijack; the big blind never opens, so it has no entry.
    """
    cell = normalize_hand(hand)
    return {pos: chart.get(cell, "fold") for pos, chart in _RANGES.items()}


if __name__ == "__main__":
    import sys

    print(hand_range(sys.argv[1] if len(sys.argv) > 1 else "AKs"))
