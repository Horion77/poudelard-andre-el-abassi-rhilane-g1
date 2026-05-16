# maison.py
from utils.input_utils import demander_choix


def actualiser_points_maison(maisons, nom_maison, points):
    if nom_maison in maisons:
        maisons[nom_maison] = maisons[nom_maison] + points
        print(nom_maison + " : " + str(points) + " points ajoutés. Total : " + str(maisons[nom_maison]) + " points.")
    else:
        print("Maison introuvable : " + nom_maison)
def afficher_maison_gagnante(maisons):
    score_max = 0
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
        print("Egalite entre : " + ", ".join(gagnantes) + " avec " + str(score_max) + " points !")

def repartition_maison(joueur, questions):
    scores = {
        "Gryffondor": 0,
        "Serpentard": 0,
        "Poufsouffle": 0,
        "Serdaigle": 0
    }