# SensAI

Assistant IA local, tournant sur Ollama. Projet Epitech Tech3. Piste actuelle : un coach de poker (Texas Hold'em).
Où on en est et ce qui reste à faire : [ROADMAP.md](ROADMAP.md).

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

## Tests

```
python3 test_web.py && python3 test_preflop.py && python3 test_glossary.py
```

## Contenu

| Fichier | Rôle |
|---|---|
| `llm.py` | Client Ollama (HTTP, streaming) |
| `server.py`, `web/index.html` | Interface web et comparaison de modèles |
| `preflop.py` | `hand_range("AKs")` : action d'ouverture par position |
| `glossary.py` | `define("UTG")` : glossaire du poker en français |
| `build_glossary.py` | Régénère `data/poker_glossary.json` depuis la source |
| `data/` | Données et leur provenance (`SOURCE.md`, `DONNEES_A_AJOUTER.md`) |
| `docs/` | Sujet, bootstrap et catalogue de features |
