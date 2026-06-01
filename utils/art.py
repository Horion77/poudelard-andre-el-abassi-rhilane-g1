# art.py
# Affiche un pixel art stocke dans data/art/<nom>.txt.
#
# Comment ca marche :
#   - chaque "pixel" dans le .txt = 2 espaces avec une couleur de fond ANSI
#     exemple : "\033[48;2;255;200;0m  \033[0m"  <- carre jaune
#   - c'est juste du texte : open() le lit, print() l'affiche.
#   - aucune bibliotheque interdite (meme principe que les couleurs ANSI du jeu).
#
# Utilisation dans un chapitre :
#   from utils.art import afficher_art
#   afficher_art("vif_or")   # affiche data/art/vif_or.txt


def afficher_art(nom):
    # En terminal : rien (le pixel art texte n'est pas joli).
    # En version graphique (jouer_gui.py), cette fonction est remplacee
    # par une vraie image PNG affichee dans la fenetre tkinter.
    pass
