# Évaluation du coach (EV1)

Coach : `qwen3:4b-instruct-2507-q4_K_M` — juge : `llama3.2:3b` — 2026-10-26 21:40 — **1/30 débriefs sans contradiction**, 6/111 faits de la référence présents selon le juge ; **74/81 retrouvés par le code** (bonne action nommée, chiffres cités).

Fichier généré par `python3 evaluate_coach.py` : ne pas modifier à la main. Le joueur prend la mauvaise décision, demande « pourquoi ? », un juge d'une autre famille de modèle coche les faits.

| Contredit | # | Thème | Décision | Faits absents ou contredits |
|:---:|---|---|---|---|
| ✗ | 27aefb08 | ouverture | relancer | La bonne réponse est : se coucher. : absent ; 96s : ouvrir en BTN, SB ; se coucher en UTG, MP, CO : contredit |
| ✗ | b1c0fc5d | tirage | suivre | La bonne réponse est : se coucher. : absent ; Outs : 4 (4 pour quinte) : contredit ; Les cartes qui ne donnent qu'une paire, une double paire ou un brelan ne comptent pas : elles ne suffisent souvent pas à gagner le coup. : absent ; Chance de toucher à la prochaine carte : 8,5 % : absent ; Chance de toucher d'ici la river : 16,5 % : absent ; Cote du pot : il faut 30,0 % d'équité (payer 6 pour un pot de 14) : absent |
| ✗ | b908cbf4 | qui_gagne | ton adversaire gagne | La bonne réponse est : tu gagnes. : absent ; Celle de ton adversaire : Paire : contredit |
| ✗ | be1d1e8c | defense_bb | suivre | La bonne réponse est : se coucher. : absent ; Équité de 42o contre la range d'ouverture du SB : 31,8 % : contredit ; Équité réalisée hors position (environ 80 %) : 25,4 % : absent ; Cote du pot : il faut 30,0 % d'équité (payer 1.5 pour un pot de 3.5) : absent |
| ✗ | 683b0301 | ouverture | relancer | La bonne réponse est : se coucher. : absent ; 73o : se coucher en UTG, MP, CO, BTN, SB : contredit |
| ✗ | 5f5c9989 | tirage | suivre | La bonne réponse est : se coucher. : absent ; Outs : 4 (4 pour quinte) : contredit ; Les cartes qui ne donnent qu'une paire, une double paire ou un brelan ne comptent pas : elles ne suffisent souvent pas à gagner le coup. : absent ; Chance de toucher à la prochaine carte : 8,5 % : contredit ; Chance de toucher d'ici la river : 16,5 % : absent |
| ✗ | 24d58074 | qui_gagne | tu gagnes | La bonne réponse est : ton adversaire gagne. : absent ; Ta meilleure main : Double paire : contredit |
| ✗ | 93ff8955 | defense_bb | relancer | La bonne réponse est : suivre ou se coucher. : absent ; Équité de 95o contre la range d'ouverture du BTN : 34,2 % : contredit ; Équité réalisée hors position (environ 80 %) : 27,4 % : absent ; Cote du pot : il faut 27,3 % d'équité (payer 1.5 pour un pot de 4) : absent |
| ✗ | 6aa24548 | ouverture | se coucher | La bonne réponse est : relancer. : absent ; J5s : ouvrir en BTN, SB ; se coucher en UTG, MP, CO : contredit |
| ✗ | 23e06b0f | tirage | relancer | La bonne réponse est : suivre ou se coucher. : absent ; Outs : 8 (8 pour quinte) : contredit ; Les cartes qui ne donnent qu'une paire, une double paire ou un brelan ne comptent pas : elles ne suffisent souvent pas à gagner le coup. : absent ; Chance de toucher à la prochaine carte : 17,0 % : contredit ; Chance de toucher d'ici la river : 31,5 % : contredit ; Cote du pot : il faut 19,9 % d'équité (payer 3.3 pour un pot de 13.3) : absent |
| ✗ | c9aaaf08 | qui_gagne | ton adversaire gagne | La bonne réponse est : tu gagnes. : absent ; Celle de ton adversaire : Paire : contredit |
| ✗ | dc3fb321 | defense_bb | se coucher | La bonne réponse est : suivre. : absent ; Équité de A8o contre la range d'ouverture du SB : 52,8 % : contredit ; Équité réalisée hors position (environ 80 %) : 42,2 % : absent ; Cote du pot : il faut 30,0 % d'équité (payer 1.5 pour un pot de 3.5) : absent |
| ✗ | 81bb14e6 | ouverture | relancer | La bonne réponse est : se coucher. : absent ; 93o : se coucher en UTG, MP, CO, BTN, SB : contredit |
| ✗ | 58ebc71f | tirage | suivre | La bonne réponse est : se coucher. : absent ; Outs : 9 (9 pour couleur) : contredit ; Les cartes qui ne donnent qu'une paire, une double paire ou un brelan ne comptent pas : elles ne suffisent souvent pas à gagner le coup. : absent ; Chance de toucher à la prochaine carte : 19,6 % : absent ; Cote du pot : il faut 30,0 % d'équité (payer 7.5 pour un pot de 17.5) : absent |
| ✗ | 30ade668 | qui_gagne | ton adversaire gagne | La bonne réponse est : tu gagnes. : absent ; Ta meilleure main : Double paire : contredit ; Celle de ton adversaire : Paire : contredit |
| ✗ | 4df5bdc2 | defense_bb | relancer | La bonne réponse est : suivre ou se coucher. : absent ; Équité de J2o contre la range d'ouverture du CO : 33,4 % : contredit ; Équité réalisée hors position (environ 80 %) : 26,7 % : absent ; Cote du pot : il faut 27,3 % d'équité (payer 1.5 pour un pot de 4) : absent |
| ✗ | 7925dffa | ouverture | relancer | La bonne réponse est : se coucher. : absent ; J3o : se coucher en UTG, MP, CO, BTN, SB : contredit |
| ✗ | af26c4d6 | tirage | suivre | La bonne réponse est : se coucher. : absent ; Outs : 4 (4 pour quinte) : contredit ; Les cartes qui ne donnent qu'une paire, une double paire ou un brelan ne comptent pas : elles ne suffisent souvent pas à gagner le coup. : absent ; Chance de toucher à la prochaine carte : 8,7 % : absent ; Cote du pot : il faut 25,0 % d'équité (payer 4 pour un pot de 12) : absent |
| ✗ | 9ddc8cb2 | qui_gagne | tu gagnes | La bonne réponse est : ton adversaire gagne. : absent ; Ta meilleure main : Paire : absent ; Celle de ton adversaire : Full : contredit |
| ✗ | 4648ff8a | defense_bb | se coucher | La bonne réponse est : suivre. : absent ; Équité de A9o contre la range d'ouverture du SB : 55,9 % : contredit ; Équité réalisée hors position (environ 80 %) : 44,8 % : absent ; Cote du pot : il faut 30,0 % d'équité (payer 1.5 pour un pot de 3.5) : absent ; Au-dessus de 55,0 % d'équité, relancer se défend aussi. : absent |
| ✗ | 300247bd | ouverture | relancer | La bonne réponse est : se coucher. : absent ; Q3o : se coucher en UTG, MP, CO, BTN, SB : contredit |
| ✗ | 1a9346cc | tirage | suivre | La bonne réponse est : se coucher. : absent ; Outs : 4 (4 pour quinte) : contredit ; Les cartes qui ne donnent qu'une paire, une double paire ou un brelan ne comptent pas : elles ne suffisent souvent pas à gagner le coup. : absent ; Chance de toucher à la prochaine carte : 8,5 % : absent ; Cote du pot : il faut 25,0 % d'équité (payer 4 pour un pot de 12) : contredit |
| ✗ | 12f649a8 | qui_gagne | ton adversaire gagne | La bonne réponse est : tu gagnes. : absent ; Ta meilleure main : Full : absent ; Celle de ton adversaire : Double paire : contredit |
| ✗ | d2f60822 | defense_bb | relancer | La bonne réponse est : suivre ou se coucher. : absent ; Équité de 94o contre la range d'ouverture du BTN : 32,9 % : contredit ; Équité réalisée hors position (environ 80 %) : 26,3 % : absent ; Cote du pot : il faut 27,3 % d'équité (payer 1.5 pour un pot de 4) : contredit |
| ✗ | fccd4959 | ouverture | se coucher | La bonne réponse est : relancer. : absent ; Q9s : ouvrir en MP, CO, BTN, SB ; se coucher en UTG : contredit |
| — | 32a2fbd2 | tirage | relancer | La bonne réponse est : suivre ou se coucher. : absent ; Outs : 9 (9 pour couleur) : absent ; Les cartes qui ne donnent qu'une paire, une double paire ou un brelan ne comptent pas : elles ne suffisent souvent pas à gagner le coup. : absent ; Chance de toucher à la prochaine carte : 19,1 % : absent ; Chance de toucher d'ici la river : 35,0 % : absent ; Cote du pot : il faut 25,0 % d'équité (payer 2 pour un pot de 6) : absent |
| ✗ | 1cd082ae | qui_gagne | tu gagnes | La bonne réponse est : ton adversaire gagne. : absent ; Celle de ton adversaire : Double paire : contredit |
| ✗ | c549800f | defense_bb | relancer | La bonne réponse est : suivre ou se coucher. : absent ; Équité de 32s contre la range d'ouverture du BTN : 33,7 % : contredit ; Équité réalisée hors position (environ 80 %) : 26,9 % : absent ; Cote du pot : il faut 27,3 % d'équité (payer 1.5 pour un pot de 4) : absent |
| ✗ | 3a5ac28e | ouverture | relancer | La bonne réponse est : se coucher. : absent ; Q6o : se coucher en UTG, MP, CO, BTN, SB : contredit |
| ✗ | 17fb7d20 | tirage | suivre | La bonne réponse est : se coucher. : absent ; Outs : 8 (8 pour quinte) : contredit ; Les cartes qui ne donnent qu'une paire, une double paire ou un brelan ne comptent pas : elles ne suffisent souvent pas à gagner le coup. : absent ; Chance de toucher à la prochaine carte : 17,4 % : contredit ; Cote du pot : il faut 25,0 % d'équité (payer 3 pour un pot de 9) : absent |

