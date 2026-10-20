# Données du projet

Ce dossier contient les données du projet (défi NASA SPACE : rotations culturales résilientes).

## Organisation

<<<<<<< HEAD
- `raw/` : données brutes téléchargées. On ne les modifie jamais.
- `interim/` : données nettoyées (valeurs manquantes, unités, échelles).
- `processed/` : jeu final prêt pour l'analyse et les modèles.
=======
- `raw/` : Données brutes téléchargées ou générées. On ne les modifie jamais.
- `interim/` : Données nettoyées en cours de traitement.
- `processed/` : Jeu final propre au format Parquet prêt pour l'analyse et les modèles.
>>>>>>> origin/main

## Sites étudiés

| Site | Latitude | Longitude |
|---|---|---|
| Abidjan | 5.36 | -4.01 |
| Bouaké | 7.69 | -5.03 |
| Korhogo | 9.46 | -5.63 |
| Yamoussoukro | 6.83 | -5.29 |

<<<<<<< HEAD
## Sources de données

| Source | Contenu | Statut |
|---|---|---|
| NASA POWER (journalier, communauté AG) | Climat : température, humidité, pluie, rayonnement, vent, pression, évaporation, humidité du sol | Téléchargé |
| NASA AppEEARS (MOD16A2GF, MOD13Q1, SMAP) | Évapotranspiration, végétation (NDVI), humidité du sol | À télécharger |
| SoilGrids (ISRIC) | Propriétés du sol : argile, sable, limon, carbone organique, pH, CEC, densité, azote | À télécharger |
| FAO EcoCrop | Besoins des cultures : température, pluie, pH, durée du cycle | À compiler |

## NASA POWER : détails

