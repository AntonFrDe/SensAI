from pathlib import Path

from glossary import ENTRIES, define, lookup

SOURCE = Path(__file__).parent / "data" / "poker_glossary_source.txt"


def test_every_source_line_became_an_entry_with_a_unique_id():
    lines = [line for line in SOURCE.read_text().splitlines() if line.strip()]
    assert len(ENTRIES) >= len(lines)  # the chat abbreviations come on top
    assert len({e.id for e in ENTRIES}) == len(ENTRIES)


def test_lookup_ignores_case_accents_and_punctuation():
    assert lookup("BIG SLICK").term == "Big slick"
    assert lookup("decaver").term == "Décaver"
    assert lookup("dead man's hand").term == "Dead man’s hand"
    assert lookup("all in").term == "All-in"
    assert lookup("nothing here") is None


def test_aliases_are_indexed():
    assert lookup("hijack").term == "Hi-jack"
    assert lookup("tanking").term == "Tanker"
    assert lookup("outs").term == "Out"              # "Out(s)"
    assert lookup("top paire").term == "Top pair"    # "Top pair(e)"
    assert lookup("la roue").term == "Bicycle"       # French gloss in parentheses
    assert lookup("in the money").term == "ITM"      # "ITM, In The Money"


def test_aliases_carry_no_leftover_prefix():
    assert lookup("pp").term == "Pocket pair"       # source: "Pocket pair (abbréviation : pp)"
    assert lookup("reg").term == "Regular"          # source: "Regular (parfois abrégé : reg)"
    assert not [(e.term, a) for e in ENTRIES for a in e.aliases if ":" in a or a != a.strip()]


def test_terms_the_models_got_wrong():
    assert define("Quads").startswith("Carré")
    assert define("Straight").startswith("Quinte")
    assert define("Set").startswith("Brelan")
    assert "Full House" in define("Main pleine")
    assert "full house" in define("Boat")


def test_cross_references_are_followed():
    assert lookup("UTG").definition is None and lookup("UTG").see == ("Under The Gun",)
    assert define("UTG") == define("Under The Gun") and define("UTG")
    assert define("Décaver") == define("Déstacker")
    assert define("Blank").startswith("Carte sans")   # "Voir aussi Brique." then its own definition
    assert define("Boîte").startswith("L’une des")
    assert define("nothing here") is None


def test_references_point_to_existing_entries():
    dangling = {ref for e in ENTRIES for ref in e.see if lookup(ref) is None}
    assert dangling == {"Grosse Blinde"}   # the source itself has no entry under that spelling (BB says "Grosse Blind")


def test_website_noise_is_gone():
    noise = ("Visiter le site", "GambleAware", "T&C", "Unibet", "PMU Poker", "bonus de bienvenue")
    assert not [e.term for e in ENTRIES if any(n in (e.definition or "") for n in noise)]


def test_chat_abbreviations_are_tagged():
    assert lookup("wtf").source == "chat" and lookup("tyvm").source == "chat"
    assert lookup("gg").source == "lexique"


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