## Détail

### 27aefb08 — ouverture

> Table 6 joueurs, 100 blindes · tu es sous le canon (UTG).
> Tu parles en premier (UTG). Tu as 9♠ 6♠.

Décision : relancer

**Débrief du coach :**

> Tu es UTG avec 9♠6♠.  
> La référence dit : **96s se coucher en UTG, MP, CO**.  
> 
> → Donc, **relancer en UTG est une erreur**.  
> 
> Pourquoi ?  
> - 96s est une main **faible en UTG**.  
> - En position de départ (UTG), tu n’as pas de position sur les autres joueurs.  
> - La référence précise que **96s ne doit pas être ouverte en UTG**.  
> - Le **côté du pot** est de 100 blindes, donc le pot est petit, et 96s ne peut pas payer un relance.  
> 
> → En UTG, **se coucher** est la **seule action acceptable**.  
> → Relancer = **sortir de la main**, car tu n’as pas le potentiel de gagner un relance.  
> 
> 👉 **Conclusion** :  
> Tu as 96s. Tu es UTG.  
> → **Se coucher** est la bonne action.  
> → **Relancer = erreur**.  
> 
> Tu as compris ?  
> Pose-moi une question à choix :  
> 1. Quel est le cote du pot en UTG avec 96s ?  
> 2. Quelle est la meilleure action avec 96s en UTG ?  
> 3. Quelle main peut ouvrir en UTG ?  
> 
> Choisis l’un.

*25.9 s*

### b1c0fc5d — tirage

> Table 6 joueurs, 100 blindes · tu es au bouton (BTN).
> Au flop, ton adversaire mise 6 bb dans un pot de 8 bb. Tu as 4♥ 3♥.
> Board : 5♠ 10♣ A♥ · pot 14 bb, à payer 6 bb.

Décision : suivre

**Débrief du coach :**

> Tu as 4♥ 3♥.  
> Le board est : 5♠ 10♣ A♥.  
> 
> Tu as une **quinte possible** (4-5-10-A), mais **pas de carré**, **pas de flush**, **pas de full**, **pas de pair** au flop.  
> Tu n’as **qu’un seul out** : le 4, car le 3 est déjà sur le board.  
> Donc **4 outs** (4♥, 4♠, 4♦, 4♣) → **4**.
> 
> Chances de toucher à la river : **8,5 %** → **pas de chance** de faire une quinte en 1 carte.  
> Chances de toucher d’ici la river (flop à river) : **16,5 %** → **pas assez** pour gagner.
> 
> Cote du pot : **30,0 %** (tu dois payer 6 bb pour un pot de 14 bb).  
> Tu as **16,5 %** d’équité → **moins de 30 %** → **pas de cote**.
> 
> 👉 Donc **se coucher** est la **bonne action**.  
> Tu ne gagnes pas, tu n’as pas de chance, tu ne peux pas gagner le coup.
> 
> Tu as **4 outs**, **8,5 %** de chance de toucher, **16,5 %** de chance d’arriver à la river.  
> Tu as besoin de **30 %** d’équité → **tu n’en as pas**.
> 
> 👉 **Se coucher** = la bonne action.
> 
> **Question à choix :**  
> Tu as 4♥ 3♥ sur 5♠ 10♣ A♥.  
> Si tu avais eu 4♥ 4♠, quelle action aurait été correcte ?  
> A) Suivre  
> B) Se coucher  
> C) Sembluff  
> D) Payer 6 bb pour gagner  
> 
> Réponds-moi (A/B/C/D).

*37.6 s*

### b908cbf4 — qui_gagne

> Table 6 joueurs, quiz d'abattage.
> Le coup est fini : abattage. Ton adversaire montre 7♦ 3♥. Tu as 7♥ 4♣.
> Board : 6♦ 10♠ 6♣ 8♥ 4♦.

Décision : ton adversaire gagne

**Débrief du coach :**

> Tu as **7♥ 4♣** et le board est **6♦ 10♠ 6♣ 8♥ 4♦**.
> 
> Analysons les mains **avec les chiffres tels qu’ils sont dans la référence** :
> 
> ---
> 
> 🔹 **Ta main** : 7♥ 4♣  
> → Tu as **7** et **4**.  
> → Le board a : 6♦, 10♠, 6♣, 8♥, 4♦  
> → Tu as **7** (dans ta main) + **4** (dans le board) → **7** et **4**  
> → Tu as **7** et **4** → **Double paire** (7 et 4)
> 
> ---
> 
> 🔹 **Main de ton adversaire** : 7♦ 3♥  
> → Il a **7** et **3**  
> → Le board a : 6♦, 10♠, 6♣, 08♥, 4♦  
> → Il a **7** (dans sa main) + **6**, **10**, **8**, **4** → il a **7** → **paire de 7**  
> → Il n’a pas de **4** ni de **8** → pas de paire de 4 ou de 8  
> → Il n’a **pas** de **double paire**
> 
> ---
> 
> 🔹 **Règle** : chacun garde ses **5 meilleures cartes** parmi ses 2 cartes et les 5 du board.
> 
> → Tu as **7** (main) + **4** (board) → **7** et **4** → **double paire**  
> → Ton adversaire a **7** (main) + **6**, **10**, **8**, **4** → **seule paire** (7)
> 
> ---
> 
> ✅ **Référence** dit :  
> - **Bonnes actions** : **tu gagnes**  
> - **Actions acceptables** : aucune  
> → Donc, **tu dois gagner**, pas ton adversaire.
> 
> ---
> 
> ❌ **Erreur** : tu as dit que ton adversaire gagne → **c’est faux**.
> 
> ---
> 
> 📌 **Pourquoi ?**  
> Parce que **tu as une double paire** (7 et 4), **ton adversaire a seulement une paire** (7).  
> Et **la règle** dit que **chacun garde ses 5 meilleures cartes** → donc tu as **plus de paires** → tu gagnes.
> 
> ---
> 
> 👉 **Tu as gagné** → **la bonne action est de gagner**, pas de perdre.
> 
> Tu comprends ?  
> Pose-moi une question pour vérifier :  
> ➡️ Quelle est ta main ? (7♥ 4♣)  
> ➡️ Quel est le board ? (6♦ 10♠ 6♣ 8♥ 4♦)  
> ➡️ Quelle est la règle ? (chacun garde ses 5 meilleures cartes)
> 
> Pose-moi une question à choix avec l’outil **poser_question**.

*39.0 s*

### be1d1e8c — defense_bb

> Table 6 joueurs, 100 blindes · tu es à la grosse blinde (BB).
> Tout le monde se couche jusqu'au SB, qui relance à 2.5 bb ; les autres se couchent. Tu as 2♣ 4♥.
> Avant le flop · pot 3.5 bb, à payer 1.5 bb.

Décision : suivre

**Débrief du coach :**

> Parce que tu as **2♣ 4♥** : une main très faible, sans couleur, sans paire, sans connexion.
> 
> La **référence** dit clairement :
> 
> - Ton **équité contre la range d’ouverture du SB** est de **31,8 %**  
> - L’**équité réalisée hors position** (environ 80 %) est de **25,4 %**  
> - La **cote du pot** est de **30,0 %** (tu dois avoir **30 % d’équité** pour payer 1.5 bb dans un pot de 3.5 bb)
> 
> 👉 Donc :  
> Tu as **25,4 % d’équité réelle** (hors position),  
> Mais **il faut 30,0 %** pour que le coup soit équilibré.
> 
> Tu **ne remplis pas la condition** : **25,4 % < 30,0 %** → **tu ne peux pas suivre**.
> 
> 👉 **Se coucher** est la **bonne action**.
> 
> Tu as **moins de 30 % d’équité**, donc **suivre = perdre**.
> 
> C’est **l’erreur** que tu as faite.  
> Et c’est **dans la référence** :  
> > *Équité réalisée hors position : 25,4 %*  
> > *Cote du pot : 30,0 %*  
> > → **pas assez d’équité → se coucher**.
> 
> Tu as compris ?  
> Pose-moi une question pour vérifier :  
> 👉 *Est-ce que tu as compris que l'équité réelle (25,4 %) est inférieure à la cote du pot (30,0 %) ?*  
> (Choisir : Oui / Non)

