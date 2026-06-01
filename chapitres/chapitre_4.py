# chapitre 4 - quidditch + vision ancestrale
import random
from utils.input_utils import demander_choix, load_fichier
from univers.personnage import afficher_personnage
from univers.maison import actualiser_points_maison, afficher_maison_gagnante

# couleurs ANSI : centralisees dans utils/couleurs.py (juste des strings)
from utils.couleurs import JAUNE, CYAN, VERT, ROUGE, VIOLET, GRAS, RESET
import utils.art as _art

def afficher_art(nom):
    _art.afficher_art(nom)


# -------------------------------------------------------
# PARTIE A - match de quidditch
# -------------------------------------------------------

def creer_equipe(maison, equipe_data, est_joueur=False, joueur=None):
    equipe = {
        "nom": maison, "score": 0,
        "a_marque": 0, "a_stoppe": 0,
        "attrape_vifdor": False,
        "joueurs": equipe_data["joueurs"]
    }
    if est_joueur and joueur is not None:
        # le joueur prend la place de l'attrapeur (toujours en tete)
        nom_joueur = joueur["Prenom"] + " " + joueur["Nom"] + "(Attrapeur)"
        nouvelle_liste = [nom_joueur]
        for j in equipe_data["joueurs"]:
            if "(Attrapeur)" not in j:
                nouvelle_liste.append(j)
        equipe["joueurs"] = nouvelle_liste
    return equipe


def tentative_marque(equipe_attaque, equipe_defense, joueur_est_joueur=False):
    # >= 6 sur 1-10 = but
    jet = random.randint(1, 10)
    if jet >= 6:
        if joueur_est_joueur:
            buteur = equipe_attaque["joueurs"][0]
        else:
            buteur = random.choice(equipe_attaque["joueurs"])
        equipe_attaque["score"] = equipe_attaque["score"] + 10
        equipe_attaque["a_marque"] = equipe_attaque["a_marque"] + 1
        print(VERT + buteur + " marque ! (+10)" + RESET)
    else:
        equipe_defense["a_stoppe"] = equipe_defense["a_stoppe"] + 1
        print(equipe_defense["nom"] + " bloque l'attaque.")


def apparition_vifdor():
    return random.randint(1, 6) == 6


def attraper_vifdor(e1, e2):
    # tirage entre les deux equipes - le resultat est revele dans match_quidditch
    gagnant = random.choice([e1, e2])
    gagnant["score"] = gagnant["score"] + 150
    gagnant["attrape_vifdor"] = True
    return gagnant


def afficher_score(e1, e2):
    print("\nScore :")
    print("  " + e1["nom"] + " : " + str(e1["score"]) + " pts")
    print("  " + e2["nom"] + " : " + str(e2["score"]) + " pts")


def afficher_equipe(maison, equipe):
    print("\nEquipe de " + maison + " :")
    for j in equipe["joueurs"]:
        print("  - " + j)


