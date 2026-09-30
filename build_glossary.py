"""Build data/poker_glossary.json from data/poker_glossary_source.txt.

Source format: one entry per line, "Term – definition", paragraphs joined by " ¶ ".
Run: python3 build_glossary.py
"""
import json
import re
import unicodedata
from pathlib import Path

DATA = Path(__file__).parent / "data"

# "ou hijack", "en français : rivière", "abréviation : pp"... -> the bare alias
ALIAS_PREFIX = re.compile(r"^(?:ou|en français|abb?réviation|parfois abrégé|orthographe exacte)\s*:?\s+", re.I)
# a definition that starts with "voir X" / "(voir X)" / "Voir aussi X." is a cross-reference
CROSS_REF = re.compile(r"^\(?[Vv]oir(?: aussi)?\s+([^.()]+?)\)?(?:\.\s*|$)(.*)$", re.S)

# Chat abbreviations from the same page that have no glossary entry of their own.
CHAT = [
    ("gla", [], "Good luck all : bonne chance à tous."),
    ("wd", [], "Well done : bravo."),
    ("gh", [], "Good hand : bonne main."),
    ("n1", [], "Nice one : joli."),
    ("np", [], "No problem : pas de problème. Peut aussi vouloir dire « nice play » (joli coup)."),
    ("nb", [], "Nice bet : jolie mise."),
    ("lol", ["rofl", "lmao"], "Laugh out loud / rolling on the floor / laughing my ass off : indique le rire, parfois gras, à des degrés divers."),
    ("omg", [], "Oh my God : oh mon Dieu."),
    ("wtf", [], "What the fuck : se traduit poliment par « c’est quoi cette blague ? »."),
    ("ffs", [], "For fuck sake : se traduit par « mais c’est pas possible ! »."),
    ("tx", ["tyvm"], "Thank you / thank you very much : merci, merci beaucoup."),
    ("uw", [], "You welcome : de rien (variante de yw)."),
    ("zzzzz", [], "Onomatopée signifiant que le joueur s’ennuie, souvent quand un autre joueur prend trop de temps pour jouer."),
    ("brb", [], "Be right back : je reviens."),
]


def slug(text: str) -> str:
    ascii_text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", ascii_text.lower()).strip("-")


def clean_alias(text: str) -> str | None:
    text = ALIAS_PREFIX.sub("", text.strip())
    return None if not text or "littéralement" in text else text


def parse_term(raw: str) -> tuple[str, list[str]]:
    """"Out(s)" -> ("Out", ["Outs"]); "BB (Big blind)" -> ("BB", ["Big blind"]); "ITM, In The Money" -> ("ITM", ["In The Money"])."""
    aliases: list[str] = []
    attached = re.search(r"\S\((\w+)\)", raw)  # optional ending glued to a word: Out(s), Top pair(e)
    if attached:
        aliases.append(raw.replace("(", "").replace(")", ""))
        raw = raw.replace(attached.group(0), attached.group(0)[0])
    for gloss in re.findall(r"\s\(([^)]*)\)", raw):  # spaced parentheses: a synonym, translation or abbreviation
        aliases.append(gloss)
    raw = re.sub(r"\s\([^)]*\)", "", raw)
    main, *others = [p.strip() for p in re.split(r",| / ", raw)]
    return main, [a for a in map(clean_alias, aliases + others) if a]


def parse_definition(text: str) -> tuple[str | None, tuple[str, ...]]:
    paragraphs = [p.strip() for p in text.split(" ¶ ")]
    see: tuple[str, ...] = ()
    if match := CROSS_REF.match(paragraphs[0]):
        see = (match.group(1).strip(),)
        paragraphs[0] = match.group(2).strip()
    body = "\n".join(p for p in paragraphs if p)
    return (body or None), see


def build() -> dict:
    entries, used = [], set()

    def add(term: str, aliases: list[str], definition: str | None, see: tuple[str, ...], source: str) -> None:
        base = slug(term) or "entry"
        entry_id, n = base, 2
        while entry_id in used:
            entry_id, n = f"{base}-{n}", n + 1
        used.add(entry_id)
        entries.append({"id": entry_id, "term": term, "aliases": aliases, "definition": definition,
                        "see": list(see), "source": source})

    for number, line in enumerate((DATA / "poker_glossary_source.txt").read_text().splitlines(), 1):
        if not line.strip():
            continue
        raw_term, sep, raw_definition = line.partition(" – ")
        if not sep:
            raise ValueError(f'line {number}: expected "Term – definition": {line[:60]!r}')
        term, aliases = parse_term(raw_term)
        definition, see = parse_definition(raw_definition)
        add(term, aliases, definition, see, "lexique")
    for term, aliases, definition in CHAT:
        add(term, aliases, definition, (), "chat")
    return {
        "meta": {
            "language": "fr",
            "source": "French poker glossary (lexique du poker), pasted by the user; see data/SOURCE.md",
            "note": "definition is null for pure cross-references; `see` lists the entries to follow",
        },
        "entries": entries,
    }


if __name__ == "__main__":
    out = build()
    (DATA / "poker_glossary.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n")
    refs = sum(1 for e in out["entries"] if e["see"])
    print(f"{len(out['entries'])} entries ({refs} with cross-references) -> data/poker_glossary.json")
