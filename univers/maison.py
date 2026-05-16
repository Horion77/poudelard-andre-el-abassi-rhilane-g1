# maison.py
from utils.input_utils import demander_choix


def actualiser_points_maison(maisons, nom_maison, points):
    if nom_maison in maisons:
        maisons[nom_maison] = maisons[nom_maison] + points
        print(nom_maison + " : " + str(points) + " points ajoutés. Total : " + str(maisons[nom_maison]) + " points.")
    else:
        print("Maison introuvable : " + nom_maison)