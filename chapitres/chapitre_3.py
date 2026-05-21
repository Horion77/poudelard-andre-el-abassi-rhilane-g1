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
            offensifs.append(sort)
            print("Tu viens d'apprendre le sortilège : " + sort["nom"] + " (" + sort["type"] + ")")
            input("Appuie sur Entrée pour continuer...")
        elif sort["type"] == "Défensif" and len(defensifs) < 1 and sort not in defensifs:
            defensifs.append(sort)
            print("Tu viens d'apprendre le sortilège : " + sort["nom"] + " (" + sort["type"] + ")")
            input("Appuie sur Entrée pour continuer...")
        elif sort["type"] == "Utilitaire" and len(utilitaires) < 3 and sort not in utilitaires:
            utilitaires.append(sort)
            print("Tu viens d'apprendre le sortilège : " + sort["nom"] + " (" + sort["type"] + ")")
            input("Appuie sur Entrée pour continuer...")

    sorts_appris = offensifs + defensifs + utilitaires
    for sort in sorts_appris:
        ajouter_objet(joueur, "Sortilèges", sort["nom"])

    print("\nTu as terminé ton apprentissage de base à Poudlard !")
    print("Voici les sortilèges que tu maîtrises désormais :")
    for sort in sorts_appris:
        print("- " + sort["nom"] + " (" + sort["type"] + ") : " + sort["description"])






def lancer_chapitre_3(personnage, maisons):
    apprendre_sorts(personnage)
    score = quiz_magie(personnage)
    actualiser_points_maison(maisons, personnage["Maison"], score)
    afficher_maison_gagnante(maisons)
    afficher_personnage(personnage)