# chapitre_2.py
from utils.input_utils import demander_choix, load_fichier
from univers.personnage import afficher_personnage
from univers.maison import repartition_maison
from utils.couleurs import JAUNE, VERT, ROUGE, CYAN, GRIS, GRAS, RESET, COULEUR_MAISON, titre, colorer


def pause():
    input(GRIS + "  (Entrée pour continuer...)" + RESET)


def transition_king_cross(joueur):
    print(titre("CHAPITRE 2 — La voie 9¾"))
    print()
    print("La fin de l'été a filé entre tes doigts. Et ce matin, c'est le grand jour.")
    print("La gare de " + colorer("King's Cross", GRAS) + " grouille de monde. Valise à la main,")
    print("ta chouette qui s'agite dans sa cage, tu cherches ton quai.")
    pause()

    print("\nTon billet indique : " + colorer("voie neuf trois-quarts", JAUNE) + ".")
    print("Sauf qu'entre la voie 9 et la voie 10... il n'y a qu'un mur de briques massif.")
    print("Les Moldus passent sans rien voir. Personne pour t'aider. Hagrid avait prévenu :")
    print(colorer("« Fais attention en traversant le mur. »", CYAN) + " Traverser le mur ?!")
    pause()

    print("\nUne famille de roux passe en trombe près de toi en parlant de 'Moldus'.")
    print("L'un après l'autre, ils foncent vers la barrière... et disparaissent dedans.")

    choix = demander_choix(
        "\nLe train part dans deux minutes. Comment traverses-tu ?",
        ["Je fonce sans réfléchir, à pleine vitesse", "J'avance doucement, la main tendue vers le mur"]
    )
    if choix == "Je fonce sans réfléchir, à pleine vitesse":
        print("\nTu pousses ton chariot et tu cours. Tu fermes les yeux. Le choc ne vient jamais.")
        joueur["Attributs"]["courage"] = joueur["Attributs"]["courage"] + 1
        print(colorer("(courage +1)", GRIS))
    else:
        print("\nTes doigts touchent la brique... et s'enfoncent. Le mur n'oppose aucune résistance.")
        print("Tu traverses, le cœur battant.")
    pause()

    print("\nDe l'autre côté, le monde change.")
    print(colorer("Le Poudlard Express", ROUGE) + ", énorme locomotive écarlate, crache sa vapeur.")
    print("Des centaines d'élèves s'embrassent, des crapauds s'échappent, des hiboux hululent.")
    print("Le sifflet retentit. Tu grimpes à bord juste à temps.")
    pause()


def rencontrer_amis(joueur):
    print("\nTu pousses la porte d'un compartiment. Un garçon à lunettes rondes,")
    print("une étrange cicatrice en éclair sur le front, lève les yeux vers toi.")
    print(colorer("— Salut. Moi c'est Harry. Assieds-toi, il reste de la place.", JAUNE))
    pause()

    print("\nUn garçon roux le suit, des taches de rousseur plein le visage.")
    print("— Salut ! Moi c'est Ron Weasley. Tu veux bien qu'on s'assoie ensemble ?")
    choix_ron = demander_choix("Que réponds-tu ?", ["Bien sûr, assieds-toi !", "Désolé, je préfère voyager seul."])
    if choix_ron == "Bien sûr, assieds-toi !":
        print(colorer("Ron sourit : — Génial ! Avec Harry, cette année va être mémorable.", VERT))
        joueur["Attributs"]["loyauté"] = joueur["Attributs"]["loyauté"] + 1
    else:
        print("Ron hoche la tête, un peu déçu. Harry te jette un regard surpris.")
        joueur["Attributs"]["ambition"] = joueur["Attributs"]["ambition"] + 1

    print("\nUne fille entre, une pile de livres dans les bras, le ton assuré.")
    print("— Bonjour, je m'appelle Hermione Granger. Vous avez lu 'Histoire de la Magie' ?")
    choix_hermione = demander_choix("Que réponds-tu ?", ["Oui, j'adore apprendre de nouvelles choses !", "Euh… non, je préfère les aventures aux bouquins."])
    if choix_hermione == "Oui, j'adore apprendre de nouvelles choses !":
        print(colorer("Hermione sourit : — Enfin quelqu'un de sérieux ! On va bien s'entendre.", VERT))
        joueur["Attributs"]["intelligence"] = joueur["Attributs"]["intelligence"] + 1
    else:
        print("Hermione fronce les sourcils : — Il faudrait pourtant s'y mettre. Ron pouffe.")
        joueur["Attributs"]["courage"] = joueur["Attributs"]["courage"] + 1

    print("\nLa porte coulisse une dernière fois. Un garçon blond, le menton levé.")
    print(colorer("— Drago Malefoy. Mieux vaut bien choisir ses amis dès le départ, non ?", GRIS))
    choix_drago = demander_choix("Comment réagis-tu ?", ["Je lui serre la main poliment.", "Je l'ignore complètement.", "Je lui réponds avec arrogance."])
    if choix_drago == "Je lui serre la main poliment.":
        print("Drago sourit : — Sage décision.")
        joueur["Attributs"]["ambition"] = joueur["Attributs"]["ambition"] + 1
    elif choix_drago == "Je l'ignore complètement.":
        print("Drago se vexe : — Tu le regretteras ! — et il claque la porte.")
        joueur["Attributs"]["loyauté"] = joueur["Attributs"]["loyauté"] + 1
    else:
        print("Drago recule, surpris : — On se reverra ! Harry te lance un clin d'œil.")
        joueur["Attributs"]["courage"] = joueur["Attributs"]["courage"] + 1

    print(colorer("\nLe château de Poudlard se profile à l'horizon. Vous y êtes presque.", JAUNE))
    print("Sans le savoir, tu viens de rencontrer ceux qui changeront ta vie.")
    print(colorer("\nTes attributs après ces rencontres : ", GRAS) + str(joueur["Attributs"]))
    pause()


