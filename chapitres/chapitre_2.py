# chapitre_2.py
from utils.input_utils import demander_choix, load_fichier
from univers.personnage import afficher_personnage
from univers.maison import repartition_maison

def rencontrer_amis(joueur):
    print("\nVous montez à bord du Poudlard Express. Le train démarre lentement en direction du Nord...")
    print("Un garçon roux entre dans votre compartiment, l'air amical.")
    print("— Salut ! Moi c'est Ron Weasley. Tu veux bien qu'on s'assoie ensemble ?")

    choix_ron = demander_choix("Que répondez-vous ?", ["Bien sûr, assieds-toi !", "Désolé, je préfère voyager seul."])

    if choix_ron == "Bien sûr, assieds-toi !":
        print("Ron sourit : — Génial ! Tu verras, Poudlard, c'est incroyable !")
        joueur["Attributs"]["loyauté"] = joueur["Attributs"]["loyauté"] + 1
    else:
        print("Ron hoche la tête, un peu déçu.")
        joueur["Attributs"]["ambition"] = joueur["Attributs"]["ambition"] + 1

    print("\nUne fille entre ensuite, portant déjà une pile de livres.")
    print("— Bonjour, je m'appelle Hermione Granger. Vous avez déjà lu 'Histoire de la Magie' ?")

    choix_hermione = demander_choix("Que répondez-vous ?", ["Oui, j'adore apprendre de nouvelles choses !", "Euh… non, je préfère les aventures aux bouquins."])

    if choix_hermione == "Oui, j'adore apprendre de nouvelles choses !":
        print("Hermione sourit : — Excellent ! On va bien s'entendre !")
        joueur["Attributs"]["intelligence"] = joueur["Attributs"]["intelligence"] + 1
    else:
        print("Hermione fronce les sourcils : — Il faudrait pourtant s'y mettre un jour !")
        joueur["Attributs"]["courage"] = joueur["Attributs"]["courage"] + 1

    print("\nPuis un garçon blond entre avec un air arrogant.")
    print("— Je suis Drago Malefoy. Mieux vaut bien choisir ses amis dès le départ, tu ne crois pas ?")

    choix_drago = demander_choix("Comment réagissez-vous ?", ["Je lui serre la main poliment.", "Je l'ignore complètement.", "Je lui réponds avec arrogance."])

    if choix_drago == "Je lui serre la main poliment.":
        print("Drago sourit : — Sage décision.")
        joueur["Attributs"]["ambition"] = joueur["Attributs"]["ambition"] + 1
    elif choix_drago == "Je l'ignore complètement.":
        print("Drago fronce les sourcils, vexé. — Tu le regretteras !")
        joueur["Attributs"]["loyauté"] = joueur["Attributs"]["loyauté"] + 1
    else:
        print("Drago recule, surpris. — On se reverra !")
        joueur["Attributs"]["courage"] = joueur["Attributs"]["courage"] + 1

    print("\nLe train continue sa route. Le château de Poudlard se profile à l'horizon...")
    print("Tes choix semblent déjà en dire long sur ta personnalité !")
    print("\nTes attributs mis à jour : " + str(joueur["Attributs"]))

def mot_de_bienvenue():
    print("\n=== Arrivée à Poudlard ===")
    print("Le professeur Dumbledore s'avance vers le pupitre et prend la parole :")
    print("« Bienvenue à tous à Poudlard !")
    print("Que cette année vous apporte sagesse, courage et magie!")
    print("Souvenez-vous : ce n'est pas nos capacités qui montrent ce que nous sommes vraiment,")
    print("c'est nos choix. Bonne année à tous ! »")
    input("\nAppuyez sur Entrée pour continuer...")

def ceremonie_repartition(joueur):
    questions = [
        (
            "Tu vois un ami en danger. Que fais-tu ?",
            ["Je fonce l'aider", "Je réfléchis à un plan", "Je cherche de l'aide", "Je reste calme et j'observe"],
            ["Gryffondor", "Serpentard", "Poufsouffle", "Serdaigle"]
        ),
        (
            "Quel trait te décrit le mieux ?",
            ["Courageux et loyal", "Rusé et ambitieux", "Patient et travailleur", "Intelligent et curieux"],
            ["Gryffondor", "Serpentard", "Poufsouffle", "Serdaigle"]
        ),
        (
            "Face à un défi difficile, tu...",
            ["Fonces sans hésiter", "Cherches la meilleure stratégie", "Comptes sur tes amis", "Analyses le problème"],
            ["Gryffondor", "Serpentard", "Poufsouffle", "Serdaigle"]
        )
    ]

    print("\nLa cérémonie de répartition commence dans la Grande Salle...")
    print("Le Choixpeau magique t'observe longuement avant de poser ses questions :")

    maison = repartition_maison(joueur, questions)
    joueur["Maison"] = maison

    print("\nLe Choixpeau s'exclame : " + maison + " !!!")
    print("Tu rejoins les élèves de " + maison + " sous les acclamations !")


def installation_salle_commune(joueur):
    maisons_data = load_fichier("../data/maisons.json")
    maison = joueur["Maison"]
    
    if maison in maisons_data:
        info = maisons_data[maison]
        print("\nVous suivez les préfets à travers les couloirs du château...")
        print("\n" + info["description"])
        print("\n" + info["message_installation"])
        print("Les couleurs de votre maison : " + ", ".join(info["couleurs"]))
    else:
        print("Erreur : maison '" + maison + "' introuvable dans le fichier.")


def lancer_chapitre_2(personnage):
    rencontrer_amis(personnage)
    mot_de_bienvenue()
    ceremonie_repartition(personnage)
    installation_salle_commune(personnage)
    afficher_personnage(personnage)
    print("\nFin du Chapitre 2 ! Les cours commencent à Poudlard...")