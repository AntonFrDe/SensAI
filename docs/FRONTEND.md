# Frontend poker — Nikita

Interface web de SensAI (feature X1 du sujet) : une table de Texas Hold'em en tête-à-tête contre l'IA, avec le
coach, des repères chiffrés et des outils pour revoir ses mains. Le frontend affiche et envoie des actions ; les
règles, les montants légaux et tous les chiffres viennent du backend Python.

## Lancer

```
python3 server.py                          # API sur http://127.0.0.1:8000
cd frontend && npm install && npm run dev  # http://localhost:5173, Vite relaie /api vers le port 8000
```

Sans Ollama, la partie reste jouable : l'IA joue avec sa règle de secours et l'écran d'accueil dit quel modèle
manque (voir « État de l'IA locale »). `SENSAI_API=http://127.0.0.1:<port> npm run dev` relaie vers un autre
backend.

## Choix techniques

| Choix | Pourquoi | Écarté |
|---|---|---|
| React 19 + TypeScript strict | Composer la table à partir de l'état renvoyé par le serveur ; types partagés pour les cartes, les actions et l'état | JavaScript sans types : l'état de partie a plus de 20 champs |
| Vite | Démarrage instantané, proxy `/api` intégré, build statique | Create React App (abandonné), Next.js (pas besoin de rendu serveur) |
| CSS natif, un seul `styles.css` | Peu de composants, aucun besoin d'une bibliothèque ; attributs `data-*` pour les préférences | Tailwind, bibliothèques UI : dépendances et style générique |
| Vitest + Testing Library | Même configuration que Vite, tests au niveau de ce que voit l'utilisateur (rôles, libellés) | Jest : configuration en double |
| Playwright 1.63 | Parcours complets dans Chromium contre le vrai `server.py` et le faux Ollama | Cypress : plus lourd, un navigateur de plus à installer |
| Aucun framework LLM | Exigé par le sujet : le frontend ne parle qu'au backend, qui parle à Ollama en HTTP | — |

## Organisation de `frontend/src`

Un composant par fichier `PascalCase.tsx`, son type `XxxProps` exporté avec lui ; la logique sans affichage est
dans des modules `camelCase.ts` testés à part. Tous les appels HTTP sont dans `api.ts`.

| Écran ou zone | Composants | Logique |
|---|---|---|
| Accueil | `HomeScreen` (blindes, tapis de départ, reprise de partie), `ServerStatus`, `PreferencesPanel` | `savedGame.ts`, `preferences.ts` |
| Table | `PokerTable`, `Seat`, `PlayingCard`, `CommunityCards`, `HandInfo`, `HandBadge`, `OpponentNote`, `Term` | — |
| Actions | `ActionControls` (boutons, montant, curseur, montants rapides, raccourcis) | `betSizing.ts`, `shortcuts.ts` |
| Colonne de droite | `CoachPanel` (chat), `OddsPanel` (repères), `SessionStats` | `sessionStats.ts` |
| Après les mains | `HandHistory`, `HandLog`, `HandReplay`, `StackChart`, `GameSummary` | `handTracking.ts`, `handLog.ts`, `handExport.ts` |
| Pages d'aide | `GlossaryScreen`, `HandRankings`, `Banque` (situations générées, partie d'Anton) | — |

`App.tsx` tient la partie en cours, envoie les actions et demande à l'IA de jouer quand c'est son tour.
`useHandTracking` détecte la fin de chaque main (passage à l'abattage) ; les statistiques et le journal des mains
s'y abonnent, ce qui évite deux détections différentes.

## Contrat avec le backend

Toutes les routes sont dans `server.py` ; l'état public de la partie est construit par `poker_api.py`. Champs
JSON en camelCase.

| Route | Rôle |
|---|---|
| `POST /api/games` `{options: {blinds, stackBigBlinds}}` | Nouvelle partie (blindes `5/10`, `10/20` ou `25/50`, tapis de 20 à 500 grosses blindes) |
| `POST /api/state` `{gameId}` | Relire une partie, pour la reprendre après un rechargement |
| `POST /api/actions` `{gameId, action, amount?}` | Jouer une action légale ; montant total pour `bet` et `raise` |
| `POST /api/opponent` `{gameId}` | Faire jouer l'IA quand c'est son tour |
| `POST /api/next-hand` `{gameId}` | Main suivante, une fois la main finie |
| `POST /api/odds` `{gameId}` | Cote du pot, équité contre une main au hasard (`equity.py`), outs (`odds.py`) |
| `POST /api/coach` `{gameId, messages?}` | Conseil en streaming NDJSON ; `messages` = suite de la conversation |
| `GET /api/status` | Ollama joignable, modèles du coach et de l'adversaire installés ou non |
| `GET /api/glossary`, `GET /api/glossary?term=` | Glossaire complet ou définition d'un terme |
| `GET /api/hand-rankings` | Les dix combinaisons, avec un exemple en cartes |

L'état d'une partie contient en plus des cartes, du pot et des tapis : `controls` (actions légales, bornes de
mise, `toCall`), `seats` (mise du tour, couché, tapis, donneur, blinde), `blinds`, `history` (actions publiques
par street), `awards`, `hands` (meilleure main de 5 cartes de chaque joueur dévoilé, calculée par l'évaluateur
du moteur) et `gameOver`. Les cartes de l'IA ne sont envoyées qu'à l'abattage.
