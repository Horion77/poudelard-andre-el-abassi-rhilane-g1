# maison.py
from utils.input_utils import demander_choix


def actualiser_points_maison(maisons, nom_maison, points):
    if nom_maison in maisons:
        maisons[nom_maison] = maisons[nom_maison] + points
        print(nom_maison + " : " + str(points) + " points ajoutés. Total : " + str(maisons[nom_maison]) + " points.")
    else:
        print("Maison introuvable : " + nom_maison)
def afficher_maison_gagnante(maisons):
    #score_max initialisé à -1 au lieu de 0 pour éviter que toutes les maisons à 0 soient déclarées ex æquo dès le début
    score_max = -1
    for maison in maisons:
        if maisons[maison] > score_max:
            score_max = maisons[maison]

    gagnantes = []
    for maison in maisons:
        if maisons[maison] == score_max:
            gagnantes.append(maison)

    if len(gagnantes) == 1:
        print("La maison gagnante est " + gagnantes[0] + " avec " + str(score_max) + " points !")
    else:
        print("Egalité entre : " + ", ".join(gagnantes) + " avec " + str(score_max) + " points !")

def repartition_maison(joueur, questions):
    scores = {
        "Gryffondor": 0,
        "Serpentard": 0,
        "Poufsouffle": 0,
        "Serdaigle": 0
    }

    attributs = joueur["Attributs"]
    scores["Gryffondor"] = scores["Gryffondor"] + attributs["courage"] * 2
    scores["Serpentard"] = scores["Serpentard"] + attributs["ambition"] * 2
    scores["Poufsouffle"] = scores["Poufsouffle"] + attributs["loyauté"] * 2
    scores["Serdaigle"] = scores["Serdaigle"] + attributs["intelligence"] * 2

    for question in questions:
        texte = question[0]
        options = question[1]
        maisons_associees = question[2]

        choix = demander_choix(texte, options)

        index = 0
        for i in range(len(options)):
            if options[i] == choix:
                index = i

        maison_choisie = maisons_associees[index]
        scores[maison_choisie] = scores[maison_choisie] + 3

    print("\nRésumé des scores :")
    for maison in scores:
        print(maison + " : " + str(scores[maison]) + " points")

    maison_finale = ""
    score_max = 0
    for maison in scores:
        if scores[maison] > score_max:
            score_max = scores[maison]
            maison_finale = maison

    return maison_finale