from utils.input_utils import demander_texte, demander_nombre, demander_choix, load_fichier
from univers.personnage import initialiser_personnage, afficher_personnage, modifier_argent, ajouter_objet


def introduction():
    print("Bienvenue dans Poudlard : L'Art de Coder comme un Sorcier !")
    print("Une aventure magique vous attend...")
    input("Appuyez sur Entrée pour commencer...")


def creer_personnage():
    print("\n=== Création de votre personnage ===")
    nom = demander_texte("Entrez le nom de votre personnage : ")
    prenom = demander_texte("Entrez le prénom de votre personnage : ")

    print("\nChoisissez vos attributs :")
    courage = demander_nombre("Niveau de courage (1-10) : ", 1, 10)
    intelligence = demander_nombre("Niveau d'intelligence (1-10) : ", 1, 10)
    loyaute = demander_nombre("Niveau de loyauté (1-10) : ", 1, 10)
    ambition = demander_nombre("Niveau d'ambition (1-10) : ", 1, 10)

    attributs = {
        "courage": courage,
        "intelligence": intelligence,
        "loyauté": loyaute,
        "ambition": ambition
    }

    joueur = initialiser_personnage(nom, prenom, attributs)
    afficher_personnage(joueur)
    return joueur


def recevoir_lettre():
    print("\nUne chouette traverse la fenêtre et vous apporte une lettre scellée du sceau de Poudlard...")
    print("« Cher élève,")
    print("Nous avons le plaisir de vous informer que vous avez été admis à l'école de sorcellerie de Poudlard ! »")

    options = ["Oui, bien sûr !", "Non, je préfère rester avec l'oncle Vernon..."]
    choix = demander_choix("Souhaitez-vous accepter cette invitation et partir pour Poudlard ?", options)

    if choix == "Non, je préfère rester avec l'oncle Vernon...":
        print("Vous déchirez la lettre, l'oncle Vernon pousse un cri de joie:")
        print("« EXCELLENT ! Enfin quelqu'un de NORMAL dans cette maison ! »")
        print("Le monde magique ne saura jamais que vous existiez... Fin du jeu.")
        exit()


def rencontrer_hagrid(personnage):
    print("\nHagrid : 'Salut " + personnage["Prenom"] + " ! Je suis venu t'aider à faire tes achats sur le Chemin de Traverse.'")

    choix = demander_choix("Voulez-vous suivre Hagrid ?", ["Oui", "Non"])

    if choix == "Non":
        print("Hagrid insiste gentiment et vous entraîne quand même avec lui!")


def acheter_fournitures(personnage):
    catalogue = load_fichier("data/inventaire.json")
    restants = ["Baguette magique", "Robe de sorcier", "Manuel de potions"]
    animaux = [["Chouette", 20], ["Chat", 15], ["Rat", 10], ["Crapaud", 5]]

    print("\nBienvenue sur le Chemin de Traverse !")
    print("\nCatalogue des objets disponibles :")
    for numero in catalogue:
        nom_objet = catalogue[numero][0]
        prix = catalogue[numero][1]
        print(numero + ". " + nom_objet + " - " + str(prix) + " galions")

    while len(restants) > 0:
        print("\nVous avez " + str(personnage["Argent"]) + " galions.")
        print("Objets obligatoires restant à acheter : " + ", ".join(restants))

        numero = str(demander_nombre("Entrez le numéro de l'objet à acheter : ", 1, len(catalogue)))
        nom_objet = catalogue[numero][0]
        prix = catalogue[numero][1]

        if personnage["Argent"] < prix:
            print("Vous n'avez pas assez de galions. Fin du jeu.")
            exit()

        modifier_argent(personnage, -prix)
        ajouter_objet(personnage, "Inventaire", nom_objet)
        print("Vous avez acheté : " + nom_objet + " (-" + str(prix) + " galions).")

        if nom_objet in restants:
            restants.remove(nom_objet)

    print("\nTous les objets obligatoires ont été achetés !")
    print("\nIl est temps de choisir votre animal de compagnie pour Poudlard !")
    print("Vous avez " + str(personnage["Argent"]) + " galions.")
    print("\nVoici les animaux disponibles :")
    for i in range(len(animaux)):
        print(str(i + 1) + ". " + animaux[i][0] + " - " + str(animaux[i][1]) + " galions")

    choix_animal = demander_nombre("Quel animal voulez-vous ?\nVotre choix : ", 1, len(animaux))
    nom_animal = animaux[choix_animal - 1][0]
    prix_animal = animaux[choix_animal - 1][1]

    if personnage["Argent"] < prix_animal:
        print("Vous n'avez pas assez de galions pour un animal. Fin du jeu.")
        exit()

    modifier_argent(personnage, -prix_animal)
    ajouter_objet(personnage, "Inventaire", nom_animal)
    print("Vous avez choisi : " + nom_animal + " (-" + str(prix_animal) + " galions).")

    print("\nTous les objets obligatoires ont été achetés avec succès ! Voici votre inventaire final :")
    afficher_personnage(personnage)


def lancer_chapitre_1():
    introduction()
    joueur = creer_personnage()
    recevoir_lettre()
    rencontrer_hagrid(joueur)
    acheter_fournitures(joueur)
    print("\nFin du Chapitre 1 ! Votre aventure commence à Poudlard...")
    return joueur