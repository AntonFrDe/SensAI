# Plan : banque de situations générées par le LLM

Rédigé le 2026-10-08 sur `refonte/entraineur`. Complète `docs/REFONTE.md` (sections 2, 4 et 7).

## But

Le LLM invente les situations d'entraînement, sans banque écrite à la main. Chaque situation est :

1. **générée** par le modèle en JSON qui suit un schéma (feature **T5**) ;
2. **vérifiée** par le code ; si elle est refusée, les erreurs sont renvoyées au modèle, qui corrige, avec
   3 essais au plus (boucle générer → vérifier → corriger, feature **A1**) ;
3. **remplacée** par une situation tirée au hasard par le code si les 3 essais échouent ou si Ollama ne répond
   pas (repli) ;
4. **notée par le code** : la bonne réponse vient de `preflop.py` et `odds.py`, jamais du modèle ;
5. **ajoutée à la banque** `data/situations_generees.jsonl`, puis affichée dans une page web visuelle.

Deux thèmes pour commencer, ceux dont la référence se calcule déjà :

| Thème | Situation | Référence |
|---|---|---|
| `ouverture` | Avant le flop, tout le monde s'est couché jusqu'au joueur : ouvrir ou se coucher | `preflop.hand_range` |
| `tirage` | Au flop ou au turn, tirage couleur ou quinte, l'adversaire mise : suivre ou se coucher | `odds.outs`, `odds.hit_chance`, `odds.pot_odds` |

## Contrat : une situation de la banque

C'est l'interface entre les deux tâches. Une ligne JSON par situation dans la banque, et le même objet dans
les réponses HTTP.

```json
{
  "id": "3f9a1c2e",
  "theme": "tirage",
  "niveau": "intermediaire",
  "position": "BTN",
  "cartes": ["Ah", "5h"],
  "board": ["Kh", "7h", "2c"],
  "pot": 6,
  "a_payer": 2,
  "historique": "Au flop, ton adversaire mise 2 bb.",
  "actions": ["fold", "call", "raise"],
  "reference": {
    "bonnes": ["call"],
    "acceptables": [],
    "faits": ["Outs : 15 (9 pour couleur, 6 pour paire)", "Chance de toucher à la prochaine carte : 31,9 %", "…"]
  },
  "source": "llm",
  "tentatives": 2,
  "erreurs": [["carte en double : Kh"]],
  "cree_le": "2026-10-08T14:03:12"
}
```

- Cartes : codes `valeur + couleur`, valeurs `AKQJT98765432`, couleurs `s h d c` (`T` = 10).
- `niveau` : `debutant`, `intermediaire` ou `avance`. Montants en blindes (bb).
- `source` : `llm` (le modèle a produit une situation valide) ou `repli` (tirée par le code).
- `tentatives` : nombre d'appels au modèle. `erreurs` : une liste de messages par essai refusé.
- Une action absente de `bonnes` et de `acceptables` est une erreur.

## Tâche A : backend (génération, vérification, banque, routes HTTP)

Fichiers : `llm.py`, `config.json`, `prompts/generation.txt`, `generation.py` (nouveau), `server.py`,
`test_generation.py` (nouveau), `test_web.py`. Ne touche à rien d'autre.

### A1. `llm.py`

- Dans `stream_chat`, ajoute `"temperature": cfg["temperature"]` aux `options` quand `"temperature" in cfg`.
- Ajoute `complete(messages, cfg) -> str` : la réponse entière, sans streaming, via
  `"".join(data for kind, data in stream_chat(messages, cfg) if kind == "token")`.

### A2. `config.json`

Ajoute `"banque_file": "data/situations_generees.jsonl"`. Le chemin est relatif à la racine du dépôt ; un
chemin absolu (cas des tests) est utilisé tel quel (`ROOT / chemin` le permet).

### A3. `prompts/generation.txt` (texte exact)

