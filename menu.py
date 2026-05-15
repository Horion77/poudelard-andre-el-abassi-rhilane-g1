from chapitres.chapitre_1 import lancer_chapitre_1


def afficher_menu_principal():
    print("\n=== Poudlard : L'Art de Coder comme un Sorcier ===")
    print("1. Lancer le Chapitre 1 - L'arrivée dans le monde magique.")
    print("2. Quitter le jeu.")


def lancer_choix_menu():
    continuer = True
    while continuer:
        afficher_menu_principal()
        choix = input("Votre choix : ").strip()

        if choix == "1":
            lancer_chapitre_1()
            continuer = False
        elif choix == "2":
            print("À bientôt dans le monde des sorciers !")
            continuer = False
        else:
            print("Choix invalide, veuillez entrer 1 ou 2.")