*26.8 s*

### 683b0301 — ouverture

> Table 6 joueurs, 100 blindes · tu es à la petite blinde (SB).
> Tout le monde s'est couché jusqu'à toi (SB). Tu as 3♠ 7♦.

Décision : relancer

**Débrief du coach :**

> Tu es à la petite blinde (SB) avec 3♠ 7♦ (73o).  
> La référence dit clairement : **73o se coucher en UTG, MP, CO, BTN, SB**.  
> 
> Donc, **à la SB**, avec 73o, **la bonne action est de se coucher**.  
> 
> Tu as relancé → erreur.  
> 
> Pourquoi ?  
> → 73o est une main dépareillée (pas de couleur, pas de pair).  
> → En 6-max, 100 blindes, les ranges d’ouverture sont très restrictifs.  
> → La référence dit : **aucune action acceptable** en SB avec 73o.  
> 
> Donc, **aucune action n’est acceptable** ici.  
> Tu n’as pas de cote suffisante, ni de chance de gagner.  
> 
> **Conclusion** : relancer = erreur. Se coucher = la bonne action.  
> 
> Tu comprends ?  
> ➡️ Pose-moi une question à choix pour vérifier :  
> 1. Est-ce que 73o est une main forte en SB ?  
> 2. A-t-on besoin de cote pour relancer avec 73o ?  
> 3. Y a-t-il un cas où 73o peut relancer ?  
> 4. Quel est le seuil de cote pour 73o en SB ?  
> 
> Réponds-moi avec un numéro.

*21.1 s*

### 5f5c9989 — tirage

> Table 6 joueurs, 100 blindes · tu es sous le canon (UTG).
> Au flop, ton adversaire mise 7.5 bb dans un pot de 10 bb. Tu as 6♠ 7♦.
> Board : 9♠ 4♣ 10♣ · pot 17.5 bb, à payer 7.5 bb.

Décision : suivre

**Débrief du coach :**

> Tu as 6♠ 7♦ sur un flop de 9♠ 4♣ 10♣.  
> Tu as 4 outs pour une quinte (6-7-9-10), soit 4 cartes qui te donnent un bon coup.  
> 
> La **chance de toucher** cette quinte à la river est de **8,5 %**.  
> Cela signifie que tu as **8,5 % de chances** de gagner le coup en tirant une carte à la river.  
> 
> Mais le **pot** est de 17,5 bb, et tu dois payer 7,5 bb.  
> Donc, la **cote du pot** est de **17,5 / (17,5 + 7,5) = 17,5 / 25 = 70 %**.  
> 
> Mais **l'équité que tu as** est de **8,5 %** (chance de toucher).  
> Tu dois avoir **au moins 30,0 % d'équité** pour que le coup soit acceptable.  
> 
> 👉 **8,5 % < 30,0 %** → donc, **suivre est une erreur**.  
> 
> Tu ne gagnes pas assez de chances pour justifier de payer 7,5 bb.  
> La bonne action est de **te coucher**.  
> 
> C’est la référence : **bonnes actions : se coucher**.  
> 
> Tu n’as pas assez de chances.  
> Tu n’as pas de gains implicites.  
> Tu n’as pas de semi-bluff.  
> 
> 👉 **Tu dois te coucher.**  
> 
> Tu comprends ?  
> Pose-moi une question pour vérifier :  
> **1. Quelle est la cote du pot ?**  
> **2. Quelle est la chance de toucher à la river ?**  
> **3. Quelle est l’équité minimale requise ?**  
> **4. Quelle est la bonne action ?**  
> 
> 👉 Choisis une.

*28.1 s*

### 24d58074 — qui_gagne

> Table 6 joueurs, quiz d'abattage.
> Le coup est fini : abattage. Ton adversaire montre 7♥ 5♠. Tu as K♣ 7♣.
> Board : 5♣ Q♦ Q♥ 5♥ 6♥.

Décision : tu gagnes

**Débrief du coach :**

> Tu as K♣ 7♣.  
> Le board est : 5♣ Q♦ Q♥ 5♥ 6♥.  
> 
> Analysons les mains :
> 
> 👉 **Ton adversaire a 7♥ 5♠**  
> - Il peut former :  
>   - 5♣ (board) + 5♥ (board) + 7♥ (sa carte) → **un cinq pair**  
>   - Q♦, Q♥ → **un pair de queens**  
>   → Il a **un full** : **pair de queens** + **pair de cinq**.  
> 
> 👉 **Ta main : K♣ 7♣**  
> - Tu as :  
>   - 7♣ (ta carte) + 5♣ (board) → **un pair de sept**  
>   - Q♦, Q♥ → **pair de queens**  
>   → Tu as **double paire** : pair de sept et pair de queen.  
> 
> Mais ici, **le full** (pair de queens + pair de cinq) **vaut plus** que **la double paire** (pair de queen + pair de sept).  
> 
> ➡️ **Règle du poker** :  
> > Si tu as un full, tu gagnes **à tout prix** contre une double paire.  
> > Un full = un pair + un autre pair.  
> > Une double paire = deux paires différentes, mais pas un full.  
> 
> 👉 **Le full > la double paire**  
> → Donc ton adversaire **gagne**.  
> 
> Tu as **erroné** : tu penses avoir gagné, mais **le full de ton adversaire** (7♥ 5♠) forme **un full de queens** (Q♦ Q♥) + **un pair de cinq** (5♣ 5♥).  
> Tu as **double paire**, mais **pas de full**.  
> 
> ✅ **Conclusion** :  
> - **Adversaire** : Full → **gagne**  
> - **Toi** : Double paire → **perd**  
> → **Tu as perdu**, donc **ta décision de "gagner" est fausse**.  
> 
> Tu as compris ?  
> ➡️ Pose-moi une question pour vérifier :  
> 1. Quel est le meilleur full possible ici ?  
> 2. Quelle est la différence entre un full et une double paire ?  
> 3. Pourquoi le full gagne-t-il contre la double paire ?  
> 
> 👉 Utilise l’outil **poser_question** pour choisir une de ces questions.

*31.7 s*

### 93ff8955 — defense_bb

> Table 6 joueurs, 100 blindes · tu es à la grosse blinde (BB).
> Tout le monde se couche jusqu'au BTN, qui relance à 2.5 bb ; les autres se couchent. Tu as 5♣ 9♥.
> Avant le flop · pot 4 bb, à payer 1.5 bb.

Décision : relancer

**Débrief du coach :**

> Parce que **tu as 34,2 % d'équité** contre la range d'ouverture du BTN, mais **il faut 27,3 % d'équité** pour que le relance soit rentable.
> 
> Tu as **34,2 %** → c’est ce que tu mérites en équité face à l’adversaire.  
> Mais **le pot te demande 27,3 %** pour être rentable (payer 1,5 bb pour un pot de 4 bb).
> 
> 👉 Donc : **34,2 % > 27,3 %** → *en théorie, tu devrais suivre*.
> 
> Mais attention : **l’équité réalisée hors position est de 27,4 %** (moyenne).  
> Cela signifie que, **en position, tu n’as pas assez de force pour justifier un relance**.
> 
> 👉 Donc : **aucune action n’est rentable ici**.
> 
> Tu as **déjà perdu** en faisant un relance.
> 
> **Conclusion** :  
> → Le relance est **une erreur**.  
> → La bonne action est **de suivre** (ou de se coucher), car **tu n’as pas assez d’équité** pour payer ce relance.
> 
> Tu as **34,2 % d’équité** → ce n’est pas suffisant **en situation réelle** (27,4 % en position).
> 
> 👉 **Tu ne peux pas payer 1,5 bb pour un pot de 4 bb** avec seulement 27,4 % de chance de gagner.
> 
> **Pose-toi cette question** :  
> 👉 Si tu avais 5♣ 9♥, et que tu as 34,2 % d’équité contre le BTN, est-ce que tu devrais relancer ?  
> A. Oui, car 34,2 % > 27,3 %  
> B. Non, car l’équité réalisée hors position est de 27,4 %  
> C. Oui, car le pot est de 4 bb  
> D. Non, car tu es hors position  
> 
> 👉 Réponds-moi avec A, B, C ou D.

*30.0 s*

### 6aa24548 — ouverture

> Table 6 joueurs, 100 blindes · tu es au bouton (BTN).
> Tout le monde s'est couché jusqu'à toi (BTN). Tu as 5♦ J♦.

Décision : se coucher

**Débrief du coach :**

