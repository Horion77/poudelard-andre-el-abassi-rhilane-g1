from utils.input_utils import demander_texte, demander_nombre, demander_choix, load_fichier
from univers.personnage import initialiser_personnage, afficher_personnage, modifier_argent, ajouter_objet
from utils.couleurs import JAUNE, VERT, ROUGE, CYAN, VIOLET, GRIS, GRAS, RESET, titre, colorer
import utils.art as _art

def afficher_art(nom):
    _art.afficher_art(nom)


def pause():
    input(GRIS + "  (Entrée pour continuer...)" + RESET)


def introduction():
    afficher_art("ch1_intro")
    print(titre("CHAPITRE 1 — La lettre qui change tout"))
    print()
    print("Toute ta vie, on t'a répété que tu étais un enfant " + colorer("normal", GRIS) + ".")
    print("Mais tu sais que c'est faux.")
    pause()

    print("\nIl y a eu ce jour où un verre s'est brisé sans que personne n'y touche.")
    print("Cette fois où tu t'es retrouvé sur le toit sans savoir comment.")
    print("Et ces rêves... toujours les mêmes : un château, une chouette, une porte.")
    pause()

    print("\nCe soir, le vent frappe aux carreaux. Quelque chose va arriver.")
    print("Quelque chose que tu attends depuis longtemps, sans oser le dire.")
    pause()


def creer_personnage():
    print("\n" + colorer("Mais avant tout... qui es-tu vraiment ?", GRAS))
    nom = demander_texte("Entrez le nom de votre personnage : ")
    prenom = demander_texte("Entrez le prénom de votre personnage : ")

    print("\nFerme les yeux. Quatre forces sommeillent en toi.")
    print("À toi de dire lesquelles te définissent (1 = faible, 10 = immense).")
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
    print("\n" + colorer(prenom + " " + nom + ".", GRAS) + " Retiens bien ce nom.")
    print("Dans quelques années, tout le monde le connaîtra.")
    afficher_personnage(joueur)
    return joueur


def recevoir_lettre():
    afficher_art("ch1_lettre")
    print("\nUn battement d'ailes. " + colorer("Une chouette", JAUNE) + " traverse la fenêtre")
    print("et se pose devant toi, une lettre scellée de cire serrée dans son bec.")
    pause()

    print("\nSur l'enveloppe, à l'encre vert émeraude, ton nom. Ton adresse. Ta chambre.")
    print("Comme s'ils savaient exactement où te trouver.")
    print(colorer("\n« Cher élève,", VERT))
    print(colorer("  Nous avons le plaisir de vous informer que vous avez été admis", VERT))
    print(colorer("  à l'école de sorcellerie de Poudlard. »", VERT))
    pause()

    print("\nLe monde s'arrête une seconde. Sorcellerie. Poudlard.")
    print("Alors c'était donc ça, depuis le début.")

    afficher_art("ch1_choix")
    options = ["Oui, bien sûr !", "Non, je préfère rester avec l'oncle Vernon..."]
    choix = demander_choix("Souhaitez-vous accepter cette invitation et partir pour Poudlard ?", options)

    if choix == "Non, je préfère rester avec l'oncle Vernon...":
        print(colorer("\nVous déchirez la lettre. L'oncle Vernon pousse un cri de joie :", ROUGE))
        print("« EXCELLENT ! Enfin quelqu'un de NORMAL dans cette maison ! »")
        print("Le monde magique ne saura jamais que vous existiez... " + colorer("Fin du jeu.", ROUGE))
        exit()

    print(colorer("\nTu serres la lettre contre toi. Ta vraie vie commence maintenant.", JAUNE))
    pause()


def rencontrer_hagrid(personnage):
    afficher_art("ch1_hagrid")
    print("\nLe lendemain, une ombre immense bouche l'entrée. Un géant à la barbe broussailleuse,")
    print("le regard doux, se baisse pour passer la porte.")
    print(colorer("\nHagrid : « Salut " + personnage["Prenom"] + " ! Géant Hagrid, gardien des Clés de Poudlard.", CYAN))
    print(colorer("Je viens t'aider à faire tes achats sur le Chemin de Traverse.", CYAN))
    print(colorer("Je sors justement d'en accompagner un autre... un certain Harry. Tu verras. »", CYAN))

    choix = demander_choix("Voulez-vous suivre Hagrid ?", ["Oui", "Non"])

    if choix == "Non":
        print("Hagrid éclate d'un grand rire et te pose une main sur l'épaule.")
        print("« Allez, pas de discussion ! » — et il t'entraîne quand même avec lui.")
    else:
        print("« Bonne réponse ! Suis-moi, et reste près de moi dans la foule. »")
    pause()


