# chapitre_3.py
import random
from utils.input_utils import load_fichier
from univers.personnage import afficher_personnage, ajouter_objet
from univers.maison import actualiser_points_maison, afficher_maison_gagnante


def apprendre_sorts(joueur, chemin_fichier="data/sorts.json"):
    tous_les_sorts = load_fichier(chemin_fichier)
    offensifs = []
    defensifs = []
    utilitaires = []
    sorts_appris = []

    print("\nTu commences tes cours de magie à Poudlard...")

    while len(offensifs) < 1 or len(defensifs) < 1 or len(utilitaires) < 3:
        sort = random.choice(tous_les_sorts)
        if sort["nom"] in joueur["Sortilèges"]:
            continue
        if sort["type"] == "Offensif" and len(offensifs) < 1 and sort not in offensifs:
            offensifs.append(sort)
            sorts_appris.append(sort)
            print("Tu viens d'apprendre le sortilège : " + sort["nom"] + " (" + sort["type"] + ")")
            ajouter_objet(joueur, "Sortilèges", sort["nom"])
            input("Appuie sur Entrée pour continuer...")
        elif sort["type"] == "Défensif" and len(defensifs) < 1 and sort not in defensifs:
            defensifs.append(sort)
            sorts_appris.append(sort)
            print("Tu viens d'apprendre le sortilège : " + sort["nom"] + " (" + sort["type"] + ")")
            ajouter_objet(joueur, "Sortilèges", sort["nom"])
            input("Appuie sur Entrée pour continuer...")
        elif sort["type"] == "Utilitaire" and len(utilitaires) < 3 and sort not in utilitaires:
            utilitaires.append(sort)
            sorts_appris.append(sort)
            print("Tu viens d'apprendre le sortilège : " + sort["nom"] + " (" + sort["type"] + ")")
            ajouter_objet(joueur, "Sortilèges", sort["nom"])
            input("Appuie sur Entrée pour continuer...")

    print("\nTu as terminé ton apprentissage de base à Poudlard !")
    print("Voici les sortilèges que tu maîtrises désormais :")
    for sort in sorts_appris:
        print("- " + sort["nom"] + " (" + sort["type"] + ") : " + sort["description"])


def quiz_magie(joueur, chemin_fichier="data/quiz_magie.json"):
    # Le score du quiz est ajouté aux points de la maison du joueur dans lancer_chapitre_3.
    toutes_les_questions = load_fichier(chemin_fichier)
    questions_choisies = []
    while len(questions_choisies) < 4:
        question = random.choice(toutes_les_questions)
        if question not in questions_choisies:
            questions_choisies.append(question)

    print("\nBienvenue au quiz de magie de Poudlard !")
    print("Réponds correctement aux 4 questions pour faire gagner des points à ta maison.")

    score = 0
    numero = 1
    for q in questions_choisies:
        print("\n" + str(numero) + ". " + q["question"])
        reponse = input("> ").strip().lower()
        if reponse == q["reponse"].lower():
            print("Bonne réponse ! +25 points pour ta maison.")
            score = score + 25
        else:
            print("Mauvaise réponse. La bonne réponse était : " + q["reponse"])
        numero = numero + 1

    print("\nScore obtenu : " + str(score) + " points")
    print("Ces points seront ajoutés au total de ta maison.")
    return score


def lancer_chapitre_3(personnage, maisons):
    apprendre_sorts(personnage)
    score = quiz_magie(personnage)
    actualiser_points_maison(maisons, personnage["Maison"], score)
    afficher_maison_gagnante(maisons)
    afficher_personnage(personnage)
