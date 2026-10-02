# Poker Engine

Ce dossier contient le moteur de poker Texas Hold'em utilisé par le projet.
L'objectif est de séparer clairement la logique de jeu du reste de l'application.

## Rôle du moteur

Le moteur gère :

- la création d'une main,
- la distribution des cartes,
- les mises et les actions légales,
- le passage d'une phase à la suivante,
- la résolution du coup au showdown,
- le partage du pot, y compris les side pots,
- l'historique de main.

Le moteur ne s'occupe pas de l'interface web ni du raisonnement IA.
Il expose seulement un état de jeu et des actions de poker.

## Fichiers principaux

- `game.py` : orchestration d'une main, actions de jeu, distribution du pot.
- `game_state.py` : état courant de la table, des phases, du pot et des cartes communes.
- `player.py` : représentation d'un joueur, de son stack, de sa main et de ses mises.
- `card.py` : cartes, couleurs et valeurs.
- `deck.py` : paquet de cartes et pioche.
- `hand_evaluator.py` : évaluation et comparaison des mains de poker.
- `action.py` : enum des actions possibles.

## Déroulé d'une main

Le moteur suit la séquence suivante :

1. préflop
2. round de mise
3. flop
4. round de mise
5. turn
6. round de mise
7. river
8. round de mise
9. showdown

La classe `Game` déclenche automatiquement la street suivante quand une ronde de mise est terminée.

## Actions disponibles

Le moteur permet :

- fold
- check
- call
- bet
- raise
- all in

Chaque action vérifie si elle est légale dans le contexte courant.
Par exemple :

- un check est interdit face à une mise,
- un bet est interdit si une mise existe déjà,
- un raise doit respecter le minimum autorisé,
- un joueur ne peut agir que s'il est le joueur courant.

## Résolution du coup

Au showdown, le moteur :

- récupère les joueurs encore en course,
- compare leurs mains avec `HandEvaluator`,
- attribue le pot au meilleur joueur,
- partage le pot en cas d'égalité,
- gère le jeton impair selon l'ordre à partir du bouton,
- gère les side pots quand les contributions diffèrent,
- attribue le pot restant si tous les autres joueurs ont fold.

## Side pots

Les side pots sont construits à partir des contributions cumulées de chaque joueur pendant la main.
Cela permet de gérer les cas où un joueur est all in avec moins de jetons que les autres.

Chaque niveau de contribution forme un pot distinct.
Seuls les joueurs encore éligibles pour ce niveau peuvent le gagner.

## Historique de main

Le moteur conserve un historique de main dans `GameState`.

Cet historique enregistre notamment :

- le début de la main,
- les blinds,
- les actions des joueurs,
- la distribution des streets,
- la résolution finale du pot.

L'historique est vidé au début d'une nouvelle main.

## Interactions avec l'IA et l'interface web

Le moteur reste indépendant de l'IA et de l'interface web.

En pratique :

- l'IA peut lire un résumé de l'état de la main ou l'historique,
- le backend web peut afficher l'état courant,
- le moteur reste la source de vérité pour les règles du poker.

Cette séparation rend l'intégration plus simple :

- le moteur calcule,
- le backend orchestre,
- l'interface affiche.

## Tests

La suite de tests du dossier couvre :

- la distribution des cartes,
- les phases de jeu,
- les actions légales et illégales,
- la comparaison de mains,
- le showdown,
- les égalités,
- les side pots,
- l'historique de main.

Pour lancer les tests :

```bash
python3 -m pytest poker_engine/tests -q
```

## Point important

Le moteur est volontairement écrit pour rester lisible.
L'idée est que chaque brique soit simple à comprendre et simple à brancher au reste du projet.