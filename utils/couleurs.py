# couleurs.py
# Couleurs ANSI partagees par tous les chapitres.
# Ce sont juste des chaines de caracteres : aucun import, donc compatible
# avec les contraintes du projet (seuls random et json sont autorises).

ROUGE = "\033[91m"
VERT = "\033[92m"
JAUNE = "\033[93m"
BLEU = "\033[94m"
VIOLET = "\033[95m"
CYAN = "\033[96m"
GRIS = "\033[90m"
BLANC = "\033[97m"

GRAS = "\033[1m"
SOULIGNE = "\033[4m"
RESET = "\033[0m"

# Couleur associee a chaque maison (pour la narration).
COULEUR_MAISON = {
    "Gryffondor": ROUGE,
    "Serpentard": VERT,
    "Poufsouffle": JAUNE,
    "Serdaigle": BLEU
}


def titre(texte):
    # Renvoie un titre encadre (a passer a print).
    ligne = "=" * (len(texte) + 4)
    return GRAS + JAUNE + ligne + "\n  " + texte + "\n" + ligne + RESET


def colorer(texte, couleur):
    # Renvoie le texte entoure d'une couleur puis remis a zero.
    return couleur + texte + RESET