> Tu es au bouton (BTN) avec J5s.  
> La référence dit : **"ouvrir en BTN, SB ; se coucher en UTG, MP, CO"**.
> 
> Donc, **en tant que bouton**, tu **dois relancer**, pas te coucher.  
> 
> Tu as une main de départ **J5s** (assortie) :  
> - C’est une main **forte** en position.  
> - En **BTN**, tu as **la position** pour relancer.  
> 
> La référence dit clairement : **"ouvrir en BTN"** → donc **relancer** est la bonne action.  
> 
> 👉 **Tu as 100 blindes, tu es au bouton, tu as J5s → relancer.**  
> 
> Tu te couches ? → **Erreur.**  
> 
> Tu as **une ouverture valide** dans ta position.  
> 
> **C’est la règle.**  
> 
> Pose-toi cette question :  
> 👉 *Avec J5s au bouton, est-ce que tu dois relancer ou te coucher ?*  
> A. Relancer  
> B. Se coucher  
> 
> Réponds-moi.

*18.5 s*

### 23e06b0f — tirage

> Table 6 joueurs, 100 blindes · tu es à la petite blinde (SB).
> Au flop, ton adversaire mise 3.3 bb dans un pot de 10 bb. Tu as 8♥ 9♠.
> Board : 5♦ J♥ 7♥ · pot 13.3 bb, à payer 3.3 bb.

Décision : relancer

**Débrief du coach :**

> Parce que tu as 8♥ 9♠ sur un flop de 5♦ J♥ 7♥.
> 
> Tu as une quinte possible (8-9-10-J-Q), mais **seulement 8 outs** (les 8 et les 9 restants) pour la quinte, donc **17,0 % de chance de toucher** ta main à la turn.
> 
> La **cote du pot** est de **19,9 %** : tu dois avoir au moins 19,9 % d’équité pour que le relance soit correct.
> 
> Or, **17,0 % < 19,9 %**, donc tu n’as pas assez de chance de gagner.
> 
> 👉 **Tu n’as pas de bonne action** : relancer est **une erreur**.
> 
> Tu dois **suivre** (si tu as déjà une bonne action) ou **te coucher** (si tu n’as pas de chance).
> 
> Tu n’as **aucun out** qui te donne une main forte suffisante pour gagner face à un relance de 3,3 bb.
> 
> 👉 **Conclusion : relancer = erreur** — c’est une action **au-dessus de ton niveau**.  
> 
> Tu as besoin de **suivre** ou **te coucher**.  
> 
> Tu as compris ?  
> Pose-moi une question pour vérifier :  
> ➡️ *Quel est le pourcentage d’équité nécessaire pour payer 3,3 bb dans un pot de 13,3 bb ?*  
> (1) 17,0 %  
> (2) 19,9 %  
> (3) 31,5 %  
> (4) 8 %  
> 
> Réponds-moi.

*25.5 s*

### c9aaaf08 — qui_gagne

> Table 6 joueurs, quiz d'abattage.
> Le coup est fini : abattage. Ton adversaire montre 6♠ 2♣. Tu as 4♣ 9♣.
> Board : 10♠ 8♠ 10♦ 9♦ A♣.

Décision : ton adversaire gagne

**Débrief du coach :**

> Tu as **4♣ 9♣** et le board est **10♠ 8♠ 10♦ 9♦ A♣**.
> 
> Regardons les 5 meilleures cartes de chaque joueur :
> 
> ---
> 
> **Ta main (4♣ 9♣)**  
> - Tu as un **9♣** sur le board → tu as **9♣** + **9♦** = **paire de 9**  
> - Tu as un **4♣** → pas de paire  
> - Tu as un **10** (10♠, 10♦) → tu as un **10**  
> - Tu as un **8** (8♠) → tu as un **8**  
> - Tu as un **A** (A♣) → tu as un **A**  
> 
> 👉 Tu as **9♣** et **9♦** → **paire de 9**  
> 👉 Tu as **10♠**, **10♦** → **paire de 10**  
> 👉 Tu as **8♠** → un 8  
> 👉 Tu as **A♣** → un as  
> 
> ✅ Tu as **deux paires** : 9 et 10 → **double paire**
> 
> ---
> 
> **Main de ton adversaire (6♠ 2♣)**  
> - Il a **6♠** → 6 sur le board ? Non → pas de 6  
> - Il a **2♣** → 2 sur le board ? Non → pas de 2  
> - Le board a : 10♠, 8♠, 10♦, 9♦, A♣ → pas de 6 ni de 2  
> - Il n’a **aucune carte** en commun avec le board  
> 
> 👉 Il n’a **aucune carte** en commun avec le board → **pas de paire**  
> 
> ❌ Il n’a **aucune paire** → **main vide**
> 
> ---
> 
> ✅ **Conclusion** :  
> - Tu as **double paire** (9 et 10)  
> - Il a **aucune paire**  
> - La règle : chacun garde ses **5 meilleures cartes** → tu as 2 paires, il n’en a aucune  
> 
> 👉 **Tu gagnes** → **la décision du joueur ("ton adversaire gagne") est une erreur**
> 
> ---
> 
> 📌 **Référence calculée (fais-la confiance)** :  
> - Bonnes actions : **tu gagnes**  
> - Actions acceptables : aucune  
> - Ta meilleure main : **Double paire**  
> - Celle de ton adversaire : **Paire** → ❌ erreur, il n’a pas de paire  
> 
> ➡️ **Tu gagnes**, car tu as **double paire**, il n’a **aucune paire**.
> 
> ---
> 
> Tu comprends ?  
> 👉 Pose-toi cette question :  
> **Quelle est la meilleure main possible dans cette situation ?**  
> A) Paire  
> B) Double paire  
> C) Full  
> D) Straight  
> 
> Réponds-moi avec A, B, C ou D.

*37.3 s*

### dc3fb321 — defense_bb

> Table 6 joueurs, 100 blindes · tu es à la grosse blinde (BB).
> Tout le monde se couche jusqu'au SB, qui relance à 2.5 bb ; les autres se couchent. Tu as 8♣ A♥.
> Avant le flop · pot 3.5 bb, à payer 1.5 bb.

Décision : se coucher

**Débrief du coach :**

> Parce que tu as **52,8 % d'équité** contre la range d'ouverture du SB, et que **le pot te demande 30,0 % d'équité** pour payer 1,5 bb.
> 
> Tu **suis** parce que **52,8 % > 30,0 %**.
> 
> C’est une décision **clairement justifiée** par les chiffres de la référence.
> 
> > ✅ Bonnes actions : **suivre**  
> > ❌ Actions acceptables : **aucune**  
> > 📌 Cote du pot : **30,0 %**  
> > 📌 Équité réelle : **52,8 %**
> 
> Tu as **plus d'équité que ce qu’il faut** → tu dois **suivre**, pas te coucher.
> 
> Tu as compris ?  
> 👉 Pose-toi cette question :  
> **Si tu avais eu 8♣ 9♣ au lieu de 8♣ A♥, est-ce que tu suivrais ?**  
> (Choisis : oui / non)  
> → Utilise l’outil *poser_question* pour répondre.

*19.1 s*

### 81bb14e6 — ouverture

> Table 6 joueurs, 100 blindes · tu es au cut-off (CO).
> Tout le monde s'est couché jusqu'à toi (CO). Tu as 3♠ 9♥.

Décision : relancer

**Débrief du coach :**

> Tu as 9♠3♥ (93o), au cut-off (CO), 100 blindes.  
> 
> La référence dit clairement :  
> 👉 **93o : se coucher en UTG, MP, CO, BTN, SB**  
> 
> Cela veut dire que **à tout moment**, avec 93o, **le seul bon coup est de se coucher**.  
> 
> En position de CO, tu n’as pas assez de main pour relancer.  
> Le pot est de 100 blindes → le cote est de 100.  
> Mais 93o n’a que **12 % de chance de gagner** (référence : 12 %) contre un range de mains en position.  
> 
> Tu as **12 % de chance de gagner** → c’est **moins de 1/8**.  
> Tu ne peux pas faire un relancer avec une main qui ne gagne que 12 %, surtout quand tu es en position de CO, où les autres joueurs ont déjà des mains plus fortes.  
> 
> 👉 **Relancer = erreur**  
> 👉 **Se coucher = la bonne action**  
> 
> Tu n’as pas de carte de couleur, pas de carré, pas de flush.  
> 93o est une main dépareillée, très faible.  
> 
> **Conclusion :**  
> Tu devrais **te coucher**, car **la référence dit clairement que 93o se coucher en CO**.  
> Tu n’as pas de cote, pas de chance, pas de position.  
> 
> Tu as fait une erreur en relançant.  
> 
> Tu veux vérifier ?  
> 👉 Poser une question ?  
> 
> (Choisir : A) Oui, pose-moi une question.  
> (B) Non, je comprends.

*25.3 s*

### 58ebc71f — tirage

> Table 6 joueurs, 100 blindes · tu es au cut-off (CO).
> Au turn, ton adversaire mise 7.5 bb dans un pot de 10 bb. Tu as 7♣ K♣.
> Board : 6♣ 6♥ J♣ 9♦ · pot 17.5 bb, à payer 7.5 bb.

