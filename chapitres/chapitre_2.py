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
