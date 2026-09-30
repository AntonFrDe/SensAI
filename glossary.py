"""French poker glossary, loaded from data/poker_glossary.json (built by build_glossary.py, see data/SOURCE.md)."""
import json
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Entry:
    id: str
    term: str
    aliases: tuple[str, ...]
    definition: str | None  # None for a pure cross-reference such as "Ventrale – voir Gutshot"
    see: tuple[str, ...]    # entries to look at instead of / in addition to this one
    source: str             # "lexique" (the glossary) or "chat" (online chat abbreviations)


def normalize(text: str) -> str:
    """Lookup key: no accents, lower case, punctuation collapsed. "Dead man’s hand" -> "dead man s hand"."""
    plain = "".join(c for c in unicodedata.normalize("NFKD", text) if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", plain.casefold()).strip()


_raw = json.loads((Path(__file__).parent / "data" / "poker_glossary.json").read_text())["entries"]
ENTRIES: tuple[Entry, ...] = tuple(
    Entry(e["id"], e["term"], tuple(e["aliases"]), e["definition"], tuple(e["see"]), e["source"]) for e in _raw
)

_INDEX: dict[str, Entry] = {}
for _entry in ENTRIES:  # main terms first, so an alias can never shadow a real term
    _INDEX.setdefault(normalize(_entry.term), _entry)
for _entry in ENTRIES:
    for _alias in _entry.aliases:
        _INDEX.setdefault(normalize(_alias), _entry)


def lookup(term: str) -> Entry | None:
    """The entry for a term or alias, ignoring case, accents and punctuation."""
    return _INDEX.get(normalize(term))


def define(term: str) -> str | None:
    """Definition of a term, following "voir X" cross-references."""
    entry, visited = lookup(term), set()
    while entry and entry.definition is None and entry.id not in visited:
        visited.add(entry.id)
        entry = next(filter(None, map(lookup, entry.see)), None)
    return entry.definition if entry else None
