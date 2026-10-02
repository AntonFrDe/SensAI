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

`ai.py` injecte le classement des combinaisons (`data/hand_rankings.json`) avant chaque question. Sans lui,
`qwen3:4b-instruct` répondait « As, Roi, Dame, Roi, 10 » 5 fois sur 5 ; avec, « quinte flush royale » 5 fois
sur 5. Chaque combinaison est donnée avec une force de 10 à 1 plutôt qu'un rang de 1 à 10 : avec des rangs,
le modèle lit « 5 > 4 » et conclut qu'une couleur bat un full.

## Tests

```
python3 test_web.py && python3 test_preflop.py && python3 test_glossary.py && python3 test_ai.py
```

## Contenu

| Fichier | Rôle |
|---|---|
| `llm.py` | Client Ollama (HTTP, streaming) |
| `ai.py` | Question en ligne de commande, avec le classement des combinaisons injecté |
| `server.py`, `web/index.html` | Interface web et comparaison de modèles |
| `preflop.py` | `hand_range("AKs")` : action d'ouverture par position |
| `glossary.py` | `define("UTG")` : glossaire du poker en français |
| `build_glossary.py` | Régénère `data/poker_glossary.json` depuis la source |
| `data/` | Données du poker, voir « Données » ci-dessous |
| `docs/` | Sujet, bootstrap et catalogue de features |

## Données

| Fichier | Contenu | Source et droits |
|---|---|---|
| `data/hand_rankings.json` | Les 10 combinaisons, `{rang, fr, en, description, exemple}`, rang 1 = la plus forte | Règles standard, écrit à la main le 2026-09-30 |
| `data/preflop_rfi.json` | Ranges d'ouverture (RFI) 6-max 100bb, par position (UTG, MP, CO, BTN, SB). Main absente = fold | [AHTOOOXA/poker-charts](https://github.com/AHTOOOXA/poker-charts), `src/data/ranges/pekarstas.ts`, récupéré le 2026-09-21. Code sous MIT, mais les ranges viennent de sites tiers : droits incertains |
| `data/poker_glossary_source.txt`, `data/poker_glossary.json` | Glossaire français : 313 entrées du lexique et 14 abréviations de chat, construit par `build_glossary.py` | Texte copié depuis un site affilié (il cite PokerListings). Droits inconnus |

Le dépôt est privé : ces données tierces conviennent pour un projet d'école, mais **ne doivent pas être publiées**.
Le glossaire a été nettoyé à la main (publicités et index retirés, paragraphes joints par ` ¶ `), coquilles de la
source comprises.