def mot_de_bienvenue():
    print("\n" + titre("Arrivée à Poudlard"))
    print("\nDans la Grande Salle, sous un plafond magique étoilé, " + colorer("Dumbledore", CYAN) + " se lève.")
    print(colorer("« Bienvenue à tous à Poudlard !", CYAN))
    print(colorer("Souvenez-vous : ce ne sont pas nos capacités qui montrent ce que nous sommes,", CYAN))
    print(colorer("c'est nos choix. Bonne année à tous ! »", CYAN))
    pause()

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

    print("\nLe professeur McGonagall pose un vieux chapeau rapiécé sur un tabouret.")
    print("Quand vient ton tour, le " + colorer("Choixpeau magique", GRIS) + " glisse sur tes yeux.")
    print("Une petite voix murmure dans ta tête : « Voyons voir... »")
    pause()

    maison = repartition_maison(joueur, questions)
    joueur["Maison"] = maison

    couleur = COULEUR_MAISON.get(maison, JAUNE)
    print("\nLe Choixpeau s'exclame : " + colorer(maison + " !!!", couleur + GRAS))
    print("Tu rejoins la table de " + colorer(maison, couleur) + " sous les acclamations !")
    if maison == "Gryffondor":
        print(colorer("Harry et Ron, déjà à la table, te font signe : tu es des nôtres !", VERT))
    pause()


def appliquer_bonus_maison(joueur, info):
    if "bonus_attributs" not in info:
        return

    bonus = info["bonus_attributs"]
    print("\nBonus de votre maison :")
    for attribut in bonus:
        joueur["Attributs"][attribut] = joueur["Attributs"][attribut] + bonus[attribut]
        print("  - " + attribut + " : +" + str(bonus[attribut]))


def installation_salle_commune(joueur):
    maisons_data = load_fichier("data/maisons.json")
    maison = joueur["Maison"]

    if maison in maisons_data:
        info = maisons_data[maison]
        couleur = COULEUR_MAISON.get(maison, JAUNE)
        print("\nTu suis les préfets à travers les couloirs mouvants du château...")
        if "emoji" in info:
            print(info["emoji"])
        print("\n" + colorer(info["description"], couleur))
        print("\n" + info["message_installation"])
        print("Les couleurs de ta maison : " + colorer(", ".join(info["couleurs"]), couleur))
        appliquer_bonus_maison(joueur, info)
    else:
        print(colorer("Erreur : maison '" + maison + "' introuvable dans le fichier.", ROUGE))


def lancer_chapitre_2(personnage):
    transition_king_cross(personnage)
    rencontrer_amis(personnage)
    mot_de_bienvenue()
    ceremonie_repartition(personnage)
    installation_salle_commune(personnage)
    afficher_personnage(personnage)
    print(colorer("\n— Fin du Chapitre 2 —", GRAS + JAUNE))
    print("Demain, les cours commencent. Et avec eux, les ennuis...")
    pause()
    return personnage