```
Tu crées des situations d'entraînement au Texas Hold'em pour un coach de poker.
Table de 6 joueurs, tapis de 100 blindes, montants en blindes (bb).
Tu réponds uniquement par un objet JSON, sans texte autour.

Notation des cartes : valeur puis couleur, sans espace.
Valeurs : A K Q J T 9 8 7 6 5 4 3 2 (T = 10). Couleurs : s = pique, h = cœur, d = carreau, c = trèfle.
Exemples : "Kd" = roi de carreau, "Th" = 10 de cœur, "2c" = 2 de trèfle. Une carte n'apparaît qu'une fois.

Champs :
- position : la place du joueur (UTG, MP, CO, BTN, SB ou BB) ;
- cartes : les 2 cartes du joueur ;
- board : les cartes communes ;
- pot : le pot au moment de décider, mise adverse comprise ;
- a_payer : ce que le joueur doit payer pour suivre ;
- historique : 1 ou 2 phrases, en tutoyant le joueur, qui racontent ce qui s'est passé avant sa décision. Ne donne ni la bonne réponse, ni de calcul.

Varie les situations : positions, hauteurs de cartes, couleurs et boards différents.
```

### A4. `generation.py`

Docstring de module en français, comme `odds.py`. Bibliothèque standard + modules du dépôt uniquement.

Constantes :

```python
THEMES = ("ouverture", "tirage")
NIVEAUX = ("debutant", "intermediaire", "avance")
CARTES = [r + s for r in "AKQJT98765432" for s in "shdc"]          # les 52 codes
POSITIONS = {"ouverture": ["UTG", "MP", "CO", "BTN", "SB"],        # la BB n'ouvre jamais
             "tirage": ["UTG", "MP", "CO", "BTN", "SB", "BB"]}
ACTIONS = {"ouverture": ["fold", "raise"], "tirage": ["fold", "call", "raise"]}
CHAMPS = ("position", "cartes", "board", "pot", "a_payer", "historique")  # ce que le modèle écrit
MAX_TENTATIVES = 3
TEMPERATURE = 0.9  # de la variété : à 0, le modèle redonnerait toujours la même situation
```

Consignes envoyées au modèle (texte exact) :

- `ouverture` : « Avant le flop. Tout le monde s'est couché jusqu'au joueur, qui doit ouvrir (relancer) ou se
  coucher. board vide, a_payer 0, pot 1.5 (les deux blindes). position parmi UTG, MP, CO, BTN, SB. »
- `tirage` : « Au flop (board de 3 cartes) ou au turn (4 cartes). Le joueur n'a pas encore de main faite mais
  un tirage couleur ou quinte. Un adversaire vient de miser a_payer ; pot = pot avant la mise + la mise,
  donc a_payer est plus petit que pot. »
- `debutant` : « décision nette : une main clairement à jouer ou clairement à jeter. »
- `intermediaire` : « décision moins évidente : position précoce ou main limite. »
- `avance` : « décision serrée, proche de la limite. »

Fonctions :