def match_quidditch(joueur, maisons):
    equipes_data = load_fichier("data/equipes_quidditch.json")
    maison_joueur = joueur["Maison"]

    adversaires = []
    for m in equipes_data:
        if m != maison_joueur:
            adversaires.append(m)
    maison_adverse = random.choice(adversaires)

    e1 = creer_equipe(maison_joueur, equipes_data[maison_joueur], est_joueur=True, joueur=joueur)
    e2 = creer_equipe(maison_adverse, equipes_data[maison_adverse])

    print("\n" + GRAS + JAUNE + "== Match de Quidditch : " + maison_joueur + " vs " + maison_adverse + " ==" + RESET)
    afficher_equipe(maison_joueur, e1)
    afficher_equipe(maison_adverse, e2)
    print("\nTu joues pour " + maison_joueur + " en tant qu'Attrapeur.")
    print(CYAN + "Dans les gradins, Hermione brandit une banderole et Ron hurle ton nom." + RESET)
    input("\nAppuyez sur Entree pour commencer...")

    for tour in range(1, 21):
        print("\n--- Tour " + str(tour) + " ---")
        tentative_marque(e1, e2, joueur_est_joueur=True)
        tentative_marque(e2, e1)
        afficher_score(e1, e2)

        if apparition_vifdor():
            afficher_art("vif_or")
            print("\n" + JAUNE + "Le Vif d'Or scintille dans le ciel ! Tu fonces vers lui." + RESET)
            gagnant_vifdor = attraper_vifdor(e1, e2)

            if gagnant_vifdor["nom"] == maison_joueur:
                # le joueur l'attrape -> on lance la scene de chute/vision
                # (le resultat est revele a la fin de la vision)
                scene_chute_et_vision(joueur)
            else:
                print("L'Attrapeur de " + maison_adverse + " te coupe la route et l'attrape !")
                print("Fin du match.")
            break

        input("\nEntree pour continuer...")

    # resultats
    afficher_art("maisons")
    print("\n" + GRAS + "== Resultat final ==" + RESET)
    afficher_score(e1, e2)

    if e1["score"] > e2["score"]:
        print("\n" + VERT + maison_joueur + " remporte le match !" + RESET)
        actualiser_points_maison(maisons, maison_joueur, 500)
    elif e2["score"] > e1["score"]:
        print("\n" + maison_adverse + " remporte le match.")
        actualiser_points_maison(maisons, maison_adverse, 500)
    else:
        print("\nMatch nul.")


# -------------------------------------------------------
# PARTIE B - vision ancestrale
# -------------------------------------------------------

def scene_chute_et_vision(joueur):
    prenom = joueur["Prenom"]

    print("\n" + "=" * 48)
    input("\n[Entree...]")

    print("\nLe Vif d'Or file vers le sol. Tu plonges derriere lui.")
    print("Ta main se tend. Tes doigts sont a quelques centimetres.")
    input("[Entree...]")

    print("\nEt puis -- un choc.")
    print("Un joueur adverse te percute a pleine vitesse. Balai contre balai.")
    print("Ton balai part sous toi.")
    input("[Entree...]")

    print("\n" + prenom + " tombe.")
    print("Le bruit du stade s'eloigne.")
    input("[Entree...]")

    print("\nLe sol se rapproche.")
    print("Et pendant la chute, quelque chose change.")
    input("[Entree...]")

    print("\n...")
    input("[Entree...]")

    print("\nUne voix. Calme. Que tu n'as jamais entendue, mais que tu reconnais.")
    print('"' + prenom + '."')
    input("[Entree...]")

    print("\nDes images passent. Un arbre genealogique sur un vieux parchemin.")
    print("Des noms. Les tiens. Ceux de ta famille, sur plusieurs generations.")
    input("[Entree...]")

    print("\nDans ta famille, on en parlait sans vraiment y croire.")
    print("Un don rare : voir des fragments du futur, dans les moments de tension extreme.")
    print("Ta grand-mere y faisait allusion. Personne ne l'avait jamais eveille.")
    input("[Entree...]")

    print("\nLa voix reprend :")
    print('"Ce que tu vas voir n\'est pas un reve. C\'est une possibilite."')
    input("\n[Entree pour entrer dans la vision...]")

    maison = joueur["Maison"]
    if maison == "Gryffondor":
        vision_gryffondor(joueur)
    elif maison == "Serpentard":
        vision_serpentard(joueur)
    elif maison == "Poufsouffle":
        vision_poufsouffle(joueur)
    elif maison == "Serdaigle":
        vision_serdaigle(joueur)

    # c'est seulement ici qu'on revele qu'il a attrape le Vif d'Or
    print("\n" + "=" * 48)
    print("\nTu rouvres les yeux. Tu es allonge sur l'herbe du terrain.")
    print("Ta main droite est fermee. Tu la desserres.")
    print(JAUNE + "Le Vif d'Or est la, au creux de ta paume." + RESET)
    input("[Entree...]")

    print("\nLa foule t'acclame. Tes coequipiers arrivent en courant.")
    print("Tu restes une seconde sans bouger.")
    print("Ce que tu viens de voir n'etait pas qu'un evanouissement.")
    print("Le don de ta famille s'est reveille.")
    input("\n[Entree pour continuer...]")


