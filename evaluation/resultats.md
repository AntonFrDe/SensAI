# Résultats de l'évaluation

Modèle : `qwen3:4b-instruct-2507-q4_K_M` — 2026-10-05 15:41 — **18/33 réussies** (55%)

Fichier généré par `python3 evaluate.py` : ne pas modifier à la main. Le verdict est donné par le modèle lui-même, à relire.

| Réussi | # | Thème | Question | Différences relevées par le modèle |
|:---:|---|---|---|---|
| ☑ | q01 | combinaisons | Quelle est la meilleure main au poker ? | — |
| ☑ | q02 | combinaisons | Est-ce qu'une couleur bat un full ? | — |
| ☑ | q03 | combinaisons | Qu'est-ce qui est le plus fort : une quinte ou un brelan ? | — |
| ☑ | q04 | combinaisons | Entre une double paire et un brelan, quelle main gagne ? | — |
| ☑ | q05 | combinaisons | L'as peut-il servir dans une quinte basse ? | — |
| ☐ | q06 | combinaisons | Si deux joueurs ont exactement la même main, la couleur (pique, cœur...) les départage-t-elle ? | Le pot est partagé : absent |
| ☑ | q07 | combinaisons | Qu'est-ce que le kicker ? | — |
| ☑ | q08 | règles | Combien de cartes reçoit chaque joueur au Texas Hold'em, et comment forme-t-on sa main ? | — |
| ☑ | q09 | règles | Dans quel ordre sont dévoilées les cartes communes ? | — |
| ☑ | q10 | règles | Que sont les blindes ? | — |
| ☑ | q11 | règles | Qui parle en premier avant le flop, et après le flop ? | — |
| ☐ | q12 | règles | En no-limit, quelle est la relance minimum quand un joueur a misé 10 ? | La relance minimum est à 20 : absent |
| ☑ | q13 | règles | Qu'est-ce qu'un side pot ? | — |
| ☑ | q14 | position | Pourquoi le bouton est-il la meilleure position ? | — |
| ☐ | q15 | vocabulaire | Que veut dire avoir les « nuts » ? | Cela dépend des cartes du board : absent |
| ☐ | q16 | vocabulaire | Qu'est-ce qu'un set ? | Il est formé avec une paire en main et une carte du board : absent |
| ☐ | q17 | vocabulaire | Qu'est-ce qu'un tirage ventral (gutshot) ? | Il a 4 outs : absent |
| ☑ | q18 | vocabulaire | Qu'est-ce qu'un check-raise ? | — |
| ☑ | q19 | vocabulaire | Que veut dire « limper » ? | — |
| ☑ | q20 | vocabulaire | Que veut dire être « en tilt » ? | — |
| ☑ | q21 | vocabulaire | Qu'est-ce qu'un joueur TAG ? | — |
| ☐ | q22 | préflop | En 6-max à 100bb, premier à parler, faut-il ouvrir 7-2 dépareillés (72o) depuis UTG ? | Non, on se couche avec 72o à UTG : contredit |
| ☐ | q23 | préflop | En 6-max à 100bb, premier à parler, depuis quelles positions ouvre-t-on Roi-9 assortis (K9s) ? | On ouvre K9s depuis MP, CO, le bouton et la petite blinde : absent ; On se couche avec K9s à UTG : absent |
| ☐ | q24 | préflop | En 6-max à 100bb, premier à parler, ouvre-t-on Dame-Valet dépareillés (QJo) depuis UTG ? | Non, on se couche avec QJo à UTG : contredit |
| ☐ | q25 | équité | Avant le flop, quelle est l'équité d'une paire d'As contre une main au hasard ? | L'équité d'une paire d'As contre une main au hasard est d'environ 85 % : contredit |
| ☐ | q26 | équité | Avant le flop, As-Roi assortis contre une paire de 8 : qui est favori ? | La paire de 8 est légèrement favorite : absent ; Environ 52 % contre 48 % : contredit |
| ☐ | q27 | équité | Avant le flop, paire de Rois contre paire de Dames : quelles chances pour chacun ? | Les Rois gagnent environ 82 % du temps : absent ; Les Dames environ 18 % : absent |
| ☑ | q28 | outs | J'ai Ah Kh, le flop est Qh 7h 2c. Combien ai-je d'outs ? | — |
| ☐ | q29 | outs | J'ai 8h 9d et le flop est 7c 6s 2h. Combien d'outs pour la quinte ? | 8 outs pour la quinte : absent ; Les quatre 5 et les quatre 10 : contredit |
| ☐ | q30 | outs | Avec un tirage couleur au turn (9 outs), quelle chance de toucher à la river ? | Environ 19,6 % (9 sur 46), ou environ 18 % avec la règle du 2 : absent |
| ☐ | q31 | outs | Qu'est-ce que la règle du 2 et du 4 ? | Au flop, outs × 4 donne la chance de toucher d'ici la river : absent ; Au turn, outs × 2 donne la chance de toucher à la river : absent |
| ☐ | q32 | cote du pot | Le pot est de 100 (mise adverse comprise) et je dois payer 50. Quelle équité minimum faut-il pour suivre ? | Il faut au moins 33,3 % d'équité (50 / 150) : absent |
| ☑ | q33 | décision | J'ai As Ad, le flop est Kc 7d 2s. Le pot est de 90 avec la mise adverse et je dois payer 30. Que faire ? | — |

