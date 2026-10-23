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

## Entraîneur en ligne de commande (B1) et outils MCP (T1)

```
python3 main.py                        # le parcours d'exercices ; modèle et serveurs MCP lus dans config.json
python3 main.py --model llama3.2:3b    # autre modèle, sans toucher au code
python3 main.py --no-tools             # sans serveur MCP
python3 main.py --seed 7               # mêmes situations à chaque lancement (démo, keynote)
python3 main.py --pseudo amine         # niveau, résultats et fiches gardés dans profiles/amine.json
python3 main.py --libre                # chat libre avec le modèle, sans le parcours
```

Le parcours (`trainer.py`, sans entrée-sortie) : SensAI demande le niveau, tire une situation du niveau (d'abord
dans la banque générée par le modèle, sinon tirée par le code, sans attente), le joueur répond par une touche
(`f` se coucher, `c` suivre, `r` relancer ; pour le quiz « qui gagne ? », `m` moi, `a` l'adversaire, `e` égalité), le code note la décision (bon, acceptable, erreur) d'après la
référence calculée et affiche ses faits. Puis le débrief : chat en streaming avec le coach (`coach.py`,
`prompts/coach.txt`), qui reçoit la situation, la décision, le verdict et la référence, et l'explique sans la
recalculer.

```
Situation 1 · Table 6 joueurs, 100 blindes · tu es à la petite blinde (SB).
Tout le monde s'est couché jusqu'à toi (SB). Tu as 5♥ J♠.
Que fais-tu ?  [f] se coucher   [r] relancer
> f
✅ Bon : se coucher, c'est la bonne réponse.
- J5o : se coucher en UTG, MP, CO, BTN, SB
- Référence : ranges d'ouverture 6-max, 100 blindes.
> Pourquoi ?
```

| Niveau | Thèmes |
|---|---|
| Je découvre | Ouvrir ou se coucher, premier à parler (mains nettes) ; qui gagne à l'abattage (`m`, `a`, `e`) |
| Je joue un peu | Ouvertures, tirages au flop ou au turn |
| Je joue souvent | Tirages : outs contre cote du pot ; défendre sa grosse blinde face à une ouverture (équité contre la range de l'ouvreur) |

Réponse affichée au fil de l'eau, historique du débrief gardé jusqu'à la situation suivante. Commandes :
`/exercice` (situation suivante), `/fiche` (fiche de fin d'exercice), `/niveau` (changer de niveau), `/reprendre`
(dernier débrief du profil), `/reset` (oublier le débrief), `/tools` (outils chargés), `/quit` ou Ctrl-D. Ctrl-C
coupe une réponse sans quitter.

- **Profil (M1)** : avec `--pseudo`, `profils.py` garde dans `profiles/<pseudo>.json` (jamais commité) le niveau,
  les verdicts par thème, le dernier débrief et les 20 dernières fiches. Au retour, SensAI ne redemande pas le
  niveau, cite les thèmes à revoir et les sert plus souvent (jusqu'à 3 fois plus) ; le coach reçoit les résultats.
- **Sorties structurées (T5)** : le niveau peut se dire en toutes lettres (« je compte mes outs ») ; le modèle le
  classe en `{niveau, raison}` (schéma JSON imposé à Ollama, `prompts/niveau.txt`), le code le vérifie et, s'il
  est inutilisable, repose la question par numéro. `/fiche` écrit `{a_retenir, theme_a_revoir}`
  (`prompts/fiche.txt`), vérifiée de la même façon.
- **Questions (X4)** : pendant le débrief, le coach peut appeler l'outil local `poser_question` ; la question
  s'affiche avec ses choix numérotés, le joueur répond par un numéro (envoyé en toutes lettres) ou par écrit.
Ollama éteint, modèle absent, configuration illisible : message clair et arrêt. Message vide : refusé sans
appeler le modèle.

Le modèle peut **appeler des outils** au lieu de répondre : il émet une demande (nom + arguments), `main.py`
l'exécute via MCP et lui renvoie le résultat, puis il continue (5 tours d'outils au plus par question). Les
serveurs MCP sont déclarés dans `config.json` (`mcp_servers`), client et serveur écrits en bibliothèque
standard (`mcp_client.py`, `mcp_server.py`) :

| Serveur | Outils | Exemple de question |
|---|---|---|
| `poker` (le nôtre, `mcp_server.py`) | `hand_odds`, `define_term`, `preflop_open`, `hand_rankings` | « J'ai As Roi de cœur, flop dame de cœur, 7 de cœur, 2 de trèfle, 100 au pot, 50 à payer. Je suis ? » |
| `fichiers` ([serveur officiel](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem), via `npx`) | `list_directory`, `read_text_file`, `write_file`, limités au dossier `notes/` | « Qu'est-ce que j'ai noté dans mes notes de jeu ? » |

`mcp_server.py` fonctionne avec n'importe quel client MCP. Un serveur qui ne démarre pas est signalé et le chat
continue sans lui. `write_file` remplace tout le fichier : le modèle doit le réécrire en entier pour ajouter une
ligne.

## API de l'entraîneur (phase 3, pour le web)

`server.py` sert le même parcours que le CLI, sur `trainer.py` : une session par joueur, gardée en mémoire du
serveur. Corps et réponses en JSON ; le débrief arrive en NDJSON, comme `/api/chat`.

| Route (POST) | Corps | Réponse |
|---|---|---|
| `/api/sessions` | `{pseudo?, graine?}` | `201 {sessionId, niveau, niveaux, profil}` ; `niveau` est connu si le profil l'a ; `graine` rejoue les situations de `main.py --seed` |
| `/api/sessions/<id>/niveau` | `{reponse}` : numéro, nom ou texte libre (T5) | `{niveau, raison}` ; 400 si non compris |
| `/api/sessions/<id>/situations` | `{}` | `201 {numero, situation}` : sans la référence, avec `texte`, `question`, `actions` |
| `/api/sessions/<id>/decision` | `{action}` | `{verdict, reference}` |
| `/api/sessions/<id>/messages` | `{texte}` (un numéro répond à la question du coach) | NDJSON : `queued`, `thinking`, `token`, `outil`, `question` (X4), puis `done` ou `error` |
| `/api/sessions/<id>/fiche` | `{}` | `{fiche: {a_retenir, theme_a_revoir}}` |
| `/api/sessions/<id>/reprendre` | `{}` | le dernier débrief du profil : `{situation, action, verdict, reference, debrief}` |

Une session traite une demande à la fois : une autre demande arrivée pendant ce temps reçoit un 400. Chaque
appel au modèle prend une place du sémaphore RAM. Le débrief a les mêmes outils que le CLI : les serveurs MCP de la config,
lancés une fois au démarrage et partagés par les sessions (`python3 server.py --no-tools` pour s'en passer), et
`poser_question`. Les écrans React de ce parcours restent à faire.

## Jouer contre l'IA (frontend React)

```
python3 server.py                                  # API sur http://localhost:8000
cd frontend && npm install && npm run dev          # puis http://localhost:5173 (Vite relaie /api)
```

- **Adversaire IA** : à son tour, le frontend appelle `/api/opponent`. Le modèle reçoit ses cartes, le board et
  les calculs d'`odds.py`, et doit répondre en JSON conforme à un schéma (`format` d'Ollama) limité aux actions
  légales. Montant hors bornes : ramené dans les bornes. Réponse inutilisable ou Ollama en panne : règle de
  secours (check, sinon suivre), signalée à l'écran. Compter 15 à 40 s par décision sur CPU.
- **Coach SensAI** : `/api/coach` envoie votre situation à `ai.build_prompt` (même contexte que la CLI) et
  diffuse le conseil en streaming. Disponible seulement à votre tour.
- Les deux passent par le sémaphore RAM de `server.py` et le modèle de `config.json`. La logique est dans
  `poker_ai.py` (testée sans Ollama par `test_poker_ai.py`).

L'interface (détails, routes et user stories dans `docs/FRONTEND.md`) :

- **Entraîneur Jeton** (écran d'accueil, plein écran) : niveau, situation, correction, débrief et fiche. Le menu
  **Plus** de l'en-tête ouvre les autres modes, et chaque page revient à l'entraîneur par « Entraîneur ».
- **Partie contre l'IA** (menu) : blindes et tapis de départ au choix, reprise de la partie en cours après un
  rechargement, état d'Ollama et des modèles avec la commande `ollama pull` à copier, préférences d'affichage (thème
  clair, jeu à quatre couleurs, grandes cartes, animations).
- **Table** : donneur, blindes, mises du tour et dernière action sur chaque siège ; nom de votre main et de ses
  cinq cartes, calculé par l'évaluateur du moteur ; termes reliés au glossaire.
- **Actions** : seules les actions légales sont actives ; montants rapides (½ pot, ¾ pot, pot, tapis), curseur,
  raccourcis clavier F, C, R, T.
- **Coach** en chat (questions de suite, arrêt), **Repères** chiffrés par le code (cote du pot, équité, outs),
  **Statistiques** de la partie et depuis toujours, bilan ajoutable à `notes/sessions.md` (lu par le coach CLI).
- **Mains précédentes** : revoir une main étape par étape, courbe du tapis, export texte ou JSON, bilan de fin
  de partie. Pages **Mes parties**, **Glossaire**, **Classement des mains** et **Banque de situations**, dans le menu
  **Plus** ; visite guidée à la première partie.

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

### Évaluation du coach (EV1)

```
python3 evaluate_coach.py                          # 30 situations, coach et juge de config.json
python3 evaluate_coach.py --nombre 6 --graine 1    # moins de situations, un autre tirage
python3 evaluate_coach.py --modele llama3.2:3b     # un autre coach ; --juge pour un autre correcteur
```

Le principe de SensAI est que le coach explique la référence calculée par le code sans la contredire : ce script
le mesure. Il tire des situations de chaque thème (graine fixe : le même jeu d'une fois sur l'autre), y prend la
mauvaise décision et demande « pourquoi ? » au coach, avec le même contexte que le parcours. Un juge d'une autre
famille de modèle (`judge_model`, `llama3.2:3b`) coche ensuite chaque fait de la référence (la bonne réponse,
puis les faits chiffrés) : présent, absent ou contredit. Score principal : la part des débriefs sans
contradiction. Résultats dans `evaluation/coach_resultats.md` et `.json` ; un verdict illisible n'est pas compté.
Le code vérifie aussi, sans modèle, que le débrief nomme la bonne action et cite les chiffres de la référence
(`--relire` recalcule cette vérification sur les résultats enregistrés).

Premier essai (2026-10-22, 8 situations, coach `qwen3:4b-instruct`) : **21 faits sur 24 retrouvés par le code**,
mais le juge `llama3.2:3b` n'en voit qu'1 sur 28 et signale 5 contradictions sur 8, la plupart fausses (il
marque « absent » des chiffres cités mot pour mot). Ce juge n'est pas fiable : il en faut un plus gros, ou
d'une autre famille (`gemma3:4b`, prévu par le plan, n'est pas installé ici). Les vraies erreurs relevées en
relisant : des chiffres inventés hors référence (« moins de 10 % de chance de gagner » pour 73o).

## Tests

```
python3 test_cli.py && python3 test_trainer.py && python3 test_coach.py && python3 test_profils.py && python3 test_generation.py && python3 test_evaluate_coach.py && python3 test_mcp_client.py && python3 test_mcp_server.py && python3 test_web.py && python3 test_poker_api.py && python3 test_poker_ai.py && python3 test_preflop.py && python3 test_glossary.py && python3 test_ai.py && python3 test_equity.py && python3 test_odds.py && python3 test_evaluate.py
python3 -m pytest poker_engine/tests       # moteur de poker
cd frontend && npm test                    # composants React (Vitest, jsdom, serveur simulé)
```

Les tests du frontend simulent `fetch` : ils ne demandent ni `server.py` ni Ollama. `npm run test:watch` les
relance à chaque modification.

`cd frontend && npm run test:e2e` joue les parcours principaux dans un vrai Chromium (Playwright 1.63) : il lance
`server.py` sur le port 8791 avec le faux Ollama de `fake_ollama.py`, et Vite sur le port 5191. Première fois :
`npx playwright install chromium` si le navigateur manque.

## Contenu

| Fichier | Rôle |
|---|---|
| `poker_engine/` | Moteur de poker : cartes, paquet, joueurs, partie, actions, évaluation des mains |
| `llm.py` | Client Ollama (HTTP, streaming) |
| `ai.py` | Question en ligne de commande, avec le classement des combinaisons injecté |
| `equity.py` | Chances de gagner d'une main selon le board, note avant le flop |
| `evaluate.py`, `evaluation/` | Jeu d'évaluation : questions de référence, résultats remplis par le script |
| `evaluate_coach.py` | Évaluation du coach (EV1) : le débrief contredit-il la référence ? Juge d'une autre famille |
| `odds.py` | Outs, cote du pot et analyse complète d'une situation, injectée par `ai.py` |
| `server.py`, `web/index.html` | Interface web, comparaison de modèles, API de jeu, adversaire IA et coach |
| `main.py` | Entraîneur en ligne de commande (et chat libre avec `--libre`), avec appels d'outils |
| `trainer.py` | Parcours d'exercices sans entrée-sortie : niveau, situation, décision, verdict, débrief |
| `coach.py`, `prompts/coach.txt` | Contexte du débrief, boucle d'appels d'outils, question à choix (X4) |
| `prompts/niveau.txt`, `prompts/fiche.txt` | Sorties structurées (T5) : niveau en toutes lettres, fiche de fin d'exercice |
| `profils.py` | Profils JSON des joueurs (M1) : niveau, résultats par thème, dernier débrief, fiches |
| `generation.py` | Situations et leur référence : banque générée par le modèle, tirage par le code |
| `mcp_client.py`, `mcp_server.py` | Client MCP (lance les serveurs de la config) ; nos outils de poker en serveur MCP |
| `notes/` | Notes de jeu, accessibles au modèle par le serveur MCP de fichiers |
| `poker_ai.py`, `poker_api.py` | Ce que le modèle voit d'une main (coach, adversaire) ; état public de la partie |
| `frontend/` | Table de poker React (Vite) |
| `preflop.py` | `hand_range("AKs")` : action d'ouverture par position |
| `glossary.py` | `define("UTG")` : glossaire du poker en français |
| `build_glossary.py` | Régénère `data/poker_glossary.json` depuis la source |
| `config.json`, `prompts/system.txt` | Réglages de l'interface web et prompt système |
| `data/` | Données du poker, voir « Données » ci-dessous |
| `docs/` | Sujet, bootstrap et catalogue de features |
| `docs/DEMO.md` | Démo de la keynote, rejouable avec `--seed 187` |
| `USER_STORIES.md` | Deux user stories par feature, avec l'état de chaque critère |

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