Décision : suivre

**Débrief du coach :**

> Tu as 7♣ K♣ sur un board de 6♣ 6♥ J♣ 9♦.
> 
> Tu as 9 outs pour une couleur (les 9, 10, 11, 12, 13, 1-9, 10-13, 14-14 → 9 cartes qui te permettent de faire une couleur).
> 
> La chance de toucher ta couleur à la prochaine carte est de **19,6 %**.
> 
> Le **côté du pot** est de **30,0 %** : tu dois avoir au moins 30 % d’équité pour payer 7,5 bb dans un pot de 17,5 bb.
> 
> Tu as seulement **19,6 %**, donc **moins de la moitié** de la cote du pot.
> 
> 👉 La bonne action est **de se coucher**.
> 
> Tu ne peux pas suivre à ce niveau, car tu n’as pas assez de chances de gagner.
> 
> Tu as fait une erreur : **suivre** est **une mauvaise action** ici.
> 
> ✅ Référence : *chance de toucher : 19,6 %*, *côté du pot : 30,0 %*.
> 
> Tu as moins de chance que le pot exige. C’est une erreur.
> 
> ---
> 
> Pose-toi cette question (à choix) :
> 
> 👉 Quel est le vrai cote du pot dans cette situation ?  
> A) 19,6 %  
> B) 25,0 %  
> C) 30,0 %  
> D) 40,0 %
> 
> Réponds-moi.

*24.4 s*

### 30ade668 — qui_gagne

> Table 6 joueurs, quiz d'abattage.
> Le coup est fini : abattage. Ton adversaire montre 6♠ 6♣. Tu as 9♠ 8♣.
> Board : 9♥ 2♣ 4♦ 7♣ 8♥.

Décision : ton adversaire gagne

**Débrief du coach :**

> Tu as **9♠ 8♣** et le board est **9♥ 2♣ 4♦ 7♣ 8♥**.
> 
> Regardons ce que chacun peut faire :
> 
> 👉 **Ta main** :  
> Tu as un **9** et un **8**.  
> Sur le board, il y a un **9♥** et un **8♥**.  
> Donc tu as :  
> - 9♠, 9♥ → **paire de 9**  
> - 8♣, 8♥ → **paire de 8**  
> → **Double paire** ✅
> 
> 👉 **Adversaire** :  
> Il a **6♠ 6♣** → deux 6.  
> Sur le board, il n’y a **aucun 6**.  
> Donc il n’a **aucune paire** sur le board.  
> → **Pas de paire** ❌
> 
> ➡️ **Règle** : chacun garde ses 5 meilleures cartes (2 mains + 5 board).  
> → Tu as **double paire** (9 et 8).  
> → Il a **aucune paire**.
> 
> ✅ **Donc tu gagnes**.  
> ❌ **Erreur** : tu as dit qu’il gagnait → c’est faux.
> 
> **Conclusion** :  
> - Ta main = **double paire**  
> - Sa main = **pas de paire**  
> → Tu gagnes.  
> → **La bonne action est de gagner**, car le code dit : *bonnes actions : tu gagnes*.
> 
> 👉 **Tu as raison de vouloir gagner**, mais tu as mal interprété le résultat.
> 
> Tu as perdu ? Non. Tu as gagné.  
> Le code dit clairement : **tu gagnes**.
> 
> Tu veux vérifier ?  
> 👉 Pose-toi cette question :  
> **Quelle est la meilleure main ici ?**  
> A. Double paire  
> B. Paire  
> C. Aucune paire  
> D. Full
> 
> Réponds-moi avec A, B, C ou D.

*28.1 s*

### 4df5bdc2 — defense_bb

> Table 6 joueurs, 100 blindes · tu es à la grosse blinde (BB).
> Tout le monde se couche jusqu'au CO, qui relance à 2.5 bb ; les autres se couchent. Tu as J♠ 2♣.
> Avant le flop · pot 4 bb, à payer 1.5 bb.

Décision : relancer

**Débrief du coach :**

> Parce que tu as **33,4 % d'équité** contre la range d'ouverture du CO, mais **il faut 27,3 % d'équité** pour que le relance soit correct.
> 
> Tu as donc **moins d'équité** que la cote du pot.  
> C’est une erreur de relancer.
> 
> > ✅ **Équité contre la range** : 33,4 %  
> > ❌ **Cote du pot** : 27,3 %  
> > → Tu dois **suivre ou te coucher**.
> 
> Tu n’as pas assez de chances pour justifier un relance.  
> C’est la règle : **tu ne relances jamais si ton équité est inférieure à la cote du pot**.
> 
> 👉 C’est exactement ce que dit la référence : *il faut 27,3 % d'équité (payer 1.5 pour un pot de 4)*.
> 
> Tu as 33,4 % → c’est **suffisant** ? OUI.  
> Mais **le relance est une action qui demande plus que ça**, surtout hors position.
> 
> Et la référence dit : **aucune bonne action**.  
> Donc **relancer = erreur**.
> 
> Tu dois **suivre ou te coucher**.
> 
> Tu as compris ?  
> 👉 Poser_question :  
> **Quel est le seuil minimal d'équité pour relancer, selon la référence ?**  
> A. 27,3 %  
> B. 33,4 %  
> C. 80 %  
> D. 26,7 %  
> 
> Réponds-moi.

*24.3 s*

### 7925dffa — ouverture

> Table 6 joueurs, 100 blindes · tu es au bouton (BTN).
> Tout le monde s'est couché jusqu'à toi (BTN). Tu as J♦ 3♠.

Décision : relancer

**Débrief du coach :**

> Parce que, selon la référence, **J3o** doit **se coucher** en **UTG, MP, CO, BTN, SB** dans un tournoi de 6 joueurs à 100 blindes.
> 
> Tu es au **bouton (BTN)**, donc dans une position où tu devrais **ne pas relancer** avec une main dépareillée comme J3o.
> 
> La référence dit clairement :  
> → **"J3o : se coucher en UTG, MP, CO, BTN, SB"**  
> → **"actions acceptables : aucune"**  
> 
> Donc, **relancer = erreur**.  
> 
> Tu n’as pas de cote suffisante, ni de chances de gagner assez pour justifier un relance avec une main comme J3o.  
> 
> 👉 C’est une main **faible**, **dépareillée**, sans couleur ni pair fort.  
> 
> Tu ne peux pas espérer battre un pair ou une couleur.  
> 
> Et même si tu as un joker (J), tu n’as pas de combo forte.  
> 
> 👉 **La bonne action est de se coucher.**  
> 
> Tu as 100 blindes. Tu ne gagnes pas de pot avec un relance ici.  
> 
> Tu as donc **perdu ton tour**.  
> 
> Tu veux savoir si tu comprends ?  
> 👉 Poser une question ?  
> Oui / Non ?  
> 
> (Choisir une seule réponse.)

*22.7 s*

### af26c4d6 — tirage

> Table 6 joueurs, 100 blindes · tu es au cut-off (CO).
> Au turn, ton adversaire mise 4 bb dans un pot de 8 bb. Tu as K♣ 9♠.
> Board : 10♥ 7♠ 10♠ Q♥ · pot 12 bb, à payer 4 bb.

Décision : suivre

**Débrief du coach :**

> Tu as K♣ 9♠ sur un board de 10♥ 7♠ 10♠ Q♥.  
> 
> Tu as 4 outs (quinte possible : 8 ou 5) → **chance de toucher : 8,7 %**.  
> Cela signifie que tu as **8,7 % de chance de gagner le coup** avec la prochaine carte.  
> 
> Le **pot est de 12 bb**, et tu dois payer **4 bb**.  
> → **Cote du pot = 12 / 4 = 3,0** (c’est-à-dire que tu dois gagner 1/3 de la mise pour que le coup soit équilibré).  
> 
> Mais pour gagner, tu as besoin de **25,0 % d’équité** (c’est-à-dire 25 % de chance de gagner le pot).  
> 
> 👉 Tu as **8,7 %**, **moins de 25 %** → **pas assez de chance**.  
> 
> **Donc : se coucher est la bonne action.**  
> 
> Tu ne peux pas suivre ici, car même avec une bonne main (K9), tu n’as pas assez de chances de gagner.  
> 
> 👉 **Référence : cote du pot = 25,0 % → tu as 8,7 % → erreur de décision.**  
> 
> Tu as suivi → c’est une erreur.  
> 
> Tu as 4 outs → 8,7 % → pas assez pour payer 4 bb dans un pot de 100 blindes.  
> 
> **Conclusion : tu devrais te coucher.**  
> 
> Tu as compris ?  
> 
> 👉 Pose-toi cette question :  
> **Quelle est la cote du pot ici ?**  
> A) 25,0 %  
> B) 3,0  
> C) 8,7 %  
> D) 12 bb  
> 
> Réponds-moi avec la lettre.

*28.2 s*

### 9ddc8cb2 — qui_gagne

