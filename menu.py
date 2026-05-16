from chapitres.chapitre_1 import lancer_chapitre_1
from chapitres.chapitre_2 import lancer_chapitre_2


def afficher_menu_principal():
    print("\n=== Poudlard : L'Art de Coder comme un Sorcier ===")
    print("1. Lancer l'aventure (Chapitres 1 et 2).")
    print("2. Quitter le jeu.")


def lancer_choix_menu():
    maisons = {
        "Gryffondor": 0,
        "Serpentard": 0,
        "Poufsouffle": 0,
        "Serdaigle": 0
    }

    continuer = True
    while continuer:
        afficher_menu_principal()
        choix = input("Votre choix : ").strip()

        if choix == "1":
            joueur = lancer_chapitre_1()
            lancer_chapitre_2(joueur)
            continuer = False
        elif choix == "2":
            print("À bientôt dans le monde des sorciers !")
            continuer = False
        else:
            print("Choix invalide, veuillez entrer 1 ou 2.")