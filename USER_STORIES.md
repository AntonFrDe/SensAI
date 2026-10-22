# User stories de SensAI

Deux user stories par feature retenue (`docs/REFONTE.md`, section 4), au format du sujet : *En tant que…, je
veux…, afin de…*, puis des critères observables. État au 2026-10-22 : ✅ fait et testé, ⚠️ en partie, ⬜ à faire.
Les user stories de l'interface de jeu (table, coach, cotes, suivi des parties) sont dans `docs/FRONTEND.md`.

## B1 : chat CLI, le parcours d'exercices

1. En tant que joueur qui vient de rater une situation, je veux poser des questions de suite au coach, afin de
   comprendre mon erreur sans tout réexpliquer.
   - ✅ La réponse s'affiche au fil de l'eau.
   - ✅ Une deuxième question (« et au bouton ? ») est comprise grâce à l'historique du débrief.
   - ✅ `/reset` efface l'historique du débrief ; `/exercice` en ouvre un neuf.
2. En tant que joueur dont l'ordinateur est hors ligne ou mal configuré, je veux un message clair, afin de savoir
   quoi faire.
   - ✅ Ollama éteint : message « ollama serve », sortie propre.
   - ✅ Modèle absent : la commande `ollama pull` exacte est affichée.
   - ✅ Message vide : refusé, rien n'est envoyé au modèle.

## X4 : questions et formulaires

1. En tant que nouveau joueur, je veux indiquer mon niveau en un choix, afin de recevoir des situations à ma
   portée.
   - ⚠️ La question arrive avec 3 choix : numéros en CLI ✅ ; la liste est servie par l'API, les boutons React
     sont à faire.
   - ✅ Un numéro hors des choix est redemandé.
   - ✅ Le choix est enregistré dans le profil.
2. En tant que joueur en débrief, je veux répondre aux questions de contrôle du coach en un clic, afin de vérifier
   que j'ai compris.
   - ✅ Le coach pose une question avec des choix (outil `poser_question`, « combien d'outs ? 13 / 10 / 8 / 5 »).
   - ✅ Ma réponse lui revient en toutes lettres (« Je réponds : 13 ») et il la corrige.
   - ⚠️ La bonne valeur est dans la référence calculée par le code, que le coach reçoit ; rien ne vérifie encore
     que les choix proposés la contiennent.

## T5 : sortie structurée

1. En tant que joueur qui décrit son expérience avec ses mots, je veux que SensAI en déduise mon niveau, afin de
   ne pas devoir rentrer dans une case.
   - ✅ « Je compte mes outs à chaque main » donne un niveau parmi les trois, avec une raison (`{niveau, raison}`).
   - ✅ Une sortie non conforme au schéma déclenche la question à choix fermés.
   - ✅ Le niveau déduit est affiché et modifiable (`/niveau`).
2. En tant que joueur qui enchaîne les exercices, je veux une fiche courte à la fin de chacun, afin de retenir
   l'essentiel.
   - ✅ La fiche a toujours les mêmes champs (`a_retenir`, `theme_a_revoir`), vérifiés par le code.
   - ✅ Le thème à revoir fait partie de la liste des thèmes connus (ou « aucun »).
   - ✅ La fiche est enregistrée dans le profil. Elle s'écrit à la demande (`/fiche`) : un appel au modèle de plus
     coûte 15 à 40 s sur CPU.

## M1 : profil et sessions

1. En tant que joueur qui revient le lendemain, je veux que SensAI se souvienne de mon niveau, afin de reprendre
   sans répondre à nouveau.
   - ✅ Au lancement (`--pseudo`), le niveau et le nombre d'exercices faits sont affichés.
   - ✅ Le prompt du coach contient le résumé du profil (résultats par thème, thèmes à revoir).
   - ✅ `/niveau` permet d'en changer.
2. En tant que joueur qui se trompe souvent sur le même type de coup, je veux qu'on me le propose plus souvent,
   afin de progresser là où je suis faible.
   - ✅ Les résultats par thème sont enregistrés après chaque décision.
   - ✅ Un thème raté revient plus souvent (jusqu'à 3 fois plus s'il est toujours raté).
   - ✅ `/reprendre` recharge le dernier débrief et son historique.

## T1 : outils MCP

1. En tant que joueur curieux, je veux demander « et si j'avais eu As-Roi ? », afin d'explorer la situation.
   - ✅ Le coach appelle `hand_odds` ou `preflop_open` et l'appel est affiché.
   - ⚠️ Les chiffres de la réponse viennent de l'outil ; qu'il les recopie fidèlement dépend du modèle (mesuré par
     EV1, à faire).
   - ✅ Une carte invalide donne une explication, pas un plantage.
2. En tant que joueur qui tient un carnet, je veux que le coach y note ce que j'ai appris, afin de le relire plus
   tard.
   - ✅ « Note ça dans mon carnet » écrit dans `notes/` via le serveur MCP officiel.
   - ✅ « Qu'est-ce que j'ai noté ? » relit le carnet.
   - ✅ Un chemin hors de `notes/` est refusé par le serveur officiel.

## X1 : interface web

1. En tant que joueur qui préfère la souris, je veux faire le même parcours dans le navigateur, afin de voir la
   table et les cartes.
   - ⚠️ Niveau, situation, décision et débrief s'enchaînent par l'API (`/api/sessions…`) ✅ ; les écrans React
     sont à faire.
   - ✅ Le débrief arrive au fil de l'eau (NDJSON).
   - ✅ Seules les actions possibles sont proposées (`actions` de la situation) ; une autre est refusée (400).
2. En tant qu'équipe de développement, je veux que le web et le CLI partagent le même cœur, afin qu'un correctif
   profite aux deux.
   - ⬜ Les mêmes situations et verdicts sortent du CLI et du web pour une même graine (le web n'a pas encore de
     graine).
   - ✅ Les routes du parcours n'appellent que `trainer.py`.
   - ✅ Les tests du parcours passent sans navigateur (`test_trainer.py`, `test_web.py`).

## EV1 : évaluation (bonus)

1. En tant qu'équipe, je veux mesurer à chaque changement de prompt si le coach contredit la référence, afin de ne
   pas régresser sans le voir.
   - ⬜ `python3 evaluate.py` produit un score sur un jeu de situations (aujourd'hui : sur des questions).
   - ⬜ Chaque contradiction est listée avec la situation.
   - ⬜ Le juge est un modèle d'une autre famille que le coach.
2. En tant que joueur, je veux savoir que les chiffres du coach sont vérifiés, afin de lui faire confiance.
   - ⬜ Le README affiche le dernier score et sa date.
   - ⬜ Les situations ratées par l'évaluation servent de tests.
   - ⬜ Le score est versionné dans `evaluation/`.
