# Données du projet

Ce dossier contient les données du projet (défi NASA SPACE : rotations culturales résilientes).

## Organisation

- `raw/` : Données brutes téléchargées ou générées. On ne les modifie jamais.
- `interim/` : Données nettoyées en cours de traitement.
- `processed/` : Jeu final propre au format Parquet prêt pour l'analyse et les modèles.

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
