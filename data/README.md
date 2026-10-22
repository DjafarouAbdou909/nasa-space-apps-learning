# Dictionnaire des Données - Phase 2 (Data Preparation)

Ce dossier contient et documente les données du projet (défi NASA SPACE : rotations culturales résilientes).

## Organisation des Dossiers

- `data/raw/` : Données brutes originales téléchargées ou générées. On ne les modifie jamais.
- `data/interim/` : Données nettoyées ou agrégations en cours de traitement intermédiaire.
- `data/processed/` : Jeux de données finaux propres au format Parquet, prêts pour les modèles.

## Sites étudiés

| Site | Latitude | Longitude |
|---|---|---|
| Abidjan | 5.36 | -4.01 |
| Bouaké | 7.69 | -5.03 |
| Korhogo | 9.46 | -5.63 |
| Yamoussoukro | 6.83 | -5.29 |

## 1. Données Climat Harmonisées (NASA POWER)

Données quotidiennes historiques (1981-2025) nettoyées et stockées au format Parquet.
* **Chemin :** `data/processed/power_[ville]_clean.parquet`
* **Résolution spatiale :** ~50 km (Grille de modèle, ne représente pas une parcelle isolée).

| Variable | Description Technique | Unité | Rôle dans le Modèle |
| :--- | :--- | :--- | :--- |
| `date` | Identifiant temporel normalisé (YYYY-MM-DD) | Date | Clé de jointure primaire |
| `YEAR` | Année civile de la mesure | Année | Suivi des tendances |
| `DOY` | Jour de l'année (Day of Year) | 1 à 366 | Repérage des saisons |
| `T2M` | Température moyenne de l'air à 2 mètres | °C | Accumulation thermique |
| `T2M_MAX` | Température maximale enregistrée à 2 mètres | °C | Détection des stress thermiques |
| `T2M_MIN` | Température minimale enregistrée à 2 mètres | °C | Refroidissement nocturne |
| `PRECTOTCORR`| Précipitations totales corrigées | mm/jour | À convertir en cumuls glissants |
| `RH2M` | Humidité relative à 2 mètres | % | Saturation de l'air |
| `ALLSKY_SFC_SW_DWN` | Rayonnement solaire incident (ciel réel) | MJ/m²/jour| Vide avant 1984 (limite satellite) |
| `ALLSKY_SFC_LW_DWN` | Rayonnement infrarouge descendant thermique | MJ/m²/jour| Vide avant 1988 (limite satellite) |
| `GWETROOT` | Humidité du sol dans la zone racinaire | Sans unité | Index modélisé entre 0 et 1 |

*Note sur les valeurs manquantes : Les codes absents `-999` ont été convertis en `None` (NaN) lors du pipeline de nettoyage.*

## 2. Propriétés Physico-Chimiques du Sol (SoilGrids)

Données géospatiales extraites de l'ISRIC caractérisant la couche arable de surface (0-5 cm).
* **Chemin :** `data/raw/soilgrids_cote_divoire.tif`
* **Résolution spatiale :** 250 mètres par pixel.

| Variable | Description Agronomique | Unité | Rôle dans le Modèle |
| :--- | :--- | :--- | :--- |
| `clay_0-5cm_mean` | Proportion moyenne d'argile dans le sol | g/kg | Rétention en eau |
| `sand_0-5cm_mean` | Proportion moyenne de sable dans le sol | g/kg | Drainage et perméabilité |
| `silt_0-5cm_mean` | Proportion moyenne de limon dans le sol | g/kg | Texture et équilibre |
| `phh2o_0-5cm_mean`| Potentiel Hydrogène (pH) mesuré dans l'eau | pH x 10 | Évaluation de l'acidité |

## 3. Données de Télédétection Satellites (NASA AppEEARS)

Indicateurs réels à intégrer pour remplacer le prototypage synthétique.
* **Chemin :** `data/raw/appeears_[ville]_raw.csv`
* **Pas de temps :** Composites de 8 à 16 jours.

| Variable | Capteur Source | Unité | Description Agronomique |
| :--- | :--- | :--- | :--- |
| `MOD13Q1_NDVI` | MODIS (Indice de végétation) | 0 à 1 | Vigueur et santé de la plante |
| `MOD16A2GF_ET` | MODIS (Évapotranspiration) | mm/8 jours| Consommation en eau culturelle |
| `SMAP_ZONE_RACINAIRE`| SMAP (Radiomètre Micro-ondes) | m³/m³ | Humidité mesurée de la zone racinaire |

## Guide d'exécution du pipeline (Ephrem)

Pour régénérer les fichiers ou actualiser les pipelines locaux, exécutez ces scripts depuis la racine :

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
Les index temporels `date` sont alignés et prêts pour le calcul des indicateurs agronomiques (comme les cumuls de pluie et seuils de jours secs).
