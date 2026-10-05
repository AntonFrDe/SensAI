# Frontend poker — Nikita

## Choix technique

- React pour composer les vues et actualiser la table à partir du Game State.
- TypeScript pour typer les cartes, les joueurs et les actions échangées.
- Vite pour lancer le serveur de développement et construire les fichiers statiques.
- CSS natif pour le responsive et les visuels, sans bibliothèque UI initiale.

## Organisation prévue

- `frontend/` contiendra le projet, ses dépendances et ses composants.
- Trois vues principales : accueil, partie et analyse après la main.
- Composants de partie : table, cartes, stacks, pot et commandes du joueur.
- Le frontend transmettra les actions au backend et affichera son état de jeu.
- Le moteur Python restera responsable des règles et des actions autorisées.
- Le backend devra exposer le Game State via une API JSON à définir avec l'équipe.

## Prochaine étape
Initialiser le projet Vite avec React et TypeScript dans `frontend/`.
