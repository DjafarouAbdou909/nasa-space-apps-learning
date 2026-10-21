# Données du projet

Ce dossier contient les données du projet (défi NASA SPACE : rotations culturales résilientes).

## Organisation

- `raw/` : données brutes téléchargées. On ne les modifie jamais.
- `interim/` : données nettoyées en cours de traitement.
- `processed/` : jeu final propre au format Parquet, prêt pour l'analyse et les modèles.

## Sites étudiés

| Site | Latitude | Longitude |
|---|---|---|
| Abidjan | 5.36 | -4.01 |
| Bouaké | 7.69 | -5.03 |
| Korhogo | 9.46 | -5.63 |
| Yamoussoukro | 6.83 | -5.29 |

## Sources de données et statut actuel

| Source | Contenu | Statut |
|---|---|---|
| NASA POWER (journalier, communauté AG) | Climat : température, humidité, pluie, rayonnement, vent, pression, évaporation, humidité du sol | Téléchargé et nettoyé (Parquet) |
| GROW-Africa (4 fichiers Excel) | Rendements agricoles : cropcut, survey (LSMS), Point, Regional | Chargés dans `notebooks/02_data_understanding` |
| NASA AppEEARS (MOD16A2GF, MOD13Q1, SMAP) | Évapotranspiration, végétation (NDVI), humidité du sol | **Données de test générées (synthétiques), pas de vraies données NASA** |
| SoilGrids (ISRIC) | Propriétés du sol : argile, sable, limon, carbone organique, pH, CEC, densité, azote | Partiel : carte d'argile 0-5 cm téléchargée |
| FAO EcoCrop | Besoins des cultures : température, pluie, pH, durée du cycle | À compiler |

> **Attention :** les fichiers AppEEARS actuels sont des données de test générées par un script pour tester le pipeline.
> Ils ne doivent jamais servir à entraîner un modèle ni à afficher un résultat. Ils seront remplacés par les vraies extractions AppEEARS.

## 1. Données climat (NASA POWER)

- **Période** : du 01/01/1981 au 31/12/2025, un jour par ligne.
- **Résolution** : environ 0,5° x 0,625° (la valeur est celle du point de grille du modèle, pas celle de la parcelle).
- **Fichiers propres** : `data/processed/power_[ville]_clean.parquet`
- **Colonnes ajoutées au nettoyage** : `date` (format AAAA-MM-JJ, créée à partir de `YEAR` et `DOY`).

### Colonnes du fichier POWER

À confirmer par Ephrem : le fichier propre doit contenir les 18 paramètres ci-dessous (pas seulement les principaux).

| Colonne | Description | Unité | Source |
|---|---|---|---|
| T2M, T2M_MAX, T2M_MIN | Température à 2 m (moyenne, max, min) | °C | MERRA-2 |
| T2MDEW | Point de rosée à 2 m | °C | MERRA-2 |
| RH2M | Humidité relative à 2 m | % | MERRA-2 |
| QV2M | Humidité spécifique à 2 m | g/kg | MERRA-2 |
| PRECTOTCORR | Précipitations corrigées | mm/jour | MERRA-2 |
| ALLSKY_SFC_SW_DWN | Rayonnement solaire (ciel réel) | MJ/m²/jour | CERES |
| CLRSKY_SFC_SW_DWN | Rayonnement solaire (ciel clair) | MJ/m²/jour | CERES |
| ALLSKY_SFC_LW_DWN | Rayonnement infrarouge descendant | MJ/m²/jour | CERES |
| WS2M | Vitesse du vent à 2 m | m/s | MERRA-2 |
| PS | Pression de surface | kPa | MERRA-2 |
| TS | Température de surface | °C | MERRA-2 |
| EVLAND | Évaporation des terres | mm/jour | MERRA-2 |
| EVPTRNS | Flux d'énergie d'évapotranspiration | MJ/m²/jour | MERRA-2 |
| GWETTOP, GWETROOT, GWETPROF | Humidité du sol (surface, zone racinaire, profil), entre 0 et 1 | sans unité | MERRA-2 |

### Valeurs manquantes

- Dans les fichiers bruts, `-999` signifie « donnée absente ». Le nettoyage les remplace par des valeurs vides (NaN).
- À Abidjan : `ALLSKY_SFC_SW_DWN` et `CLRSKY_SFC_SW_DWN` sont vides de 1981 à 1983, et `ALLSKY_SFC_LW_DWN` de 1981 à 1987. Les satellites qui les fournissent n'existaient pas avant. Les autres colonnes sont complètes.
- Ce constat a été fait sur le fichier d'Abidjan : à vérifier pour les trois autres sites.

### Lecture des fichiers

Fichier propre (usage normal) :

```python
import pandas as pd
df = pd.read_parquet("data/processed/power_abidjan_clean.parquet")
```

Fichier brut CSV (pour vérification) : le bloc de texte descriptif fait 26 lignes sur le fichier d'Abidjan.

```python
df = pd.read_csv("data/raw/power_abidjan_daily_1981_2025.csv", skiprows=26)
df = df.replace(-999, pd.NA)
```

