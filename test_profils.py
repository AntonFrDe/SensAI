"""Tests de profils.py : pseudo, lecture, écriture et résultats par thème.

    python3 test_profils.py
"""
import tempfile
from pathlib import Path

import profils


def raises(fn, *args):
    try:
        fn(*args)
    except ValueError:
        return True
    return False


def test_valider_pseudo_keeps_safe_file_names():
    assert profils.valider_pseudo(" Amine_42 ") == "amine_42"
    assert raises(profils.valider_pseudo, "../etc") and raises(profils.valider_pseudo, "")
    assert raises(profils.valider_pseudo, "élodie") and raises(profils.valider_pseudo, "a" * 33)


def test_a_missing_profile_is_new():
    with tempfile.TemporaryDirectory() as tmp:
        assert profils.charger("amine", {"profiles_dir": tmp}) == profils.nouveau("amine")


def test_enregistrer_then_charger_gives_the_profile_back():
    with tempfile.TemporaryDirectory() as tmp:
        cfg = {"profiles_dir": tmp}
        profil = {**profils.nouveau("amine"), "niveau": "intermediaire"}
        profils.enregistrer(profil, cfg)
        relu = profils.charger("Amine", cfg)
        assert relu["niveau"] == "intermediaire" and "mis_a_jour" in relu
        assert (Path(tmp) / "amine.json").exists()


def test_an_unreadable_profile_is_replaced_by_a_new_one():
    with tempfile.TemporaryDirectory() as tmp:
        (Path(tmp) / "amine.json").write_text("{pas du json")
        assert profils.charger("amine", {"profiles_dir": tmp}) == profils.nouveau("amine")


def test_noter_counts_the_verdicts_by_theme_without_editing_the_profile():
    profil = profils.nouveau("amine")
    apres = profils.noter(profils.noter(profil, "tirage", "erreur"), "tirage", "bon")
    assert apres["resultats"] == {"tirage": {"bon": 1, "acceptable": 0, "erreur": 1}}
    assert profil["resultats"] == {}


def test_themes_faibles_puts_the_most_missed_first():
    profil = {**profils.nouveau("amine"), "resultats": {
        "ouverture": {"bon": 3, "acceptable": 0, "erreur": 1},
        "tirage": {"bon": 1, "acceptable": 0, "erreur": 1},
        "parfait": {"bon": 2, "acceptable": 1, "erreur": 0},
    }}
    assert profils.themes_faibles(profil) == ["tirage", "ouverture"]


def test_resume_is_one_line_per_theme():
    assert profils.resume(profils.nouveau("amine")) == "aucun exercice encore"
    profil = profils.noter(profils.noter(profils.nouveau("amine"), "tirage", "erreur"), "tirage", "erreur")
    assert profils.resume(profil) == "tirage : 0 bon, 0 acceptable, 2 erreurs"


def test_ajouter_fiche_keeps_only_the_latest():
    profil = profils.nouveau("amine")
    for n in range(profils.MAX_FICHES + 5):
        profil = profils.ajouter_fiche(profil, {"a_retenir": str(n)})
    assert len(profil["fiches"]) == profils.MAX_FICHES and profil["fiches"][-1]["a_retenir"] == "24"


if __name__ == "__main__":
    for name, test in list(globals().items()):
        if name.startswith("test_"):
            test()
            print("ok", name)
