# Évaluation du coach (EV1)

Coach : `qwen3:4b-instruct-2507-q4_K_M` — juge : `llama3.2:3b` — 2026-10-22 14:23 — **3/8 débriefs sans contradiction**, 1/28 faits de la référence présents selon le juge ; **21/24 retrouvés par le code** (bonne action nommée, chiffres cités).

Fichier généré par `python3 evaluate_coach.py` : ne pas modifier à la main. Le joueur prend la mauvaise décision, demande « pourquoi ? », un juge d'une autre famille de modèle coche les faits.

| Contredit | # | Thème | Décision | Faits absents ou contredits |
|:---:|---|---|---|---|
| — | a987c0ed | ouverture | relancer | La bonne réponse est : se coucher. : absent ; 96s : ouvrir en BTN, SB ; se coucher en UTG, MP, CO : absent |
| — | aa6fe0fe | tirage | relancer | La bonne réponse est : suivre ou se coucher. : absent ; Outs : 10 (4 pour quinte, 6 pour paire) : absent ; Chance de toucher à la prochaine carte : 21,3 % : absent ; Chance de toucher d'ici la river : 38,4 % : absent ; Cote du pot : il faut 30,0 % d'équité (payer 6 pour un pot de 14) : absent |
| ✗ | b813e077 | qui_gagne | ton adversaire gagne | Ta meilleure main : Double paire : absent ; Celle de ton adversaire : Paire : contredit |
| — | d8ed1596 | defense_bb | suivre | La bonne réponse est : se coucher. : absent ; Équité de 42o contre la range d'ouverture du SB : 31,8 % : absent ; Équité réalisée hors position (environ 80 %) : 25,4 % : absent ; Cote du pot : il faut 30,0 % d'équité (payer 1.5 pour un pot de 3.5) : absent |
| ✗ | be0bf158 | ouverture | relancer | La bonne réponse est : se coucher. : absent ; 73o : se coucher en UTG, MP, CO, BTN, SB : contredit |
| ✗ | f661fb70 | tirage | suivre | La bonne réponse est : se coucher. : absent ; Outs : 8 (4 pour full, 4 pour quinte) : absent ; Chance de toucher à la prochaine carte : 17,4 % : contredit ; Cote du pot : il faut 33,3 % d'équité (payer 10 pour un pot de 20) : absent |
| ✗ | 76e7f3a2 | qui_gagne | tu gagnes | La bonne réponse est : ton adversaire gagne. : absent ; Ta meilleure main : Paire : absent ; Celle de ton adversaire : Double paire : contredit |
| ✗ | f372688b | defense_bb | se coucher | La bonne réponse est : suivre. : absent ; Équité de ATs contre la range d'ouverture du SB : 59,5 % : absent ; Équité réalisée hors position (environ 80 %) : 47,6 % : absent ; Cote du pot : il faut 30,0 % d'équité (payer 1.5 pour un pot de 3.5) : contredit ; Au-dessus de 55,0 % d'équité, relancer se défend aussi. : contredit |

## Détail

### a987c0ed — ouverture

> Table 6 joueurs, 100 blindes · tu es sous le canon (UTG).
> Tu parles en premier (UTG). Tu as 9♠ 6♠.

Décision : relancer

**Débrief du coach :**

> Parce que tu es en UTG (premier joueur), et que **96s** (assorties) **ne doivent pas être ouvertes en UTG** selon la référence.
> 
> La référence dit clairement :  
> 👉 **"96s : ouvrir en BTN, SB ; se coucher en UTG, MP, CO"**
> 
> Donc en UTG, **la bonne action est de se coucher**.  
> Tu n’as pas le range ni la cote pour relancer ici.  
> 
> Tu as 96s, qui est une main de "cœur" (mid-range), mais **en UTG, tu n’as pas de pouvoir de pression**.  
> Les joueurs à droite (BTN, SB) ont une position avantageuse, et tu es en position faible.
> 
> 👉 **Le relancer ici est une erreur** : c’est hors de la plage d’ouverture autorisée en UTG.
> 
> Tu n’as pas besoin d’aller plus loin.  
> **Se coucher = la bonne action.**  
> 
> Tu as compris ?  
> 👉 Pose-moi une question pour vérifier :  
> 1. Quel est le niveau de position de 96s en UTG ?  
> 2. Quelle est la cote du pot en 100 blindes avec 96s en UTG ?  
> 3. Quelle est la plage d’ouverture autorisée pour 96s en 6-max ?  
> 
> Choisis une seule.

*79.4 s*

### aa6fe0fe — tirage

> Table 6 joueurs, 100 blindes · tu es au bouton (BTN).
> Au flop, ton adversaire mise 6 bb dans un pot de 8 bb. Tu as 4♥ 3♥.
> Board : 5♠ 10♣ A♥ · pot 14 bb, à payer 6 bb.

