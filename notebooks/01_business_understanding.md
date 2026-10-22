# Phase 1 – Compréhension du métier (CRISP-DM)

Projet : African Crop Yield Intelligence – NASA Space Apps, « Agriculture résiliente et rotations culturales »
Responsable : Djafarou Abdou (lead / ML) · Statut : version 1, à valider par l'équipe

Ce document est la version courte de la phase 1. Le détail (exigences, planning, risques) est dans le cahier des charges.

---

## 1. Contexte

Les agriculteurs font face à des sols qui se dégradent, à l'eau qui manque et à un climat de plus en plus imprévisible. Ces contraintes rendent difficile le choix de rotations culturales qui protègent les champs, préservent l'eau et favorisent la résilience à long terme.

Le défi NASA SPACE demande un outil d'aide à la décision qui exploite les observations de la Terre de la NASA, ainsi que les informations locales sur les sols, les caractéristiques des cultures et les priorités des agriculteurs, pour les aider à explorer des stratégies de rotation susceptibles d'améliorer la santé des sols et d'adapter leurs exploitations aux conditions changeantes.

## 2. Objectif métier

Construire et déployer un outil qui compare plusieurs stratégies de rotation culturale sur plusieurs saisons ou années, et présente les résultats, les compromis et les incertitudes dans une interface compréhensible par un agriculteur ou un conseiller agricole.

L'outil doit :
- analyser le climat historique et actuel d'une zone (pluie, température, rayonnement, sécheresses) ;
- caractériser le sol et ses contraintes ;
- comparer les besoins en eau et les cycles de croissance des cultures ;
- tenir compte des priorités de l'agriculteur : rendement, économies d'eau, coûts, fertilité du sol, résilience climatique ;
- dire clairement ce qui est **observé**, ce qui est **estimé par un modèle** et ce qui est un **indicateur indirect**.

## 3. Pour qui

| Utilisateur | Besoin | Ce que l'outil lui donne |
|---|---|---|
| Agriculteur | Choisir quoi planter après quoi, sans perdre en eau ni en fertilité | Comparaison simple par critère, avec incertitude, lisible sur téléphone |
| Conseiller agricole | Appuyer ses conseils sur des données | Détail des indicateurs, sources, limites |
| Jury et partenaires du défi | Juger la rigueur et l'utilité | Transparence sur la nature des données, démonstration qui fonctionne |

## 4. Traduction en problème de data science

| Question métier | Question data science |
|---|---|
| « Quelle culture planter cette saison dans ma zone ? » | Prédire le **rendement (t/ha)** d'une culture, pour une zone et une campagne, à partir du climat et du sol (cible A) |
| « Mon sol et mon eau tiennent-ils ? » | Indicateurs d'humidité du sol et de végétation (cibles B : NDVI, C : humidité SMAP) |
| « Quelle succession de cultures est la plus résiliente ? » | Comparer les rendements prédits et leur risque pour plusieurs cultures, puis appliquer des règles agronomiques sourcées (EcoCrop) |

**Cible retenue par défaut : A (rendement).** On passe à B si les rendements de la zone d'étude sont trop peu nombreux (décision D2 du cahier des charges).

**Limite à assumer.** Le modèle ne prouve pas qu'une culture rend plus après une autre. Il faudrait suivre la même parcelle sur plusieurs campagnes (hhid + plotid + AgYearStart), ce qui reste à vérifier dans GROW-Africa. Sans cela, l'effet de rotation vient de règles issues de la littérature, citées, et non d'une preuve du modèle.

## 5. Critères de succès

| N° | Critère | Mesure |
|---|---|---|
| CS1 | Pour chaque rotation comparée, un résultat par critère (eau, sol, rendement attendu, risque) avec son incertitude | Revue de l'interface par Product |
| CS2 | Le modèle retenu fait mieux que la référence simple (moyenne par culture et par zone) sur des données jamais vues | RMSE et MAE sur un jeu de test découpé par zone et par année |
| CS3 | Chaque indicateur affiché a une définition écrite et une source | Contrôle de `docs/` par le lead |
| CS4 | Une personne extérieure à l'équipe compare deux rotations sans aide | Test avec 2 ou 3 personnes, en moins de 5 minutes |
| CS5 | Une version déployée est accessible par un lien public avant la démonstration | Essai la veille |

Ces cibles sont à valider par l'équipe.

## 6. Ressources, contraintes, hypothèses

**Ressources.** Équipe de 6 personnes : 2 Data Scientists (Michel, Ronel), 1 Data Engineer (Ephrem), 1 ML (Djafarou Abdou), 1 Backend (Souleymane), 1 Product scientifique et Frontend(Aimard). Données : NASA POWER, GROW-Africa, SoilGrids, AppEEARS, EcoCrop. Dépôt GitHub commun.

**Contraintes.**
- Délai : date limite du défi à confirmer auprès des organisateurs (D6).
- Un seul Data Engineer, et Aimard cumule Backend et Product : risque de goulot et de surcharge.
- Hébergement gratuit : l'application peut être en veille pendant la démonstration.
- Licences : vérifier et citer les sources avant toute publication.

**Hypothèses (non encore vérifiées).**
- GROW-Africa contient assez de rendements pour la Côte d'Ivoire (D1).
- Le climat et le sol d'un point à 50 km représentent suffisamment bien une zone de culture.
- Les cultures retenues ont assez de lignes de rendement et une fiche EcoCrop (D3).

## 7. Risques principaux

| Risque | Réponse |
|---|---|
| Peu ou pas de rendements pour la zone | Compter dès la semaine 1 ; sinon cible B ou zone élargie |
| Coordonnées dégradées à 5 km | Moyennes sur un rayon ; le dire dans l'interface |
| Rotation non observable dans les données | Règles sourcées ; ne pas prétendre prouver l'effet |
| Retard du Data Engineer | Cahier des charges de données clair ; Backend en renfort au début |