> Table 6 joueurs, quiz d'abattage.
> Le coup est fini : abattage. Ton adversaire montre 4♣ 4♠. Tu as 2♥ 7♣.
> Board : 4♦ 6♦ 6♥ J♥ 8♣.

Décision : tu gagnes

**Débrief du coach :**

> Tu as 2♥ 7♣.  
> Ton adversaire a 4♣ 4♠.  
> Board : 4♦ 6♦ 6♥ J♥ 8♣.
> 
> Regardons les mains formées avec les 5 meilleures cartes :
> 
> 👉 **Ta main** :  
> - Tu as 2♥, 7♣  
> - Board : 4♦, 6♦, 6♥, J♥, 8♣  
> → Tu peux faire **une paire avec le 6** (6♦ et 6♥), mais tu n’as pas de 6 dans tes cartes.  
> → Tu as 2♥ et 7♣ → tu n’as **aucune carte en commun avec le board** sauf peut-être le 6… mais tu n’as pas de 6.  
> → Tu n’as **aucune paire** possible.  
> → Tu n’as **aucune main forte**.  
> → **Ta meilleure main = aucune paire** → **main faible**.
> 
> 👉 **Adversaire** :  
> - 4♣, 4♠  
> - Board : 4♦, 6♦, 6♥, J♥, 8♣  
> → Il a **deux 4** (4♣, 4♠) + **4♦** sur le board → **trois 4** → **une paire de 4**  
> → Il a aussi 6♦, 6♥ → **une paire de 6**  
> → Il a donc **un full** : **paire de 4** + **paire de 6** → **full**  
> → **Full = main forte**.
> 
> ✅ Règle : chacun garde ses 5 meilleures cartes.  
> → Full > Paire > Aucune paire.
> 
> 👉 Donc :  
> - **Adversaire a un full**  
> - **Tu as aucune paire** → **tu n’as pas de main**  
> → **Tu perds**.
> 
> ❌ Tu dis "je gagne" → **erreur**.
> 
> 📌 **La bonne action est de ne pas jouer** ou de **rester au sol** → tu n’as pas assez.  
> Le full est supérieur à une paire, donc ton adversaire gagne.
> 
> > Tu as 2♥ 7♣ → pas de paire → **main nulle**  
> > Adversaire a 4♣ 4♠ → avec 4♦ → **trois 4** → **full**  
> > Full > paire → **adversaire gagne**
> 
> ✅ C’est la référence : **bonnes actions : adversaire gagne**.
> 
> Tu as fait une erreur de lecture des cartes ou des mains.  
> Tu n’as pas de 6 → tu n’as pas de paire.  
> Tu n’as que des cartes isolées.
> 
> 👉 **Tu perds.**
> 
> Pose-toi cette question :  
> **Quelle est ta meilleure main avec 2♥ 7♣ sur le board 4♦ 6♦ 6♥ J♥ 8♣ ?**  
> A) Paire  
> B) Aucune paire  
> C) Full  
> D) Couleur
> 
> 👉 Réponds avec l'outil : **poser_question** (choisir A, B, C ou D).

*54.5 s*

### 4648ff8a — defense_bb

> Table 6 joueurs, 100 blindes · tu es à la grosse blinde (BB).
> Tout le monde se couche jusqu'au SB, qui relance à 2.5 bb ; les autres se couchent. Tu as 9♥ A♣.
> Avant le flop · pot 3.5 bb, à payer 1.5 bb.

Décision : se coucher

**Débrief du coach :**

> Parce que tu as **55,9 % d'équité** contre la range d'ouverture du SB, et que **le pot demande seulement 30,0 % d'équité** pour payer 1,5 bb.
> 
> Tu n’as pas besoin de suivre pour gagner, mais tu **dois relancer** car :
> 
> - **55,9 % > 55,0 %** → c’est au-dessus du seuil de défense.
> - **44,8 %** est l’équité réalisée hors position (mais c’est une moyenne, pas une limite).
> - **30,0 %** est la cote du pot (tu dois payer 1,5 bb pour un pot de 3,5 bb).
> 
> 👉 Donc, **suivre** est **bonne action**, **relancer** est **acceptable**, **se coucher** est **erreur**.
> 
> Tu as **plus d’équité que le seuil**, donc tu **ne dois pas te coucher**.
> 
> Tu as **9♥ A♣** → c’est un A9o, une main forte contre un SB qui ouvre avec une range de 6-max.
> 
> ✅ **Conclusion** : tu dois **suivre** (ou relancer), **pas te coucher**.
> 
> Tu as compris ?  
> 👉 Pose-moi une question à choix pour vérifier :  
> 1. Quelle est la cote du pot ?  
> 2. Quelle est l’équité de A9o contre le SB ?  
> 3. Quel seuil d’équité permet de relancer ?  
> 4. Quelle est l’équité réalisée hors position ?  
> 
> Choisis-en une.

*24.3 s*

### 300247bd — ouverture

> Table 6 joueurs, 100 blindes · tu es au bouton (BTN).
> Tout le monde s'est couché jusqu'à toi (BTN). Tu as 3♦ Q♣.

Décision : relancer

**Débrief du coach :**

> Parce que **Q3o** (valet et trois dépareillés) est une main très faible, surtout en position de **bouton (BTN)**.
> 
> La référence dit clairement :  
> 👉 **"Q3o : se coucher en UTG, MP, CO, BTN, SB"**
> 
> Donc, **à tout moment**, y compris au bouton, **Q3o ne doit pas être relancé**.
> 
> Tu as 100 blindes, donc le pot est petit.  
> Le **côté du pot** (pot odds) pour un relance de Q3o est **trop faible** pour justifier une action.
> 
> La référence ne donne **aucune action acceptable** pour Q3o en position de bouton.
> 
> 👉 **Conclusion** : *relancer = erreur*  
> → **Se coucher est la seule bonne action**.
> 
> Tu as 3♦ Q♣ → dépareillées, pas de couleur, pas de paire.
> 
> ✅ La bonne action est **se coucher**, car **Q3o n’est pas dans le range d’ouverture en 6-max à 100 blindes**.
> 
> Tu comprends ?  
> 👉 Poser_question :  
> *Est-ce que tu as compris que Q3o ne doit pas être relancé en position de bouton en 6-max à 10-100 blindes ?*  
> Choisis :  
> A) Oui  
> B) Non

*21.2 s*

### 1a9346cc — tirage

> Table 6 joueurs, 100 blindes · tu es au bouton (BTN).
> Au flop, ton adversaire mise 4 bb dans un pot de 8 bb. Tu as 9♣ 10♥.
> Board : 6♠ 3♦ 8♥ · pot 12 bb, à payer 4 bb.

Décision : suivre

**Débrief du coach :**

> Tu as 9♣ 10♥ sur un flop de 6♠ 3♦ 8♥.  
> Tu as 4 outs pour une quinte (9-10-8-6), soit 4 cartes qui t’offrent une main gagnante.
> 
> La **chance de toucher** ta quinte à la river est de **8,5 %** → donc **16,5 % d’équité d’ici la river** (c’est la probabilité cumulée de toucher au flop ou au turn).
> 
> Mais le **pot est de 12 bb**, et tu dois payer **4 bb** pour suivre.  
> → Cote du pot = 4 / (12) = **33,3 %**.
> 
> La **référence** dit que tu as besoin de **25,0 % d’équité** pour justifier un appel.  
> Tu en as **16,5 %** → **moins de la moitié** du seuil.
> 
> 👉 Tu n’as pas assez de chances de gagner pour suivre.  
> La bonne action est **de te coucher** (fold), car tu ne mérites pas de payer 4 bb pour une équité de 16,5 %.
> 
> **Conclusion :**  
> Tu as 4 outs → 8,5 % de chance à la river → 16,5 % d’équité totale → **moins de 25 %** → **pas assez** → **suivre = erreur**.
> 
> Tu as compris ?  
> Pose-moi une question à choix :  
> 👉 A. Tu as besoin de 25 % d’équité pour suivre ?  
> 👉 B. 16,5 % est la chance de toucher à la river ?  
> 👉 C. Le pot est de 12 bb ?  
> 👉 D. 9♣ 1-0♥ fait une quinte ?  
> 
> Réponds-moi avec une lettre.

*27.4 s*

### 12f649a8 — qui_gagne

> Table 6 joueurs, quiz d'abattage.
> Le coup est fini : abattage. Ton adversaire montre 10♣ 7♦. Tu as 6♦ 2♥.
> Board : 5♣ K♥ 6♠ 6♥ 5♦.

Décision : ton adversaire gagne

**Débrief du coach :**

