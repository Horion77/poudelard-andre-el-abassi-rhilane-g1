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


# =====================================================================
# VERSION ALTERNATIVE (IMMERSIVE) — mise en scène + cours de Rogue 3-en-1.
# À DÉCIDER AVEC LE GROUPE : on garde laquelle ?
# Pour l'ACTIVER : commenter les fonctions ci-dessus (apprendre_sorts,
# quiz_magie, lancer_chapitre_3) et décommenter TOUT le bloc ci-dessous
# (les deux lignes d'import comprises).
# =====================================================================
#
# from utils.input_utils import demander_choix
# from utils.couleurs import JAUNE, VERT, ROUGE, CYAN, VIOLET, GRIS, GRAS, RESET, titre, colorer
#
#
# def pause():
#     input(GRIS + "  (Entrée pour continuer...)" + RESET)
#
#
# def apprendre_sorts(joueur, chemin_fichier="data/sorts.json"):
#     tous_les_sorts = load_fichier(chemin_fichier)
#     offensifs = []
#     defensifs = []
#     utilitaires = []
#     sorts_appris = []
#
#     print("\n" + titre("CHAPITRE 3 — Les cours commencent"))
#     print("\nPremier cours de Sortilèges. Le minuscule professeur Flitwick")
#     print("se tient debout sur sa pile de livres. « Baguette levée, et... swish ! »")
#     print("À côté de toi, Hermione réussit du premier coup. Évidemment.")
#     pause()
#
#     while len(offensifs) < 1 or len(defensifs) < 1 or len(utilitaires) < 3:
#         sort = random.choice(tous_les_sorts)
#         if sort["nom"] in joueur["Sortilèges"]:
#             continue
#         if sort["type"] == "Offensif" and len(offensifs) < 1 and sort not in offensifs:
#             offensifs.append(sort)
#             sorts_appris.append(sort)
#             print(colorer("Tu maîtrises : " + sort["nom"], VERT) + GRIS + " (" + sort["type"] + ")" + RESET)
#             ajouter_objet(joueur, "Sortilèges", sort["nom"])
#         elif sort["type"] == "Défensif" and len(defensifs) < 1 and sort not in defensifs:
#             defensifs.append(sort)
#             sorts_appris.append(sort)
#             print(colorer("Tu maîtrises : " + sort["nom"], VERT) + GRIS + " (" + sort["type"] + ")" + RESET)
#             ajouter_objet(joueur, "Sortilèges", sort["nom"])
#         elif sort["type"] == "Utilitaire" and len(utilitaires) < 3 and sort not in utilitaires:
#             utilitaires.append(sort)
#             sorts_appris.append(sort)
#             print(colorer("Tu maîtrises : " + sort["nom"], VERT) + GRIS + " (" + sort["type"] + ")" + RESET)
#             ajouter_objet(joueur, "Sortilèges", sort["nom"])
#
#     print(colorer("\nTes cinq premiers sortilèges :", GRAS))
#     for sort in sorts_appris:
#         print("  - " + colorer(sort["nom"], JAUNE) + " (" + sort["type"] + ") : " + sort["description"])
#     pause()
#
#
# def cours_de_rogue(joueur):
#     # Mini-jeu en 3 manches (reconnaissance / potion / logique).
#     # Chaque bonne reponse rapporte 10 points a la maison. Renvoie le total.
#     print("\n" + titre("Cachots — Cours de Potions"))
#     print("\nLa porte claque. Le professeur " + colorer("Rogue", VIOLET) + " avance entre les pupitres,")
#     print("la voix basse et glaciale. « Voyons si vous valez mieux que les autres. »")
#     pause()
#
#     points = 0
#
#     # Manche 1 : reconnaissance de sort
#     print(colorer("\n— Manche 1 : reconnaissance —", GRAS))
#     print("« Un adversaire pointe sa baguette sur vous. Quel sort le désarme ? »")
#     rep = demander_choix("Votre réponse :", ["Expelliarmus", "Lumos", "Reparo"])
#     if rep == "Expelliarmus":
#         print(colorer("Rogue hausse un sourcil. « ...Correct. » (+10)", VERT))
#         points = points + 10
#     else:
#         print(colorer("« Lamentable. C'était Expelliarmus. »", ROUGE))
#     pause()
#
#     # Manche 2 : ordre des ingredients (memoire)
#     print(colorer("\n— Manche 2 : la potion —", GRAS))
#     print("Rogue dicte une fois, sans répéter :")
#     print(colorer("  1) Racine de mandragore  2) Bile de tatou  3) Crochet de serpent", CYAN))
#     print("« Dans l'ordre. Par quoi commencez-vous ? »")
#     rep = demander_choix("Premier ingrédient :", ["Racine de mandragore", "Bile de tatou", "Crochet de serpent"])
#     if rep == "Racine de mandragore":
#         print(colorer("Le chaudron vire au bleu parfait. (+10)", VERT))
#         points = points + 10
#     else:
#         print(colorer("Le chaudron crache une fumée noire. « Encore raté. »", ROUGE))
#     pause()
#
#     # Manche 3 : enigme de logique
#     print(colorer("\n— Manche 3 : l'énigme —", GRAS))
#     print("Sept flacons devant une porte de flammes. Un seul fait avancer.")
#     print("« Le plus petit flacon est à côté du poison. Le danger guette les pressés. »")
#     rep = demander_choix(
#         "Quel flacon choisis-tu ?",
#         ["Le plus petit flacon", "Le plus grand flacon", "Celui du milieu, au hasard"]
#     )
#     if rep == "Le plus petit flacon":
#         print(colorer("Tu bois. Le froid t'envahit. Tu traverses les flammes. (+10)", VERT))
#         points = points + 10
#     else:
#         print(colorer("Mauvais choix. Rogue esquisse presque un sourire. « Décevant. »", ROUGE))
#     pause()
#
#     print("\nRogue te toise. « " + str(points) + " points. Ne vous croyez pas brillant pour autant. »")
#     return points
#
#
# def quiz_magie(joueur, chemin_fichier="data/quiz_magie.json"):
#     toutes_les_questions = load_fichier(chemin_fichier)
#     questions_choisies = []
#     while len(questions_choisies) < 4:
#         question = random.choice(toutes_les_questions)
#         if question not in questions_choisies:
#             questions_choisies.append(question)
#
#     print("\n" + titre("Interrogation écrite"))
#     print("« Parchemin et plume. Quatre questions. Pas de triche. »")
#
#     score = 0
#     numero = 1
#     for q in questions_choisies:
#         print("\n" + str(numero) + ". " + q["question"])
#         reponse = input("> ").strip().lower()
#         if reponse == q["reponse"].lower():
#             print(colorer("Bonne réponse ! +25 points pour ta maison.", VERT))
#             score = score + 25
#         else:
#             print(colorer("Mauvaise réponse. La bonne réponse était : " + q["reponse"], ROUGE))
#         numero = numero + 1
#
#     print("\nScore obtenu : " + colorer(str(score) + " points", JAUNE))
#     return score
#
#
# def lancer_chapitre_3(personnage, maisons):
#     apprendre_sorts(personnage)
#     points_rogue = cours_de_rogue(personnage)
#     score_quiz = quiz_magie(personnage)
#     actualiser_points_maison(maisons, personnage["Maison"], points_rogue + score_quiz)
#     afficher_maison_gagnante(maisons)
#     afficher_personnage(personnage)
