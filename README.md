# SensAI

Assistant IA local, tournant sur Ollama. Projet Epitech Tech3. Piste actuelle : un coach de poker (Texas Hold'em).

## Installation

1. Installer [Ollama](https://ollama.com), puis récupérer le modèle par défaut :
   `ollama pull qwen3:4b-instruct-2507-q4_K_M`
2. Python 3.10 ou plus :
   `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`

## Interface web

```
python3 server.py            # puis http://localhost:8000
python3 server.py --model llama3.2:3b --port 8080
```

Réglages dans `config.json` : modèle, URL d'Ollama, taille du contexte, fichier du prompt système
(`prompts/system.txt`) et `max_parallel_models`.

Le bouton **Comparer** envoie la même question à plusieurs modèles installés. Un sémaphore n'en laisse tourner
qu'`max_parallel_models` à la fois (1 par défaut) ; les autres attendent, et chaque modèle est déchargé de la
RAM dès qu'il a répondu. Sans authentification : ne pas utiliser `--host 0.0.0.0` sur un réseau non sûr.

## Question en ligne de commande

```
python3 ai.py "Quelle est la meilleure main au poker ?"
```

`ai.py` injecte le classement des combinaisons (`data/hand_rankings.json`) avant chaque question, et les
entrées du glossaire dont le terme apparaît dans la question (le glossaire entier, ~15 000 tokens, dépassait le
contexte d'Ollama). Sans lui,
`qwen3:4b-instruct` répondait « As, Roi, Dame, Roi, 10 » 5 fois sur 5 ; avec, « quinte flush royale » 5 fois
sur 5. Chaque combinaison est donnée avec une force de 10 à 1 plutôt qu'un rang de 1 à 10 : avec des rangs,
le modèle lit « 5 > 4 » et conclut qu'une couleur bat un full.

## Chances de gagner d'une main

```
python3 equity.py As Kh                          # avant le flop, 1 adversaire, avec la note
python3 equity.py As Kh --board Ah 7c 2d -a 3    # au flop, contre 3 adversaires
python3 equity.py --table                        # recalcule data/preflop_equity.json (~7 min)
```

`equity.py` donne gagne, égalité, perd et équité (part du pot gagnée en moyenne) contre des mains adverses
aléatoires, avec le board connu (0, 3, 4 ou 5 cartes). C'est la référence de comparaison ; le calcul contre
les ranges probables des adversaires viendra à côté.

| Situation | Méthode | Temps | Précision |
|---|---|---|---|
| Turn ou river, 1 adversaire | Énumération de toutes les issues | ~0,3 s | exacte |
| Autres cas | Monte Carlo, 10 000 tirages | 0,1 à 0,3 s | ±1 % au plus, à 95 % (affichée à chaque calcul) |
| Note avant le flop | Lecture de `data/preflop_equity.json` | instantané | calculée une fois, 20 000 tirages par main |

La note va de 10 (top 10 % des 1 326 mains de départ) à 1, pour 1 à 5 adversaires. L'évaluateur de mains
lit les 7 cartes en un seul passage : mêmes résultats que `poker_engine/hand_evaluator.py` (vérifié par un
test), environ 50 fois plus vite.

## Outs et cote du pot

```
python3 odds.py Ah Kh --board Qh 7h 2c --pot 100 --payer 50
```

`odds.py` ajoute à l'équité les **outs** (cartes qui améliorent la combinaison grâce à nos cartes, groupées par
combinaison ; une carte qui ne fait que pairer le board ne compte pas), la chance exacte d'en toucher un, et la
**cote du pot** : équité minimale = à payer / (pot + à payer), où le pot inclut la mise adverse.

`ai.py` s'en sert : si la question contient au moins 2 cartes (`Ah`, `10d`, `Q♣`), les 2 premières sont la main,
les suivantes le board ; « pot 100 », « payer 50 » (ou « mise », « suivre ») et « 3 adversaires » sont lus aussi.
Les calculs sont injectés avant la question et le modèle doit les citer, pas les refaire :

```
python3 ai.py "J'ai Ah Kh, flop Qh 7h 2c, pot de 100, je dois payer 50. Je suis ?"
```

## Jeu d'évaluation

```
python3 evaluate.py                          # les 33 questions, modèle par défaut
python3 evaluate.py --modele llama3.2:3b     # comparer un autre modèle
python3 evaluate.py --questions q01 q28      # quelques questions seulement
python3 evaluate.py --temperature 0.7        # comparer avec le réglage par défaut d'Ollama
```

`evaluation/questions.jsonl` contient 33 questions de poker (combinaisons, règles, vocabulaire, ranges préflop,
équité, outs, cote du pot) avec une réponse de référence vérifiée (`equity.py`, `odds.py`, `preflop.py`).
Pour chacune, le modèle local répond comme dans `ai.py`, puis reçoit la référence et sa propre réponse : il
découpe la référence en faits et dit pour chacun s'il est présent, absent ou contredit, en JSON (sortie contrainte
par `format`). Le script compte la question réussie si tous les faits sont présents : jugée « en bloc », la
réponse était refusée par le petit modèle dès qu'elle contenait du texte en plus. Le script remplit
`evaluation/resultats.md` : une ligne par question, case cochée ☑ si réussie, différences relevées, puis le
détail des réponses ; `evaluation/resultats.json` garde tout. Seul le modèle local (Ollama) est appelé.

Les réponses sont générées à température 0 (`TEMPERATURE` dans `ai.py`) : mêmes réponses à chaque lancement,
donc deux scores sont comparables. Cela ne rend pas les réponses plus justes : testé, une réponse fausse faute de
contexte reste fausse à 0. La température utilisée est notée dans `resultats.md`.

Le correcteur est le même petit modèle : relire les verdicts, il peut être indulgent.

## Tests

```
python3 test_web.py && python3 test_preflop.py && python3 test_glossary.py && python3 test_ai.py && python3 test_equity.py && python3 test_odds.py && python3 test_evaluate.py
python3 -m pytest poker_engine/tests       # moteur de poker
```

## Contenu

| Fichier | Rôle |
|---|---|
| `poker_engine/` | Moteur de poker : cartes, paquet, joueurs, partie, actions, évaluation des mains |
| `llm.py` | Client Ollama (HTTP, streaming) |
| `ai.py` | Question en ligne de commande, avec le classement des combinaisons injecté |
| `equity.py` | Chances de gagner d'une main selon le board, note avant le flop |
| `evaluate.py`, `evaluation/` | Jeu d'évaluation : questions de référence, résultats remplis par le script |
| `odds.py` | Outs, cote du pot et analyse complète d'une situation, injectée par `ai.py` |
| `server.py`, `web/index.html` | Interface web et comparaison de modèles |
| `preflop.py` | `hand_range("AKs")` : action d'ouverture par position |
| `glossary.py` | `define("UTG")` : glossaire du poker en français |
| `build_glossary.py` | Régénère `data/poker_glossary.json` depuis la source |
| `config.json`, `prompts/system.txt` | Réglages de l'interface web et prompt système |
| `data/` | Données du poker, voir « Données » ci-dessous |
| `docs/` | Sujet, bootstrap et catalogue de features |

## Données

| Fichier | Contenu | Source et droits |
|---|---|---|
| `data/hand_rankings.json` | Les 10 combinaisons, `{rang, fr, en, description, exemple}`, rang 1 = la plus forte | Règles standard, écrit à la main le 2026-09-30 |
| `data/preflop_equity.json` | Équité et percentile des 169 mains de départ, contre 1 à 5 adversaires | Calculé par `equity.py --table` (Monte Carlo, graine fixe : relancer redonne le même fichier). Vérifié : AA 85,1 %, AKs 67,0 %, 72o 34,5 % en tête-à-tête |
| `data/preflop_rfi.json` | Ranges d'ouverture (RFI) 6-max 100bb, par position (UTG, MP, CO, BTN, SB). Main absente = fold | [AHTOOOXA/poker-charts](https://github.com/AHTOOOXA/poker-charts), `src/data/ranges/pekarstas.ts`, récupéré le 2026-09-21. Code sous MIT, mais les ranges viennent de sites tiers : droits incertains |
| `data/poker_glossary_source.txt`, `data/poker_glossary.json` | Glossaire français : 313 entrées du lexique et 14 abréviations de chat, construit par `build_glossary.py` | Texte copié depuis un site affilié (il cite PokerListings). Droits inconnus |

Le dépôt est privé : ces données tierces conviennent pour un projet d'école, mais **ne doivent pas être publiées**.
Le glossaire a été nettoyé à la main (publicités et index retirés, paragraphes joints par ` ¶ `), coquilles de la
source comprises.