def vision_gryffondor(joueur):
    prenom = joueur["Prenom"]

    print("\n" + ROUGE + GRAS + "~ VISION -- Gryffondor ~" + RESET)
    input("[Entree...]")

    print("\nTu te vois adulte.")
    print("Un couloir de Poudlard. La nuit. Les torches arrachees des murs.")
    print("Des traces de sorts encore fumantes sur les pierres noires.")
    input("[Entree...]")

    afficher_art("mangemort")
    print("\nDevant toi -- un Mangemort.")
    print("Grand, masque, baguette levee. Il n'est pas seul.")
    print("Tu entends d'autres pas quelque part dans le chateau.")
    print("Tes amis sont la-dedans. Tu ne peux pas fuir.")
    input("[Entree...]")

    print("\nIl lance son premier sort sans meme te regarder dans les yeux.")
    pts = 0

    # premier sort
    c1 = demander_choix(
        "\nUn jet de lumiere verte fonce sur toi. Que fais-tu ?",
        ["Expelliarmus !", "Protego !", "Tu plonges sur le cote"]
    )
    if c1 == "Expelliarmus !":
        print("\nLes deux sorts se rencontrent. Le choc projette le Mangemort en arriere.")
        print("Il se releve, mais il marque un temps d'hesitation.")
        pts = pts + 2
    elif c1 == "Protego !":
        print("\nLe bouclier tient. Le sort explose en gerbes d'etincelles.")
        print("Tu recules d'un pas mais tu tiens bon.")
        pts = pts + 1
    else:
        print("\nTu roules sur le sol. Le sort passe a quelques centimetres.")
        print("Tu es intact. Mais tu es a genoux et il avance.")
    input("[Entree...]")

    # un allie tombe
    print("\nUn cri. Court. Sec.")
    print("L'un de tes amis vient de tomber dans la piece d'a cote.")
    c2 = demander_choix(
        "\nQue fais-tu ?",
        [
            "Tu lances Stupéfix sur le Mangemort d'abord, puis tu fonces",
            "Tu fonces vers ton ami, quitte a tourner le dos au Mangemort",
            "Tu cries pour attirer d'autres eleves en renfort"
        ]
    )
    if c2 == "Tu lances Stupéfix sur le Mangemort d'abord, puis tu fonces":
        print("\nStupéfix. Le Mangemort s'effondre.")
        print("Tu rejoins ton ami. Il est blesse mais conscient.")
        pts = pts + 2
    elif c2 == "Tu fonces vers ton ami, quitte a tourner le dos au Mangemort":
        print("\nUn sort dans le dos. Tu t'etales.")
        print("Mais ton ami te voit arriver. Ca lui donne la force de se relever.")
        pts = pts + 1
    else:
        print("\nTon cri resonne dans les couloirs vides. Personne ne repond.")
        print("Mais le Mangemort hesite -- il ne sait plus combien vous etes.")
        pts = pts + 1
    input("[Entree...]")

    # moment decisif
    print("\nLe Mangemort reprend ses esprits. Un deuxieme entre par la fenetre.")
    print("Les dernieres torches s'eteignent. La piece est presque noire.")
    c3 = demander_choix(
        "\nTon dernier choix :",
        [
            "Tu attends dans l'ombre et tu lances quand ils approchent",
            "Lumos Maxima -- tu illumines tout et tu charges droit sur eux",
            "Tu tentes un sortilege que tu n'as encore jamais essaye"
        ]
    )
    if c3 == "Tu attends dans l'ombre et tu lances quand ils approchent":
        print("\nIls avancent. Tu laisses passer trois secondes.")
        print("Bang. Bang. Stupéfix double. Les deux a terre en meme temps.")
        print("Le couloir retrouve le silence.")
        pts = pts + 2
    elif c3 == "Lumos Maxima -- tu illumines tout et tu charges droit sur eux":
        print("\nLa lumiere les aveugle. Tu en neutralises un au vol.")
        print("L'autre prefere fuir.")
        pts = pts + 1
    else:
        print("\nUn sort que tu ne connais pas encore sort de ta baguette.")
        print("Les deux Mangemorts projetes contre les murs.")
        print("Tu regardes ta baguette. Tu ne sais pas ce que tu viens de faire.")
        pts = pts + 2
    input("[Entree...]")

    print("\n" + ROUGE + "~ resultat ~" + RESET)
    if pts >= 4:
        print("VISION -- Tu tiens le couloir.")
        print("\nLes deux Mangemorts sont a terre. Tes amis te rejoignent.")
        print("La menace est passee, pour cette fois.")
    elif pts >= 2:
        print("VISION -- Tu t'en sors, et tes amis aussi.")
        print("\nLa nuit a ete difficile, mais vous etes tous encore la.")
    else:
        print("VISION -- Tu tiens, de justesse.")
        print("\nLe couloir est devaste. Tu es blesse, mais vivant.")
    input("[Entree...]")