def acheter_fournitures(personnage):
    afficher_art("ch1_chemin")
    catalogue = load_fichier("data/inventaire.json")
    restants = ["Baguette magique", "Robe de sorcier", "Manuel de potions"]
    animaux = [["Chouette", 20], ["Chat", 15], ["Rat", 10], ["Crapaud", 5]]

    print("\n" + titre("Le Chemin de Traverse"))
    print("Hagrid pousse une brique du mur, et la rue magique se déplie devant toi.")
    print("Des chaudrons qui fument, des balais dernier cri, des hiboux par centaines.")
    print("Quelque part, on murmure : « Le garçon qui a survécu est ici aujourd'hui... »")
    pause()

    print("\n" + colorer("Catalogue des objets disponibles :", GRAS))
    for numero in catalogue:
        nom_objet = catalogue[numero][0]
        prix = catalogue[numero][1]
        print("  " + numero + ". " + nom_objet + colorer(" - " + str(prix) + " galions", JAUNE))

    while len(restants) > 0:
        print("\nVous avez " + colorer(str(personnage["Argent"]) + " galions", JAUNE) + ".")
        print("Objets obligatoires restant à acheter : " + colorer(", ".join(restants), ROUGE))

        numero = str(demander_nombre("Entrez le numéro de l'objet à acheter : ", 1, len(catalogue)))
        nom_objet = catalogue[numero][0]
        prix = catalogue[numero][1]

        if personnage["Argent"] < prix:
            print(colorer("Vous n'avez pas assez de galions. Fin du jeu.", ROUGE))
            exit()

        modifier_argent(personnage, -prix)
        ajouter_objet(personnage, "Inventaire", nom_objet)
        print(colorer("Vous avez acheté : " + nom_objet + " (-" + str(prix) + " galions).", VERT))

        if nom_objet in restants:
            restants.remove(nom_objet)

    print(colorer("\nTous les objets obligatoires ont été achetés !", VERT))
    print("\nDevant l'animalerie magique, Hagrid sourit : « Un sorcier a besoin d'un compagnon. »")
    print("Vous avez " + colorer(str(personnage["Argent"]) + " galions", JAUNE) + ".")
    print("\nVoici les animaux disponibles :")
    for i in range(len(animaux)):
        print("  " + str(i + 1) + ". " + animaux[i][0] + colorer(" - " + str(animaux[i][1]) + " galions", JAUNE))

    choix_animal = demander_nombre("Quel animal voulez-vous ?\nVotre choix : ", 1, len(animaux))
    nom_animal = animaux[choix_animal - 1][0]
    prix_animal = animaux[choix_animal - 1][1]

    if personnage["Argent"] < prix_animal:
        print(colorer("Vous n'avez pas assez de galions pour un animal. Fin du jeu.", ROUGE))
        exit()

    modifier_argent(personnage, -prix_animal)
    ajouter_objet(personnage, "Inventaire", nom_animal)
    print(colorer("Vous avez choisi : " + nom_animal + " (-" + str(prix_animal) + " galions).", VERT))

    print(colorer("\nTes achats sont faits. Voici ton inventaire :", GRAS))
    afficher_personnage(personnage)


def lancer_chapitre_1():
    introduction()
    joueur = creer_personnage()
    recevoir_lettre()
    rencontrer_hagrid(joueur)
    acheter_fournitures(joueur)
    print(colorer("\n— Fin du Chapitre 1 —", GRAS + JAUNE))
    print("Hagrid te tend un billet de train un peu étrange : voie neuf trois-quarts.")
    print("« On se reverra là-bas, petit. Et fais attention en traversant le mur ! »")
    pause()
    return joueur
