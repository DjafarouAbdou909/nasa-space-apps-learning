import os
import requests

# Ou on range le fichier brut
DOSSIER_SORTIE = "data/raw"

print("Debut du telechargement des donnees SoilGrids")

# L'adresse pour chopper la carte d'argile de la Cote d'Ivoire
url_soilgrids = "https://isric.org"

# Le chemin pour sauvegarder le fichier de sol
chemin_sauvegarde = os.path.join(DOSSIER_SORTIE, "soilgrids_cote_divoire.tif")

try:
    # Lancement du telechargement et ultimatum de 60 secondes parce que la pufff
    reponse = requests.get(url_soilgrids, timeout=60)
    
    # Si le serveur repond 200 c'est bon, on cree le fichier
    if reponse.status_code == 200:
        with open(chemin_sauvegarde, 'wb') as f:
            f.write(reponse.content)
        print(f"Fichier sol sauvegarde avec succes : {chemin_sauvegarde}")
    else:
        print(f"Erreur de serveur SoilGrids, code : {reponse.status_code}")

except Exception as e:
    # Si internet coupe ou que ca bug, on capte le probleme ici
    print(f"Erreur pendant le telechargement : {e}")

print("Wesh fin du traitement des donnees SoilGrids")