def vision_serpentard(joueur):
    prenom = joueur["Prenom"]

    print("\n" + VERT + GRAS + "~ VISION -- Serpentard ~" + RESET)
    input("[Entree...]")

    afficher_art("ministere")
    print("\nTu te vois adulte, dans un bureau que tu ne reconnais pas.")
    print("Des robes du Ministere de la Magie. Des visages graves. Des voix feutrees.")
    print("Tu portes une identite qui n'est pas la tienne -- Polynectar.")
    input("[Entree...]")

    print("\nTa mission : recuperer un dossier classe secret sans laisser de trace.")
    print("Tu as trente minutes avant que la potion s'estompe.")
    print("Et quelqu'un dans cette piece commence a te regarder de travers.")
    input("[Entree...]")

    discrecion = 0
    suspicion = 0

    # un fonctionnaire trop curieux
    c1 = demander_choix(
        "\nUn fonctionnaire s'approche : 'Je ne vous ai pas vu hier. Vous etiez ou ?'",
        [
            "'Reunion au 4e etage. Tres longue.' -- ton ton est calme, naturel",
            "Tu detournes la conversation sur lui avant qu'il finisse sa phrase",
            "Tu lui reponds que ca ne le regarde pas"
        ]
    )
    if c1 == "'Reunion au 4e etage. Tres longue.' -- ton ton est calme, naturel":
        print("\nIl hoche la tete. 'Ah oui, celle sur les Moldus. Terrible.'")
        print("Il repart. Tu souffles discretement.")
        discrecion = discrecion + 2
    elif c1 == "Tu detournes la conversation sur lui avant qu'il finisse sa phrase":
        print("\n'A propos, j'ai entendu dire que votre rapport avait ete retarde ?'")
        print("Son visage change d'un coup. Il part regler ca. Efficace.")
        discrecion = discrecion + 2
    else:
        print("\nIl fronce les sourcils. Il va parler a son superieur.")
        print("Tu as quelques minutes avant que ca se complique.")
        suspicion = suspicion + 1
    input("[Entree...]")

    # acceder aux archives
    print("\nTu arrives devant la salle des archives. Deux gardes. Une serrure magique.")
    c2 = demander_choix(
        "\nComment tu entres ?",
        [
            "Tu montres un faux badge prepare a l'avance",
            "Tu fais semblant d'apporter des documents a deposer",
            "Tu lances Alohomora quand ils regardent ailleurs"
        ]
    )
    if c2 == "Tu montres un faux badge prepare a l'avance":
        print("\nIls regardent, comparent, hochent la tete. 'Entrez, monsieur.'")
        discrecion = discrecion + 2
    elif c2 == "Tu fais semblant d'apporter des documents a deposer":
        print("\nTu deposes une liasse de papiers bidon. Tu reperes le dossier. Propre.")
        discrecion = discrecion + 1
    else:
        print("\nAlohomora. Ca marche. Mais un garde a entendu le declic.")
        print("Il te regarde. Tu soutiens son regard sans ciller. Il tourne la tete.")
        suspicion = suspicion + 1
    input("[Entree...]")

    # sortir
    print("\nLe dossier est dans ta poche interieure. Il faut partir maintenant.")
    print("Mais a l'entree, un Auror vient d'arriver et fait des controles.")
    c3 = demander_choix(
        "\nTu fais quoi ?",
        [
            "Tu passes normalement. Droit. Pas trop vite, pas trop lentement.",
            "Tu sors par une sortie de secours reperee a l'arrivee",
            "Tu attends que l'Auror soit occupe puis tu files"
        ]
    )
    if c3 == "Tu passes normalement. Droit. Pas trop vite, pas trop lentement.":
        print("\nL'Auror te jette un coup d'oeil. Tu le regardes sans t'arreter.")
        print("Il te laisse passer. Dehors. Tu reprends ta vraie apparence.")
        discrecion = discrecion + 2
    elif c3 == "Tu sors par une sortie de secours reperee a l'arrivee":
        print("\nQuelqu'un te voit prendre cette sortie inhabituelle.")
        print("Mais tu es deja dehors et tu te fondes dans la foule.")
        discrecion = discrecion + 1
    else:
        print("\nTu attends trop longtemps. La potion commence a s'effacer.")
        print("Quelqu'un crie. Tu cours.")
        suspicion = suspicion + 2
    input("[Entree...]")

    print("\n" + VERT + "~ resultat ~" + RESET)
    if suspicion == 0 and discrecion >= 4:
        print("VISION -- Mission accomplie sans la moindre trace.")
        print("\nLe dossier change de mains le soir meme.")
        print("Personne au Ministere ne saura jamais que tu etais passe par la.")
    elif suspicion <= 1:
        print("VISION -- Mission reussie.")
        print("\nQuelques regards suspects, peut-etre des questions le lendemain.")
        print("Mais le dossier est en securite.")
    else:
        print("VISION -- Mission reussie, mais de peu.")
        print("\nTu repars avec le dossier. Le Ministere va se poser des questions.")
    input("[Entree...]")


