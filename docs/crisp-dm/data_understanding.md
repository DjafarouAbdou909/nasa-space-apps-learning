# Phase 2 – Compréhension des données (CRISP-DM)

**Projet :** NASA SPACE — Rotations culturales résilientes  
**Source principale :** données climatiques quotidiennes NASA POWER, 1981–2025

## 1. Périmètre

Le notebook [`data_understanding.ipynb`](../../notebooks/data_understanding.ipynb) explore les données climatiques de quatre sites en Côte d’Ivoire : Abidjan, Bouaké, Korhogo et Yamoussoukro. Il constitue une première base d’analyse pour le projet de comparaison de rotations culturales.

Les fichiers d’entrée attendus sont `power_abidjan_daily_1981_2025.csv`, `power_bouake_daily_1981_2025.csv`, `power_korhogo_daily_1981_2025.csv` et `power_yamoussoukro_daily_1981_2025.csv`.

## 2. Préparation et qualité

Le notebook charge les séries quotidiennes, harmonise leur structure et construit une date à partir de `YEAR` et `DOY`. Les valeurs sentinelles NASA POWER (`-999`) sont remplacées par des valeurs manquantes (`NaN`).

Les contrôles portent notamment sur les dates dupliquées, les jours manquants, les valeurs manquantes et les incohérences physiques. Les séries sont ensuite réunies dans `df_all`, avec une colonne `site`, et conservées par site dans `dfs`.

## 3. Exploration réalisée

L’analyse couvre :

- les cycles saisonniers des précipitations et des températures ;
- les distributions de température maximale, de précipitations les jours pluvieux, d’humidité relative et d’humidité du sol de surface ;
- l’évolution annuelle de la température moyenne et des cumuls de pluie ;
- les statistiques descriptives, les tendances linéaires et les valeurs extrêmes ;
- des indicateurs exploratoires de sécheresse et de stress hydrique ;
- la préparation de variables temporelles et retardées pour de futurs modèles.

Les variables examinées incluent notamment la température (`T2M`, `T2M_MAX`, `T2M_MIN`), les précipitations corrigées (`PRECTOTCORR`), l’humidité relative (`RH2M`), l’humidité du sol (`GWETTOP`, `GWETROOT`, `GWETPROF`) et le rayonnement solaire.

## 4. Points de vigilance

- Les seuils des indicateurs de sécheresse et de stress sont provisoires et doivent être validés par l’équipe.
- Le bilan `PRECTOTCORR - EVLAND` est une approximation ; `EVLAND` ne représente pas l’évapotranspiration potentielle.
- Le traitement des valeurs manquantes doit être adapté au modèle et ne doit pas introduire de fuite temporelle.
- Les variables retardées et les fenêtres glissantes doivent être calculées séparément par site et à partir du passé uniquement.
- Les choix de cible, de variables et de découpage temporel pour l’apprentissage restent à confirmer.

## 5. Limites et prochaines étapes

Cette exploration porte sur le climat et ne constitue pas encore un jeu de données final pour l’apprentissage automatique. Elle n’intègre pas encore les données de sol SoilGrids ni les observations AppEEARS. Il reste à définir la cible du modèle, à fusionner les sources, à valider les indicateurs agronomiques et à établir une séparation temporelle entraînement/validation/test.