## Détail

### ☑ q01 — Quelle est la meilleure main au poker ?

**Référence :** La quinte flush royale : As, Roi, Dame, Valet et 10 de la même couleur.

**Réponse du modèle :**

> - (Action à faire) : Ne rien faire (attendre une meilleure main)  
> - (Combien miser) : 0  
> - (Pourquoi) : La meilleure main au poker est la **quinte flush royale** (As, Roi, Dame, Valet, 10 de la même couleur), force 10/10. C’est la combinaison la plus forte selon le classement officiel. Toutefois, dans une partie en cours, il est préférable de ne pas miser si on n’a pas cette main. Aucun calcul d’équité ou de cote n’est nécessaire ici car la question est purement descriptive.

*1.9 s*

### ☑ q02 — Est-ce qu'une couleur bat un full ?

**Référence :** Non. Le full (un brelan et une paire) bat la couleur.

**Réponse du modèle :**

> - Oui  
> - 6/10 vs 7/10  
> - Une couleur (6/10) n’emporte pas un full (7/10) → le full bat la couleur.  
> → Réponse : **Non, une couleur ne bat pas un full.**

*1.1 s*

### ☑ q03 — Qu'est-ce qui est le plus fort : une quinte ou un brelan ?

**Référence :** La quinte bat le brelan.

**Réponse du modèle :**

> - (Action à faire) : Une quinte est plus forte qu’un brelan  
> - (Combien miser) : 0 (pas applicable ici)  
> - (Pourquoi) : D’après le classement, une quinte (force 5/10) est au-dessus d’un brelan (force 4/10).  
> → Cote du pot : N/A (question de force de combinaison, pas de décision de mise)  
> → Équité : 5 > 4 → quinte > brelan ✅

*1.7 s*

### ☑ q04 — Entre une double paire et un brelan, quelle main gagne ?

**Référence :** Le brelan bat la double paire.

**Réponse du modèle :**

> - (Action à faire) : Le brelan gagne  
> - (Combien miser) : 0 (pas de mise à faire)  
> - (Pourquoi) : D'après le classement, le brelan (force 4/10) est supérieur à la double paire (force 3/10). Aucun calcul d'équité ou d'outs n'est nécessaire ici, car c'est une comparaison directe de forces de mains.

*1.5 s*

### ☑ q05 — L'as peut-il servir dans une quinte basse ?

**Référence :** Oui : A-2-3-4-5 (la « roue ») est la plus petite quinte. Une quinte ne peut pas « tourner » : Dame-Roi-As-2-3 n'est pas une quinte.

**Réponse du modèle :**

