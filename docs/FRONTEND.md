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
| `POST /api/notes` `{hands, won, net, remark?}` | Ajoute une ligne de bilan à `notes/sessions.md`, que le coach CLI lit par le serveur MCP de fichiers |
| `GET /api/status` | Ollama joignable, modèles du coach et de l'adversaire installés ou non |
| `GET /api/glossary`, `GET /api/glossary?term=` | Glossaire complet ou définition d'un terme |
| `GET /api/hand-rankings` | Les dix combinaisons, avec un exemple en cartes |

L'état d'une partie contient en plus des cartes, du pot et des tapis : `controls` (actions légales, bornes de
mise, `toCall`), `seats` (mise du tour, couché, tapis, donneur, blinde), `blinds`, `history` (actions publiques
par street), `awards`, `hands` (meilleure main de 5 cartes de chaque joueur dévoilé, calculée par l'évaluateur
du moteur) et `gameOver`. Les cartes de l'IA ne sont envoyées qu'à l'abattage.

## Le code calcule, l'interface affiche

- Les actions possibles et les bornes de mise viennent de `poker_api.player_controls` ; les montants rapides
  (½ pot, ¾ pot, pot, tapis) sont seulement des raccourcis ramenés dans ces bornes.
- Le nom des mains, les cartes de la meilleure main, l'équité et les outs sont calculés en Python ; le frontend
  ne les recalcule jamais.
- Le verdict du panneau « Repères » compare deux nombres du serveur (équité et cote du pot) ; aucun chiffre
  n'est produit par le modèle.

## Accessibilité et confort

- Chaque carte a un nom lisible (« Q de cœur, dans la meilleure main ») ; la table, les sièges et les panneaux
  sont des régions nommées ; les changements (tour, pot, conseil) sont annoncés par des zones `aria-live`.
- Clavier : F se coucher, C checker ou suivre, R miser ou relancer (sinon aller au montant), T préparer un tapis,
  Entrée dans le champ du montant ; flèches et Échap dans le revoir d'une main et dans la courbe du tapis.
- Courbe du tapis : une seule série, ligne de 2 px, repère du tapis de départ, info-bulle au survol et au
  clavier, tableau des valeurs pour qui ne lit pas le graphique.
- Préférences : thème clair, jeu à quatre couleurs (♦ bleu, ♣ vert), grandes cartes, animations coupées ;
  `prefers-reduced-motion` est aussi respecté.
- Mise en page sur une colonne sous 600 px, cibles tactiles de 44 px.

## Tests

```
cd frontend && npm run build      # tsc --noEmit + build Vite
cd frontend && npm test           # Vitest : composants et logique, fetch simulé
cd frontend && npm run test:e2e   # Playwright : parcours complets dans Chromium
```

Les tests Vitest sont à côté du code (`Xxx.test.tsx`). Les tests de bout en bout (`e2e/game.spec.ts`) lancent
`e2e/e2e_server.py` : `server.py` sur le port 8791, branché sur `fake_ollama.py`, et Vite sur le port 5191.
Côté Python, `test_poker_api.py` couvre l'état public, les options de partie, les mains, les repères et le
classement des mains ; `test_web.py` couvre les routes.

## Limites connues

- Le moteur fait du donneur la grosse blinde en tête-à-tête et autorise une mise de 1 jeton après le flop :
  ce sont des règles de `poker_engine/` (Alexandre), affichées telles quelles.
- L'équité est calculée contre une main au hasard, pas contre la range probable de l'IA.
- Une partie vit en mémoire du serveur : redémarrer `server.py` la perd, la reprise ne marche qu'avec le même
  serveur.
- Les statistiques « depuis toujours » et les préférences sont dans le `localStorage` du navigateur.

## User stories de l'interface (X1)

Format du sujet : *En tant que…, je veux…, afin de…*, puis des critères observables. Chaque critère est vérifié
par un test Vitest, un test Playwright ou un essai dans le navigateur.

**Table et actions**

1. En tant que joueur débutant, je veux ne voir que les actions permises, afin de ne jamais tenter un coup
   illégal.
   - Les boutons des actions interdites sont grisés ; « Call » affiche la somme à payer.
   - Un montant hors des bornes du serveur grise « Bet » et « Raise ».
   - L'IA ne peut pas être interrompue : pendant son tour, tous les boutons sont grisés.
