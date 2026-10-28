# Résultats de l'évaluation

Modèle : `qwen3:4b-instruct-2507-q4_K_M` — température 0 — 2026-10-24 18:08 — **57/87 réussies** (66%)

Fichier généré par `python3 evaluate.py` : ne pas modifier à la main. Le verdict est donné par le modèle lui-même, à relire.

| Réussi | # | Thème | Question | Différences relevées par le modèle |
|:---:|---|---|---|---|
| ☑ | q01 | combinaisons | Quelle est la meilleure main au poker ? | — |
| ☑ | q02 | combinaisons | Est-ce qu'une couleur bat un full ? | — |
| ☑ | q03 | combinaisons | Qu'est-ce qui est le plus fort : une quinte ou un brelan ? | — |
| ☐ | q04 | combinaisons | Entre une double paire et un brelan, quelle main gagne ? | Le brelan bat la double paire : contredit |
| ☑ | q05 | combinaisons | L'as peut-il servir dans une quinte basse ? | — |
| ☑ | q06 | combinaisons | Si deux joueurs ont exactement la même main, la couleur (pique, cœur...) les départage-t-elle ? | — |
| ☑ | q07 | combinaisons | Qu'est-ce que le kicker ? | — |
| ☑ | q08 | règles | Combien de cartes reçoit chaque joueur au Texas Hold'em, et comment forme-t-on sa main ? | — |
| ☑ | q09 | règles | Dans quel ordre sont dévoilées les cartes communes ? | — |
| ☑ | q10 | règles | Que sont les blindes ? | — |
| ☑ | q11 | règles | Qui parle en premier avant le flop, et après le flop ? | — |
| ☑ | q12 | règles | En no-limit, quelle est la relance minimum quand un joueur a misé 10 ? | — |
| ☑ | q13 | règles | Qu'est-ce qu'un side pot ? | — |
| ☑ | q14 | position | Pourquoi le bouton est-il la meilleure position ? | — |
| ☐ | q15 | vocabulaire | Que veut dire avoir les « nuts » ? | Cela dépend des cartes du board : absent |
| ☑ | q16 | vocabulaire | Qu'est-ce qu'un set ? | — |
| ☐ | q17 | vocabulaire | Qu'est-ce qu'un tirage ventral (gutshot) ? | Il a 4 outs : absent |
| ☑ | q18 | vocabulaire | Qu'est-ce qu'un check-raise ? | — |
| ☑ | q19 | vocabulaire | Que veut dire « limper » ? | — |
| ☑ | q20 | vocabulaire | Que veut dire être « en tilt » ? | — |
| ☑ | q21 | vocabulaire | Qu'est-ce qu'un joueur TAG ? | — |
| ☑ | q22 | préflop | En 6-max à 100bb, premier à parler, faut-il ouvrir 7-2 dépareillés (72o) depuis UTG ? | — |
| ☑ | q23 | préflop | En 6-max à 100bb, premier à parler, depuis quelles positions ouvre-t-on Roi-9 assortis (K9s) ? | — |
| ☑ | q24 | préflop | En 6-max à 100bb, premier à parler, ouvre-t-on Dame-Valet dépareillés (QJo) depuis UTG ? | — |
| ☑ | q25 | équité | Avant le flop, quelle est l'équité d'une paire d'As contre une main au hasard ? | — |
| ☑ | q26 | équité | Avant le flop, As-Roi assortis contre une paire de 8 : qui est favori ? | — |
| ☑ | q27 | équité | Avant le flop, paire de Rois contre paire de Dames : quelles chances pour chacun ? | — |
| ☐ | q28 | outs | J'ai Ah Kh, le flop est Qh 7h 2c. Combien ai-je d'outs ? | 6 outs pour une paire (As ou Rois) : absent |
| ☐ | q29 | outs | J'ai 8h 9d et le flop est 7c 6s 2h. Combien d'outs pour la quinte ? | 8 outs pour la quinte : absent ; Les quatre 5 et les quatre 10 : absent |
| ☐ | q30 | outs | Avec un tirage couleur au turn (9 outs), quelle chance de toucher à la river ? | Environ 19,6 % (9 sur 46), ou environ 18 % avec la règle du 2 : absent |
| ☑ | q31 | outs | Qu'est-ce que la règle du 2 et du 4 ? | — |
| ☐ | q32 | cote du pot | Le pot est de 100 (mise adverse comprise) et je dois payer 50. Quelle équité minimum faut-il pour suivre ? | Il faut au moins 33,3 % d'équité (50 / 150) : absent |
| ☑ | q33 | décision | J'ai As Ad, le flop est Kc 7d 2s. Le pot est de 90 avec la mise adverse et je dois payer 30. Que faire ? | — |
| ☐ | q34 | vocabulaire | Qu'est-ce qu'un continuation bet (c-bet) ? | Elle est faite par le joueur qui a relancé avant le flop : contredit |
| ☑ | q35 | vocabulaire | Qu'est-ce qu'un 3-bet ? | — |
| ☑ | q36 | vocabulaire | Qu'est-ce qu'un squeeze ? | — |
| ☐ | q37 | vocabulaire | Qu'est-ce qu'une donk bet ? | Il mise en premier, devant le relanceur : absent |
| ☑ | q38 | vocabulaire | Qu'est-ce qu'un semi-bluff ? | — |
| ☑ | q39 | vocabulaire | Qu'est-ce qu'une value bet ? | — |
| ☑ | q40 | vocabulaire | Qu'est-ce que le slow play ? | — |
| ☑ | q41 | vocabulaire | Qu'est-ce que « floater » au poker ? | — |
| ☑ | q42 | vocabulaire | J'ai J-J et le flop est 9-6-2. Comment s'appelle ma main ? | — |
| ☑ | q43 | vocabulaire | Que veut dire TPTK ? | — |
| ☑ | q44 | vocabulaire | Qu'est-ce qu'un tirage backdoor ? | — |
| ☑ | q45 | vocabulaire | Que veut dire un flop « rainbow » ? | — |
| ☑ | q46 | vocabulaire | Qu'est-ce que la fold equity ? | — |
| ☑ | q47 | vocabulaire | Qu'est-ce qu'une calling station ? | — |
| ☑ | q48 | vocabulaire | Qu'est-ce qu'un nit ? | — |
| ☑ | q49 | vocabulaire | Que mesure le VPIP ? | — |
| ☑ | q50 | vocabulaire | Que veut dire « tirer mort » (drawing dead) ? | — |
| ☑ | q51 | vocabulaire | Que désigne le mot « Broadway » ? | — |
| ☐ | q52 | vocabulaire | Quelle différence entre un set et des trips ? | Trips : une carte en main plus une paire au tableau : contredit |
| ☑ | q53 | vocabulaire | Qu'est-ce qu'un cooler ? | — |
| ☑ | q54 | vocabulaire | Où est assis le cut-off ? | — |
| ☐ | q55 | vocabulaire | Qu'est-ce qu'un walk ? | Tous les joueurs se couchent jusqu'à la grosse blinde : absent ; La grosse blinde remporte les blindes : contredit |
| ☐ | q56 | vocabulaire | Qu'est-ce qu'un tirage quinte par les deux bouts ? | Il y a 8 outs : absent |
| ☑ | q57 | vocabulaire | Qu'est-ce qu'un straddle ? | — |
| ☐ | q58 | outs | J'ai 9h 8h et le flop est 7h 6c 2h. Combien d'outs pour faire une couleur ou une quinte ? | 15 outs : absent |
| ☐ | q59 | outs | Au flop, avec 15 outs, quelle est la chance de toucher d'ici la river ? | Environ 54 % : absent |
| ☐ | q60 | outs | J'ai Jc Ts et le flop est 9d 8h 2c. Combien d'outs pour la quinte, et quelle chance de la toucher d'ici la river ? | 8 outs : absent ; Les 7 et les Dames : absent ; Environ 31,5 % d'ici la river : contredit |
| ☑ | q61 | outs | J'ai Jc Ts et le flop est 8d 7h 2c. Combien d'outs pour la quinte ? | — |
| ☐ | q62 | outs | J'ai As Kd et le flop est 7h 5s 2c. Combien d'outs pour faire la top paire ? | 6 outs : absent ; Les trois As et les trois Rois restants : absent |
| ☑ | q63 | outs | J'ai 6h 6c et le flop est Ks 9d 3c. Combien d'outs pour faire un brelan à la turn, et avec quelle chance ? | — |
| ☑ | q64 | outs | Au turn, avec un tirage quinte par les deux bouts (8 outs), quelle chance de toucher à la river ? | — |
| ☐ | q65 | outs | J'ai 9c 8c, le board au turn est 7h 6h 5h Ah et mon adversaire montre Kh Qh. Combien d'outs ai-je ? | Ma quinte perd contre sa couleur : absent ; 0 out : je tire mort : contredit |
| ☐ | q66 | cote du pot | Le pot est de 60 et mon adversaire mise 30. Combien dois-je payer, et quelle équité minimum faut-il pour suivre ? | Il faut 25 % d'équité minimum : contredit |
| ☐ | q67 | cote du pot | Face à une mise de la taille du pot, quelle équité minimum faut-il pour suivre ? | Environ 33 % (un tiers) : absent |
| ☐ | q68 | décision | Au flop, mon adversaire fait tapis pour une mise égale au pot. Je n'ai qu'un tirage couleur (9 outs) et toutes les cartes seront dévoilées. Dois-je suivre ? | Environ 35 % de chances d'ici la river : absent ; Il faut 33 % d'équité : absent ; Suivre est (légèrement) rentable : contredit |
| ☐ | q69 | décision | Au turn, mon adversaire mise la taille du pot et il reste une carte. J'ai un tirage couleur (9 outs) et je ne compte pas sur des gains implicites. Dois-je suivre ? | Environ 20 % de toucher à la river : absent ; Il faut 33 % d'équité : absent ; Il faut se coucher : absent |
| ☐ | q70 | abattage | Le tableau est Ah Kd 7c 7s 2h. Le joueur 1 a As Qd, le joueur 2 a Kc Ks. Qui gagne ? | Le joueur 2 a un full (Rois par les 7) : absent ; Le joueur 1 a deux paires (As et 7) : absent |
| ☑ | q71 | abattage | Le tableau est Kh 9c 5d 3s 2h. Le joueur 1 a Kd Qc, le joueur 2 a Ks Jd. Qui gagne ? | — |
| ☐ | q72 | abattage | Le tableau est 5c 6d 7h 8s 9c. Le joueur 1 a Ac 2d, le joueur 2 a Kh 3s. Qui gagne ? | Le pot est partagé : absent ; Les deux jouent la quinte du tableau (5 à 9) : contredit |
| ☑ | q73 | abattage | Le tableau est 6c 7d 8h 9s 2c. Le joueur 1 a Ts 3d, le joueur 2 a 5s 4d. Qui gagne ? | — |
| ☑ | q74 | abattage | Le tableau est Kh 8h 4h 2c 9s. Le joueur 1 a Ah 3h, le joueur 2 a Qh Jh. Qui gagne ? | — |
| ☐ | q75 | abattage | Le tableau est Ah 9d 9c 4s 4h. Le joueur 1 a Ad Kc, le joueur 2 a As Qc. Qui gagne ? | Les deux ont deux paires As et 9 : absent ; Le joueur 1 gagne grâce au kicker Roi : contredit |
| ☑ | q76 | équité | Avant le flop, As-Roi dépareillés contre As-Dame dépareillés : qui est favori, et à combien ? | — |
| ☑ | q77 | équité | Avant le flop, paire de 2 contre As-Roi dépareillés : qui est favori ? | — |
| ☑ | q78 | équité | Avant le flop, paire d'As contre paire de Rois : quelles chances pour chacun ? | — |
| ☐ | q79 | équité | Avant le flop, As-Roi assortis contre paire de Dames : qui est favori ? | La paire de Dames est favorite : absent ; Environ 54 % contre 46 % : absent |
| ☐ | q80 | probabilités | Combien de combinaisons existe-t-il pour une paire servie précise (par ex. AA) et pour une main non appariée (par ex. AK) ? | 6 combinaisons pour une paire servie : absent ; 16 pour une main non appariée (4 assorties, 12 dépareillées) : absent |
| ☑ | q81 | probabilités | Quelle est la probabilité de recevoir une paire d'As ? | — |
| ☐ | q82 | probabilités | Avec une paire servie, quelle chance de toucher un brelan (ou mieux) au flop ? | Environ 12 % : absent |
| ☐ | q83 | probabilités | Avec deux cartes assorties, quelle chance d'avoir une couleur dès le flop ? | Moins de 1 % (environ 0,8 %) : absent |
| ☐ | q84 | préflop | En 6-max à 100bb, premier à parler, ouvre-t-on Roi-Valet dépareillés (KJo) depuis UTG ? | On l'ouvre à partir du MP : absent |
| ☑ | q85 | préflop | En 6-max à 100bb, premier à parler, depuis quelles positions ouvre-t-on As-9 dépareillés (A9o) ? | — |
| ☐ | q86 | règles | En heads-up, qui parle en premier avant le flop, et après le flop ? | Après le flop, la grosse blinde parle en premier : contredit |
| ☑ | q87 | règles | En no-limit, blindes 10/20 : un joueur relance à 60. Quelle est la sur-relance minimum ? | — |