def vision_poufsouffle(joueur):
    prenom = joueur["Prenom"]

    print("\n" + CYAN + GRAS + "~ VISION -- Poufsouffle ~" + RESET)
    input("[Entree...]")

    print("\nTu te vois adulte, au bord du lac de Poudlard. Nuit noire.")
    print("L'eau est sombre et froide. Des lueurs magiques sous la surface.")
    input("[Entree...]")

    print("\nTes amis sont la-dessous. Retenus par une magie ancienne.")
    print("Tu as vu des Epouvantards aquatiques les emporter.")
    print("Personne d'autre ne peut y aller. Le temps est compte.")
    input("[Entree...]")

    courage = 0

    # comment respirer sous l'eau
    c1 = demander_choix(
        "\nQuel sort tu utilises pour tenir sous l'eau ?",
        [
            "Branchiflors -- transforme temporairement tes poumons",
            "Respiro -- une bulle d'air autour de ta tete",
            "Tu retiens ta respiration et tu nages le plus vite possible"
        ]
    )
    if c1 in ["Branchiflors -- transforme temporairement tes poumons",
              "Respiro -- une bulle d'air autour de ta tete"]:
        print("\nParfait. Tu peux rester sous l'eau plusieurs minutes.")
        print("Tu plonges.")
        courage = courage + 1
    else:
        print("\nC'est risque. Mais si tu vas assez vite...")
        print("Tu plonges.")
    input("[Entree...]")

    # les Grindylows
    afficher_art("grindylow")
    print("\nL'eau est glacee. La lumiere disparait vite.")
    print("Tu vois la lueur retenant tes amis -- encore loin.")
    print("\nMais quelque chose te tire la cheville. Des Grindylows.")
    print("Trois. Petits mais rapides, avec leurs doigts crochus.")
    c2 = demander_choix(
        "\nQue fais-tu ?",
        [
            "Flipendo -- tu les projettes en arriere",
            "Tu tires fort pour te degager et tu continues a nager",
            "Tu essaies de les contourner en changeant de direction"
        ]
    )
    if c2 == "Flipendo -- tu les projettes en arriere":
        print("\nBang. Les trois tourbillonnent dans l'eau et disparaissent dans le noir.")
        print("Tu reprends ta trajectoire.")
        courage = courage + 2
    elif c2 == "Tu tires fort pour te degager et tu continues a nager":
        print("\nTu perds dix secondes. Mais tu es libre.")
        courage = courage + 1
    else:
        print("\nTu les perds de vue mais tu perds aussi du temps.")
    input("[Entree...]")

    # liberer les amis
    print("\nTu les vois. Immobiles dans la lumiere bleue du fond.")
    print("Des chaines de lumiere les retiennent. Magiques.")
    c3 = demander_choix(
        "\nComment tu les liberes ?",
        [
            "Tu cherches l'ancre magique au fond et tu la detruis",
            "Diffindo sur chaque chaine, une par une",
            "Tu prends tes amis par la main et tu nages vers le haut avec tout ce qui te reste"
        ]
    )
    if c3 == "Tu cherches l'ancre magique au fond et tu la detruis":
        print("\nTu reperes une sphere lumineuse ancree dans la vase. Reducto.")
        print("Les chaines de tous tes amis disparaissent en meme temps.")
        print("Ils commencent a remonter d'eux-memes.")
        courage = courage + 2
    elif c3 == "Diffindo sur chaque chaine, une par une":
        print("\nCa marche. Un par un. Tu en liberes la plupart avant de manquer d'air.")
        print("Le dernier te tend la main et vous remontez ensemble.")
        courage = courage + 1
    else:
        print("\nLes chaines cedent sous l'effort conjoint.")
        print("Vous remontez tous ensemble, en groupe serre.")
        courage = courage + 1
    input("[Entree...]")

    print("\n" + CYAN + "~ resultat ~" + RESET)
    if courage >= 4:
        print("VISION -- Tu les ramenes tous a la surface.")
        print("\nIls reprennent leur souffle sur la rive, trempes mais vivants.")
    elif courage >= 2:
        print("VISION -- Tu en ramenes la plupart.")
        print("\nLe lac redevient calme derriere vous.")
        print("Tu n'as pas pu aller aussi vite que tu voulais, mais l'essentiel est sauve.")
    else:
        print("VISION -- Vous remontez tous, de justesse.")
        print("\nL'air t'a manque sur la fin. Mais personne n'est reste au fond.")
    input("[Entree...]")


