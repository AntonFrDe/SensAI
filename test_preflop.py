from preflop import hand_range, normalize_hand


def raises(hand, position):
    return "raise" in hand_range(hand)[position]


def test_normalize():
    assert normalize_hand("AKs") == "AKs"
    assert normalize_hand("kas") == "AKs"      # rank order and case
    assert normalize_hand("AsKs") == "AKs"     # exact cards, suited
    assert normalize_hand("KdAs") == "AKo"     # exact cards, offsuit
    assert normalize_hand("7h7c") == "77"      # exact cards, pair
    assert normalize_hand(" tt ") == "TT"


def test_normalize_rejects_bad_input():
    for bad in ["", "AK", "AAs", "AKx", "1Ks", "AsAs", "AxKd", "AKsx"]:
        try:
            normalize_hand(bad)
        except ValueError:
            continue
        raise AssertionError(f"{bad!r} should be rejected")


def test_all_positions_returned():
    assert list(hand_range("AA")) == ["UTG", "MP", "CO", "BTN", "SB"]


def test_premium_and_trash():
    assert all(raises("AA", p) for p in hand_range("AA"))
    assert not any(raises("72o", p) for p in hand_range("72o"))


def test_ranges_widen_toward_the_button():
    def width(p):
        return sum(raises(h, p) for h in ("22", "A9o", "K9s", "T9s", "65s", "Q9o", "54s", "J8s"))
    assert width("UTG") < width("CO") < width("BTN")


def test_mixed_cell_and_input_forms_agree():
    assert hand_range("22")["UTG"] == ("raise", "fold")   # marginal open
    assert hand_range("AsKd") == hand_range("AKo") == hand_range("KAo")


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