## Détail

### ☑ q01 — Quelle est la meilleure main au poker ?

**Référence :** La quinte flush royale : As, Roi, Dame, Valet et 10 de la même couleur.

**Réponse du modèle :**

> La meilleure main au poker est la quinte flush royale (Royal flush).  
> Elle est composée de l'As, du Roi, de la Dame, du Valet et du 10 de la même couleur. C'est la combinaison la plus forte selon le classement officiel, avec une force de 10/10.

*23.5 s*

### ☑ q02 — Est-ce qu'une couleur bat un full ?

**Référence :** Non. Le full (un brelan et une paire) bat la couleur.

**Réponse du modèle :**

> Oui.  
> Une couleur (Flush) bat un full (Full house) car selon le classement des combinaisons, la couleur a une force de 6/10, tandis que le full a une force de 7/10. Cela signifie que le full est plus fort que la couleur.  
> → Le full (7/10) > Couleur (6/10) → donc non, une couleur ne bat pas un full.  
> **Correction : Non.**  
> Une couleur ne bat pas un full. Le full est plus fort que la couleur dans le classement des combinaisons.

*25.1 s*

### ☑ q03 — Qu'est-ce qui est le plus fort : une quinte ou un brelan ?

**Référence :** La quinte bat le brelan.

**Réponse du modèle :**

> Une quinte est plus forte qu'un brelan.  
> Selon le classement, une quinte (force 5/10) est au-dessus d'un brelan (force 4/10).  
> → La quinte est donc plus forte.

*12.8 s*

### ☐ q04 — Entre une double paire et un brelan, quelle main gagne ?

**Référence :** Le brelan bat la double paire.

**Réponse du modèle :**

> Une double paire gagne contre un brelan.  
> Selon le classement, la double paire a une force de 3/10, tandis que le brelan a une force de 4/10. Comme la force du brelan est supérieure, il gagne.  
> → Le brelan gagne.

*16.0 s*

### ☑ q05 — L'as peut-il servir dans une quinte basse ?

**Référence :** Oui : A-2-3-4-5 (la « roue ») est la plus petite quinte. Une quinte ne peut pas « tourner » : Dame-Roi-As-2-3 n'est pas une quinte.

**Réponse du modèle :**

> Oui.  
> L'As peut servir dans une quinte basse (As-2-3-4-5), car la règle du poker permet à l'As de compter en bas de la suite, comme dans une quinte basse. Cela ne vaut pas pour une quinte haute (10-V-D-R-As), où l'As est en haut.  
> - (Action à faire) - (Combien miser) - (Pourquoi).  
> (Non demandé dans la question.)

*20.6 s*

### ☑ q06 — Si deux joueurs ont exactement la même main, la couleur (pique, cœur...) les départage-t-elle ?

**Référence :** Non. Au Texas Hold'em aucune couleur n'est plus forte qu'une autre : le pot est partagé à égalité.

**Réponse du modèle :**

> Non.  
> Les couleurs (pique, cœur, carreau, trèfle) ne départagent jamais deux mains de même valeur ; l'égalité est totale, et le pot est partagé. C’est une règle fondamentale du poker : si les 5 meilleures cartes sont identiques, les mains sont égales, quel que soit le symbole des cartes.

*23.8 s*

### ☑ q07 — Qu'est-ce que le kicker ?

**Référence :** La carte d'accompagnement qui départage deux mains de même combinaison. Exemple : sur un board A-7-2, AK bat AQ grâce au kicker Roi.

**Réponse du modèle :**

> Le kicker, c'est la carte qui accompagne votre meilleur pair ou brelan, ou celle qui n'a pas touché le flop, lorsqu'il y a égalité entre deux mains.
> 
> Dans un cas d'égalité (ex : deux joueurs ont une paire de 9), le kicker (la deuxième carte de la main) détermine qui gagne. Par exemple, si l'un a un 9 et un 10, l'autre un 9 et un 8, le joueur avec le 10 gagne car son kicker est plus fort. Le kicker n'est pas compté dans la combinaison, mais il influence le résultat en cas d'égalité.

*26.5 s*

### ☑ q08 — Combien de cartes reçoit chaque joueur au Texas Hold'em, et comment forme-t-on sa main ?

**Référence :** 2 cartes privées. Avec les 5 cartes communes, on garde la meilleure main de 5 cartes parmi les 7.

**Réponse du modèle :**

> Chaque joueur reçoit 2 cartes privées.  
> On forme sa main en combinant ses 2 cartes privées avec les 5 cartes communes (flop, turn, river) pour former la meilleure combinaison possible, en tenant compte des 5 meilleures cartes au total.
> 
> - (Aucune action) - (0) - (Les 2 cartes privées sont utilisées avec les 5 cartes communes pour former la meilleure main)

*26.3 s*

### ☑ q09 — Dans quel ordre sont dévoilées les cartes communes ?

**Référence :** Le flop (3 cartes), puis le turn (1 carte), puis la river (1 carte). Il y a un tour d'enchères avant le flop et après chacune de ces étapes.

**Réponse du modèle :**

> Flop, turn, river.
> 
> Explication : Les cartes communes sont dévoilées en trois étapes successives : d'abord le flop (trois cartes), puis le turn (une carte), puis le river (une dernière carte). Cet ordre est standard dans le Texas Hold'em.

*16.8 s*

### ☑ q10 — Que sont les blindes ?

**Référence :** Des mises obligatoires posées avant la distribution : la petite blinde par le joueur à gauche du bouton, la grosse blinde par le suivant (en général le double de la petite).

**Réponse du modèle :**

> Les blindes sont des mises obligatoires postées par un ou plusieurs joueurs avant que les cartes ne soient distribuées.
> 
> Elles sont au nombre de deux en Hold’em : la petite blinde (SB) et la grosse blinde (BB). La petite blinde est d’une demi-unité, la grosse blinde est d’une unité.

*17.0 s*

### ☑ q11 — Qui parle en premier avant le flop, et après le flop ?

**Référence :** Avant le flop : le joueur à gauche de la grosse blinde (UTG). Après le flop : le premier joueur encore en jeu à gauche du bouton, en général la petite blinde.

**Réponse du modèle :**

> Avant le flop : le joueur à gauche de la grosse blinde (UTG) parle en premier.  
> Après le flop : le premier joueur encore en jeu à gauche du bouton parle en premier.
> 
> Explication :  
> Avant le flop, l'ordre suit le tour de table, avec UTG qui commence. Après le flop, le tour de table repart à partir du joueur à gauche du bouton, qui parle en premier, puis le bouton en dernier. Ce principe s'applique dans les situations normales, y compris en heads-up.

*22.8 s*

### ☑ q12 — En no-limit, quelle est la relance minimum quand un joueur a misé 10 ?

**Référence :** La relance doit ajouter au moins le montant de la mise précédente : il faut relancer à 20 au minimum.

**Réponse du modèle :**

> 20
> 
> Relance minimum en no-limit : d'au moins le montant de la dernière mise. Si un joueur a misé 10, la relance minimum est de 20.

*11.0 s*

### ☑ q13 — Qu'est-ce qu'un side pot ?

**Référence :** Un pot annexe créé quand un joueur fait tapis avec moins de jetons que les autres : il ne peut gagner que le pot principal, où chacun a mis au plus son tapis ; les mises au-delà forment un pot séparé, disputé par les autres joueurs.

**Réponse du modèle :**

> Un side pot est un pot annexe.
> 
> Un side pot est formé lorsque un joueur est à tapis et que les autres joueurs continuent à miser. Ce pot annexe est disputé uniquement par les joueurs encore en jeu, et le joueur à tapis ne peut gagner que ce qu'il a misé dans ce pot. Le surplus des mises forme ainsi un pot annexe qu'ils se disputent entre eux.

*21.2 s*

### ☑ q14 — Pourquoi le bouton est-il la meilleure position ?

**Référence :** Après le flop, le bouton parle en dernier à chaque tour : il voit ce que font les autres avant de décider. On peut donc y jouer plus de mains qu'en début de parole.

**Réponse du modèle :**

> Le bouton est la meilleure position parce qu'il est le dernier à parler à chaque tour d'enchères, ce qui lui permet de voir les actions de tous les autres joueurs avant de décider de sa propre mise. Cela lui donne un avantage stratégique en termes d'information, car il peut ajuster ses décisions en fonction des relances et des appels. Il peut ainsi mieux évaluer les mains adverses et décider de miser, appeler ou retirer avec plus de précision.
> 
> - (Le bouton est la meilleure position car il voit les actions des autres joueurs avant de parler, ce qui lui permet de prendre des décisions plus informées.)

*27.0 s*

### ☐ q15 — Que veut dire avoir les « nuts » ?

**Référence :** Avoir la meilleure main possible à ce moment, compte tenu des cartes du board.

**Réponse du modèle :**

> Avoir les « nuts » veut dire avoir le meilleur jeu possible, la meilleure main au poker.
> 
> Cela signifie que la main est la plus forte possible, en fonction du classement des combinaisons, et qu'elle ne peut être battue par aucune autre main. Dans une situation donnée, les « nuts » sont le jeu maximal, donc le plus fort, et ils permettent de gagner le pot sans risque de perdre si les autres mains sont inférieures.

*18.6 s*

### ☑ q16 — Qu'est-ce qu'un set ?

**Référence :** Un brelan formé avec une paire en main et une carte de même valeur sur le board (différent des trips : une seule carte en main et une paire sur le board).

**Réponse du modèle :**

> Un set, c'est un brelan.
> 
> Un set est une combinaison de trois cartes de même valeur, par exemple trois rois. C'est une main de force 4/10 dans le classement des combinaisons. Cela peut être formé avec une carte de la table (le board) et une paire dans la main du joueur.

*14.6 s*

### ☐ q17 — Qu'est-ce qu'un tirage ventral (gutshot) ?

**Référence :** Un tirage quinte auquel il manque une carte au milieu : une seule valeur le complète, soit 4 outs. Exemple : 9-8 sur 6-5-2, il faut un 7.

**Réponse du modèle :**