| Fonction | Rôle |
|---|---|
| `schema(theme) -> dict` | Schéma JSON pour le `format` d'Ollama : objet avec les 6 `CHAMPS`, tous requis, `additionalProperties: false`. `position` : enum `POSITIONS[theme]`. `cartes` : tableau d'enum `CARTES`, 2 éléments exactement. `board` : tableau d'enum `CARTES`, 0 élément pour `ouverture`, 3 à 4 pour `tirage`. `pot`, `a_payer` : `number`. `historique` : `string`. |
| `demande(theme, niveau, recentes) -> str` | Message utilisateur : `Thème : <theme> — <consigne>`, `Niveau du joueur : <niveau> — <consigne>`, puis, si `recentes` n'est pas vide, `Déjà dans la banque, ne les répète pas : <recentes séparées par « ; »>`, puis `Réponds avec le JSON seulement.` |
| `cle(theme, sit) -> str` | Identité d'une situation pour repérer les doublons : `f"{theme}\|{position}\|{cartes triées}\|{board}"`. |
| `valider(brut, theme, niveau, deja_vues) -> list[str]` | Liste des erreurs en français (vide si la situation est valide). Détail plus bas. |
| `reference(sit) -> dict` | `{"bonnes": [...], "acceptables": [...], "faits": [...]}`. Détail plus bas. |
| `repli(theme, niveau, rng, deja_vues) -> dict` | Situation brute (les 6 `CHAMPS`) tirée au hasard avec `rng` (`random.Random`), retirée jusqu'à ce que `valider` renvoie `[]` (5 000 essais au plus, sinon `RuntimeError`). `ouverture` : board vide, pot 1.5, a_payer 0, historique « Tout le monde s'est couché jusqu'à toi. ». `tirage` : board de 3 ou 4 cartes, `pot_avant` parmi 4, 6, 8, 10, `mise = round(pot_avant * f, 1)` avec `f` parmi 0.33, 0.5, 0.75, 1, `pot = pot_avant + mise`, `a_payer = mise`, historique « Au flop, ton adversaire mise 2 bb. » (ou « Au turn »). |
| `lire_banque(cfg) -> list[dict]` | Situations de `ROOT / cfg.get("banque_file", "data/situations_generees.jsonl")`, dans l'ordre du fichier. Fichier absent → `[]`. Ligne illisible → ignorée avec un avertissement sur `stderr`. |
| `ajouter(situation, cfg) -> None` | Ajoute une ligne JSON (`ensure_ascii=False`) à la banque, sous un `threading.Lock` du module ; crée le dossier au besoin. |
| `generer(theme, niveau, cfg) -> dict` | La boucle complète, détail plus bas. Renvoie la situation au format du contrat, déjà ajoutée à la banque. |

`valider(brut, theme, niveau, deja_vues)`, dans cet ordre :

1. `brut` n'est pas un `dict` → `["la réponse doit être un objet JSON"]`.
2. Champ absent → `champ manquant : <nom>` (un message par champ ; on s'arrête là s'il en manque).
3. `position` hors de `POSITIONS[theme]` → `position impossible pour ce thème : <position>`.
4. `cartes` : liste de 2 codes de `CARTES` ; code inconnu → `carte inconnue : <code>` ; mauvais nombre →
   `il faut exactement 2 cartes`.
5. `board` : codes de `CARTES` ; longueur 0 pour `ouverture`, 3 ou 4 pour `tirage`, sinon
   `board de <n> cartes impossible pour ce thème`.
6. Carte présente deux fois dans `cartes + board` → `carte en double : <code>`.
7. `pot` et `a_payer` : nombres (`int` ou `float`, pas `bool`). `ouverture` : `pot == 1.5` et `a_payer == 0`,
   sinon `avant le flop sans relance, pot 1.5 et a_payer 0`. `tirage` : `0 < a_payer < pot`, sinon
   `a_payer doit être positif et plus petit que pot`.
8. `historique` : chaîne non vide de 300 caractères au plus, sinon `historique vide ou trop long`.
9. S'il y a déjà des erreurs, on les renvoie. Sinon :
   - `ouverture` et `debutant` : la cellule de `preflop.hand_range("".join(cartes))[position]` est mixte (un
     `tuple`) → `main limite à cette position : trop ambiguë pour un débutant` ;
   - `tirage` : `odds.outs(...)` n'a ni la clé `"Couleur"` ni la clé `"Quinte"` →
     `pas de tirage couleur ou quinte` ;
   - `cle(theme, brut) in deja_vues` → `situation déjà dans la banque`.

`reference(sit)` (cartes converties avec `equity.parse_cards(" ".join(codes))`, pourcentages avec `equity.pct`) :

- `ouverture` : `cellule = hand_range(...)[position]`. `"raise"` → bonnes `["raise"]` ; `"fold"` → bonnes
  `["fold"]` ; tuple → acceptables `["raise", "fold"]`. Faits :
  `"<main> : ouvrir en <positions> ; limite en <positions> ; se coucher en <positions>"` (on omet les parties
  vides ; `<main>` = `preflop.normalize_hand`), puis `"Référence : ranges d'ouverture 6-max, 100 blindes."`.
