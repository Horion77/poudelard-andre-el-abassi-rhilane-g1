import json


def demander_texte(message):
    saisie = input(message).strip()
    while saisie == "":
        saisie = input(message).strip()
    return saisie


def demander_nombre(message, min_val=None, max_val=None):
    while True:
        saisie = input(message).strip()

        # Vérifier que chaque caractère est un chiffre (ou '-' en premier)
        valide = True
        if len(saisie) == 0:
            valide = False
        else:
            debut = 0
            if saisie[0] == '-':
                debut = 1
            if debut == len(saisie):
                valide = False
            else:
                for i in range(debut, len(saisie)):
                    if ord(saisie[i]) < ord('0') or ord(saisie[i]) > ord('9'):
                        valide = False

        if not valide:
            print("Veuillez entrer un nombre valide.")
            continue

        nombre = int(saisie)

        if min_val is not None and nombre < min_val:
            print("Veuillez entrer un nombre entre " + str(min_val) + " et " + str(max_val) + ".")
            continue
        if max_val is not None and nombre > max_val:
            print("Veuillez entrer un nombre entre " + str(min_val) + " et " + str(max_val) + ".")
            continue

        return nombre


def demander_choix(message, options):
    print(message)
    for i in range(len(options)):
        print(str(i + 1) + ". " + options[i])
    numero = demander_nombre("Votre choix : ", 1, len(options))
    return options[numero - 1]


def load_fichier(chemin_fichier):
    with open(chemin_fichier, 'r', encoding='utf-8') as f:
        donnees = json.load(f)
    return donnees