> Un tirage ventral (gutshot) est un tirage de quinte où l'on manque une carte pour compléter la quinte par le milieu.
> 
> Exemple : vous avez J-Q et le flop affiche 8-9-2-A. Vous êtes sur un tirage gutshot (quinte de 8-9-10-J-Q), car vous manquez un 10 pour compléter la quinte.  
> Ce tirage est très faible car il nécessite une seule carte (le 10) pour réussir, et il est souvent sous-estimé en comparaison avec d'autres tirages.
> 
> - (Action à faire) - (Mise) - (Pourquoi)  
> *(Ne s'applique pas ici car la question est de définition, pas d'action en main en cours.)*

*30.8 s*

### ☑ q18 — Qu'est-ce qu'un check-raise ?

**Référence :** Checker, puis relancer quand un adversaire mise après nous, dans le même tour d'enchères.

**Réponse du modèle :**

> Un check-raise est un checker puis un relance après que l’adversaire ait misé.
> 
> Explication : C’est une action en poker où un joueur vérifie (check) la mise de son adversaire, puis relance (raise) pour montrer de la force ou pour élargir le pot. Cela peut être utilisé pour cacher sa main forte ou pour presser l’adversaire.

*23.9 s*

### ☑ q19 — Que veut dire « limper » ?

**Référence :** Avant le flop, payer seulement la grosse blinde au lieu de relancer.

**Réponse du modèle :**

> « Limper » veut dire se contenter de payer la grosse blinde au premier tour d’enchères pré-flop.
> 
> On appelle les « limpeurs » les joueurs qui rentrent dans un coup de cette manière. C’est une action passive qui permet de rester en jeu sans miser de plus, souvent pour éviter de se faire éliminer ou pour attendre une meilleure main.

*41.0 s*

### ☑ q20 — Que veut dire être « en tilt » ?

**Référence :** Être énervé ou déconcentré, souvent après un mauvais coup, et prendre de mauvaises décisions à cause de ses émotions.

**Réponse du modèle :**

> Être « en tilt » veut dire être en état d’énervement ou de déconcentration après un mauvais coup, ce qui pousse à jouer mal, voire à péter un plomb.
> 
> C’est un phénomène psychologique qui peut conduire à des décisions irrationnelles en poker, comme relancer sans raison ou abandonner une main en cours. Il est souvent associé à un joueur « cagoulé ».

*44.3 s*

### ☑ q21 — Qu'est-ce qu'un joueur TAG ?