- `tirage` : `n` = total des outs, `une = hit_chance(n, len(board))["prochaine carte"]`,
  `deux = hit_chance(...).get("d'ici la river")`, `requis = pot_odds(pot, a_payer)`.
  `une >= requis` → bonnes `["call"]` ; sinon `deux` existe et `deux >= requis` → acceptables
  `["call", "fold"]` ; sinon bonnes `["fold"]`. Faits : `"Outs : 15 (9 pour couleur, 6 pour paire)"`,
  `"Chance de toucher à la prochaine carte : 31,9 %"`, `"Chance de toucher d'ici la river : 54,1 %"` (au flop
  seulement), `"Cote du pot : il faut 25,0 % d'équité (payer 2 pour un pot de 6)"`,
  `"Hypothèse : sans gains implicites ni semi-bluff."`.

`generer(theme, niveau, cfg)` :

1. `banque = lire_banque(cfg)` ; `deja_vues = {cle(s["theme"], s) for s in banque}` ; `recentes` = les 10
   dernières situations du même thème, résumées en `"Kd 9d BTN"` (cartes, board s'il y en a, position).
2. `gen_cfg = {**cfg, "system_prompt": <prompts/generation.txt>, "format": schema(theme), "temperature": TEMPERATURE}`.
3. Jusqu'à `MAX_TENTATIVES` appels à `complete(messages, gen_cfg)` (importé par `from llm import LLMError, complete`,
   pour que les tests puissent remplacer `generation.complete`) :
   - `LLMError` → `erreurs.append([f"modèle indisponible : {e}"])` et on sort de la boucle ;
   - réponse non JSON → erreurs `["la réponse n'est pas du JSON"]` ;
   - sinon `problemes = valider(json.loads(reponse), theme, niveau, deja_vues)` ;
   - `problemes == []` → `source = "llm"`, fin ;
   - sinon on ajoute `problemes` à `erreurs`, puis deux messages à l'historique : la réponse du modèle
     (`assistant`) et `"Situation refusée : <problèmes séparés par « ; »>. Corrige et renvoie le JSON complet."` (`user`).
4. Pas de situation valide → `brut = repli(theme, niveau, random.Random(), deja_vues)`, `source = "repli"`.
5. Situation finale : `id` (`uuid4().hex[:8]`), `theme`, `niveau`, les 6 `CHAMPS`, `actions`, `reference`,
   `source`, `tentatives` (appels faits au modèle), `erreurs`, `cree_le`
   (`datetime.now().isoformat(timespec="seconds")`). `ajouter(...)`, puis `return`.

### A5. `server.py`

- `GET /api/banque` → `200 {"situations": [...]}`, **la plus récente en premier**.
- `POST /api/banque` (même contrôle `Content-Type` et taille que les autres routes) avec `{"theme", "niveau"}` :
  thème hors de `THEMES` → `400 {"error": "Thème inconnu."}` ; niveau hors de `NIVEAUX` →
  `400 {"error": "Niveau inconnu."}`. Sinon, sous `with self.slots:` (le garde-fou RAM),
  `generation.generer(theme, niveau, self.cfg)` → `201 {"situation": ...}`.
- Branche la route avant la construction des `jobs`, comme `GAME_ROUTES`. Ne modifie pas les autres routes.

### A6. Tests (même style que `test_odds.py` : fonctions `test_*` et exécution par `__main__`)

