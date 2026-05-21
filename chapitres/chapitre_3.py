# chapitre_3.py
import random
from utils.input_utils import load_fichier
from univers.personnage import afficher_personnage,ajouter_objet
from univers.maison import actualiser_points_maison,afficher_maison_gagnante

def apprendre_sorts(joueur, chemin_fichier="data/sorts.json"):
    tous_les_sorts = load_fichier(chemin_fichier)
    offensifs = []
    defensifs = []
    utilitaires = []

    print("\nTu commences tes cours de magie à Poudlard...")

    while len(offensifs) < 1 or len(defensifs) < 1 or len(utilitaires) < 3:
        sort = random.choice(tous_les_sorts)
        if sort["type"] == "Offensif" and len(offensifs) < 1 and sort not in offensifs: