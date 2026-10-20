import os
import pandas as pd

# Definitions des chemins des dossiers
DOSSIER_BRUT = "data/raw"
DOSSIER_PROPRE = "data/processed"

# Liste des 4 fichiers de la NASA a traiter
fichiers_nasa = [
    "power_abidjan_daily_1981_2025.csv",
    "power_bouake_daily_1981_2025.csv",
    "power_korhogo_daily_1981_2025.csv",
    "power_yamoussoukro_daily_1981_2025.csv"
]

print("Debut du nettoyage des fichiers NASA POWER")

for nom_fichier in fichiers_nasa:
    chemin_entree = os.path.join(DOSSIER_BRUT, nom_fichier)
    
    if not os.path.exists(chemin_entree):
        print(f"Fichier introuvable : {nom_fichier}")
        continue
        
    print(f"Traitement du fichier : {nom_fichier}")

    # Recherche dynamique de la fin de l'en-tete
    lignes_a_sauter = 0
    with open(chemin_entree, 'r') as f:
        for i, ligne in enumerate(f):
            if "-END HEADER-" in ligne:
                lignes_a_sauter = i + 1
                break

    # Chargement du CSV
    df = pd.read_csv(chemin_entree, skiprows=lignes_a_sauter)

    # Remplacement de la valeur manquante -999 par None
    df = df.replace(-999, None)

    # Conversion des colonnes de temps en entiers
    df['YEAR'] = df['YEAR'].astype(int)
    df['DOY'] = df['DOY'].astype(int)
    
    # Creation de la colonne date
    df['date'] = pd.to_datetime(df['YEAR'].astype(str) + '-' + df['DOY'].astype(str), format='%Y-%j')
    ville = nom_fichier.split('_')[1]
    
    # Preparation du chemin de sauvegarde
    nom_sortie = f"power_{ville}_clean.parquet"
    chemin_sortie = os.path.join(DOSSIER_PROPRE, nom_sortie)

    # Sauvegarde au format Parquet
    df.to_parquet(chemin_sortie, index=False)
    print(f"Fichier sauvegarde : {chemin_sortie}")

print("Fin du traitement des fichiers NASA POWER")