> - Oui  
> - 0  
> - Une quinte basse est une suite de cinq cartes consécutives, comme 5-4-3-2-A. L'as peut servir dans une quinte basse **seulement si** elle est au début (A-2-3-4-5), car les as ne peuvent pas être utilisés comme "carte haute" dans une suite qui commence à partir de 2.  
> → L'as **peut** être dans une quinte basse **si** elle est au début (A-2-3-4-5), mais **ne peut pas** être dans une quinte basse qui commence après l'as (ex : 6-7-8-9-10).  
> → En pratique, les quintes basse ne sont pas définies avec l'as comme élément central.  
> → Donc, **l'as peut servir dans une quinte basse**, **seulement dans A-2-3-4-5**, ce qui est une quinte basse valide.  
> → Cela ne change pas le classement : A-2-3-4-5 est une quinte, force 5/10, comme toute autre quinte.  
> → Aucun calcul d'équité ou d'outs n'est nécessaire ici.  
> 
> ✅ Réponse normalisée :  
> - (Oui)  
> - (0)  
> - (L'as peut servir dans une quinte basse seulement dans A-2-3-4-5, qui est une quinte valide, force 5/10.)

*4.2 s*

### ☐ q06 — Si deux joueurs ont exactement la même main, la couleur (pique, cœur...) les départage-t-elle ?

**Référence :** Non. Au Texas Hold'em aucune couleur n'est plus forte qu'une autre : le pot est partagé à égalité.

**Réponse du modèle :**

> - Non  
> - 0  
> - Non, la couleur ne départage pas les mains si elles sont identiques en valeur. Le classement se fait par la force de la combinaison, pas par la couleur des cartes. Si les mains sont identiques (même valeur, même couleur), elles sont égales. La couleur n’a pas d’effet sur le classement dans ce cas.

*1.4 s*

### ☑ q07 — Qu'est-ce que le kicker ?

**Référence :** La carte d'accompagnement qui départage deux mains de même combinaison. Exemple : sur un board A-7-2, AK bat AQ grâce au kicker Roi.

**Réponse du modèle :**

> - (Définition)  
> Le kicker est la carte la plus forte dans une main qui n’a pas formé une combinaison (comme une paire ou un brelan), ou qui complète une combinaison en cas d’égalité.  
> Exemple : si deux joueurs ont une paire de 9, le kicker est la carte la plus haute (ex : 10 > 8), qui détermine le gagnant.  
> 
> → C’est la carte la plus forte **en dehors** de la combinaison principale.  
> → Utilisé pour briser l’égalité.  
> 
> (SensAI : le kicker n’est pas une action, il est un élément de la main. Il ne s’applique pas dans une décision en jeu. Si tu as une question sur une action à jouer, dis-le.)

*2.5 s*

### ☑ q08 — Combien de cartes reçoit chaque joueur au Texas Hold'em, et comment forme-t-on sa main ?

**Référence :** 2 cartes privées. Avec les 5 cartes communes, on garde la meilleure main de 5 cartes parmi les 7.

**Réponse du modèle :**

> - 2 cartes (les "hole cards")  
> - Sa main est formée à partir de ses 2 cartes + les 5 cartes communes (community cards) sur le tableau  
> - On choisit les 5 cartes les plus fortes parmi les 7 cartes disponibles (2 privées + 5 publiques) pour évaluer sa combinaison.

*1.4 s*

### ☑ q09 — Dans quel ordre sont dévoilées les cartes communes ?

**Référence :** Le flop (3 cartes), puis le turn (1 carte), puis la river (1 carte). Il y a un tour d'enchères avant le flop et après chacune de ces étapes.

**Réponse du modèle :**

> - (Dévoiler les cartes communes de gauche à droite, en deux étapes)  
> - (1ère carte : la première carte commune, puis la deuxième)  
> - (Pourquoi : dans le Hold’em, les cartes communes sont dévoilées en deux rounds : la "flop" (3 cartes) puis la "turn" (1 carte), puis la "river" (1 carte). L'ordre est donc : flop → turn → river.)  
> 
> → **Note :** Le contexte ne contient pas de calculs d'équité, d'outs ou de cote du pot, donc aucune estimation n’est requise ici. La réponse est purement basée sur la règle du jeu.

*2.2 s*

### ☑ q10 — Que sont les blindes ?

**Référence :** Des mises obligatoires posées avant la distribution : la petite blinde par le joueur à gauche du bouton, la grosse blinde par le suivant (en général le double de la petite).

**Réponse du modèle :**

> - (Les blindes sont des mises obligatoires placées avant le début d'une manche de poker, sans appel.)  
> - (Elles servent à établir le pot initial et à donner un avantage à chaque joueur.)  
> - (Exemple : en blindes, le petit blind est la mise minimale, le grand blind est le double du petit blind.)  
> 
> → Cela ne concerne pas la décision dans une partie en cours.  
> → La question est d'ordre réglementaire, pas stratégique.  
> 
> **Réponse :** - (Les blindes sont des mises obligatoires au début d'une manche.)

*1.9 s*

### ☑ q11 — Qui parle en premier avant le flop, et après le flop ?

**Référence :** Avant le flop : le joueur à gauche de la grosse blinde (UTG). Après le flop : le premier joueur encore en jeu à gauche du bouton, en général la petite blinde.

**Réponse du modèle :**

> - (Qui parle en premier avant le flop) : Les joueurs plient leurs cartes (pré-flop), puis font leur premier tour d’enchères (blind bets).  
> - (Qui parle après le flop) : Les joueurs font leur second tour d’enchères (flop check/raise), puis le turn, puis le river.  
> 
> 👉 En résumé :  
> - Avant le flop : Pré-flop (blind bets).  
> - Après le flop : Post-flop (check/raise sur flop, turn, river).  
> 
> *Note : Ce n’est pas un calcul d’équité ou de cote, mais une règle de progression de la partie.*

*2.0 s*

### ☐ q12 — En no-limit, quelle est la relance minimum quand un joueur a misé 10 ?

**Référence :** La relance doit ajouter au moins le montant de la mise précédente : il faut relancer à 20 au minimum.

**Réponse du modèle :**

> - (Relancer)  
> - (10)  
> - (En no-limit, la relance minimum est égale à la mise précédente. Ici, le joueur a misé 10, donc la relance minimum est de 10. Aucun calcul d'équité ou d'outs n'est nécessaire ici, car la règle du no-limit impose une relance minimale égale à la mise précédente.)

*1.4 s*

### ☑ q13 — Qu'est-ce qu'un side pot ?

**Référence :** Un pot annexe créé quand un joueur fait tapis avec moins de jetons que les autres : il ne peut gagner que le pot principal, où chacun a mis au plus son tapis ; les mises au-delà forment un pot séparé, disputé par les autres joueurs.

**Réponse du modèle :**

> - (Définition)  
> Un side pot est un pot annexe formé lorsque un joueur est à tapis (sans jetons), et que les autres joueurs continuent à miser. Ce pot n'est pas accessible au joueur à tapis, qui ne peut prétendre qu'au pot initial.  
> 
> - (Pourquoi)  
> Il permet de continuer la partie sans que les joueurs à tapis perdent tout leur investissement dans le pot initial.  
> 
> - (Exemple)  
> Si le pot initial est de 100 € et un joueur a 50 €, il peut mettre 50 € dans le pot initial. Si un autre joueur met 100 €, un side pot de 100 € est créé pour les joueurs encore en jeu. Le joueur à tapis ne peut que jouer dans le pot initial.  
> 
> → Cela ne change pas l'équité, mais permet une continuation de la partie.

*2.7 s*

### ☑ q14 — Pourquoi le bouton est-il la meilleure position ?

**Référence :** Après le flop, le bouton parle en dernier à chaque tour : il voit ce que font les autres avant de décider. On peut donc y jouer plus de mains qu'en début de parole.

**Réponse du modèle :**

> - (Action à faire) : Ne rien faire (attendre les autres joueurs)  
> - (Combien miser) : 0  
> - (Pourquoi) : Le bouton est la meilleure position car il agit *après* tous les autres joueurs, ce qui lui permet de voir leurs actions avant de décider. Cela lui donne une information cruciale sur les forces des adversaires, ce qui améliore son équité de décision.  
> → *Équité* : Il peut évaluer les mains des autres, ajuster ses mises en fonction des agressivités.  
> → *Cote du pot* : Il peut mieux estimer la cote du pot, en tenant compte des mises précédentes.  
> → *Glossaire* : Position de donneur, dernière à parler, info sur les adversaires.

*2.5 s*

### ☐ q15 — Que veut dire avoir les « nuts » ?

**Référence :** Avoir la meilleure main possible à ce moment, compte tenu des cartes du board.

**Réponse du modèle :**

> - (Avoir les « nuts ») = Avoir le meilleur jeu possible, la combinaison la plus forte au moment donné (ex : quinte flush royale, quinte flush, carré, etc.)  
> - (Pourquoi) = Parce que les « nuts » représentent le plus haut classement de combinaison (force 10/10), donc le plus fort possible.  
> → C’est le jeu qui ne peut être dépassé par aucun autre.  
> 
> *Note : Dans le contexte, "nuts" = le meilleur jeu, donc la combinaison la plus forte selon le classement.*

*1.9 s*

### ☐ q16 — Qu'est-ce qu'un set ?

**Référence :** Un brelan formé avec une paire en main et une carte de même valeur sur le board (différent des trips : une seule carte en main et une paire sur le board).

**Réponse du modèle :**

> - (Action à faire) : Expliquer  
> - (Combien miser) : 0  
> - (Pourquoi) : Un set est un brelan (trois cartes de même valeur). Il s'agit d'une combinaison de force 4/10. Cela correspond à la définition donnée dans le glossaire.

*1.2 s*

### ☐ q17 — Qu'est-ce qu'un tirage ventral (gutshot) ?

**Référence :** Un tirage quinte auquel il manque une carte au milieu : une seule valeur le complète, soit 4 outs. Exemple : 9-8 sur 6-5-2, il faut un 7.

**Réponse du modèle :**

> - (Qu'est-ce qu'un tirage ventral ?)  
> Un tirage ventral (gutshot) est un tirage de quinte où vous avez besoin d'une seule carte pour compléter une suite, et cette carte est située au milieu de la suite.  
> Exemple : vous avez 8-9 sur le board, vous avez besoin d’un 10 pour compléter une quinte.  
> → C’est un tirage de quinte avec une seule carte manquante (le "milieu" de la suite).  
> 
> - (Combien miser ?)  
> Aucun montant spécifique — dépend du contexte.  
> 
> - (Pourquoi ?)  
> Car c’est un tirage à faible équité (1 out), donc faible potentiel. Cote du pot > 4 :2, donc en général, on ne mise pas pour un gutshot.  
> Équité : 1 out → 1/47 ≈ 2,1% (cote du pot ~4,7).  
> → Mise très faible ou abdication.  
> 
> ➡️ **Conclusion : - (Ne pas miser ou miser très peu)**  
> → Car c’est un tirage faible, peu de chances, peu d’outs.

*3.4 s*

### ☑ q18 — Qu'est-ce qu'un check-raise ?

**Référence :** Checker, puis relancer quand un adversaire mise après nous, dans le même tour d'enchères.

**Réponse du modèle :**

> - (Action à faire) Check-raise  
> - (Combien miser) 0 (check), puis mise > 0 (relance)  
> - (Pourquoi) C’est un check puis une relance après que l’adversaire ait misé. Cela permet de renforcer sa position, de montrer de la force sans avoir à miser immédiatement, et de pousser l’adversaire à miser plus, ce qui augmente la cote du pot.  
> → C’est une stratégie offensive pour évaluer la force de l’adversaire et maximiser le gain.

*1.9 s*

### ☑ q19 — Que veut dire « limper » ?

**Référence :** Avant le flop, payer seulement la grosse blinde au lieu de relancer.

**Réponse du modèle :**

> - (Action à faire) Limper  
> - (Combien miser) 0 (ou la grosse blinde)  
> - (Pourquoi) Se contenter de payer la grosse blinde au premier tour d’enchères pré-flop, sans miser de plus. Cela permet de rester dans la partie sans risquer de mise supplémentaire.  
> 
> ➡️ *Note : Ce terme est une action de mise minimale, pas une stratégie de jeu. Il n’est pas lié à l’équité, aux outs ou à la cote du pot.*

*1.6 s*

### ☑ q20 — Que veut dire être « en tilt » ?

**Référence :** Être énervé ou déconcentré, souvent après un mauvais coup, et prendre de mauvaises décisions à cause de ses émotions.

**Réponse du modèle :**

> - (Être en tilt = être en colère ou déconcentré après un mauvais coup)  
> - (0)  
> - (C’est un état psychologique qui perturbe la prise de décision, conduisant à des erreurs de jeu, comme miser trop ou trop peu, ou abandonner.)

*1.2 s*

### ☑ q21 — Qu'est-ce qu'un joueur TAG ?

**Référence :** Tight-aggressive : il joue peu de mains, mais il les joue de façon agressive (en misant et en relançant plutôt qu'en suivant).

**Réponse du modèle :**

> - (Un joueur TAG est un joueur serré mais agressif. Il joue peu de mains, mais quand il les joue, il les mise fortement.)  
> - (C’est un type de joueur considéré comme excellent, car il évalue les mains avec précision et agit avec conviction.)  
> - (Il privilégie les mains fortes, évite les mains faibles, et exerce une pression sur l'adversaire par des raises ou bets en position.)

*1.6 s*

### ☐ q22 — En 6-max à 100bb, premier à parler, faut-il ouvrir 7-2 dépareillés (72o) depuis UTG ?

**Référence :** Non, on se couche. 72o ne s'ouvre depuis aucune position : c'est la plus faible main de départ.

**Réponse du modèle :**

> - Oui (ouvrir)  
> - Miser 3bb (environ 30%)  
> - Pourquoi :  
>   - 7-2o est une main dépareillée, faible en équité (force 2/10), mais en position UTG, on doit ouvrir pour élargir la zone de jeu.  
>   - Équité estimée : ~15% (cote du pot : 100bb → 100bb, donc cote ~1:1.5).  
>   - Outs : 0 (pas de carte qui complète), donc pas de chance.  
>   - Cependant, en 6-max UTG, ouvrir 7-2o avec 3bb permet de gagner des rounds sans risque élevé, car les adversaires ne peuvent pas le suivre sans se tromper.  
>   - Règle : ouvrir une main dépareillée de 3bb en UTG en 6-max est standard (équité 15% vs 30% de cote).  
>   → **Ouvrir à 3bb est justifié par la position et la structure de la table.**  
> 
> *Note : Ce n’est pas une main forte, mais une ouverture de position en UTG pour équilibrer le jeu.*

*3.6 s*

### ☐ q23 — En 6-max à 100bb, premier à parler, depuis quelles positions ouvre-t-on Roi-9 assortis (K9s) ?

**Référence :** MP, CO, bouton et petite blinde. On se couche depuis UTG.

**Réponse du modèle :**

> - (Ouvrir avec K9s)  
> - (Miser 100bb)  
> - (Pourquoi) : En 6-max à 100bb, K9s est une paire de force 2/10 (paire). Dans un jeu à 6 joueurs, le premier à parler est en position de force (early position), où les chances de réussite sont faibles. K9s a une équité de ~20% contre un range de main moyenne (calculé via simulation : 20% de chance de gagner vs. un range de 50% de mains). La cote du pot est de 100bb / 100bb = 1.0, donc le ratio est 1.0.  
> → ROI = (gain - investissement) / investissement = (100bb - 100bb) / 100bb = 0% → pas de rentabilité.  
> → Cela signifie que K9s en position de départ est **faible** : il faut **ne pas ouvrir** en position de départ.  
> → **Conseil : ne pas ouvrir en position de départ**.  
> 
> → **Réponse normalisée** :  
> - (Ne pas ouvrir)  
> - (0bb)  
> - (Équité de 20% vs. un range de mains, cote du pot de 1.0 → ROI = 0% → pas de rentabilité)

*4.2 s*

### ☐ q24 — En 6-max à 100bb, premier à parler, ouvre-t-on Dame-Valet dépareillés (QJo) depuis UTG ?

**Référence :** Non, fold depuis UTG et MP. On l'ouvre depuis le cut-off, le bouton et la petite blinde.

**Réponse du modèle :**

> - Oui (ouvrir avec QJo depuis UTG en 6-max à 100bb)  
> - Miser 30bb (environ 30% du pot)  
> - Pourquoi : QJo est une paire de haute valeur (force 2/10), et en position UTG, l’ouverture est justifiée par la force de la main et la possibilité de progresser au flop.  
> - Équité : 40% de chance de gagner contre un adversaire avec une main au-dessus (ex. : KQ, KJ, etc.).  
> - Outs : 4 outs pour une quinte (ex. : 8, 9, 10, J), mais pas de flush.  
> - Cote du pot : 30bb / (100bb + 30bb) = 23% (cote du pot = 0.23).  
> - Conclusion : QJo est une main de base en UTG, mais avec une cote du pot de 23% vs équité de 40%, on est en avance (équité > cote du pot).  
> → **Ouverture justifiée.**

*3.4 s*

### ☐ q25 — Avant le flop, quelle est l'équité d'une paire d'As contre une main au hasard ?

**Référence :** Environ 85 %.

**Réponse du modèle :**

> - (Évaluer l'équité)  
> - (50 %)  
> - (Équité d'une paire d'As contre une main au hasard : 50 %, car les mains sont équiprobables. Dans un jeu de 52 cartes, les paires d'As sont 4 cartes (4 As), donc 4/52 = 1/13. La probabilité qu'une autre main soit une paire ou plus forte est ~40 %, donc l'équité d'une paire d'As est ~50 % en moyenne. Cela signifie qu’elle a 50 % de chances de gagner contre une main au hasard.)

*2.1 s*

### ☐ q26 — Avant le flop, As-Roi assortis contre une paire de 8 : qui est favori ?

**Référence :** La paire de 8, de peu : environ 52 % contre 48 %. C'est un « coin flip ».

**Réponse du modèle :**

> - (Action à faire) : Appeler  
> - (Combien miser) : 100 (ex. : égal au montant du coup actuel)  
> - (Pourquoi) : Tu as une paire (As-Roi), force 2/10, contre une paire de 8, force 2/10 → même force.  
> 
> Équité : 50 % (mêmes combinaisons, même force).  
> Outs : 0 (aucun out pour améliorer la main).  
> Cote du pot : 1 (si pot = 100, mise = 100 → cote 1).  
> 
> → Équité = 50 %, cote du pot = 1 → **égalité**, donc appeler est optimal.  
> 
> **Conclusion : égalité entre les mains → appeler.**

*2.6 s*

### ☐ q27 — Avant le flop, paire de Rois contre paire de Dames : quelles chances pour chacun ?

**Référence :** Les Rois gagnent environ 82 % du temps, les Dames environ 18 %.

**Réponse du modèle :**

> - (Action à faire) : Attendre le flop  
> - (Combien miser) : 0 (ne pas miser)  
> - (Pourquoi) : Aucune équité n’est encore déterminée. Avant le flop, les deux mains sont des paires, mais les valeurs sont différentes (Rois vs Dames). La force des paires est identique en valeur (force 2/10), donc aucune équité n’est avancée.  
> 
> → Équité :  
> - Paire de Rois : 50 % (hypothèse équilibrée sans flop)  
> - Paire de Dames : 50 %  
> 
> → Cote du pot : pas applicable (pas de mise)  
> → Outs : 0 (pas de carte dévoilée)  
> 
> → Conclusion : Pas de décision à prendre avant le flop.

*2.5 s*

### ☑ q28 — J'ai Ah Kh, le flop est Qh 7h 2c. Combien ai-je d'outs ?

**Référence :** 15 outs : 9 cœurs pour la couleur et 6 cartes pour une paire (3 As et 3 Rois). Environ 54 % de toucher d'ici la river.

**Réponse du modèle :**

> - (Action à faire) : Check  
> - (Combien miser) : 0  
> - (Pourquoi) : Vous avez 15 outs (9 pour couleur, 6 pour paire). Équité de 73,0 % contre des mains aléatoires. Cependant, avec une main de carte haute (A♥K♥) sur un flop de couleur (Q♥7♥), vous êtes en position de tirer une couleur ou une paire. Les 15 outs sont valides : 9 cœurs (2♥ à 6♥, 8♥, 9♥, 10♥, J♥) et 6 paires (A♠, A♦, A♣, K♠, K♦, K♣). La chance de toucher un out est de 54,1 % d'ici la river.  
> 
> ✅ **Outs : 15** (9 couleur + 6 paire) — calculs exacts fournis.

*3.2 s*

### ☐ q29 — J'ai 8h 9d et le flop est 7c 6s 2h. Combien d'outs pour la quinte ?

**Référence :** 8 outs : les quatre 5 et les quatre 10 (tirage quinte par les deux bouts). Environ 31 % de la toucher d'ici la river.

**Réponse du modèle :**

> - (Action à faire) : Appeler  
> - (Combien miser) : 14  
> - (Pourquoi) : 14 outs pour la quinte (5♠ 5♥ 5♦ 5♣ 10♠ 10♥ 10♦ 10♣), soit 8 pour 5-6-7-8-9, 6 pour 8-9-10-J-Q. Équité 49,4 % contre hasard (±1,0 %). La cote du pot est de 51,2 % de toucher un out d'ici la river.  
> 
> → **14 outs** (donc **14**). ✅

*2.5 s*

### ☐ q30 — Avec un tirage couleur au turn (9 outs), quelle chance de toucher à la river ?

**Référence :** 9 sur 46 cartes inconnues, soit environ 19,6 % (la règle du 2 donne environ 18 %).

**Réponse du modèle :**

> - (Toucher à la river)  
> - (41,5%)  
> - (9 outs × 2 = 18 outs → 18/47 ≈ 38,3% → arrondi à 41,5% avec approximation standard : 2 × outs / 47)  
> → Probabilité de toucher une couleur à la river avec 9 outs : **environ 41,5%**.

*1.6 s*

### ☐ q31 — Qu'est-ce que la règle du 2 et du 4 ?

**Référence :** Une approximation de la chance de toucher un tirage : au flop, outs × 4 pour le turn et la river ensemble ; au turn, outs × 2 pour la river seule. Le résultat est en pourcentage.

**Réponse du modèle :**

> - (Règle du 2) : Si tu as une paire, tu peux jouer avec une carte de même valeur (2e carte de ta paire).  
> - (Règle du 4) : Si tu as un brelan, tu peux jouer avec une carte de valeur différente (4e carte de ta combinaison).  
> 
> → Ces règles sont utilisées pour évaluer les chances de réussite dans un jeu de poker, notamment en fonction des outs (cartes qui améliorent ta main).  
> Exemple : Si tu as un brelan (3 de même valeur), tu as 4 outs pour faire un brelan (une carte de valeur égale).  
> → Cela permet de calculer l'équité (probabilité de réussir) :  
> - 4 outs → 4/47 (≈ 8,5%) chance de réussir à la fin du tour.  
> → Cela donne une cote de 4/47 ≈ 5,7 : 1 (cote du pot).  
> 
> → Si la cote du pot > cote de l'équité (5,7 : 1), il faut jouer.  
> → Si la cote du pot < cote de l'équité, il faut abandonner.  
> 
> → Règle du 2 et du 4 : aide à estimer les outs pour décider si une main est valable.  
> → En pratique :  
> - 2 outs → 2/47 ≈ 4,3% → faible  
> - 4 outs → 4/47 ≈ 8,5% → moyenne  
> → Utilise ces valeurs pour juger si le coup est rentable.  
> 
> ✅ Conclusion :  
> - (Action à faire) : Évaluer les outs (2 ou 4)  
> - (Combien miser) : 0 (si pas de gain)  
> - (Pourquoi) : Pour estimer la probabilité de réussir (équité) à partir de la règle du 2 ou du 4.

*5.4 s*

### ☐ q32 — Le pot est de 100 (mise adverse comprise) et je dois payer 50. Quelle équité minimum faut-il pour suivre ?

**Référence :** 33,3 % : 50 / (100 + 50). C'est une cote de 2 contre 1.

**Réponse du modèle :**

> - Suivre  
> - 50  
> - Équité minimale : 50/(100+50) = 1/3 ≈ 33,3%  
> → Si ta main a au moins 33,3% de chance de gagner, tu dois suivre.  
> 
> **Justification** : Tu dois payer 50 pour un pot de 100, donc le pot est de 150 (100 + 50). L'équité minimale est donc 50/150 = 1/3. Si ta main a une équité ≥ 33,3%, tu dois suivre.

*2.1 s*

### ☑ q33 — J'ai As Ad, le flop est Kc 7d 2s. Le pot est de 90 avec la mise adverse et je dois payer 30. Que faire ?

**Référence :** Au minimum suivre, et relancer pour la valeur est aussi correct : il faut 25 % d'équité (30 / 120) et une paire d'As au-dessus du board (overpair) en a bien plus. Se coucher est une erreur.

**Réponse du modèle :**

> - Suivre  
> - 30  
> - Équité de 88,6 % contre des mains aléatoires > 25 % (cote du pot : 30/90 = 1/3 → 33,3 %). Le calcul montre que suivre est rentable à long terme.  
> (Attention : équité réelle face à une main réelle est probablement inférieure, mais ici, le calcul fourni est suffisant pour justifier la décision.)

*2.1 s*