### Reproduire un téléchargement POWER

Exemple pour Abidjan (latitude 5.36, longitude -4.01). Pour un autre site, changer seulement ces deux nombres dans l'URL (la longitude vient avant la latitude) :
https://power.larc.nasa.gov/api/temporal/daily/point?parameters=T2M,T2M_MAX,T2M_MIN,T2MDEW,RH2M,QV2M,PRECTOTCORR,ALLSKY_SFC_SW_DWN,CLRSKY_SFC_SW_DWN,ALLSKY_SFC_LW_DWN,WS2M,PS,TS,EVLAND,EVPTRNS,GWETTOP,GWETROOT,GWETPROF&community=AG&longitude=-4.01&latitude=5.36&start=19810101&end=20251231&format=CSV

## 2. Données sol (SoilGrids)

- **Fichier brut** : `data/raw/soilgrids_cote_divoire.tif`
- **Format** : image géographique GeoTIFF.
- **Contenu** : taux d'argile moyen pour la couche de surface (0-5 cm), couvrant la Côte d'Ivoire.
- **Limite** : une seule propriété et une seule profondeur. Il manque encore le sable, le limon, le carbone organique, le pH, la CEC, la densité apparente, l'azote, et les autres profondeurs (jusqu'à 100-200 cm).
- Le `.gitignore` du projet exclut les fichiers `.tif` : si le fichier est absent après un `git pull`, le régénérer avec le script d'ingestion (voir le guide plus bas).

## 3. Données végétation et eau (NASA AppEEARS) : DONNÉES DE TEST

- **Fichiers générés** : `data/raw/appeears_[ville]_raw.csv`
- **Nature** : données de test synthétiques, créées pour vérifier le pipeline. Ce ne sont pas des mesures NASA.
- **Variables de test incluses** :
  * `MOD13Q1_NDVI` : indice de végétation (0 à 1).
  * `MOD16A2GF_ET` : évapotranspiration (mm/8 jours).
  * `SMAP_ZONE_RACINAIRE` : humidité du sol (m³/m³).
- **À faire (Ephrem)** : remplacer ces fichiers par les vraies extractions AppEEARS (point sample, format CSV, avec les colonnes de qualité QA), et déplacer les données de test hors de `raw/` (par exemple dans `data/synthetic/`), pour qu'on ne les confonde pas avec des données réelles.

## 4. Données rendements (GROW-Africa)

Quatre fichiers Excel, chargés dans `notebooks/02_data_understanding` :

| Fichier | Lignes x colonnes | Nature |
|---|---|---|
| GROW-Africa_LSMS_cropcut | 11 345 x 20 | Rendements mesurés par carré de rendement |
| GROW-Africa_LSMS_survey | 195 152 x 27 | Enquêtes ménages (rendements déclarés) |
| GROW-Africa_Point | 131 812 x 17 | Parcelles, essais et enquêtes |
| GROW-Africa_Regional | 197 535 x 25 | Statistiques administratives (FAOSTAT, HarvestStat) |

- Le détail des colonnes et les limites (coordonnées à 5 km, dates incomplètes, noms de cultures non harmonisés) sont dans le cahier des charges, section 5 et annexe A.
- Les identifiants de ménage (`holder_id`, `household_id`, `hhid`) ne doivent jamais être publiés ni exposés dans l'API : les supprimer à la préparation.

## Nature des données

- **Mesure satellite** : rayonnement (CERES), NDVI et réflectance (MODIS).
- **Sortie de modèle** : pluie, température, humidité, évaporation et humidité du sol de POWER (MERRA-2), humidité de la zone racinaire de SMAP, SoilGrids.
- **Indicateur indirect** : stress hydrique, santé du sol (déduits d'autres variables).

À préciser dans le rapport final : la plupart des variables climatiques sont des estimations de modèles, pas des mesures au sol.

## Guide d'exécution du pipeline (maintenu par Ephrem)

Pour régénérer les fichiers localement, ouvrir un terminal à la racine du projet et lancer :

1. **Nettoyage climatique complet (NASA POWER) :**
```bash
   python src/ingestion/load_power.py
```
2. **Téléchargement de la carte de sol (SoilGrids) :**
```bash
   python src/ingestion/fetch_soilgrids.py
```
3. **Génération des données de test (NASA AppEEARS), pas de vraies données :**
```bash
   python src/ingestion/fetch_appeears.py
```

La lecture des fichiers Parquet demande la bibliothèque `pyarrow` (déjà dans `requirements.txt`).

## Consignes pour l'équipe

- Les fichiers climatiques propres se chargent en une ligne avec Pandas (voir « Lecture des fichiers »). La colonne `date` est alignée et prête pour le calcul des indicateurs.
- Les fichiers de `raw/` ne sont jamais modifiés à la main.
- Noms de fichiers : minuscules, sans accents, `<source>_<site>_<...>`.
- Pas de gros fichiers bruts (SMAP, MODIS) dans Git : on pousse uniquement les extractions légères.
- Toute nouvelle source est ajoutée dans le tableau des sources avec son URL et sa date de téléchargement.