Décision : relancer

**Débrief du coach :**

> Parce que tu as **21,3 % de chance de toucher** ta main (4♥3♥) au turn, et **38,4 % d’ici la river**, mais tu dois **payer 6 bb pour un pot de 14 bb**, ce qui correspond à une **cote du pot de 30,0 %**.
> 
> Ta main n’a pas assez de chance d’être bonne pour justifier un relance.  
> Tu as **10 outs**, mais ce n’est pas suffisant pour atteindre la cote du pot.
> 
> 👉 **Référence** :  
> - Cote du pot : **30,0 %**  
> - Chance de toucher d’ici la river : **38,4 %**  
> - Cote du pot > chance de toucher → **pas de relance**
> 
> Tu ne peux pas relancer ici.  
> La bonne action est **suivre** (ou se coucher si tu n’as pas de cotes).
> 
> Tu as **21,3 % de chance de toucher** ta main, ce qui est **moins que 30 %**, donc **tu ne gagnes pas**.
> 
> 👉 **Conclusion** : *Tu ne peux pas relancer ici. C’est une erreur.*
> 
> Tu as compris ?  
> Pose-moi une question à choix pour vérifier :  
> 1. Quelle est la cote du pot ?  
> 2. Quel est le pourcentage de chance de toucher ta main ?  
> 3. Quelle est la bonne action ici ?  
> 
> 👉 Réponds-moi avec un numéro.

*83.6 s*

### b813e077 — qui_gagne

> Table 6 joueurs, quiz d'abattage.
> Le coup est fini : abattage. Ton adversaire montre 7♦ 3♥. Tu as 7♥ 4♣.
> Board : 6♦ 10♠ 6♣ 8♥ 4♦.

Décision : ton adversaire gagne

**Débrief du coach :**

> Tu as **7♥ 4♣** et le board est **6♦ 10♠ 6♣ 8♥ 4♦**.
> 
> Regardons ce que chacun peut faire :
> 
> 👉 **Ta main** :  
> - Tu as un **7♥** et un **4♣**.  
> - Le board a un **6♦**, un **10♠**, un **6♣**, un **8♥**, un **4♦**.  
> - Tu peux faire :  
>   - **7♥** + **6♣** → **pair de 6**  
>   - **7♥** + **8♥** → **pair de 8**  
>   - **4♣** + **4♦** → **pair de 4**  
> - Tu as donc **trois paires** possibles → tu as **au moins une paire**, mais surtout : **tu as une double paire** (pair de 6 + pair de 4).  
> ✅ **Double paire** = tu as **deux paires** différentes (6 et 4).
> 
> 👉 **Adversaire** :  
> - Il a **7♦ 3♥**.  
> - Le board a **6♦, 10♠, 6♣, 8♥, 4♦**.  
> - Il peut faire :  
>   - **7♦** → pair de 7  
>   - **6♦** et **6♣** → pair de 6  
> - Donc : **pair de 6** (deux 6)  
> - Il n’a pas de 4 (il a un 3, pas de 4) → pas de pair de 4  
> - Il n’a pas de 8 → pas de pair de 8  
> - Donc : **seulement une paire (de 6)** → **paire seule**
> 
> ✅ Règle : **chacun garde ses 5 meilleures cartes**  
> → Tu as **double paire** (6 + 4) → **meilleure main**  
> → Adversaire a **paire** → **moins forte**
> 
> 👉 **Référence** dit :  
> - **Bonnes actions** : **tu gagnes**  
> - **Actions acceptables** : **aucune**  
> → Donc, **tu devais gagner**  
> → **Adversaire ne gagne pas** → **erreur de décision**
> 
> ❌ Tu as dit : "mon adversaire gagne" → **c’est faux**  
> ✅ Tu devais **gagner**, car **tu as double paire**, **il n’a qu’une paire**.
> 
> 👉 **Conclusion** :  
> Tu as **double paire** → **meilleure main**  
> Il a **paire** → **moins forte**  
> → **Tu gagnes** → **c’est correct**
> 
> Tu as fait une erreur de compréhension de la main.
> 
> Tu as dit : "adversaire gagne" → **c’est faux**  
> → **Tu gagnes** → **c’est vrai**
> 
> Pose-toi cette question :  
> 👉 **Tu as un 4♣ et un 4♦ sur le board → tu as un pair de 4. Tu as un 7♥ et un 6♣ → tu as un pair de 6. Tu as donc deux paires : 6 et 4 → double paire.**  
> 👉 Adversaire a 7♦ → pair de 7, mais pas de 4, pas de 8 → **seulement un pair (6)** → **pas de double paire**.
> 
> ✅ Donc : **tu gagnes** → **c’est juste**.
> 
> Tu as **mal interprété** le résultat.
> 
> 👉 **Question à choix** (utilise l’outil *poser_question*) :  
> **Tu as 7♥ 4♣ et le board a 6♦ 10♠ 6♣ 8♥ 4♦. Quelle est ta meilleure main ?**  
> A) Paire  
> B) Double paire  
> C) Full house  
> D) Straight
> 
> 👉 Réponds-moi avec A, B, C ou D.