> Tu as **6♦ 2♥**.  
> Le board est : **5♣ K♥ 6♠ 6♥ 5♦**.  
> 
> Regardons les **5 meilleures cartes** de chaque joueur selon la règle : *chacun garde ses 5 meilleures cartes parmi ses 2 cartes et les 5 du board*.
> 
> ---
> 
> ### ✅ Ta main (6♦ 2♥) :
> - Tu as : 6♦, 2♥  
> - Board : 5♣, K♥, 6♠, 6♥, 5♦  
> 
> → Tu as **deux 6** (6♦ et 6♠), donc **un full** (un full = une paire + un trio).  
> → Tu as **6♥** sur le board → donc tu as **6♦, 6♠, 6♥** → **trois 6** → **un trio**  
> → Tu as **un 5** (5♦) → donc **une paire de 5**  
> → Tu as **un 2** → pas de paire  
> 
> → Tu as **trois 6** → **trio de 6**  
> → Tu as **deux 5** → **paire de 5**  
> → Tu as **un 2** → pas de paire  
> 
> Donc ton meilleur combo : **trio de 6** + **paire de -5-** → **full**  
> → **Full** = trio + paire (ex : 666 + 55)
> 
> ---
> 
> ### ✅ Main de ton adversaire (10♣ 7♦) :
> - Il a : 10♣, 7♦  
> - Board : 5♣, K♥, 6♠, 6♥, 5♦  
> 
> → Il a **aucun 6**, **aucun 5**, **aucun 10** sur le board  
> → Il a **10♣** → **paire de 10**  
> → Il a **7♦** → **pas de paire avec le board**  
> → Il n’a **aucun 6**, donc **pas de trio**  
> → Il n’a **aucun 5**, donc **pas de paire de 5**  
> 
> → Il a **10♣** → **paire de 10**  
> → Il a **7♦** → **pas de paire**  
> → Il n’a **aucun 6**, donc **pas de trio**  
> → Donc : **seule paire de 10**
> 
> → Il n’a **aucun trio**, donc **pas de full**
> 
> ---
> 
> ### 🚫 Règle :  
> > Chacun garde ses **5 meilleures cartes** parmi ses 2 cartes et les 5 du board.
> 
> → Pour **full**, il faut **un trio** + **une paire**  
> → Tu as **trois 6** → **trio**  
> → Tu as **deux 5** → **paire**  
> → Donc **full** ✅  
> 
> → Ton adversaire n’a **aucun 6**, donc **pas de trio**  
> → Il a **seule paire de 10** → **pas de full**  
> → Donc **pas de full**, donc **pas de main plus forte**
> 
> ---
> 
> ### 🔍 Référence du code (fais-moi confiance) :
> - Bonnes actions : **tu gagnes**  
> - Actions acceptables : **aucune**  
> - Ta meilleure main : **Full**  
> - Celle de ton adversaire : **Double paire** ❌ → **c’est faux**  
> → **Double paire** = deux paires différentes (ex : 66 + 55)  
> → Mais **ton adversaire n’a pas 6**, donc **pas de 66**, donc **pas de double paire**
> 
> ---
> 
> ### 🚨 Erreur dans la référence ?  
> Non.  
> → Le code dit : **"Celle de ton adversaire : Double paire"**  
> → C’est **faux** → il n’a pas de 6 → pas de paire de 6 → **pas de double paire**
> 
> Mais le code dit aussi : **"Ta meilleure main : Full"** → ✅  
> → Et **"bonnes actions : tu gagnes"** → ✅
> 
> Donc **le verdict : erreur** → **c’est correct**  
> → Tu gagnes, pas ton adversaire
> 
> ---
> 
> ### ✅ Conclusion :
> Tu as **un full (666 + 55)** → **trio de 6 + paire de 5**  
> Ton adversaire a **seule paire de 10** → **pas de full**  
> → Donc **tu gagnes**
> 
> → **La bonne action est de gagner**  
> → **Le code dit que tu gagnes → donc c’est bon**
> 
> ---
> 
> 📌 **Réponse finale** :  
> **Tu as un full (trio de 6 + paire de 5). Ton adversaire n’a que une paire (de 10). Tu gagnes.**
> 
> 👉 Tu as **gagné**, donc **ton adversaire a perdu** → **le verdict "erreur" est juste**.
> 
> ---
> 
> ✅ **Tu as compris ?**  
> Pose-toi cette question :  
> **Quelle est ta main avec les cartes 6♦ 2♥ sur le board 5♣ K♥ 6♠ 6♥ 5♦ ?**  
> A. Paire de 5  
> B. Full  
> C. Double paire  
> D. Trio  
> 
> 👉 Réponds avec la lettre.

*63.3 s*

### d2f60822 — defense_bb

> Table 6 joueurs, 100 blindes · tu es à la grosse blinde (BB).
> Tout le monde se couche jusqu'au BTN, qui relance à 2.5 bb ; les autres se couchent. Tu as 9♠ 4♦.
> Avant le flop · pot 4 bb, à payer 1.5 bb.

Décision : relancer

**Débrief du coach :**

> Parce que tu as **32,9 % d'équité** contre la range d'ouverture du BTN, mais **il faut 27,3 % d'équité** pour que le relance soit rentable.
> 
> Tu as donc **moins d'équité que la cote du pot** → le relance est **perdu**.
> 
> > **Équité contre la range** : 32,9 %  
> > **Cote du pot** (payer 1,5 bb pour un pot de 4 bb) : 27,3 %  
> > → 32,9 > 27,3 ? Non → **erreur**.
> 
> Tu devrais donc **suivre** ou **te coucher**.  
> Relancer = erreur.
> 
> Tu as 9♠ 4♦ → une main faible, hors position, contre un relance de 2,5 bb.
> 
> 👉 **La bonne action est la bonne parce que les chiffres disent clairement que tu n’as pas assez d’équité pour payer.**

*17.9 s*

### fccd4959 — ouverture

> Table 6 joueurs, 100 blindes · tu es au cut-off (CO).
> Tout le monde s'est couché jusqu'à toi (CO). Tu as 9♣ Q♣.

Décision : se coucher

**Débrief du coach :**

> Tu as **9♣ Q♣ (Q9s)** au **cut-off (CO)**, 6 joueurs, 100 blindes.
> 
> La référence dit clairement :  
> ✅ **Q9s ouvre en CO, BTN, MP, SB**  
> ❌ **se coucher en UTG**
> 
> Tu es au **CO**, donc **Q9s est dans la plage d’ouverture**.
> 
> 👉 Donc, **relancer est la bonne action**, pas se coucher.
> 
> Tu as **une main solide**, pas un "joueur de bas niveau".  
> Tu as **une bonne cote** (le pot est 100 blindes, tu es au CO, donc tu as un bon niveau de position).
> 
> La référence ne dit pas "relancer avec 99" ou "se coucher avec 88", elle dit : **Q9s ouvre en CO**.
> 
> 👉 C’est une main de **range d’ouverture** dans cette position.
> 
> **Conclusion** :  
> Tu dois **relancer**, pas te coucher.  
> Se coucher ici = **erreur**.
> 
> Pose-toi cette question :  
> 👉 **Tu as 9♣ Q♣ au CO, 6 joueurs, 100 blindes. La référence dit que Q9s ouvre en CO. Tu dois donc :**  
> A) Se coucher  
> B) Relancer  
> C) Appeler  
> D) Relancer ou appeler  
> 
> 👉 Quel est le bon choix ? (choisir A, B, C ou D)  
> 
> (Si tu veux, je peux t’expliquer pourquoi B est le bon choix, mais d’abord, réponds à la question.)

*24.3 s*

### 32a2fbd2 — tirage

> Table 6 joueurs, 100 blindes · tu es sous le canon (UTG).
> Au flop, ton adversaire mise 2 bb dans un pot de 4 bb. Tu as 2♠ 10♠.
> Board : 6♥ 8♠ 4♠ · pot 6 bb, à payer 2 bb.

Décision : relancer

**Débrief du coach :**

> Tu as 2♠ 10♠.  
> Le flop est 6♥ 8♠ 4♠.  
> 
> Tu as une couleur en course (2♠, 10♠, 4♠, 8♠ → 4 cartes de la couleur), mais tu n’as pas de carré, ni de flush complet.  
> Tu as 9 outs pour terminer ta couleur (les 9 cartes restantes : 3, 5, 7, 9, J, Q, K, A, et 10 de pique ? Non : tu as déjà 10♠, donc les 9 autres piques).  
> 
> ✅ Outs : 9  
> ✅ Chance de toucher à la prochaine carte : **19,1 %**  
> ✅ Chance de toucher d’ici la river : **35,0 %**  
> ✅ Cote du pot : **25,0 %** (tu dois payer 2 bb pour un pot de 6 bb → 2/6 = 33,3 % → donc il faut 25 % d’équité pour suivre)  
> 
> Mais :  
> → Tu n’as **pas de main forte** (pas de paire au flop, pas de couleur complète).  
> → Les 9 outs ne te donnent **qu’un 19,1 % de chance** de gagner la main à la turn.  
> → Le **pot est trop petit** pour que cette équité t’offre une chance raisonnable.  
> 
> **La bonne action est de se coucher.**  
> Pourquoi ?  
> → La **cote du pot (25 %)** est **supérieure à la chance de toucher (19,1 %)** → donc tu n’as pas assez de chances.  
> → Le **code dit que les bonnes actions sont aucune**, et que **seulement suivre ou se coucher sont acceptables**.  
> → Tu n’as **aucune main forte** (pas de paire, pas de couleur, pas de brelan), donc **aucune action ne te donne une chance de gagner**.  
> 
> 👉 Donc, **relancer est une erreur**.  
> Tu ne gagneras jamais le pot avec cette main ici.  
> 
> Tu as compris ?  
> Pose-moi une question :  
> ➡️ *Est-ce que tu comprends pourquoi il faut se coucher ici ?*  
> (Choisir entre : A) Oui, B) Non)  
> 
> → Utilise **poser_question** pour vérifier.