`test_generation.py`, sans Ollama (remplace `generation.complete` par une fausse fonction, et remets
l'originale dans un `finally`) ; la banque des tests est un fichier temporaire (`tempfile`), jamais le vrai :

- `reference` ouverture : `Kd 9d` en UTG → bonnes `["fold"]` ; en BTN → bonnes `["raise"]` ; `2c 2d` en UTG →
  acceptables `["raise", "fold"]`.
- `reference` tirage : `Ah 5h` sur `Kh 7h 2c`, pot 6, à payer 2 → bonnes `["call"]` et un fait contient
  « 25,0 % » ; `8h 9d` sur `7c 6s 2h`, pot 10, à payer 8 → acceptables `["call", "fold"]` ;
  `Ah 5h` sur `Kh 7h 2c Qd`, pot 10, à payer 9 → bonnes `["fold"]`.
- `valider` repère : carte en double, carte inconnue, champ manquant, board non vide en ouverture,
  `a_payer >= pot` en tirage, cellule mixte pour un débutant (`2c 2d` UTG), pas de tirage (`2c 3d` sur `As Kh 9c`),
  situation déjà vue, réponse qui n'est pas un objet.
- `repli` donne une situation valide pour 30 graines et pour chaque thème.
- `generer` : la fausse fonction renvoie d'abord une situation avec une carte en double, puis une valide →
  `source == "llm"`, `tentatives == 2`, `len(erreurs) == 1`, le dernier message envoyé contient
  « Situation refusée », `gen_cfg` contient `format` et `temperature`, et la banque a une ligne.
- `generer` : la fausse fonction lève `LLMError` → `source == "repli"`, `tentatives == 1`, la situation est valide.
- `lire_banque` sur un fichier absent → `[]`.

`test_web.py` : ajoute `"banque_file"` (chemin temporaire absolu) à la config des nouveaux tests.

- thème inconnu → 400 ;
- avec le faux Ollama (il répond `{"action": "call"}` à toute requête avec `format`) → 3 essais refusés,
  repli, `201`, `source == "repli"`, `tentatives == 3`, puis `GET /api/banque` la renvoie en premier ;
- Ollama injoignable → `201`, `source == "repli"`.

**Fini quand** : `.venv/bin/python -m pytest -q` passe en entier (178 tests avant ce travail).

## Tâche B : affichage visuel (React)

Fichiers : `frontend/src/api.ts`, `frontend/src/Banque.tsx` (nouveau), `frontend/src/App.tsx`,
`frontend/src/styles.css`. Ne touche à rien d'autre. Ne dépend que du contrat ci-dessus.

### B1. `api.ts`

- Types `Theme`, `Niveau`, `Situation` (champs du contrat ; `actions`, `bonnes`, `acceptables` en `PokerAction[]`).
- `toCard(code: string): CardData` : `"Kd"` → `{ rank: 'K', suit: 'diamonds' }`, `"Th"` → rang `'10'` ;
  couleurs `s` → `spades`, `h` → `hearts`, `d` → `diamonds`, `c` → `clubs`.
- `fetchBanque(): Promise<Situation[]>` : `GET /api/banque`, renvoie `situations`.
- `genererSituation(theme, niveau): Promise<Situation>` : `POST /api/banque` en JSON, renvoie `situation`.
- Erreurs : `throw new Error(result.error || 'Banque indisponible.')`, comme `postGame`.

### B2. `Banque.tsx`

Composant `Banque({ onBack }: { onBack: () => void })` :

- Au montage, charge la banque ; erreur affichée dans un `<p role="alert">`.
- Formulaire : liste « Thème » (Ouverture avant le flop / Suivre un tirage), liste « Niveau » (Débutant /
  Intermédiaire / Avancé), bouton « Générer une situation ». Pendant la génération : bouton désactivé et
  message `aria-live="polite"` « Génération en cours… (15 à 40 s par essai, 3 essais au plus) ». La nouvelle
  situation s'ajoute **en tête** de la liste.
- Bouton « ← Accueil » qui appelle `onBack`.
- Une `<article className="situation">` par situation :
  - pastilles : thème, niveau, position, et la source : « LLM, 1er essai » (vert) si `source === 'llm'` et
    `tentatives === 1`, « LLM après N essais » (ambre) si `source === 'llm'`, « Repli : tirée par le code »
    (gris) sinon ;
  - un mini tapis vert : les 2 cartes du joueur (`PlayingCard`), le board avec `CommunityCards` s'il n'est pas
    vide, puis « Pot : 6 bb · À payer : 2 bb » (pas `ChipAmount`, qui affiche des jetons) ;
  - l'historique ;
  - « Référence » : chaque action de `actions` avec son libellé (fold « Se coucher », check « Checker »,
    call « Suivre », bet « Miser », raise « Relancer ») et son verdict : ✅ bon si dans `bonnes`,
    🟡 acceptable si dans `acceptables`, ❌ erreur sinon ; puis la liste des `faits` ;
  - si `erreurs` n'est pas vide : `<details>` « Essais refusés (N) » avec une ligne par essai.

### B3. `App.tsx`

Ajoute la vue `'banque'` : un second bouton « Banque de situations » sur l'accueil, et `<Banque onBack={…} />`
quand la vue est `'banque'`. Teste cette vue **avant** la condition actuelle `view === 'home' || !game || !state`.

### B4. `styles.css`

Classes `.banque-form`, `.situations` (grille `repeat(auto-fill, minmax(320px, 1fr))`), `.situation`,
`.badges`, `.badge` (variantes `.llm`, `.retry`, `.repli`), `.mini-table` (tapis vert, comme `.poker-table`
en plus petit), `.verdicts`. Même thème sombre que le reste ; contraste lisible ; rien ne déborde à 360 px de large.

**Fini quand** : `cd frontend && npm run build` passe (TypeScript + Vite).

## Ordre et vérification finale

Les tâches A et B ne partagent aucun fichier : elles tournent en parallèle. Ensuite :

1. relecture du diff ;
2. `pytest` et `npm run build` ;
3. une vraie génération avec `qwen3:4b-instruct` via `POST /api/banque`, et la page vue dans le navigateur.

## Hors périmètre (pour plus tard)

- Les thèmes « qui gagne ? » et « défendre sa grosse blinde » (équité contre une range, phase 4).
- Afficher les essais en direct (streaming NDJSON) : pour l'instant, on les voit une fois la situation finie.
- Brancher la banque sur le parcours d'exercice (`trainer.py`, phase 1).
- `odds.outs` compte aussi les cartes qui donnent une paire : la référence « suivre » est donc un peu
  optimiste (limite déjà notée dans `odds.py`).

## Bilan après l'essai avec le vrai modèle (2026-10-08)

Tâches A et B faites par deux agents Haiku en parallèle, puis trois corrections après relecture et essai réel
avec `qwen3:4b-instruct` :

1. **Bug de `equity.evaluate7`** : la branche « deux paires » plantait sans kicker (`max()` vide), donc
   `odds.outs` plantait sur tout board de turn à deux paires (par exemple `Kh Kd 7c 7s`). Cela touchait aussi
   l'outil MCP `hand_odds`. Corrigé à la source (`default=0`), avec un test de régression dans `test_odds.py`.
2. **L'historique est écrit par le code** (`generation.historique`), plus par le modèle : sur 3 historiques
   générés, les 3 étaient faux (« un pair de royale » pour A♥K♥, « tirage couleur » pour un tirage quinte,
   joueurs couchés avant UTG). C'est le principe de `REFONTE.md` (section 2, point 4) : la présentation est un
   gabarit. Le modèle ne produit plus que `position`, `cartes`, `board`, `pot` et `a_payer`.
3. **La position est tirée par le code** et imposée par le schéma ; la liste « déjà dans la banque » n'est plus
   montrée au modèle : il la recopiait (3 refus de suite pour doublon, puis repli).

Mesure sur 6 générations après correction : en ouverture, 3 situations sur 3 valides au 1er essai (7 à 9 s) ; en
tirage, 2 sur 3 réussies au 3e essai (24 à 27 s), 1 passée par le repli. Le refus « pas de tirage couleur ou
quinte » est le plus fréquent.

Pistes suivantes :

- Dans le message de refus, expliquer comment corriger (« 4 cartes de même couleur, ou 4 hauteurs qui se
  suivent »), pour que le modèle réussisse mieux le thème tirage.
- Le modèle choisit de petites mises (10 bb dans un pot de 90 bb) : la décision « suivre » devient évidente.
  On peut exiger une mise d'au moins un tiers du pot pour les niveaux intermédiaire et avancé.