*206.2 s*

### d8ed1596 — defense_bb

> Table 6 joueurs, 100 blindes · tu es à la grosse blinde (BB).
> Tout le monde se couche jusqu'au SB, qui relance à 2.5 bb ; les autres se couchent. Tu as 2♣ 4♥.
> Avant le flop · pot 3.5 bb, à payer 1.5 bb.

Décision : suivre

**Débrief du coach :**

> Parce que tu as **2♣ 4♥** contre une range d'ouverture du SB de 6-max à 100bb.
> 
> La référence dit que :
> 
> - Ton **équité face à la range du SB** est de **31,8 %**  
> - L’**équité réalisée hors position** (environ 80 %) est de **25,4 %**  
> - **La cote du pot** (payer 1.5 bb pour un pot de 3.5 bb) demande **30,0 % d’équité**
> 
> 👉 Donc :  
> Tu as **31,8 %** d’équité en théorie (face à la range), **mais** en réalité, sans position, tu as seulement **25,4 %** d’équité.  
> Et **30,0 %** est le seuil minimum pour payer.
> 
> 👉 **Tu n’as pas assez d’équité** pour suivre.  
> Tu dois **te coucher**.
> 
> Tu as **sous-évalué** ton équité réelle en position, car la référence dit que **l’équité réalisée hors position est 25,4 %**, **inférieure** à la cote du pot (30,0 %).
> 
> ➡️ **La bonne action est de se coucher** : c’est la seule action qui respecte les chiffres.  
> 
> Tu as **perdu** si tu as suivi.  
> 
> Tu as compris ?  
> Pose-moi une question pour vérifier.

*88.2 s*

### be0bf158 — ouverture

> Table 6 joueurs, 100 blindes · tu es à la petite blinde (SB).
> Tout le monde s'est couché jusqu'à toi (SB). Tu as 3♠ 7♦.

Décision : relancer

**Débrief du coach :**

> Tu as 3♠ 7♦ (73o), une main dépareillée.  
> Dans une table de 6 joueurs à 100 blindes, la référence dit clairement :  
> → **73o se coucher en UTG, MP, CO, BTN, SB**.  
> 
> Cela signifie que, **à la petite blinde (SB)**, **se coucher est la seule action correcte**.  
> 
> Tu as fait un relance → **erreur**.  
> 
> Pourquoi ?  
> Parce que **73o** a une **cote de gain très faible** (moins de 10 % de chance de gagner le pot contre une main moyenne ou forte).  
> La référence ne reconnaît **aucune action acceptable** (ni relance, ni relance de sécurité) pour cette main à la SB.  
> 
> 👉 **Tu dois te coucher.**  
> 
> C’est le **seul choix en accord avec les chiffres** de la référence.  
> 
> Tu as compris ?  
> Pose-moi une question à choix :  
> 1. Si j'avais 7♠ 8♦, que devrais-je faire à la SB ?  
> 2. Si j'avais 3♠ 7♦, et que le pot est à 100 blinde, quelle action est correcte ?  
> 3. Quelle est la cote de gain de 73o à la SB ?  
> 
> 👉 Réponds-moi avec le numéro.

*73.7 s*

### f661fb70 — tirage

> Table 6 joueurs, 100 blindes · tu es au bouton (BTN).
> Au turn, ton adversaire mise 10 bb dans un pot de 10 bb. Tu as J♠ 10♦.
> Board : 10♥ A♠ A♦ Q♥ · pot 20 bb, à payer 10 bb.

Décision : suivre

**Débrief du coach :**

> Parce que tu as **17,4 % de chance** de toucher une bonne main (full ou quinte), mais **il faut 33,3 % d'équité** pour justifier de payer 10 bb dans un pot de 20 bb.
> 
> Tout simplement :  
> 👉 17,4 % < 33,3 % → **tu n’as pas assez de chances** de gagner pour suivre.
> 
> C’est la règle :  
> **Tu ne suives que si ta cote de succès (chance de gagner) est supérieure à la cote du pot.**  
> Ici, tu es **en dessous** → **se coucher est la bonne action**.
> 
> Tu as 8 outs, donc 17,4 % de chance, comme dit dans la référence.  
> Tu as besoin de 33,3 %, comme dit dans la référence.
> 
> Donc :  
> ❌ Suivre → erreur  
> ✅ Se coucher → bonne action
> 
> Tu comprends ?  
> 👉 Pose-toi cette question :  
> **Si tu as 8 outs, quelle est la cote du pot pour suivre ?**  
> (Choisir l’une des réponses : A) 17,4 %, B) 33,3 %, C) 50 %, D) 100 %  
> → Réponds-moi.

