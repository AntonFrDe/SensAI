# Démo de la keynote : un seul fil, rejouable

Suit la trame de `docs/REFONTE.md` (annexe B). La graine fixe les situations : la démo se répète à l'identique
tant que `data/situations_generees.jsonl` et les règles de tirage ne changent pas. Vérifié le 2026-10-22 avec
`qwen3:4b-instruct-2507-q4_K_M` sur CPU : compter 15 à 40 s avant le premier mot de chaque réponse.

## Avant de monter sur scène

```
ollama serve                                   # dans un autre terminal
rm -f profiles/demo.json                       # repartir d'un profil vierge
python3 test_cli.py && python3 test_trainer.py # tout est vert
```

Lancer une fois la démo en entier la veille, et enregistrer l'écran : c'est le plan B si le modèle est trop lent.

## Le fil

```
python3 main.py --pseudo demo --seed 187
```

| Étape | On tape | On montre |
|---|---|---|
| 1. Niveau (X4) | `2` | Le niveau par un choix numéroté. Le dire avec ses mots marche aussi (T5, `{niveau, raison}`), mais un autre niveau donnerait d'autres situations : le montrer à l'étape 9 |
| 2. Situation | — | K♥ 8♠ au bouton, tout le monde s'est couché : texte écrit par un gabarit, aucun chiffre ne passe par le modèle |
| 3. Décision | `f` | 🟡 Acceptable : K8o est une main limite au bouton ; la référence vient de `preflop.py` |
| 4. Débrief (B1) | `Pourquoi c'est limite ?` | Réponse en streaming ; le coach cite la référence sans la recalculer |
| 5. « Et si… ? » (T1) | `Et si j'avais eu K9 assortis ?` | `[outil] preflop_open(...)` s'affiche : le chiffre vient de l'outil |
| 6. Question du coach (X4) | `Pose-moi une question pour vérifier` puis un numéro | Choix numérotés, la réponse revient au coach |
| 7. Fiche (T5) | `/fiche` | `À retenir` et `Thème à revoir`, vérifiés par schéma |
| 8. Situation suivante | `/exercice` puis `c` | Tirage couleur au flop (5♥ 6♣ sur J♣ 7♣ 3♣) : ✅ suivre, 12 outs, 25,5 % contre 25,0 % requis |
| 9. Le lendemain (M1, T5) | `/quit`, puis `python3 main.py --pseudo demo`, `/niveau` et `je compte mes outs à chaque main` | « Re-bonjour demo », niveau gardé, exercices comptés ; le niveau dit avec ses mots est classé ; `/reprendre` recharge le dernier débrief |

## Si quelque chose casse

- Le modèle met trop longtemps : Ctrl-C coupe la réponse sans quitter ; passer à l'étape suivante.
- Ollama ne répond plus : les étapes 2, 3 et 8 marchent sans modèle (le code tire et note) ; montrer
  l'enregistrement pour le reste.
- Le modèle n'appelle pas l'outil à l'étape 5 : le dire franchement, c'est une limite mesurée d'un modèle de 4
  milliards de paramètres, et le parcours n'en dépend pas.
