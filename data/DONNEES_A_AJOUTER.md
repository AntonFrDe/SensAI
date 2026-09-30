# Données à ajouter pour enrichir le raisonnement de l'IA

But : un coach de poker (Texas Hold'em) qui répond juste, en français, et qui explique ses décisions.
État au 2026-09-21. Provenance des données déjà présentes : voir `SOURCE.md`.

Le catalogue du sujet note qu'il vaut mieux peu de features bien intégrées qu'un empilement : cette liste
est un **menu**, pas un plan. Chaque ligne dit quelle erreur elle corrige, d'où elle vient, et quelle feature
du catalogue la consomme.

## 1. Ce qu'on a déjà, et ses limites

| Fichier | Contenu | Limite |
|---|---|---|
| `preflop_rfi.json` | Ouverture (RFI) en 6-max à 100bb, pour UTG, MP, CO, BTN, SB | Seulement l'ouverture : rien pour répondre à une relance |
| `poker_glossary.json` | 327 entrées en français (313 du lexique, 14 abréviations de chat) | Pas de combinaisons de mains ; recherche anglais → français seulement |

## 2. Les erreurs observées, et la donnée qui les corrige

Question posée aux quatre modèles : « Quelle est la meilleure main au poker ». Bonne réponse : la quinte flush royale.

| Erreur | Modèle | Donnée manquante |
|---|---|---|
| « un carré (four flush) », « quinte (five of a kind) » | gemma3:4b | D1, D2 |
| « la paire est la meilleure main » ; full mal défini | llama3.2:3b | D1 |
| « du 10 au roi » au lieu de « jusqu'à l'as » ; « rosette » pour la dame | qwen3 instruct | D1, D2 |
| Bonne réponse mais 2 208 tokens de réflexion | qwen3:4b | D8 |
| Personne ne demande « meilleure main de départ ou meilleure combinaison ? » | tous | D3, D8 |

## 3. Vue d'ensemble

| ID | Donnée | Priorité | Feature du catalogue | Source | Effort (estimation) |
|---|---|---|---|---|---|
| D1 | Hiérarchie des combinaisons, français/anglais | 1 | T1 (outil), R1 | À recopier | 30 min |
| D2 | Index inverse français → anglais du glossaire | 1 | R1 | Dérivable du glossaire + D1 | 1 h |
| D3 | Surnoms de mains → notation (`cowboys` = `KK`) | 1 | T1 | Dérivable du glossaire | 30 min |
| D4 | Jeu d'évaluation (30 à 50 questions vérifiées) | 1 | EV1 | À écrire | 2 h |
| D5 | Ranges face à une relance, 3-bet, 4-bet | 2 | T1 | Déjà téléchargeable | 1 à 2 h |
| D6 | Équité main contre main | 2 | T1 | À calculer | 2 à 3 h |
| D7 | Cotes du pot et outs | 2 | T1 | Formules standard | 1 h |
| D8 | Cadre de raisonnement (checklist de décision) | 2 | A1, T5, A7 | À rédiger | 1 h |
| D9 | Positions et ordre de parole | 2 | R1 | Règles standard | 30 min |
| D10 | Zones de M et profondeur de tapis | 3 | T1 | Dans le glossaire (texte) | 30 min |
| D11 | Décisions de solveur (PokerBench) | 3 | A7, EV1 | Hugging Face | variable |
| D12 | Profils d'adversaires avec chiffres | 3 | A5, M3 | À sourcer | 2 h |
| D13 | Textures de tableau | 3 | T1 | À coder | 1 h |
| D14 | Règles officielles et étiquette | 3 | R1 | À sourcer | 1 h |
| D15 | Catalogue d'erreurs fréquentes des débutants | 3 | A5, M3 | À rédiger | 1 h |
| D16 | Historiques de mains | 3 | M3, EV2 | Notre moteur, ou à sourcer | variable |
| D17 | Jeu responsable et cadre légal français | 3 | EV2 | À sourcer | 30 min |
| D18 | Autres variantes (Omaha, Stud, Razz) | 4 | R1 | Le glossaire les cite sans règles | à éviter |

## 4. Détail

### Priorité 1 : corrige des erreurs déjà vues

**D1. Hiérarchie des combinaisons.** Les 10 combinaisons, de la quinte flush royale à la carte haute, avec le
nom français, le nom anglais, une description et un exemple. Le glossaire n'a **aucune** de ces entrées :
« carré », « quinte » et « brelan » n'y apparaissent qu'à l'intérieur d'autres définitions.
Format proposé : `hand_rankings.json` `{rang, fr, en, description, exemple}`. Usage : outil `compare_hands`
plus prompt. Ce n'est pas au modèle de décider quelle main bat l'autre.

**D2. Index inverse.** Aujourd'hui `define("Quads")` donne « Carré », mais chercher « carré » ne trouve rien.
À construire depuis les définitions du type « Quads – Carré. », « Straight – Quinte. », « Set – Brelan. »,
« Boat – Bateau… », complétées par D1. Format proposé : un champ `fr` par entrée, ou `translations.json`.

**D3. Surnoms de mains.** Le glossaire donne 11 surnoms de mains de départ :
American Airlines, Bullets, Rockets = AA ; Big slick (alias Anna Kournikova) = AK ; Cowboys, King-Kong = KK ;
Bitches, Ladies = QQ ; Ducks = 22 ; Kojak = KJ ; Wayne Gretzky = 99.
(« Dead man's hand » et « Roue » sont des mains de 4 et 5 cartes : à part.) Format : `hand_nicknames.json`
`{surnom: notation}`. Effet direct : `hand_range("cowboys")` marcherait.

**D4. Jeu d'évaluation.** 30 à 50 questions avec réponse vérifiée, pour mesurer avant/après. Sources déjà
disponibles : la question « meilleure main » ; la terminologie (D1, D2) ; des décisions de `preflop_rfi.json` ;
des équités calculées (D6). Format : JSONL `{question, attendu, type_de_test}`. Sans lui, impossible de dire
si un changement de prompt, de modèle ou de données améliore quelque chose.

### Priorité 2 : donne au modèle de quoi raisonner

**D5. Ranges face à une action.** Vérifié dans la source déjà téléchargée (`pekarstas.ts`, 46 charts, dont
seulement les 5 RFI sont utilisés) : 13 « défense face à une ouverture », 15 « face à une 3-bet »,
13 « face à une 4-bet ». La source `greenline.ts` ajoute 5 charts d'isolation face aux limpeurs.
Cellules à 4 actions (fold, call, raise, allin), avec des mixtes. Étendre `hand_range(hand)` avec un argument
de scénario. Limite : un seul format de table (6-max, 100bb) ; rien pour d'autres profondeurs de tapis ni pour le 9-max.

**D6. Équité.** Probabilité de gagner main contre main, ou main contre range. Pas de source externe : à
calculer avec un évaluateur de mains (énumération ou Monte Carlo). Cas de validation tiré du glossaire :
AK assortis contre 88 est un « coin flip » à environ 48 % contre 52 %.
Format : `equity_preflop.json` (169 mains) plus une fonction `equity(main1, main2, tableau)`.

**D7. Cotes et outs.** Cote du pot = mise à payer / (pot + mise à payer) ; nombre d'outs par tirage (couleur,
quinte par les deux bouts, ventrale, deux overcards) ; règle du 2 et du 4 ; espérance de gain (EV). Maths
standard, à mettre en fonctions plutôt qu'en texte : un LLM de 4 milliards de paramètres calcule mal.

**D8. Cadre de raisonnement.** Une checklist courte que le modèle suit avant de répondre : question ambiguë
(meilleure main ou meilleure main de départ ?), position, profondeur de tapis, action précédente, range
adverse, texture du tableau, cotes, plan. Elle structure la boucle ReAct (A1) et la sortie JSON (T5), et
évite les 2 208 tokens de réflexion libre. À rédiger, en s'appuyant sur les notions du glossaire
(range, polarisé, blocker, EV, fold equity).

**D9. Positions.** Table des positions 6-max et 9-max, avec les noms français, et l'ordre de parole avant et
après le flop. Le glossaire les décrit en morceaux dispersés (UTG, Hi-jack, Cut-off, Bouton, SB, BB).
Format : `positions.json`.

### Priorité 3 : enrichissement

**D10. Zones de M.** Le glossaire décrit les seuils en texte : M = tapis / (petite blind + grosse blind + ante) ;
plus de 20 zone verte, 10 à 20 jaune, 5 à 10 orange, 1 à 5 rouge (« push or fold »), moins de 1 critique.
À structurer et à exposer comme fonction `m_ratio`.

**D11. Décisions de solveur : PokerBench.** Vérifié sur Hugging Face le 2026-09-21 : 574 200 exemples,
licence Apache 2.0, article arXiv 2501.08328. Chaque exemple décrit un état de jeu en langage naturel et
l'action optimale calculée par un solveur. Répartition : 60 000 préflop et 500 000 postflop pour
l'entraînement, 1 000 et 10 000 pour le test. En anglais. Les jeux de test peuvent servir d'évaluation (D4),
et un extrait traduit en français peut fournir des exemples pour le prompt (A7).

**D12. Profils d'adversaires.** Le glossaire définit TAG, LAG, Nit, Rock, Fish, Calling station, VPIP, mais
sans un seul chiffre. Ajouter des valeurs typiques (VPIP, PFR, agressivité, 3-bet) par profil, **avec leur
source**. À sourcer avant d'écrire quoi que ce soit.

**D13. Textures de tableau.** Sec, humide, apparié, monochrome, connecté. Le glossaire n'en donne que
quelques termes (Dry, Rainbow, Scary board). Plutôt une fonction qui classe un tableau qu'un texte.

**D14. Règles officielles et étiquette.** Le règlement des directeurs de tournoi (TDA) est la référence
habituelle ; licence non vérifiée. Le glossaire couvre déjà une partie de l'étiquette (string bet, slow roll,
angle shooting).