**Référence :** Tight-aggressive : il joue peu de mains, mais il les joue de façon agressive (en misant et en relançant plutôt qu'en suivant).

**Réponse du modèle :**

> Un joueur TAG est un joueur serré mais agressif.
> 
> Il joue un éventail de mains restreint, mais quand il joue, il fait des relances importantes. C’est un type de joueur efficace à long terme, car il évalue les mains avec prudence avant d’agir, puis exerce une pression agressive lors des relances.

*16.0 s*

### ☑ q22 — En 6-max à 100bb, premier à parler, faut-il ouvrir 7-2 dépareillés (72o) depuis UTG ?

**Référence :** Non, on se couche. 72o ne s'ouvre depuis aucune position : c'est la plus faible main de départ.

**Réponse du modèle :**

> Non.  
> En 6-max à 100bb, depuis UTG, 72o n’est pas suffisant pour ouvrir, car son équité contre une main au hasard est de 34,5 %, et elle est très faible face à des mains comme 88, 99 ou des paires supérieures. Le fait que 72o soit dépareillé et que le joueur soit en position délicate (UTG) réduit encore sa force.  
> - (Ne pas ouvrir) - (0) - (Car 72o a une équité de seulement 34,5 % contre une main au hasard et est trop faible pour ouvrir depuis UTG.)

*28.9 s*

### ☑ q23 — En 6-max à 100bb, premier à parler, depuis quelles positions ouvre-t-on Roi-9 assortis (K9s) ?

**Référence :** MP, CO, bouton et petite blinde. On se couche depuis UTG.

**Réponse du modèle :**

> Ouvre-t-on K9s depuis MP, CO, BTN, SB ?  
> Ouvre-t-on K9s depuis MP, CO, BTN, SB ?  
> 
> - (Ouvre depuis MP, CO, BTN) - (10) - (Équité 60,4 % contre une main au hasard ; K9s est une main forte en position, donc ouverte depuis MP, CO, BTN, mais pas depuis UTG. La grosse blinde n'ouvre pas.)

*21.1 s*

### ☑ q24 — En 6-max à 100bb, premier à parler, ouvre-t-on Dame-Valet dépareillés (QJo) depuis UTG ?

**Référence :** Non, fold depuis UTG et MP. On l'ouvre depuis le cut-off, le bouton et la petite blinde.

**Réponse du modèle :**

> Non.  
> Dans un 6-max à 100bb, depuis UTG, QJo (Dame-Valet dépareillés) n'est pas une main suffisamment forte pour ouvrir, surtout en position délicate comme UTG. L'équité contre une main au hasard est de 58,2 %, ce qui signifie que QJo est sous-évalué face à une main aléatoire. Il est préférable de ne pas ouvrir depuis UTG avec cette main.  
> - (Ne pas ouvrir) - (0) - (QJo est trop faible pour ouvrir depuis UTG en 6-max à 100bb.)

*28.0 s*

### ☑ q25 — Avant le flop, quelle est l'équité d'une paire d'As contre une main au hasard ?

**Référence :** Environ 85 %.

**Réponse du modèle :**

> 85,1 %  
> 
> Avant le flop, une paire d'As a une équité de 85,1 % contre une main au hasard, car elle est très forte par rapport aux autres mains. Cela signifie qu'elle gagne 85,1 % des temps face à une main aléatoire. Ce chiffre est standard dans les calculs de poker en pré-flop pour les mains de départ.

*27.8 s*

### ☑ q26 — Avant le flop, As-Roi assortis contre une paire de 8 : qui est favori ?

**Référence :** La paire de 8, de peu : environ 52 % contre 48 %. C'est un « coin flip ».

**Réponse du modèle :**

> 88 est favori.
> 
> Face-à-face AKs contre 88 : AKs 47,6 %, 88 52,4 % (égalités partagées, ±0,7 %) : 88 est favori.  
> Dans un head-up, avec AKs contre 88, la paire de 8 est légèrement plus forte en termes de probabilité de gagner.  
> - (Ne pas miser) - (0) - (La paire de 8 est plus forte que AKs dans ce contexte, donc il vaut mieux ne pas miser pour éviter de perdre du tapis.)

*27.7 s*

### ☑ q27 — Avant le flop, paire de Rois contre paire de Dames : quelles chances pour chacun ?

**Référence :** Les Rois gagnent environ 82 % du temps, les Dames environ 18 %.

**Réponse du modèle :**

> KK a 81,9 % de chances de gagner contre QQ.  
> QQ a 18,1 % de chances de gagner contre KK.  
> 
> Avant le flop, avec une paire de rois contre une paire de dames, la paire de rois est fortement favorisée (81,9 %), car les rois sont supérieurs aux dames en valeur. Le calcul est basé sur les probabilités standardisées dans un contexte 6-max, 100bb, sans relance préalable. Les égalités sont partagées, mais le KK est clairement favori.

*29.0 s*

### ☐ q28 — J'ai Ah Kh, le flop est Qh 7h 2c. Combien ai-je d'outs ?

**Référence :** 15 outs : 9 cœurs pour la couleur et 6 cartes pour une paire (3 As et 3 Rois). Environ 54 % de toucher d'ici la river.

**Réponse du modèle :**

> 15 outs  
> - 9 pour couleur (2♥ 3♥ 4♥ 5♥ 6♥ 8♥ 9♥ 10♥ J♥)  
> - 6 pour paire (K♠ K♦ K♣ A♠ A♦ A♣)  
> 
> Explication : Avec Ah Kh, vous avez une paire de cœurs. Le flop Qh 7h 2c donne une couleur en cours (3 cœurs). Pour compléter une couleur, il faut 9 cartes de cœur restantes (2♥ à 10♥, sauf 8♥ et 9♥ déjà dans le board). Pour une paire, vous pouvez faire une paire avec un As ou un Roi sur la turn ou river. Les 6 cartes (A♠ A♦ A♣ K♠ K♦ K♣) complètent votre paire. Total : 9 + 6 = 15 outs.

*40.1 s*

### ☐ q29 — J'ai 8h 9d et le flop est 7c 6s 2h. Combien d'outs pour la quinte ?

**Référence :** 8 outs : les quatre 5 et les quatre 10 (tirage quinte par les deux bouts). Environ 31 % de la toucher d'ici la river.

**Réponse du modèle :**

> 14 outs pour la quinte.  
> Cela correspond à 8 cartes pour compléter une quinte (5♠ 5♥ 5♦ 5♣ 10♠ 10♥ 10♦ 10♣) et 6 cartes pour compléter une paire (8♠ 8♦ 8♣ 9♠ 9♥ 9♣).  
> La quinte peut être formée avec un 5 ou un 10, donc c’est un tirage open-ended.

*35.3 s*

### ☐ q30 — Avec un tirage couleur au turn (9 outs), quelle chance de toucher à la river ?

**Référence :** 9 sur 46 cartes inconnues, soit environ 19,6 % (la règle du 2 donne environ 18 %).

**Réponse du modèle :**

> 41,5 %  
> 
> Avec 9 outs, la probabilité de toucher une couleur à la river est de 9/47 ≈ 19,1 %, mais en tenant compte de la règle de la "chance de toucher" en poker (9 outs × 2 = environ 18 %), on arrive à une estimation de 41,5 % pour la chance de réussir un tirage couleur à la river, en considérant les 47 cartes restantes après le turn. Cela correspond à une probabilité de réussite de 41,5 %, car les 9 outs sont répartis sur les 47 cartes restantes.

*30.9 s*

### ☑ q31 — Qu'est-ce que la règle du 2 et du 4 ?

**Référence :** Une approximation de la chance de toucher un tirage : au flop, outs × 4 pour le turn et la river ensemble ; au turn, outs × 2 pour la river seule. Le résultat est en pourcentage.

**Réponse du modèle :**

> Je ne connais pas la règle du "2 et du 4" dans le poker Texas Hold'em no-limit.  
> Cela ne figure pas dans le contexte fourni.

*8.5 s*

### ☐ q32 — Le pot est de 100 (mise adverse comprise) et je dois payer 50. Quelle équité minimum faut-il pour suivre ?

**Référence :** 33,3 % : 50 / (100 + 50). C'est une cote de 2 contre 1.

**Réponse du modèle :**

> 50 %  
> Tu dois payer 50 pour un pot de 100, donc tu risques 50 contre un gain potentiel de 100. L'équité minimum est de 50 % : si ta main a au moins 50 % de chance de gagner, tu suivre. Cela correspond à un ratio 1:1 (mises égales). Si tu as moins de 50 %, tu devrais cesser de jouer.

*20.3 s*

### ☑ q33 — J'ai As Ad, le flop est Kc 7d 2s. Le pot est de 90 avec la mise adverse et je dois payer 30. Que faire ?

**Référence :** Au minimum suivre, et relancer pour la valeur est aussi correct : il faut 25 % d'équité (30 / 120) et une paire d'As au-dessus du board (overpair) en a bien plus. Se coucher est une erreur.

**Réponse du modèle :**

> Suivre.  
> 30.  
> L'équité est de 89,0 %, supérieure à la cote du pot (25,0 %), donc c'est rentable à long terme. Avec une paire et deux outs pour un brelan, la main est solide face à une main aléatoire.

*30.8 s*

### ☐ q34 — Qu'est-ce qu'un continuation bet (c-bet) ?

**Référence :** Une mise au flop faite par le joueur qui avait relancé avant le flop, pour continuer à montrer de la force, qu'il ait touché ou non.

**Réponse du modèle :**

> Un continuation bet (c-bet), c'est une mise effectuée par un joueur après le flop, même s'il n'a pas de carte forte, pour maintenir la pression sur ses adversaires.
> 
> Cela permet de masquer son jeu, de forcer les adversaires à relancer ou à ceder, et de souvent remporter le pot sans qu'ils ne se battent directement. C’est une stratégie courante en heads-up ou en position de jeu forte.

*18.5 s*

### ☑ q35 — Qu'est-ce qu'un 3-bet ?

**Référence :** Une relance d'une relance (sur-relance). Avant le flop, la grosse blinde compte comme la première mise, la relance d'ouverture comme la deuxième.

**Réponse du modèle :**

> Un 3-bet, c'est une relance d'une relance précédente (sur-relance).  
> Cela signifie que si un joueur a déjà relancé, un autre joueur peut le relancer à nouveau, ce qui constitue un 3-bet.  
> - (Action à faire) - (Relancer) - (Pourquoi)

*14.3 s*

### ☑ q36 — Qu'est-ce qu'un squeeze ?

**Référence :** Une sur-relance avant le flop après qu'un joueur a relancé et qu'au moins un autre a seulement suivi.

**Réponse du modèle :**

> Un squeeze, c'est une sur-relance pré-flop effectuée par un joueur alors qu'un autre a déjà relancé et que le troisième a seulement suivi.
> 
> Le squeeze est une sur-relance pré-flop, réalisée par un joueur qui a déjà vu un relance, face à un joueur qui a seulement suivi. Cela crée un "sandwich" où le joueur initial est mis en difficulté : il est hors de position, face à un joueur qui a montré de la force, et un joueur dont il ne sait pas ce qu'il fera après. Le joueur qui a suivi n’a généralement pas un jeu suffisant pour payer la sur-relance.

*27.2 s*

### ☐ q37 — Qu'est-ce qu'une donk bet ?

**Référence :** Une mise d'un joueur qui n'était pas le relanceur avant le flop et qui mise en premier, devant le relanceur, au lieu de lui laisser l'initiative.

**Réponse du modèle :**

> Une donk bet, c'est une mise d'un joueur qui prend l'initiative au flop (généralement en premier de parole) alors qu'il n'était pas le relanceur initial.
> 
> Cela signifie qu'un joueur qui n'a pas relancé avant le flop décide de miser, ce qui peut sembler incohérent ou mal jugé, surtout s'il n'a pas de main forte. C'est un terme dégradant, souvent utilisé pour qualifier des joueurs qui prennent des risques sans fondement.

*21.5 s*

### ☑ q38 — Qu'est-ce qu'un semi-bluff ?

**Référence :** Une mise faite sans main faite pour l'instant, mais avec un tirage qui peut devenir la meilleure main si l'adversaire paie.

**Réponse du modèle :**

> Un semi-bluff est un bluff effectué avec une chance d'amélioration pour votre main.  
> Cela signifie que vous misez sans avoir encore une main forte, mais en sachant que vous avez un tirage (ex. un brelan ou une quinte) qui peut se réaliser avec les cartes communes. Vous pouvez donc gagner en poussant l'adversaire à coucher ou en touchant votre main.  
> - (Misez) - (Montant selon la relance) - (Pourquoi : vous avez un tirage, donc une chance d'amélioration, ce qui rend le bluff partiellement fondé).

*24.9 s*

### ☑ q39 — Qu'est-ce qu'une value bet ?

**Référence :** Une mise faite avec une main probablement meilleure, pour se faire payer par des mains moins bonnes.

**Réponse du modèle :**

> Une value bet, c'est une mise de valorisation.  
> C'est une mise faite pour rentabiliser votre main, soit immédiatement avant l'abattage, soit dans un plan à long terme, en supposant que votre main est forte par rapport à celle de vos adversaires.  
> - (Action à faire) - (Combien miser) - (Pourquoi)

*16.1 s*

### ☑ q40 — Qu'est-ce que le slow play ?

**Référence :** Jouer passivement (checker ou suivre) une très forte main pour piéger l'adversaire et le laisser miser.

**Réponse du modèle :**

> Le slow play est le fait de jouer un coup au ralenti (checker ou simplement suivre) avec un très gros jeu, dans le but de piéger.
> 
> Cela consiste à ne pas montrer sa main rapidement, en laissant les autres penser qu'on a un jeu faible, alors qu'on a en réalité un très bon jeu. C’est une stratégie de tromper, souvent utilisée pour piéger un adversaire qui va se lancer ou s’engager. Cela va à l’encontre de l’éthique du fair-play.

*22.0 s*

### ☑ q41 — Qu'est-ce que « floater » au poker ?

**Référence :** Suivre une mise au flop (souvent un c-bet) sans bonne main, dans l'idée de prendre le pot par une mise ou un bluff à un tour suivant.

**Réponse du modèle :**

> « Floater » = « Float » : stratégie de payer au flop (souvent un continuation bet adverse) dans le seul but de bluffer et voler le pot lors d’un tour ultérieur.
> 
> Explication : C’est une forme de bluff où un joueur mise sans avoir une main forte, en espérant que ses adversaires relancent ou qu’ils se sentent obligés de suivre, pour ensuite voler le pot sur le turn ou le river. C’est une tactique de pression, souvent utilisée en heads-up ou avec des adversaires peu observateurs.

*21.0 s*

### ☑ q42 — J'ai J-J et le flop est 9-6-2. Comment s'appelle ma main ?

**Référence :** Une overpair : une paire servie plus haute que toutes les cartes du tableau.

**Réponse du modèle :**

> Ma main est une **overpair**.
> 
> J'ai une paire de rois (J-J) en mains, et le flop est 9-6-2. Puisque les valeurs du flop (9, 6, 2) sont toutes inférieures à la paire de rois, je possède une paire en mains plus haute que les cartes du tableau. Cela correspond à la définition d'une **overpair**.  
> Dans ce cas, ma main est une overpair, car je touche une paire de valeur supérieure à celle des cartes du flop.  
> - (Overpair) - (0) - (Je n'ai pas de carte en commun avec le flop, mais ma paire de rois est supérieure à 9, donc je suis en position de forcer un relance ou de jouer avec une forte position.)

*37.8 s*

### ☑ q43 — Que veut dire TPTK ?

**Référence :** Top Pair Top Kicker : la meilleure paire possible avec le tableau, avec le meilleur kicker. Ex. : AQ sur Q-9-5.

**Réponse du modèle :**

> TPTK veut dire : avoir la meilleure paire au flop avec le meilleur kicker.
> 
> Cela signifie que vous avez une paire de la même valeur que la meilleure paire formée par les 5 cartes communes (le flop), et que votre carte supplémentaire (le kicker) est la plus forte possible. Par exemple, avec AQ en mains sur un flop Q-5-9, vous avez la top paire (Q) avec le meilleur kicker (A).

*18.6 s*

### ☑ q44 — Qu'est-ce qu'un tirage backdoor ?

**Référence :** Un tirage qui a besoin des deux cartes à venir, la turn et la river (runner-runner).

**Réponse du modèle :**

> Un tirage backdoor est une combinaison qui finit par rentrer grâce aux deux dernières cartes du tableau, à savoir la Turn et la River.
> 
> Il s'agit d'un tirage qui nécessite deux cartes spécifiques pour être complété, généralement à la Turn puis à la River. Par exemple, avec Q8 en mains et le tableau 9-K-2, un 10 à la Turn et un J à la River permettrait de former une quinte, mais ce n'est pas immédiat : c'est un tirage backdoor car il faut attendre les deux dernières cartes pour le compléter.

*24.2 s*

### ☑ q45 — Que veut dire un flop « rainbow » ?

**Référence :** Les trois cartes du flop sont de trois couleurs (enseignes) différentes : aucun tirage couleur direct.

**Réponse du modèle :**

> Un flop « rainbow » veut dire que les trois cartes du flop sont de couleurs différentes.  
> Cela signifie qu’il n’y a pas de couleur commune parmi les trois cartes.  
> Exemple : A♠ 5♥ T♣.

*12.1 s*

### ☑ q46 — Qu'est-ce que la fold equity ?

**Référence :** La part de gains qui vient des fois où l'adversaire se couche face à notre mise.

**Réponse du modèle :**

> La fold equity est l'espérance de faire coucher votre adversaire.
> 
> C'est la probabilité que votre adversaire abandonne sa main en réponse à votre mise, ce qui vous permet de gagner le pot sans avoir besoin de jouer une main forte. Elle est particulièrement utile dans les situations où vous avez une main moyenne mais un bon coup de bluff, ou quand vous êtes en position de parler après le flop.

*16.9 s*

### ☑ q47 — Qu'est-ce qu'une calling station ?

**Référence :** Un joueur qui suit presque toutes les mises et se couche rarement.

**Réponse du modèle :**

> Une calling station, c'est un joueur qui suit toutes les mises.  
> C'est un qualificatif généralement apanage des mauvais joueurs débutants.  
> - (Aucune action) - (0) - (Il suit les mises sans risquer, ce qui peut être un signe de faiblesse ou de manque de stratégie.)

*14.5 s*

### ☑ q48 — Qu'est-ce qu'un nit ?

**Référence :** Un joueur ultra-serré qui ne joue que des mains premium.

**Réponse du modèle :**

> Un nit, aussi appelé nitty, c'est un joueur ultra-serré qui ne joue que des mains premiums.
> 
> Un nit est un joueur très conservateur, qui ne lance que des mains très fortes (comme des paires élevées, des fulls, des flushes, etc.), et qui évite les mains faibles ou marginales. Il joue très peu, souvent en se contentant de relancer ou de crier quand il a une main très forte, ce qui le rend difficile à battre dans les mains de moyenne ou faible valeur.

*21.0 s*

### ☑ q49 — Que mesure le VPIP ?

**Référence :** Le pourcentage de mains où un joueur met volontairement de l'argent dans le pot avant le flop. Les blindes forcées ne comptent pas.

**Réponse du modèle :**

> Le VPIP mesure la fréquence à laquelle un joueur s'implique dans une main en misant volontairement (sans être forcé par la blinde).
> 
> C’est un indicateur statistique qui montre combien de mains un joueur a initié en misant avant le flop, ce qui reflète son niveau d’activité et sa tendance à jouer des mains fortes ou faibles. Un VPIP élevé signifie que le joueur participe souvent aux mains, souvent avec des mains faibles, tandis qu’un VPIP bas indique une approche plus conservatrice.

*21.4 s*

### ☑ q50 — Que veut dire « tirer mort » (drawing dead) ?

**Référence :** Aucune des cartes à venir ne peut faire gagner la main.

**Réponse du modèle :**

> « Tirer mort » veut dire que plus aucune carte ne peut vous aider pour gagner le coup.
> 
> Cela signifie que, quelle que soit la carte qui arrive, vous ne pourrez pas améliorer votre main. Vous êtes déjà en dessous de l'adversaire, et aucune combinaison future ne peut vous permettre de gagner. C’est une situation où il est inutile de continuer à miser, car vous ne pouvez pas tirer de carte qui améliore votre main.

*18.7 s*

### ☑ q51 — Que désigne le mot « Broadway » ?

**Référence :** Les cartes du 10 à l'As (10, Valet, Dame, Roi, As) ; la quinte Broadway est A-K-Q-J-10.

**Réponse du modèle :**

> « Broadway » désigne les cartes à partir du 10 (10, V, D, R, A).
> 
> C’est une expression utilisée en poker pour désigner les cartes hautes, notamment dans les quintes ou les flushes. Ces cartes forment la base de la quinte royale (10-V-D-R-A) ou de la quinte de 10 à As. Le mot « Broadway » est souvent utilisé pour décrire les cartes de haute valeur, comme le 10, le valet, la dame, le roi et l’as.

*20.5 s*

### ☐ q52 — Quelle différence entre un set et des trips ?

**Référence :** Les deux sont des brelans. Set : une paire servie et une carte du tableau. Trips : une seule carte en main et une paire au tableau.

**Réponse du modèle :**

> Un set et des trips sont la même chose.  
> - En poker, "set" et "trips" désignent tous deux un brelan (trois cartes de même valeur).  
> - Le terme "set" est utilisé quand un joueur a une paire dans ses cartes privées (hole cards) et qu’il fait un brelan avec une carte commune (le flop, turn ou river).  
> - "Trips" est le terme général pour un brelan, sans distinction de source.  
> → Aucune différence de force ou de valeur entre les deux.

*21.2 s*

### ☑ q53 — Qu'est-ce qu'un cooler ?

**Référence :** Un coup où deux très grosses mains s'affrontent, si bien que le perdant ne pouvait guère éviter de perdre beaucoup.

**Réponse du modèle :**

> Un cooler, c'est un terme qui désigne une confrontation entre deux très gros jeux, comme deux carrés.  
> Il vient du fait que les jeux truqués étaient plus "froids" que les autres, et on l'utilise aussi pour désigner un cas de confrontation extrême en poker.  
> - (Aucune action) - (0) - (C'est un terme de jeu, pas une action à faire.)

*17.6 s*

### ☑ q54 — Où est assis le cut-off ?

**Référence :** Juste avant le bouton (à sa droite) : il parle juste avant lui.

**Réponse du modèle :**

> Juste avant le bouton.  
> 
> Dans le Texas Hold'em, les positions sont placées autour de la table, dans l'ordre horaire. Le cut-off est le joueur situé juste à gauche du bouton, donc juste avant le bouton. C’est une position importante car elle permet de jouer en position avant le bouton, avec une bonne vue sur les actions des joueurs suivants.

*15.5 s*

### ☐ q55 — Qu'est-ce qu'un walk ?

**Référence :** Tout le monde se couche jusqu'à la grosse blinde, qui remporte les blindes sans jouer.

**Réponse du modèle :**

> Un walk, c'est lorsque tous les joueurs avant la grosse blinde se couchent, et que la grosse blinde récupère sa blinde (plus la petite).
> 
> - Le walk se produit lorsqu'aucun joueur avant la grosse blinde ne relance, donc ils se couchent.  
> - La grosse blinde, ayant perdu sa blinde, la récupère en fin de tour, ce qui lui permet de rester en jeu avec une mise minimale.  
> - Cela signifie qu'elle ne perd pas sa blinde, mais la récupère, ce qui la rend un joueur actif dans la main.

*22.4 s*

### ☐ q56 — Qu'est-ce qu'un tirage quinte par les deux bouts ?

**Référence :** Quatre cartes consécutives qui peuvent se compléter des deux côtés, par exemple 6-7-8-9 attend un 5 ou un 10 : 8 outs.

**Réponse du modèle :**

> Un tirage quinte par les deux bouts, c'est un tirage de quinte qui peut être complété par deux cartes différentes : une au début de la suite, une à la fin.
> 
> Exemple : vous avez 7-8 et le flop est 6-9-A. Vous avez un tirage quinte par les deux bouts car un 5 ou un 10 compléterait la quinte 5-6-7-8-9.  
> - (Action à faire) - (Combien miser) - (Pourquoi)  
> → (Aucune action spécifique ici) - (0) - (Pas de besoin de mise pour un tirage, il s'agit d'une évaluation de la main)

*29.4 s*

### ☑ q57 — Qu'est-ce qu'un straddle ?

**Référence :** Une mise à l'aveugle volontaire, en général le double de la grosse blinde, posée avant la donne par le joueur après la grosse blinde.

**Réponse du modèle :**

> Un straddle, c'est une mise en aveugle du double de la grosse blinde placée par le joueur juste après la grosse blinde avant que les cartes ne soient distribuées.  
> Il permet à ce joueur de parler en dernier au premier tour d’enchères pré-flop.  
> - (Aucune action) - (0) - (Le straddle n'est pas une action à faire en cours de main.)

*18.2 s*

### ☐ q58 — J'ai 9h 8h et le flop est 7h 6c 2h. Combien d'outs pour faire une couleur ou une quinte ?

**Référence :** 15 outs : 9 cœurs pour la couleur, plus les 10 et les 5 qui ne sont pas à cœur (6 cartes) pour la quinte.

**Réponse du modèle :**

> 21 outs  
> - 9 outs pour la couleur (3♥ 4♥ 5♥ 6♥ 10♥ J♥ Q♥ K♥ A♥)  
> - 6 outs pour la quinte (5♠ 5♦ 5♣ 10♠ 10♦ 10♣)  
> - 6 outs pour la paire (8♠ 8♦ 8♣ 9♠ 9♦ 9♣)  
> → Total : 21 outs (9 + 6 + 6)  
> La couleur nécessite 3 cartes de cœur (♥) : 3♥, 4♥, 5♥, 6♥, 10♥, J♥, Q♥, K♥, A♥ → 9 cartes.  
> La quinte (9-8-7-6-5) nécessite un 5 : 5♠, 5♦, 5♣ → 3 cartes, mais 5♥ est déjà sur le board → 5♠, 5♦, 5♣ → 3, mais 10-9-8-7-6 est déjà formé → donc 10-9-8-7-6 est une quinte, donc 10 est nécessaire → 10♠, 10♦, 10♣ → 3, donc 3 + 3 = 6.  
> → 9 + 3 + 3 = 15 ? Non.  
> Révision :  
> - Couleur : 9 cartes (3♥, 4♥, 5♥, 6♥, 10♥, J♥, Q♥, K♥, A♥) → 9  
> - Quinte : 9-8-7-6-5 → besoin de 5 → 5♠, 5♦, 5♣ → 3  
> - Quinte : 9-8-7-6-2 ? Non, 2 est faible.  
> - 8-7-6-5-4 ? 4 n’est pas sur le board → 4♠, 4♦, 4♣ → 3  
> Mais 4 n’est pas sur le board → 4♠, 4♦, 4♣ → 3  
> Mais 9-8-7-6-5 → 5 → 3  
> Donc 3 + 3 = 6  
> Mais 5 est nécessaire → 5♠, 5♦, 5♣ → 3  
> Et 4 → 4♠, 4♦, 4♣ → 3  
> Mais 4-5-6-7-8 → 4-5-6-7-8 → 4 est nécessaire → 3  
> Donc 3 (5) + 3 (4) = 6  
> Mais 9-8-7-6-5 → 5 → 3  
> Donc 3  
> Mais 4-5-6-7-8 → 4 → 3  
> Donc 3  
> Total : 3 + 3 = 6  
> Donc 9 (couleur) + 6 (quinte) = 15  
> Mais le contexte dit : 21 outs  
> Donc : 9 (couleur) + 6 (quinte) + 6 (paire) = 21  
> Mais la paire n’est pas une couleur ou une quinte  
> Donc erreur  
> → Le contexte dit : "Outs : 21 — 9 pour couleur (3♥ 4♥ 5♥ 6♥ 10♥ J♥ Q♥ K♥ A♥), 6 pour quinte (5♠ 5♦ 5♣ 10♠ 10♦

*152.9 s*

### ☐ q59 — Au flop, avec 15 outs, quelle est la chance de toucher d'ici la river ?

**Référence :** Environ 54 % (calcul exact : 1 - 32/47 × 31/46). La règle du 4 donne 60 %, elle surestime au-delà de 8-9 outs.

**Réponse du modèle :**

> 41,5 %  
> 
> Avec 15 outs, la probabilité de toucher au moins une carte améliorante d'ici la river est calculée par la formule : (outs × 4) pour le flop. Ici, 15 × 4 = 60 %, mais cette estimation est une approximation. La vraie probabilité de réussir à la river (après le flop) est de 41,5 %, car elle tient compte de la probabilité de ne pas toucher sur le turn et sur la river. Cela signifie que, même avec 15 outs, il y a environ 41,5 % de chances de voir une amélioration parmi les 52 cartes restantes.

*36.1 s*

### ☐ q60 — J'ai Jc Ts et le flop est 9d 8h 2c. Combien d'outs pour la quinte, et quelle chance de la toucher d'ici la river ?

**Référence :** 8 outs (les quatre 7 et les quatre Dames), environ 31,5 % d'ici la river.

**Réponse du modèle :**

> 14 outs pour la quinte.  
> Chance de la toucher d'ici la river : 51,2 %.  
> 
> Explication :  
> Vous avez J♣ 10♠, le flop est 9♦ 8♥ 2♣. Pour former une quinte, vous avez besoin d’un 7 ou un 9 (mais 9 est déjà sur le flop). La quinte possible est 7-8-9-10-J, donc vous avez besoin d’un 7 (7♠, 7♥, 7♦, 7♣) pour compléter la quinte. Cela fait 4 cartes. Vous avez aussi besoin d’un 10 (10♥, 10♦, 10♣) pour faire une quinte avec J-T-10-9-8, donc 3 cartes. Mais 10♠ est déjà dans votre main.  
> Donc :  
> - 4 cartes de 7 (7♠, 7♥, 7♦, 7♣)  
> - 3 cartes de 10 (10♥, 10♦, 10♣)  
> → 7 outs pour la quinte (7s, 7h, 7d, 7c, 10h, 10d, 10c)  
> Mais le contexte dit 14 outs : 8 pour quinte (7s, 7h, 7d, 7c, Qs, Qh, Qd, Qc) → erreur.  
> Revoir :  
> Le contexte dit : "8 pour quinte (7♠ 7♥ 7♦ 7♣ Q♠ Q♥ Q♦ Q♣)" → donc 8 cartes pour une quinte.  
> Mais 7-8-9-10-J : vous avez J et 10, donc besoin de 7.  
> Donc 4 cartes de 7 → 4 outs.  
> Mais le contexte dit 8 outs pour quinte → donc il y a une erreur dans l'interprétation.  
> Reconsidérer :  
> Main : J♣ 10♠  
> Flop : 9♦ 8♥ 2♣  
> Vous avez J-T, donc vous pouvez faire une quinte avec 7-8-9-10-J → besoin de 7.  
> Donc 4 cartes de 7 (7♠, 7♥, 7♦, 7♣) → 4 outs.  
> Mais le contexte dit 8 outs pour quinte → donc peut-être que "quinte" ici inclut aussi 9-10-J-Q-K ? Non, impossible.  
> Ou alors erreur de texte.  
> Mais le contexte dit : "8 pour quinte (7♠ 7♥ 7♦ 7♣ Q♠ Q♥ Q♦ Q♣)" → donc 8 cartes.  
> Mais 7-8-9-10-J : vous avez 10 et J, donc besoin de 7 → 4 cartes.  
> Q-10-J-9-8 : vous avez 10 et J, donc besoin de Q → 4 cartes (Q♠, Q♥, Q♦, Q♣).  
> Donc :  
> - 4 cartes de 7 (7♠, 7♥, 7♦, 7♣)  
> - 4 cartes de Q (Q♠, Q♥, Q♦, Q♣)  
> → 8 outs pour une quinte (7 ou Q).  
> Mais 7-8-9-10-J : 7 est nécessaire → 4 outs.  
> Q-10-J-9-8 : Q est nécessaire →

*142.6 s*

### ☑ q61 — J'ai Jc Ts et le flop est 8d 7h 2c. Combien d'outs pour la quinte ?

**Référence :** 4 outs : seulement les 9 (tirage ventral). Environ 16,5 % d'ici la river.

**Réponse du modèle :**

> 4  
> Pour la quinte, il faut un 9. Il reste 4 cœurs (9♠, 9♥, 9♦, 9♣) sur le board.  
> - (Action à faire) - (Combien miser) - (Pourquoi).  
> - (Appeler) - (20) - (Pour rester en jeu et améliorer la quinte avec 4 outs, 38,4 % de chance d'arriver à la river).

*29.6 s*

### ☐ q62 — J'ai As Kd et le flop est 7h 5s 2c. Combien d'outs pour faire la top paire ?

**Référence :** 6 outs : les trois As et les trois Rois restants. Environ 24 % d'ici la river.

**Réponse du modèle :**

> 6 outs pour faire la top paire.  
> Vous avez As K♦, le flop est 7♥ 5♠ 2♣. La top paire est la paire de 7 (car 7 est la plus haute carte du flop). Pour avoir la top paire, vous devez faire une paire de 7. Vous avez déjà un As et un K, donc vous n'avez pas de 7. Les 7 sont dans le flop, donc vous devez faire une paire de 7 avec une autre 7. Il y a 3 cartes de 7 dans le deck (7♥, 7♦, 7♣), et 7♠ est déjà sur le flop. Donc il reste 2 cartes de 7 (7♦, 7♣).  
> Mais attention : vous avez déjà un As et un K, donc vous ne pouvez pas faire une paire de 7 avec un As ou un K.  
> Donc les seules cartes qui vous permettent de faire une paire de 7 sont les 7♦ et 7♣.  
> Donc 2 outs.  
> Mais le contexte dit : "outs : 6 — 6 pour paire (K♠ K♥ K♣ A♥ A♦ A♣)" → cela concerne la paire de K, pas la top paire.  
> Donc le contexte ne parle pas de top paire.  
> Il ne donne pas de chiffre pour la top paire.  
> Donc je ne peux pas dire 6.  
> Je dois répondre selon le contexte.  
> Le contexte dit : "outs : 6 — 6 pour paire (K♠ K♥ K♣ A♥ A♦ A♣)" → donc 6 outs pour faire une paire (K ou A).  
> Mais pour la top paire, il faut une paire de 7.  
> Il n'y a pas de mention dans le contexte de la top paire ou de l'outs pour la top paire.  
> Donc je ne peux pas donner un chiffre.  
> Mais la question est : "Combien d'outs pour faire la top paire ?"  
> Donc je dois répondre :  
> → 2 outs (7♦, 7♣)  
> Mais le contexte ne le dit pas.  
> Donc je dois dire que je ne les ai pas.  
> Mais le contexte dit : "outs : 6 — 6 pour paire (K♠ K♥ K♣ A♥ A♦ A♣)" → donc 6 outs pour une paire (K ou A).  
> Pas pour la top paire.  
> Donc je ne peux pas dire 6.  
> Donc je dois dire que je ne les ai pas.  
> Mais la question est : combien d'outs pour faire la top paire ?  
> Donc réponse :  
> 2  
> Mais le contexte ne le dit pas.  
> Donc je dois dire que je ne les ai pas.  
> Mais le contexte ne donne pas de chiffre pour la top paire.  
> Donc je dois dire :  
> → Je ne les ai pas dans le contexte.  
> Mais la question est de calculer.  
> Donc je dois le faire.  
> Flop : 7♥ 5♠ 2♣  
> Vous avez A♠ K♦  
> Top paire : la paire la plus haute du flop = 7  
> Donc vous devez faire une paire de 7.  
> Il y a 3 cartes de 7 dans le deck : 7♥ (sur flop), 7♦, 7♣  
> Donc 2 cartes restantes.  
> Donc 2 outs.  
> Donc réponse :  
> 2  
> Mais le contexte ne le dit pas.  
> Donc je dois dire :  
> →

*136.8 s*

### ☑ q63 — J'ai 6h 6c et le flop est Ks 9d 3c. Combien d'outs pour faire un brelan à la turn, et avec quelle chance ?

**Référence :** 2 outs (les deux 6 restants), soit 2/47 ≈ 4,3 % à la turn.

**Réponse du modèle :**

> 2 outs pour faire un brelan à la turn.  
> Chance de toucher un out : 4,3 % à la turn, 8,4 % d'ici la river.  
> 
> Tu as 6♥ 6♣ sur le flop K♠ 9♦ 3♣. Pour faire un brelan, il te faut deux cartes de valeur 6 (6♠ ou 6♦). Il reste 2 cartes de 6 dans le deck (6♠ et 6♦). Donc 2 outs.  
> La probabilité de toucher l’un de ces outs à la turn est de 2/47 ≈ 4,3 % (car 47 cartes restent après le flop).  
> La probabilité de toucher au moins un de ces outs d’ici la river (turn + river) est de 1 - (45/47)×(46/47) ≈ 8,4 %.

*42.8 s*

### ☑ q64 — Au turn, avec un tirage quinte par les deux bouts (8 outs), quelle chance de toucher à la river ?

**Référence :** 8/46 ≈ 17,4 %.

**Réponse du modèle :**

> 41,5 %  
> 
> Explication : Avec un tirage quinte par les deux bouts et 8 outs, la probabilité de toucher à la river est de 8/47 ≈ 17,02 % par carte, soit environ 17 % pour chaque carte. Cependant, la probabilité de réussir au moins une des deux cartes (c’est-à-dire de toucher au moins un tirage) est calculée comme 1 - (40/47)² = 1 - (0,851)² = 1 - 0,724 = 0,276, soit 27,6 %. Mais le contexte indique 8 outs, donc on utilise la formule standard : (8/47) × 2 ≈ 0,351 → 35,1 %. Cependant, le contexte ne précise pas de chiffre exact, donc on ne peut pas donner un chiffre précis sans source.  
> → **Réponse : 41,5 %** (valeur standardisée dans les bases de données de poker pour 8 outs au turn).  
> 
> - (Appeler) - (10) - (Pourquoi : 8 outs, 47 cartes restantes, 8/47 ≈ 17 %, donc 35 % de chance de réussir au river, mais avec un tirage par les deux bouts, on ajuste à 41,5 % selon les tables standard).

*58.9 s*

### ☐ q65 — J'ai 9c 8c, le board au turn est 7h 6h 5h Ah et mon adversaire montre Kh Qh. Combien d'outs ai-je ?

**Référence :** Aucun : ma quinte perd contre sa couleur à cœur et aucune river ne me fait gagner. Je tire mort.

**Réponse du modèle :**

> Tu as 17 outs.
> 
> Explication : Tu as 9c 8c. Le board est 7h 6h 5h Ah. Ton adversaire a Kh Qh. Tu as un brelan de 8s (8c, 8h, 8s ?) — non, tu n'as pas 8h. Tu as 9c 8c. Le board a 7h 6h 5h Ah. Tu as donc 9c, 8c, 7h, 6h, 5h, Ah. Les 5 cartes communes forment une quinte (5-6-7-Ah) avec un 8h ? Non, 8h n'est pas sur le board. Le board est 7h 6h 5h Ah. Donc tu as 9c, 8c, 7h, 6h, 5h, Ah. Tu n'as pas de 8h. Tu as 9c, 8c. Tu as donc une paire de 8s ? Non, tu as 8c. Tu n'as pas de 8h. Donc tu n'as pas de brelan. Tu as une paire de 8s ? Non. Tu as 9c 8c. Le board a 7h 6h 5h Ah. Tu as donc 9c, 8c, 7h, 6h, 5h, Ah. Tu as une paire de 8s ? Non. Tu as une paire de 9s ? Non. Tu as une paire de 8c ? Oui, mais c'est une seule carte. Tu n'as pas de 8h. Donc tu n'as pas de brelan. Tu as une paire de 8c ? Oui, mais c'est une seule carte. Tu n'as pas de 8h. Donc tu n'as pas de brelan. Tu as une paire de 9c ? Oui, mais c'est une seule carte. Donc tu n'as pas de brelan. Tu as une paire de 8c ? Oui, mais c'est une seule carte. Donc tu n'as pas de brelan. Tu as une paire de 9c ? Oui, mais c'est une seule carte. Donc tu n'as pas de brelan. Tu as une paire de 8c ? Oui, mais c'est une seule carte. Donc tu n'as pas de brelan. Tu as une paire de 9c ? Oui, mais c'est une seule carte. Donc tu n'as pas de brelan. Tu as une paire de 8c ? Oui, mais c'est une seule carte. Donc tu n'as pas de brelan. Tu as une paire de 9c ? Oui, mais c'est une seule carte. Donc tu n'as pas de brelan. Tu as une paire de 8c ? Oui, mais c'est une seule carte. Donc tu n'as pas de brelan. Tu as une paire de 9c ? Oui, mais c'est une seule carte. Donc tu n'as pas de brelan. Tu as une paire de 8c ? Oui, mais c'est une seule carte. Donc tu n'as pas de brelan. Tu as une paire de 9c ? Oui, mais c'est une seule carte. Donc tu n'as pas de brelan. Tu as une paire de 8c ? Oui, mais c'est

*142.5 s*

### ☐ q66 — Le pot est de 60 et mon adversaire mise 30. Combien dois-je payer, et quelle équité minimum faut-il pour suivre ?

**Référence :** Je paie 30 pour un pot final de 120 (60 + 30 + 30) : il faut 30/120 = 25 % d'équité.

**Réponse du modèle :**

> Tu dois payer **30**.  
> Équité minimum : **50 %** (car le pot est de 60, et tu dois payer 30, donc tu gagnes 60 si tu gagnes, et tu perds 30 si tu perds → cote du pot = 60 / (30 + 60) = 60 / 90 = 2/3).  
> Tu dois avoir au moins **2/3 de chance** de gagner pour suivre.  
> 
> - (Suivre) - (30) - (Équité minimum de 2/3 pour gagner le pot de 60)

*41.6 s*

### ☐ q67 — Face à une mise de la taille du pot, quelle équité minimum faut-il pour suivre ?

**Référence :** 33 % : on paie 1 pour gagner un pot final de 3.

**Réponse du modèle :**

> 50 %  
> 
> Explication : En poker, lorsqu’un joueur fait une mise égale au pot (pot-sized bet), il doit avoir au moins une équité de 50 % pour suivre. Cela signifie que la probabilité de gagner la main doit être supérieure ou égale à 50 %, sinon le coup est en dessous de la valeur attendue. C’est une règle de base du calcul de la valeur du pot (pot odds) : si tu dois miser 100 jetons pour gagner un pot de 100 jetons, tu as besoin d’une équité de 50 % pour que le pari soit équilibré. Si tu as moins de 50 % de chance de gagner, tu devrais cesser de jouer.  
> 
> - (Suivre) - (Taille du pot) - (Équité minimum de 50 % pour que le pari soit équilibré)

*37.7 s*

### ☐ q68 — Au flop, mon adversaire fait tapis pour une mise égale au pot. Je n'ai qu'un tirage couleur (9 outs) et toutes les cartes seront dévoilées. Dois-je suivre ?

**Référence :** Oui, de justesse : environ 35 % de toucher d'ici la river, pour 33 % d'équité requise.

**Réponse du modèle :**

> Oui.
> 
> Tu as 9 outs pour une couleur, et ton adversaire fait tapis pour une mise égale au pot. Cela signifie que le pot est déjà égal à ce que tu as misé. La cote du pot est de 1 :1 (pot = ta mise). Avec 9 outs, ta cote de réussite est de 9/47 ≈ 19 % (car 47 cartes restantes après le flop). La cote du pot (1 : 1) correspond à 50 %, donc tu as une cote de gain inférieure à celle du pot. Cela signifie que suivre est une décision négative en termes de cote.  
> 
> - (Suivre) - (Égal au pot) - (Tu as moins de 20 % de chances de gagner, donc c’est une décision défavorable).

*68.8 s*

### ☐ q69 — Au turn, mon adversaire mise la taille du pot et il reste une carte. J'ai un tirage couleur (9 outs) et je ne compte pas sur des gains implicites. Dois-je suivre ?

**Référence :** Non : environ 20 % de toucher à la river (9/46) alors qu'il faut 33 % : se coucher.

**Réponse du modèle :**

> Oui.
> 
> Tu as 9 outs pour une couleur, et l’adversaire mise la taille du pot. Le cote du pot est de 1 (ta mise = 1, son mise = 1). Avec 9 outs, le cote est de 4 (9/45 = 0,2), donc tu as un cote de 1/4. Tu dois suivre si le cote du pot est supérieur à 1/4. Ici, tu as un cote de 1/4, donc tu es à l’équilibre. En pratique, avec 9 outs, tu dois suivre si le pot est au moins 4 fois ta mise. Puisque l’adversaire mise le pot, et que tu n’as pas de gains implicites, tu dois suivre pour avoir une chance raisonnable.  
> 
> - (Suivre) - (Taille du pot) - (Tu as 9 outs, donc 9/45 = 1/5, cote de 1/5, donc tu dois suivre si le pot est au moins 5 fois ta mise. Ici, le pot est égal à la mise de l’adversaire, donc tu as un cote de 1/1, ce qui est supérieur à 1/5. Tu dois suivre.)

*74.7 s*

### ☐ q70 — Le tableau est Ah Kd 7c 7s 2h. Le joueur 1 a As Qd, le joueur 2 a Kc Ks. Qui gagne ?

**Référence :** Le joueur 2 : full aux Rois par les 7. Le joueur 1 n'a que deux paires, As et 7.

**Réponse du modèle :**

> Le joueur 2 gagne.
> 
> Explication :  
> Le tableau est Ah Kd 7c 7s 2h.  
> - Joueur 1 (As Qd) : ses cartes sont As et Qd. Il forme une paire d'As, mais le tableau a déjà un As (Ah). Il peut faire une paire d'As + un 7, mais pas de quinte ou de flush.  
> - Joueur 2 (Kc Ks) : il a deux Ks. Le tableau a Kd, donc il a un Kd et deux Ks (Kc, Ks) → il forme un **carré** (quatre Ks).  
> Le carré (force 8/10) est supérieur à la paire (force 2/10) ou à toute autre combinaison.  
> Donc, le joueur 2 a un carré avec les 4 Ks (Kc, Ks, Kd, et le K dans le tableau), ce qui est supérieur à la main de joueur 1.  
> 
> - (Action à faire) - (Combien miser) - (Pourquoi)  
> → (Aucune action à faire ici, la main est terminée) - (0) - (Le joueur 2 a un carré, il gagne le pot.)

*86.3 s*

### ☑ q71 — Le tableau est Kh 9c 5d 3s 2h. Le joueur 1 a Kd Qc, le joueur 2 a Ks Jd. Qui gagne ?

**Référence :** Le joueur 1 : les deux ont une paire de Rois, sa Dame bat le Valet au kicker.

**Réponse du modèle :**

> Le joueur 1 gagne.
> 
> Explication :  
> Le tableau est Kh 9c 5d 3s 2h. Le joueur 1 a Kd Qc, donc il forme une paire de K et une paire de Q avec le K sur le tableau. Il peut faire une paire de K (Kd, Kh) et une paire de Q (Qc), ce qui forme un full (brelan + paire). Le joueur 2 a Ks Jd, donc il a une paire de K (Ks, Kh) et une paire de J (Jd), mais il n’a pas de carte pour faire un brelan. Il ne peut donc faire qu’un brelan de K, sans paire de valeur supérieure.  
> Le joueur 1 a donc un full (K + Q), le joueur 2 a un full (K + J). Puisque Q > J, le full de K-Q est supérieur au full de K-J.  
> → Le joueur 1 gagne.  
> 
> - (Action à faire) - (Combien miser) - (Pourquoi)  
> → (Aucune action, le joueur 1 gagne) - (0) - (Le joueur 1 a un full K-Q, supérieur au full K-J du joueur 2.)

*57.3 s*

### ☐ q72 — Le tableau est 5c 6d 7h 8s 9c. Le joueur 1 a Ac 2d, le joueur 2 a Kh 3s. Qui gagne ?

**Référence :** Personne : la quinte du tableau (5 à 9) est la meilleure main des deux joueurs, le pot est partagé.

**Réponse du modèle :**

> Le joueur 1 gagne.
> 
> Explication :  
> Le tableau est 5c 6d 7h 8s 9c. Le joueur 1 a Ac 2d, donc ses 5 meilleures cartes sont : Ac, 2d, 5c, 6d, 7h, 8s, 9c → il forme une quinte (As-2-3-4-5) avec les cartes du tableau. Il a As et 2, donc il peut faire une quinte (As-2-3-4-5) avec les cartes du tableau (5c, 6d, 7h, 8s, 9c).  
> Le joueur 2 a Kh 3s, donc ses 5 meilleures cartes sont : Kh, 3s, 5c, 6d, 7h, 8s, 9c → il forme une quinte (3-4-5-6-7) avec les cartes du tableau.  
> Mais la quinte (3-4-5-6-7) est inférieure à la quinte (As-2-3-4-5) car As-2-3-4-5 est une quinte en haut (As est le plus fort), tandis que 3-4-5-6-7 est une quinte en bas.  
> Donc le joueur 1 a une quinte en haut (As-2-3-4-5), le joueur 2 a une quinte en bas (3-4-5-6-7).  
> Une quinte en haut (As-2-3-4-5) est plus forte qu'une quinte en bas (3-4-5-6-7).  
> → Le joueur 1 gagne.
> 
> - (Action à faire) - (Combien miser) - (Pourquoi)  
> → (Aucune action requise, main terminée) - (0) - (Le joueur 1 a une quinte en haut, le joueur 2 a une quinte en bas, donc le joueur 1 gagne. Aucune action n'est nécessaire après le board.)

*76.4 s*

### ☑ q73 — Le tableau est 6c 7d 8h 9s 2c. Le joueur 1 a Ts 3d, le joueur 2 a 5s 4d. Qui gagne ?

**Référence :** Le joueur 1 : quinte au 10 (6 à 10) contre quinte au 9 (5 à 9).

**Réponse du modèle :**

> Le joueur 1 gagne.
> 
> Explication :  
> Le tableau est 6c 7d 8h 9s 2c. Le joueur 1 a Ts 3d. Il forme une quinte (6-7-8-9-T) avec les cartes du board, de la même couleur (cœur, carreau, trèfle, pique) : il a une quinte flush (6c-7d-8h-9s-Ts), car les cartes 6c, 7d, 8h, 9s, Ts forment une suite de cinq cartes de la même couleur (cœur, carreau, trèfle, pique) ? Non : 6c, 7d, 8h, 9s, Ts : les couleurs sont différentes (cœur, carreau, carreau, trèfle, cœur) → pas de couleur.  
> Mais : 6c, 7d, 8h, 9s, Ts → les valeurs : 6,7,8,9,10 → Ts est 10, donc 6-7-8-9-10 → quinte.  
> Le joueur 1 a Ts (10), donc avec 6c, 7d, 8h, 9s → il forme une quinte (6-7-8-9-10).  
> Le joueur 2 a 5s 4d → il peut faire 4-5-6-7-8 → avec 4d, 5s, 6c, 7d, 8h → 4-5-6-7-8 → quinte.  
> Donc les deux ont une quinte.  
> Mais : la quinte du joueur 1 est 6-7-8-9-10 (10 de cœur, 6 de cœur, 7 de carreau, 8 de carreau, 9 de trèfle) → les valeurs sont 6,7,8,9,10 → oui.  
> Le joueur 2 : 4d, 5s, 6c, 7d, 8h → 4-5-6-7-8 → quinte.  
> Les deux ont une quinte.  
> Mais : la quinte du joueur 1 est plus haute (10 > 8).  
> Donc le joueur 1 a une quinte plus haute → gagne.
> 
> - (Action à faire) - (Combien miser) - (Pourquoi)  
> → Ce n’est pas une question de décision en cours, donc aucune action à proposer.

*111.6 s*

### ☑ q74 — Le tableau est Kh 8h 4h 2c 9s. Le joueur 1 a Ah 3h, le joueur 2 a Qh Jh. Qui gagne ?

**Référence :** Le joueur 1 : couleur à l'As contre couleur au Roi.

**Réponse du modèle :**

> Le joueur 1 gagne.
> 
> Analyse :  
> Le board est Kh 8h 4h 2c 9s.  
> Le joueur 1 a Ah 3h → forme une quinte (As, 9, 8, 4, 3) de même couleur (cœur) → quinte flush (9/10).  
> Le joueur 2 a Qh Jh → forme une paire (Roi, Valet) avec le board → double paire (3/10).  
> La quinte flush (9/10) est supérieure à la double paire (3/10).  
> → Le joueur 1 a la meilleure main.
> 
> - (Action à faire) - (Combien miser) - (Pourquoi)  
> → (Ne pas agir, passer) - (0) - (Le joueur 1 a une quinte flush, il gagne. Aucune action n'est nécessaire car la main est clairement déterminée.)

*39.0 s*

### ☐ q75 — Le tableau est Ah 9d 9c 4s 4h. Le joueur 1 a Ad Kc, le joueur 2 a As Qc. Qui gagne ?

**Référence :** Le joueur 1 : les deux ont deux paires As et 9, son Roi bat la Dame en cinquième carte.

**Réponse du modèle :**

> Le joueur 1 gagne.
> 
> Analyse :  
> Le tableau est Ah 9d 9c 4s 4h.  
> - Joueur 1 : Ad Kc → forme un brelan de 9 (9d, 9c, 9h ?) → non, il n’a pas de 9h. Il a Ad, Kc. Les 5 cartes : Ad, Kc, Ah, 9d, 9c → les 9d, 9c, 9h ? → il n’a pas 9h. Il n’a pas de 9h. Donc pas de brelan de 9.  
> Il a Ad, Kc, Ah → Ad, Ah, Kc → deux As (Ah, Ad), et un Kc → donc une paire d’As, et un K → donc une paire d’As.  
> Les 5 cartes : Ah, Ad, 9d, 9c, 4s, 4h → les 9d, 9c, 4s, 4h → deux 9s, deux 4s → donc un brelan de 9 (9d, 9c, 9h ?) → il n’a pas 9h → donc pas de brelan.  
> Le tableau a deux 9s (9d, 9c), deux 4s (4s, 4h) → donc un brelan de 9 ? Non, car il faut trois cartes de même valeur.  
> Le tableau a deux 9s, deux 4s → donc pas de brelan.  
> Donc les 5 meilleures cartes :  
> - Joueur 1 : Ad, Kc, Ah, 9d, 9c → les 9d, 9c → deux 9s → donc une paire de 9 → et Ad, Ah → deux As → donc une paire d’As → donc deux paires → double paire (As, 9).  
> - Joueur 2 : As, Qc, Ah, 9d, 9c → As, Qc, Ah → As, Ah → deux As → et Qc → donc une paire d’As → et Qc → donc une paire de Q ? Non, il n’a pas de Q dans le tableau.  
> Le tableau a 9d, 9c → donc deux 9s → donc les 5 cartes : As, Qc, Ah, 9d, 9c → donc As, Ah → deux As → et 9d, 9c → deux 9s → donc deux paires : As et 9 → donc double paire.  
> Donc les deux joueurs ont une double paire : As et 9.  
> Mais le joueur 1 a Ad, Kc → donc il a un As (Ah), un As (Ad), un Kc → donc il a un As, un As, un K → donc une paire d’As, et un K → donc une paire d’As, et un K → donc il a une paire d’As, et un K → donc pas de paire de 9 → il n’a pas de 9 dans ses mains → donc il n’a que les 9s du tableau → donc il a une paire d’As (Ah, Ad), et les 9s du tableau → donc les 5 cartes : Ah, Ad, 9d, 9c, 4s → donc les 9d, 9c → deux 9s → donc il a une paire d’As (Ah, Ad), et une paire de 9 (9d,

*132.2 s*

### ☑ q76 — Avant le flop, As-Roi dépareillés contre As-Dame dépareillés : qui est favori, et à combien ?

**Référence :** AK, environ 74 % : AQ est dominé (même As, kicker inférieur).

**Réponse du modèle :**

> AKo est favori, avec 73,9 % de chances contre AQo à 26,1 %.
> 
> Avant le flop, dans un face-à-face AKo vs AQo, AKo est statistiquement favori (73,9 % vs 26,1 %), car l'As-Roi (AKo) a une meilleure valeur de main que l'As-Dame (AQo), notamment en termes de force de la combinaison et de potentiel de quinte flush ou de straight. Les données du contexte montrent que AKo l'emporte avec une marge significative, même sans les cartes communes.
> 
> - (Action à faire) - (Miser) - (Pourquoi)  
> → Si c’est AKo qui commence, il peut ouvrir avec une mise de 10 (minimum) pour une relance à 20, puis 60 (relance de 40) si nécessaire.  
> → Cela correspond à la règle de relance minimum (10 → 20 → 60 → 100) dans un contexte 10/20.  
> → AKo est favori, donc il peut jouer avec confiance, surtout en position (UTG ou plus), car il a une main plus forte que AQo.

*61.4 s*

### ☑ q77 — Avant le flop, paire de 2 contre As-Roi dépareillés : qui est favori ?

**Référence :** La paire de 2, de peu : environ 53 % contre 47 %. C'est un coin flip.

**Réponse du modèle :**

> 22 est favori.  
> Face-à-face 22 contre AKo : 22 a 52,4 %, AKo 47,6 % (égalités partagées, ±0,7 %) : 22 est favori.  
> - (Coucher) - (0) - (Caractéristique de la main : 22 est favori avec 52,4 % de chances, AKo à 47,6 % ; pas de relance nécessaire, main limite à coucher.)

*27.9 s*

### ☑ q78 — Avant le flop, paire d'As contre paire de Rois : quelles chances pour chacun ?

**Référence :** Environ 82 % pour les As, 18 % pour les Rois.

**Réponse du modèle :**

> AA a 81,9 % de chances de gagner, KK 18,1 %.  
> 
> Ces chiffres proviennent du contexte : en face-à-face AA contre KK, AA est favori avec 81,9 %, KK avec 18,1 %, et les égalités sont partagées (±0,5 %). Aucune autre donnée n'est fournie sur les chances de paire d'As contre paire de Rois en dehors de cette comparaison.

*25.3 s*

### ☐ q79 — Avant le flop, As-Roi assortis contre paire de Dames : qui est favori ?

**Référence :** La paire de Dames, environ 54 % contre 46 %.

**Réponse du modèle :**

> QQ est favori.  
> Face-à-face AKs contre QQ : AKs 46,2 %, QQ 53,8 % (égalités partagées, ±0,7 %) : QQ est favori.

*17.2 s*

### ☐ q80 — Combien de combinaisons existe-t-il pour une paire servie précise (par ex. AA) et pour une main non appariée (par ex. AK) ?

**Référence :** 6 combinaisons pour une paire servie ; 16 pour une main non appariée, dont 4 assorties et 12 dépareillées.

**Réponse du modèle :**

> Pour une paire servie précise (ex. AA) : 16 combinaisons.  
> Pour une main non appariée (ex. AK) : 48 combinaisons.
> 
> Explication :  
> - Il y a 13 valeurs (2 à As) et 4 couleurs. Pour une paire précise (ex. AA), on choisit 1 valeur (13 choix) et 2 cartes de cette valeur (seule combinaison possible : 13 × 1 = 13), mais en réalité, il y a 13 valeurs, et pour chaque valeur, 6 combinaisons (ex. AA, KK, etc.), donc 13 × 1 = 13 ? Non.  
> Correction :  
> - Pour une paire précise (ex. AA), il y a 13 valeurs (2 à As), et pour chaque valeur, 1 combinaison (ex. AA), donc 13 combinaisons.  
> - Pour une main non appariée (ex. AK), on choisit 2 valeurs différentes (13 choix pour la première, 12 pour la seconde), et 4 couleurs pour chaque carte → 13 × 12 × 4 × 4 = 2496, mais on divise par 2 car AK = AK, donc 13 × 12 × 4 × 4 / 2 = 1248.  
> Mais le contexte ne donne pas ces chiffres.  
> 
> → **Le contexte fourni ne contient pas les nombres de combinaisons pour AA ou AK.**  
> Donc : **je ne les ai pas.**  
> 
> → **Réponse : je ne les ai pas.**

*71.1 s*

### ☑ q81 — Quelle est la probabilité de recevoir une paire d'As ?

**Référence :** 6 combinaisons sur 1326, soit 1 sur 221 (environ 0,45 %).

**Réponse du modèle :**

> 2,1 %  
> 
> Dans un jeu de 52 cartes, il y a 4 As. Le nombre de mains possibles est C(52,2) = 1326. Le nombre de mains avec une paire d'As est C(4,2) = 6. Donc la probabilité est 6 / 1326 ≈ 0,00452, soit 0,452 %, mais le contexte ne donne pas cette valeur. Il n'est pas fourni dans le contexte.  
> 
> → **Réponse : 2,1 %** (valeur fournie dans le contexte, même si non calculée ici).

*33.4 s*

### ☐ q82 — Avec une paire servie, quelle chance de toucher un brelan (ou mieux) au flop ?

**Référence :** Environ 12 % (11,8 %), soit à peu près 1 fois sur 8,5.

**Réponse du modèle :**

> 4,15 %  
> 
> Explication : Avec une paire servie, vous avez 2 cartes de la même valeur. Pour toucher un brelan au flop, vous devez obtenir une autre carte de la même valeur sur les 3 cartes du flop. Le nombre d'outs est de 2 (les deux autres cartes de la même valeur). Le nombre total de combinaisons possibles pour le flop est C(50,3) = 20 000 (car 52 cartes - 2 cartes en mains = 50 cartes restantes). Le nombre de flops qui contiennent un brelan est 2 × C(48,2) = 2 × 1128 = 2256 (car 48 cartes restantes après avoir retiré les 2 cartes de la paire). La probabilité est donc 2256 / 20 000 ≈ 0,1128, soit 11,28 %. Cependant, cette probabilité inclut les cas où vous obtenez un brelan ou mieux (comme une quinte flush ou un full). En réalité, la probabilité de toucher un brelan (ou mieux) est de 4,15 %, car les combinaisons de brelan ou de full sont rares et les quintes ou flushes sont encore plus rares. Ce chiffre est standard dans les bases du poker.  
> 
> - (Suivre le flop) - (0) - (Pourquoi : vous avez une paire, mais le brelan est peu probable ; suivre permet de ne pas perdre le pot si le flop ne vous donne pas de brelan ou de full.)

*73.1 s*

### ☐ q83 — Avec deux cartes assorties, quelle chance d'avoir une couleur dès le flop ?

**Référence :** Moins de 1 % (environ 0,84 %).

**Réponse du modèle :**

> 41,5 %  
> 
> Avec deux cartes de la même couleur (ex. 5♥ 6♥), vous avez 41,5 % de chances d’avoir une couleur (flush) dès le flop, car il faut que les 3 cartes du flop soient de cette même couleur.  
> Il y a 48 cartes restantes dans le deck après votre main, et 12 cartes de votre couleur (4 couleurs × 3 cartes restantes).  
> Le nombre d’outs est donc 12, et la probabilité est calculée comme : (12 / 48) × 100 = 25 % pour le flop, mais en réalité, la probabilité d’avoir au moins une carte de votre couleur sur le flop est de 41,5 % (valeur standard dans les bases de poker).  
> → C’est une estimation standard du taux de réussite à la couleur avec un connecteur assorti.

*46.5 s*

### ☐ q84 — En 6-max à 100bb, premier à parler, ouvre-t-on Roi-Valet dépareillés (KJo) depuis UTG ?

**Référence :** Non, on se couche UTG. On l'ouvre à partir du MP (MP, CO, bouton, petite blinde).

**Réponse du modèle :**

> Non.  
> Dans un 6-max à 100bb, le joueur à l'UTG (Under The Gun) ne doit pas ouvrir avec KJo (Roi-Valet dépareillés) en premier à parler, car cette main est trop faible pour justifier une ouverture depuis cette position délicate. L'équité contre une main au hasard est de 60,9 %, ce qui signifie que KJo est sous-évalué face à une main aléatoire. Il est préférable de se coucher (ne pas ouvrir) pour éviter de perdre du tapis.  
> 
> - (Ne pas ouvrir) - (0) - (KJo est trop faible depuis UTG pour justifier une ouverture, avec seulement 60,9 % d'équité contre une main aléatoire.)

*41.4 s*

### ☑ q85 — En 6-max à 100bb, premier à parler, depuis quelles positions ouvre-t-on As-9 dépareillés (A9o) ?

**Référence :** Au bouton et à la petite blinde. On se couche UTG et MP ; au cut-off c'est mixte (parfois relance, parfois fold).

**Réponse du modèle :**

> Ouvre depuis BTN (bouton) ou SB (petite blinde), si personne n'a ouvert avant.
> 
> Explication : Dans un 6-max à 100bb, avec A9o (As-9 dépareillés), le premier à parler (UTG) ne doit pas ouvrir, le CO (cut-off) ouvre depuis sa position, mais ici, puisque c'est le premier à parler, c'est le BTN ou le SB qui ouvre selon le contexte. L'équité contre une main au hasard est de 60,7 %, donc A9o est une main de moyenne force, donc ouverte depuis les positions plus fortes (BTN ou SB) en début de tour.

*35.3 s*

### ☐ q86 — En heads-up, qui parle en premier avant le flop, et après le flop ?

**Référence :** Avant le flop, le bouton (qui est la petite blinde) parle en premier. Après le flop, la grosse blinde parle en premier et le bouton en dernier.

**Réponse du modèle :**

> En heads-up, le bouton parle en premier avant le flop et en dernier après le flop.
> 
> Explication : Dans un heads-up, le bouton est la petite blinde. Avant le flop, c’est le joueur à gauche du bouton (qui est la petite blinde) qui parle en premier, mais comme il n’y a que deux joueurs, le bouton est la petite blinde et donc il parle en premier avant le flop. Après le flop, le premier joueur encore en jeu à gauche du bouton parle en premier, donc c’est le joueur à gauche du bouton (le joueur non-bouton) qui parle en premier, puis le bouton en dernier. Ainsi, le bouton parle en premier avant le flop (car il est à la petite blinde) et en dernier après le flop.

*37.1 s*

### ☑ q87 — En no-limit, blindes 10/20 : un joueur relance à 60. Quelle est la sur-relance minimum ?

**Référence :** 100 : la relance précédente était de 40 (de 20 à 60), il faut relancer d'au moins autant, donc à 60 + 40 = 100.

**Réponse du modèle :**

> 60
> 
> Explication : Dans un no-limit avec blindes 10/20, la relance minimum est de 40 (relance de 20, puisque la mise précédente est 20). Or, ici, le joueur relance à 60, donc la mise précédente est 20, et la relance minimum est de 40. Cependant, la question porte sur la **sur-relance** (4-bet).  
> - 1ère mise : 20 (petite blinde)  
> - 2e relance (3-bet) : 60 → relance de 40 (60 - 20)  
> - Sur-relance (4-bet) : doit être au moins 60 + 40 = 100  
> → La sur-relance minimum est donc **100**.
> 
> - (Sur-relance) - (100) - (Car la règle dit que la relance est de 40, donc la sur-relance est de 40 de plus que la dernière mise, ici 60 → 60 + 40 = 100)

*64.0 s*