*77.1 s*

### 76e7f3a2 — qui_gagne

> Table 6 joueurs, quiz d'abattage.
> Le coup est fini : abattage. Ton adversaire montre 10♠ 3♠. Tu as 9♣ J♠.
> Board : 7♣ 7♥ 6♠ 3♣ 8♣.

Décision : tu gagnes

**Débrief du coach :**

> Tu as 9♣ J♠.  
> Le board est : 7♣ 7♥ 6♠ 3♣ 8♣.  
> 
> Ton adversaire a 10♠ 3♠.  
> 
> On regarde les **5 meilleures cartes** de chaque joueur, en combinant leurs 2 cartes avec les 5 cartes du board.
> 
> 👉 **Ta main** :  
> - Tu as 9♣, J♠  
> - Board : 7♣, 7♥, 6♠, 3♣, 8♣  
> → Tu as une **paire** (7♠ et 7♥) → tu as **une paire de 7**.  
> → Tu n’as pas de 8 ni de 10, donc **pas de carré, pas de couleur, pas de flush**.  
> → Tu as une **paire de 7**, c’est ta meilleure main.
> 
> 👉 **Main de ton adversaire** :  
> - Il a 10♠, 3♠  
> - Board : 7♣, 7♥, 6♠,  3♣, 8♣  
> → Il a **10♠** et **3♠**  
> → Il a **3♣** sur le board → il a **une paire de 3**  
> → Il a **7♣, 7♥** → **paire de 7**  
> → Donc il a **deux paires** : 7 et 3 → **double paire**  
> → Il n’a pas de 8 ni de 10, donc pas de couleur, pas de flush.
> 
> ✅ **Règle** : chaque joueur garde ses **5 meilleures cartes**.  
> → Le **meilleur** est celui qui a la **meilleure main** (en termes de paire, puis de couleur, etc.).
> 
> 👉 **Double paire > paire**  
> → Donc ton adversaire a **une main meilleure** que la tienne.
> 
> ➡️ **Conclusion** :  
> - Tu as une **paire** (de 7)  
> - Ton adversaire a **double paire** (de 7 et de 3)  
> → **Il gagne**  
> → **Tu perds**
> 
> 👉 **Référence** :  
> - Bonnes actions : **ton adversaire gagne**  
> - Actions acceptables : **aucune**  
> → Donc **tu gagnes** est une **erreur**.
> 
> Tu as donc **perdu** — car **il a une main meilleure**.  
> 
> Tu as compris ?  
> Pose-toi cette question :  
> 👉 Quelle est la meilleure main ici ?  
> A. Paire de 7  
> B. Double paire  
> C. Couleur  
> D. Flush  
> 
> 👉 Réponse ? (Choisir une seule)

*137.7 s*

### f372688b — defense_bb

> Table 6 joueurs, 100 blindes · tu es à la grosse blinde (BB).
> Tout le monde se couche jusqu'au SB, qui relance à 2.5 bb ; les autres se couchent. Tu as A♦ 10♦.
> Avant le flop · pot 3.5 bb, à payer 1.5 bb.

Décision : se coucher

**Débrief du coach :**

> Parce que tu as **59,5 % d'équité** contre la range d'ouverture du SB, et que **le pot te demande 30,0 % d'équité** pour payer 1,5 bb.
> 
> 👉 Tu **as plus** d'équité que ce que le pot exige (59,5 % > 30,0 %), donc **suivre** est la bonne action.
> 
> De plus, **au-dessus de 55,0 % d'équité**, **relancer se défend aussi** — donc **relancer** est acceptable, même si tu ne gagnes pas tout.
> 
> Mais tu **te couches**, alors que **suivre** est la bonne action.
> 
> → C’est une **erreur**.
> 
> Tu as donc **59,5 % d’équité** (référence), donc **suivre** est la bonne décision.  
> Tu n’as pas besoin de relancer. Tu as **suffisamment de chance** de gagner.
> 
> **Pose-toi cette question** :  
> Si tu as A♦10♦ face à une range de SB, et que le pot est de 3,5 bb, est-ce que tu devrais suivre ou te coucher ?  
> A. Suivre  
> B. Relancer  
> C. Se coucher  
> 
> 👉 Réponds-moi.

*82.3 s*