2. En tant que joueur, je veux choisir une mise en un clic, afin de ne pas calculer « trois quarts du pot » de tête.
   - Les boutons Min, ½ pot, ¾ pot, Pot et Tapis remplissent le montant, toujours dans les bornes.
   - Le curseur et le champ restent synchronisés ; le bouton affiche « Raise à 120 » ou « Raise tapis ».
   - Le montant se vide quand les bornes changent d'un tour à l'autre.
3. En tant que joueur au clavier, je veux jouer sans souris, afin d'enchaîner les mains vite.
   - F, C, R et T jouent ou préparent l'action ; Entrée dans le champ mise le montant.
   - Une lettre tapée dans une question au coach ne déclenche aucune action.

**Lecture de la table**

1. En tant que joueur, je veux voir qui est donneur, qui a payé les blindes et combien chacun a misé, afin de
   comprendre le pot.
   - Badges D, SB et BB sur les sièges ; mise du tour devant chaque joueur ; « Couché » et « Tapis » affichés.
   - Le joueur qui doit parler est encadré et annoncé.
2. En tant que débutant, je veux savoir quelle main j'ai, afin d'apprendre les combinaisons en jouant.
   - Dès le flop, le nom de ma main s'affiche (« Double paire ») et ses 5 cartes sont mises en évidence.
   - À l'abattage, la main gagnante de l'IA est mise en évidence et nommée dans le résultat.
   - « Pot », « Stack », « Flop », « Turn » et « River » ouvrent leur définition du glossaire.

**Coach et repères**

1. En tant que joueur qui doute, je veux discuter de ma décision avec le coach, afin de comprendre le conseil.
   - Le conseil s'affiche au fil de l'eau ; « Arrêter » coupe la réponse et garde ce qui est écrit.
   - Une question de suite (« Et si je relance ? ») est envoyée avec la conversation.
   - Une erreur du modèle s'affiche et « Redemander » relance.
2. En tant que joueur, je veux des chiffres sûrs pour décider, afin de ne pas dépendre d'un modèle qui se trompe
   en calcul.
   - « Repères » affiche la somme à payer, la cote du pot, l'équité et les outs, calculés par le serveur.
   - Le verdict compare l'équité à la cote ; « À chaque décision » recalcule seul à chaque tour.

**Suivi de la partie**

1. En tant que joueur, je veux revoir une main finie étape par étape, afin de retrouver le moment où j'ai perdu.
   - « Mains précédentes » liste chaque main avec mes cartes, ma combinaison et le gain ou la perte.
   - « Revoir » montre le board street par street ; les cartes de l'IA n'apparaissent qu'à la fin.
   - Les mains s'exportent en texte ou en JSON.
2. En tant que joueur, je veux suivre mes résultats, afin de savoir si je progresse.
   - « Statistiques » compte les mains, gagnées, perdues, partagées, les abattages, le bilan et les séries.
   - « Depuis toujours » survit à la fermeture du navigateur ; sa remise à zéro demande une confirmation.
   - « Ajouter à mes notes » écrit une ligne datée dans `notes/sessions.md`, avec ce que je retiens.
   - La courbe du tapis et le bilan de fin de partie montrent l'évolution main après main.

**Accueil et confort**

1. En tant que joueur, je veux choisir la taille de la partie, afin de m'entraîner court ou profond.
   - Blindes 5/10, 10/20 ou 25/50 ; tapis de 20 à 500 grosses blindes, refusé au-delà, par l'écran et le serveur.
   - Les options choisies sont retenues pour la partie suivante.
2. En tant que joueur qui a rechargé la page, je veux reprendre ma partie, afin de ne pas perdre mes jetons.
   - « Reprendre la partie » rend les mêmes cartes et les mêmes tapis.
   - Une partie que le serveur ne connaît plus est oubliée sans message d'erreur.
3. En tant que joueur dont Ollama n'est pas prêt, je veux savoir ce qui manque, afin de le réparer seul.
   - L'accueil dit si Ollama répond et si les modèles du coach et de l'adversaire sont installés.
   - La commande `ollama pull` exacte se copie en un clic.
4. En tant que joueur qui voit mal certaines couleurs, je veux adapter l'affichage, afin de lire les cartes.
   - Jeu à quatre couleurs, grandes cartes, thème clair et animations coupées, retenus d'une visite à l'autre.
