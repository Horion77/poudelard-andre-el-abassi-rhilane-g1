def initialiser_personnage(nom, prenom, attributs):
    joueur = {
        "Nom": nom,
        "Prenom": prenom,
        "Argent": 100,
        "Inventaire": [],
        "Sortilèges": [],
        "Attributs": attributs
    }
    return joueur


def afficher_personnage(joueur):
    print("Profil du personnage :")
    for cle in joueur:
        valeur = joueur[cle]
        if type(valeur) == dict:
            print(cle + " :")
            for attribut in valeur:
                print("  - " + attribut + " : " + str(valeur[attribut]))
        elif type(valeur) == list:
            print(cle + " : " + ", ".join(valeur))
        else:
            print(cle + " : " + str(valeur))


def modifier_argent(joueur, montant):
    joueur["Argent"] = joueur["Argent"] + montant


def ajouter_objet(joueur, cle, objet):
    joueur[cle].append(objet)