def vision_serdaigle(joueur):
    prenom = joueur["Prenom"]

    print("\n" + VIOLET + GRAS + "~ VISION -- Serdaigle ~" + RESET)
    input("[Entree...]")

    afficher_art("porte")
    print("\nTu te vois adulte. Le Departement des Mysteres du Ministere de la Magie.")
    print("Couloirs qui changent. Portes qui se deplacent toutes seules.")
    print("Personne d'autre n'est suppose etre ici a cette heure.")
    input("[Entree...]")

    print("\nTu cherches quelque chose d'important -- une prophecie.")
    print("Mais le Departement met ton esprit a l'epreuve avant de te laisser passer.")
    print("Trois salles. Trois enigmes. Une seule chance pour chacune.")
    input("\n[Entree pour entrer dans la premiere salle...]")

    score = 0

    # salle 1 : le Temps
    print("\n--- Salle du Temps ---")
    print("\nLes Retourateurs tournent dans leurs cloches de verre.")
    print("Sur le mur, une inscription gravee dans la pierre :")
    print('\n"Je vais vers l\'avant mais on me lit de droite a gauche.')
    print(" Je mesure tout mais ne possede rien.")
    print(' Qui suis-je ?"')
    rep1 = input("\nTa reponse : ").strip().lower()
    if "temps" in rep1:
        print("\nLa porte s'ouvre en silence.")
        score = score + 1
    else:
        print("\nLa porte vibre. Ce n'est pas ca.")
        print("La bonne reponse etait : le temps.")
        print("La porte s'ouvre quand meme -- le Departement teste, il ne punit pas.")
    input("[Entree...]")

    # salle 2 : paradoxe du menteur
    print("\n--- Salle de la Pensee ---")
    print("\nUn Pensieve au centre. De la lumiere argentee.")
    print("Un gardien te barre la route. Il dit :")
    print('\n"Devant toi, deux portes.')
    print(" L'une mene a la verite. L'autre a l'illusion.")
    print(" Je garde la porte de la verite.")
    print(" Je mens toujours.")
    print(' Quelle porte choisis-tu ?"')
    c2 = demander_choix(
        "\nTa reponse :",
        [
            "La porte de gauche",
            "La porte de droite",
            "Tu lui demandes quelle porte il ne garderait jamais"
        ]
    )
    if c2 == "La porte de droite":
        # il ment -> il ne garde pas la verite -> il garde l'illusion -> droite = verite
        print("\nLe gardien s'efface.")
        print("Il ment. Il dit garder la verite donc il garde l'illusion. La droite est juste.")
        score = score + 1
    elif c2 == "Tu lui demandes quelle porte il ne garderait jamais":
        print("\nQuestion meta. Il est destabilise et repond malgre lui.")
        print("Tu entres. Tu as trouve une faille plutot que la solution directe.")
        score = score + 1
    else:
        print("\nTu entres par la gauche. C'est l'illusion.")
        print("Tu te retrouves au meme endroit une minute plus tard.")
        print("Tu recommences et tu prends l'autre porte.")
    input("[Entree...]")

    # salle 3 : les Propheties
    print("\n--- Salle des Propheties ---")
    print("\nDes milliers de spheres lumineuses alignees dans l'obscurite.")
    print("Une voix dans l'air, sans source :")
    print('"Prouve que tu es digne de l\'entendre."')
    print("\nQuestion : Qu'est-ce qui distingue une vraie prophecie d'une simple prediction ?")
    c3 = demander_choix(
        "\nTa reponse :",
        [
            "Elle est enregistree ici et ne peut etre entendue que par ceux qu'elle concerne",
            "Une prophecie est toujours vraie, une prediction peut se tromper",
            "Elle vient d'un Voyant officiellement reconnu par le Ministere"
        ]
    )
    if c3 == "Elle est enregistree ici et ne peut etre entendue que par ceux qu'elle concerne":
        print("\nExact.")
        print("La bonne sphere descend d'elle-meme vers toi, lentement.")
        score = score + 1
    else:
        print("\nPas tout a fait. La bonne reponse etait la premiere.")
        print("La sphere vibre mais ne bouge pas. Tu devras revenir.")
    input("[Entree...]")

    print("\n" + VIOLET + "~ resultat ~" + RESET)
    if score == 3:
        print("VISION -- Tu as traverse les trois salles.")
        print("\nLe Departement t'a laisse passer jusqu'au bout.")
        print("La prophecie que tu cherchais est enfin a portee de main.")
    elif score == 2:
        print("VISION -- Deux salles sur trois.")
        print("\nTu as bute sur une enigme, mais tu as avance plus loin que la plupart.")
    else:
        print("VISION -- Une salle sur trois.")
        print("\nLe Departement te laisse repartir. Tu reviendras mieux prepare.")
    input("[Entree...]")


# -------------------------------------------------------
# point d'entree du chapitre
# -------------------------------------------------------

def lancer_chapitre4_quidditch(joueur, maisons):
    print("\n" + GRAS + JAUNE + "== CHAPITRE 4 -- L'Epreuve de Quidditch ==" + RESET)
    match_quidditch(joueur, maisons)
    print("\n--- Fin du Chapitre 4 ---")
    afficher_maison_gagnante(maisons)
    afficher_personnage(joueur)