*33.4 s*

### 1cd082ae — qui_gagne

> Table 6 joueurs, quiz d'abattage.
> Le coup est fini : abattage. Ton adversaire montre J♣ J♥. Tu as A♥ 7♥.
> Board : 8♣ 6♠ 6♥ Q♠ 3♦.

Décision : tu gagnes

**Débrief du coach :**

> Tu as A♥ 7♥.  
> Le board est : 8♣ 6♠ 6♥ Q♠ 3♦.  
> 
> Tu as une paire (7-7), mais **pas de 8**, donc **pas de carré ni de full**.  
> Ton adversaire a J♣ J♥ → deux jokers → **double paire** : il a une paire de jokers, et il voit un 6 sur le board (6♠ et 6♥), donc **il a une paire de 6**.  
> 
> Il a donc **double paire** (6-6 et J-J).  
> Tu as **seule paire** (7-7).  
> 
> 👉 **La règle** : chacun garde ses 5 meilleures cartes.  
> - Tu as : A♥, 7♥, 8♣, 6♠, 6♥ → tu as une paire (7-7), mais **pas de 8** → donc **pas de 8-8**, pas de carré.  
> - Ton adversaire a : J♣, J♥, 8♣, 6♠, 6♥ → il a **double paire** (6-6 et J-J).  
> 
> 👉 **Double paire > paire** → donc **il gagne**.  
> 
> **Tu gagnes ? Non.**  
> **L’erreur ?** Tu crois que tu as une bonne main, mais **tu n’as pas de 8**, donc **pas de 8-8**.  
> Il a **6-6** et **J-J**, tu as **7-7** → mais **7 < 6 ? Non** → 7 > 6 → donc **7-7 > 6-6** ?  
> 
> 👉 **Attention !**  
> Dans le poker, **la paire de 7 > paire de 6**.  
> Donc **ta paire de 7 > sa paire de 6**.  
> 
> Mais **il a aussi une paire de J** → **J > 7** → donc **il a une paire de J** → **c’est plus fort que ta paire de 7**.  
> 
> 👉 **Double paire > paire simple**.  
> Donc :  
> - Il a **double paire** (J-J et 6-6)  
> - Tu as **paire simple** (7-7)  
> 
> ✅ **Donc il gagne**.  
> 
> **Référence** :  
> - Bonnes actions : **adversaire gagne**  
> - Ta meilleure main : **paire**  
> - Sa main : **double paire**  
> - Règle : chacun garde ses 5 meilleures cartes  
> 
> 👉 **Tu as une paire de 7 → c’est bon, mais pas assez fort face à une double paire.**  
> 
> **Conclusion** :  
> Tu as **pas assez**.  
> Il a **une paire de J** → **plus forte** que ta paire de 7.  
> 
> ➡️ **Tu as perdu.**  
> 
> **Pourquoi ?**  
> Parce que **il a une double paire**, et **tu n’as qu’une paire**.  
> Dans le poker, **une paire de 7 est inférieure à une paire de J**.  
> 
> 👉 **Double paire > paire simple** → il gagne.  
> 
> Tu as **perdu**.  
> 
> **Question à choix** :  
> Quel est le meilleur type de main dans ce cas ?  
> A) Paire  
> B) Double paire  
> C) Full  
> D) Carré  
> 
> 👉 Réponds-moi.

*42.9 s*

### c549800f — defense_bb

> Table 6 joueurs, 100 blindes · tu es à la grosse blinde (BB).
> Tout le monde se couche jusqu'au BTN, qui relance à 2.5 bb ; les autres se couchent. Tu as 2♥ 3♥.
> Avant le flop · pot 4 bb, à payer 1.5 bb.

Décision : relancer

**Débrief du coach :**

> Parce que **ta main (2♥ 3♥) a seulement 33,7 % d'équité contre la range d'ouverture du BTN**, et que **le pot demande 27,3 % d'équité pour payer**.
> 
> Tu as donc **33,7 % d'équité** (c’est ce que tu gagnes si tu gagnes le pot), mais **tu dois payer 1,5 bb pour un pot de 4 bb**, ce qui correspond à une **cote de pot de 27,3 %**.
> 
> 👉 **Tu n’as pas assez d’équité pour suivre** :  
> - 33,7 % > 27,3 % → *en théorie, c’est suffisant*  
> Mais attention : **c’est l’équité contre la range d’ouverture du BTN**, pas l’équité *réalisée*.
> 
> Et **l’équité réalisée hors position est de 26,9 %** — **moins que la cote du pot (27,3 %)**.
> 
> Donc :  
> ❌ **Relancer = erreur**  
> ✅ **Se coucher = action acceptable**  
> (ou suivre, mais pas relancer)
> 
> > **C’est une situation limite** : tu n’as pas assez de chance de gagner le pot *réellement* avec cette main, surtout sans position.
> 
> 👉 **Tu as 26,9 % d’équité réelle**, **mais il faut 27,3 %** pour payer.
> 
> Donc : **tu ne peux pas payer**.
> 
> **Résumé** :  
> - Équité contre la range : 33,7 %  
> - Équité réalisée hors position : 26,9 %  
> - Cote du pot : 27,3 %  
> → **Tu n’as pas assez d’équité réelle pour payer** → **relancer = erreur**
> 
> Tu comprends ?  
> 👉 **Pose-moi une question à choix** pour vérifier.

*26.8 s*

### 3a5ac28e — ouverture

> Table 6 joueurs, 100 blindes · tu es au bouton (BTN).
> Tout le monde s'est couché jusqu'à toi (BTN). Tu as Q♠ 6♣.

Décision : relancer

**Débrief du coach :**

> Parce que la référence dit clairement : **Q6o se coucher en UTG, MP, CO, BTN, SB**.  
> 
> Tu es au **BTN**, donc dans la liste.  
> Et **se coucher** est la **bonne action**.  
> 
> Le **côté du pot** est de 100 blindes, donc le pot est petit.  
> Q6o est une main dépareillée (pas de couleur, pas de paire), donc **pas de range forte**.  
> 
> La référence ne donne **aucune action acceptable** (ni relancer, ni check) pour Q6o en position de bouton.  
> 
> 👉 Donc : **relancer = erreur**.  
> 👉 **Se coucher = bonne action**.  
> 
> Tu as 100 blindes, tu es au bouton, tu as Q6o.  
> La référence dit : **se coucher**.  
> 
> C’est la seule action autorisée.  
> 
> Tu as compris ?  
> Poser une question ? (Oui / Non)

*16.0 s*

### 17fb7d20 — tirage

> Table 6 joueurs, 100 blindes · tu es à la grosse blinde (BB).
> Au turn, ton adversaire mise 3 bb dans un pot de 6 bb. Tu as 9♣ 4♥.
> Board : 8♥ 6♦ 5♣ 3♦ · pot 9 bb, à payer 3 bb.

Décision : suivre

**Débrief du coach :**

> Tu as 9♣ 4♥ sur un board de 8♥ 6♦ 5♣ 3♦.  
> 
> Tu as 8 outs pour une quinte (9-8-7-6-5 ou 9-8-7-6-5 avec le 9 ou le 8).  
> La chance de toucher une carte qui complète ta quinte est de **17,4 %**.  
> 
> Le **pot est de 9 bb**. L’adversaire mise 3 bb, donc tu dois payer 3 bb pour un pot de 9 bb.  
> La **cote du pot** est donc de **9 / (9 + 3) = 9 / 12 = 75 %**.  
> 
> Mais pour **gagner le coup**, tu as besoin d’au moins **25,0 %** d’équité (c’est le seuil minimum pour un appel dans une situation de cote).  
> 
> → **Tu as 17,4 % d’équité**, ce qui est **inférieur à 25,0 %**.  
> 
> Donc, **suivre est une erreur**.  
> 
> 👉 La bonne action est **se coucher** : tu n’as pas assez de chance de gagner pour justifier d’aller au turn.  
> 
> C’est une règle claire pour un joueur intermédiaire : **si ta chance de gagner est < 25 %, tu ne dois pas suivre**.  
> 
> Tu as 17,4 % → **pas assez**.  
> 
> Tu as donc **perdu ton équité** en suivant.  
> 
> Tu as compris ?  
> 
> Pose-moi une question à choix pour vérifier :  
> 1. Quelle est la cote du pot ?  
> 2. Quelle est la chance de toucher ta quinte ?  
> 3. Quel est le seuil d’équité nécessaire ?  
> 4. Quelle action est correcte ici ?  
> 
> 👉 Réponds-moi avec un numéro.

*27.2 s*