**D15. Erreurs fréquentes.** Scared money, result oriented, calling station, tilt, limp excessif : le
glossaire les définit mais ne donne pas de conseil. À rédiger pour que le coach nomme les défauts du joueur
et les retrouve d'une session à l'autre (mémoire M3).

**D16. Historiques de mains.** Le plus simple : enregistrer les mains jouées contre notre propre moteur
dans SQLite (M3). Des historiques réels de salles nécessiteraient de vérifier leur format et leur licence, et
de retirer les données personnelles (EV2).

**D17. Jeu responsable.** Le texte collé contenait des bandeaux « Jouez de manière responsable ». Pour un
coach, prévoir un message de prévention, la mention 18+ et les organismes d'aide officiels français, à
sourcer (noms et numéros non vérifiés ici). Sert de garde-fou de sortie (EV2).

### Priorité 4

**D18. Autres variantes.** Omaha, Stud, Razz, Hi-Lo : le glossaire les cite sans les expliquer. À n'ajouter
que si le périmètre s'élargit.

## 5. Ce qu'il vaut mieux ne pas ajouter

- Des articles de stratégie copiés depuis des sites : droits incertains, beaucoup de bruit (pubs, liens),
  et le modèle y trouvera des contradictions.
- Des exports de solveurs commerciaux : sous licence payante, très volumineux.
- Toute donnée dont la source n'est pas notée dans `SOURCE.md`.

## 6. Ce qui est vérifié et ce qui ne l'est pas

- **Vérifié le 2026-09-21 :** PokerBench (page Hugging Face) ; les nombres de charts dans `pekarstas.ts` et
  `greenline.ts` ; les 11 surnoms et les seuils de M dans le glossaire.
- **Non vérifié :** les licences de la source des ranges, du règlement TDA et de toute autre source citée
  « à sourcer » ; les noms et numéros des organismes d'aide ; les efforts en heures, qui sont des estimations.