- **Période** : du 01/01/1981 au 31/12/2025, un jour par ligne.
- **Résolution** : environ 0,5° x 0,625° (la valeur est celle du point de grille du modèle, pas celle de la parcelle).
- **Colonnes** : `YEAR`, `DOY` (jour de l'année), puis 18 paramètres.

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

### Lecture des fichiers

Chaque fichier commence par un bloc de texte descriptif de 26 lignes, avant les données (à vérifier sur chaque fichier).

```python
import pandas as pd
df = pd.read_csv("data/raw/power_abidjan_daily_1981_2025.csv", skiprows=26)
df = df.replace(-999, pd.NA)
```

### Valeurs manquantes

- `-999` signifie « donnée absente ». À remplacer par une valeur vide avant toute analyse.
- À Abidjan, les colonnes de rayonnement solaire (`ALLSKY_SFC_SW_DWN`, `CLRSKY_SFC_SW_DWN`) sont vides de 1981 à 1983, et `ALLSKY_SFC_LW_DWN` de 1981 à 1987. Les satellites qui les fournissent n'existaient pas avant. Les autres colonnes sont complètes.

## Nature des données

- **Mesure satellite** : rayonnement (CERES), NDVI et réflectance (MODIS).
- **Sortie de modèle** : pluie, température, humidité, évaporation et humidité du sol de POWER (MERRA-2), humidité de la zone racinaire de SMAP, SoilGrids.
- **Indicateur indirect** : stress hydrique, santé du sol (déduits d'autres variables).

À préciser dans le rapport final : la plupart des variables climatiques sont des estimations de modèles, pas des mesures au sol.

## Reproduire un téléchargement POWER

Exemple pour Abidjan (latitude 5.36, longitude -4.01). Pour un autre site, changer seulement ces deux nombres dans l’URL (la longitude vient avant la latitude) :
https://power.larc.nasa.gov/api/temporal/daily/point?parameters=T2M,T2M_MAX,T2M_MIN,T2MDEW,RH2M,QV2M,PRECTOTCORR,ALLSKY_SFC_SW_DWN,CLRSKY_SFC_SW_DWN,ALLSKY_SFC_LW_DWN,WS2M,PS,TS,EVLAND,EVPTRNS,GWETTOP,GWETROOT,GWETPROF&community=AG&longitude=-4.01&latitude=5.36&start=19810101&end=20251231&format=CSV
=======
## Sources de données et statut actuel

| Source | Contenu | Statut |
|---|---|---|
| NASA POWER (journalier, communauté AG) | Climat : température, humidité, pluie, rayonnement, vent, pression, évaporation, humidité du sol | Téléchargé & Nettoyé |
| NASA AppEEARS (MOD16A2GF, MOD13Q1, SMAP) | Évapotranspiration, végétation (NDVI), humidité du sol | Données de test générées |
| SoilGrids (ISRIC) | Propriétés du sol : argile, sable, limon, carbone organique, pH, CEC, densité, azote | Carte d'argile téléchargée |
| FAO EcoCrop | Besoins des cultures : température, pluie, pH, durée du cycle | À compiler |

## 1. Données Climat (NASA POWER)

- **Période** : Du 01/01/1981 au 31/12/2025, un jour par ligne.
- **Résolution** : Environ 0,5° x 0,625°.
- **Fichiers propres générés** : `data/processed/power_[ville]_clean.parquet`

### Colonnes principales disponibles :
* `date` : Date normalisée au format YYYY-MM-DD (créée à partir de YEAR et DOY).
* `YEAR` : Année de la mesure.
* `DOY` : Jour de l'année (1 à 365/366).
* `T2M`, `T2M_MAX`, `T2M_MIN` : Température à 2 m (moyenne, max, min en °C).
* `PRECTOTCORR` : Précipitations corrigées (mm/jour).
* `ALLSKY_SFC_SW_DWN` : Rayonnement solaire réel (MJ/m²/jour).
* `GWETROOT` : Humidité du sol dans la zone racinaire (entre 0 et 1).

### Traitement des valeurs manquantes :
- Les valeurs manquantes `-999` ont été remplacées par des valeurs `None` (NaN).
- À Abidjan, les colonnes de rayonnement solaire (`ALLSKY_SFC_SW_DWN`) sont vides de 1981 à 1983. Les autres colonnes sont complètes.

## 2. Données Sol (SoilGrids)

- **Fichier brut** : `data/raw/soilgrids_cote_divoire.tif`
- **Format** : Image géographique GeoTIFF.
- **Contenu** : Taux d'argile moyen pour la couche de surface (0-5 cm) couvrant la Côte d'Ivoire.

## 3. Données Végétation et Eau (NASA AppEEARS)

- **Fichiers bruts générés** : `data/raw/appeears_[ville]_raw.csv`
- **Variables de test incluses** :
  * `MOD13Q1_NDVI` : Indice de végétation (0 à 1).
  * `MOD16A2GF_ET` : Évapotranspiration (mm/8 jours).
  * `SMAP_ZONE_RACINAIRE` : Humidité du sol (m³/m³).

## Guide d'exécution du pipeline (Ephrem)

Pour exécuter les scripts d'ingestion et régénérer ces fichiers localement sur vos environnements, ouvrez votre terminal à la racine du projet et lancez les commandes suivantes :

1. **Nettoyage climatique complet (NASA POWER) :**
   ```bash
   python src/ingestion/load_power.py
   ```
2. **Téléchargement de la carte de sol (SoilGrids) :**
   ```bash
   python src/ingestion/fetch_soilgrids.py
   ```
3. **Génération des structures d'exemple (NASA AppEEARS) :**
   ```bash
   python src/ingestion/fetch_appeears.py
   ```

## Consignes pour l'équipe (Michel, Ronel, Djafarou)

Les fichiers climatiques épurés se chargent directement avec Pandas en une seule ligne :
```python
import pandas as pd
df = pd.read_parquet("data/processed/power_abidjan_clean.parquet")
```
Les index temporels `date` sont alignés et prêts pour le calcul des indicateurs agronomiques.
>>>>>>> origin/main
