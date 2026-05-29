"""
VERSION GRAPHIQUE (BONUS) — Poudlard.

ATTENTION : ce fichier utilise tkinter, qui n'est PAS dans les bibliotheques
autorisees par le sujet. Ce n'est donc PAS la version notee.
La version officielle (terminal, uniquement random + json) reste main.py.

Principe (a expliquer en soutenance en une phrase) :
on remplace print et input pour qu'ils parlent a une fenetre au lieu du
terminal. Le code du jeu (menu + chapitres) n'est PAS modifie : c'est
exactement le meme jeu qui tourne dans les deux modes.

Ce que cette version apporte par rapport au terminal :
  - les choix numerotes (1. ... / 2. ...) deviennent de vrais BOUTONS
    cliquables : on detecte les lignes "1. xxx" affichees juste avant un
    input(), et on fabrique un bouton par option ;
  - les pauses "(Entree pour continuer...)" deviennent un bouton "Continuer" ;
  - sinon (ex : saisir son nom) on garde un champ de texte classique ;
  - theme sombre facon parchemin de nuit + couleurs des maisons.

Astuce technique : pas de threads. input() affiche les boutons/le champ
puis appelle root.wait_variable(), qui attend le clic dans une boucle
d'evenements imbriquee, puis renvoie la saisie.
"""

import sys
import builtins
import re
import tkinter as tk
from tkinter import scrolledtext

from menu import lancer_choix_menu


# Code ANSI -> nom de tag de couleur dans la zone de texte.
CODE_VERS_TAG = {
    "91": "rouge", "92": "vert", "93": "jaune", "94": "bleu",
    "95": "violet", "96": "cyan", "90": "gris", "97": "blanc",
}

# Couleur d'affichage de chaque tag (theme sombre facon terminal).
TAG_VERS_COULEUR = {
    "rouge": "#ff6b6b", "vert": "#5af78e", "jaune": "#f3f99d",
    "bleu": "#57c7ff", "violet": "#ff6ac1", "cyan": "#9aedfe",
    "gris": "#9aa0a6", "blanc": "#ffffff",
}

# Palette de l'interface.
FOND = "#15131f"          # fond general (nuit)
FOND_TEXTE = "#1b1830"    # fond de la zone d'histoire
FOND_BAS = "#15131f"      # fond de la barre d'interaction
TEXTE = "#e8e4f3"         # couleur du texte par defaut
OR = "#d4af37"            # accent dore facon Poudlard
OR_CLAIR = "#f0d979"

MOTIF_ANSI = re.compile(r"\x1b\[([0-9;]*)m")
# Une ligne du type "1. Faire ceci" (un choix numerote).
MOTIF_OPTION = re.compile(r"^\s*(\d+)\.\s+(.+?)\s*$")


class SortieFenetre:
    """Objet qui remplace sys.stdout : il traduit les codes couleur ANSI
    en texte colore dans la zone de texte, et garde en memoire les
    dernieres lignes affichees (pour detecter les choix numerotes)."""

    def __init__(self, widget):
        self.widget = widget
        self.couleur = None
        self.gras = False
        self.ligne_courante = ""    # texte (sans ANSI) de la ligne en cours
        self.lignes = []            # historique des lignes terminees (sans ANSI)

    def write(self, texte):
        position = 0
        for trouve in MOTIF_ANSI.finditer(texte):
            avant = texte[position:trouve.start()]
            if avant:
                self._inserer(avant)
            self._appliquer_codes(trouve.group(1))
            position = trouve.end()
        reste = texte[position:]
        if reste:
            self._inserer(reste)

    def _appliquer_codes(self, codes):
        for code in codes.split(";"):
            if code == "" or code == "0":
                self.couleur = None
                self.gras = False
            elif code == "1":
                self.gras = True
            elif code in CODE_VERS_TAG:
                self.couleur = CODE_VERS_TAG[code]

    def _inserer(self, texte):
        # On met a jour notre memoire de lignes (texte brut, sans couleur).
        for caractere in texte:
            if caractere == "\n":
                self.lignes.append(self.ligne_courante)
                self.ligne_courante = ""
            else:
                self.ligne_courante = self.ligne_courante + caractere
        if len(self.lignes) > 60:
            self.lignes = self.lignes[-60:]

        # Puis on affiche dans la fenetre, avec les bons tags de couleur.
        tags = []
        if self.couleur:
            tags.append(self.couleur)
        if self.gras:
            tags.append("gras")
        self.widget.config(state="normal")
        self.widget.insert(tk.END, texte, tuple(tags))
        self.widget.see(tk.END)
        self.widget.config(state="disabled")
        self.widget.update_idletasks()

    def options_recentes(self):
        """Renvoie la liste des choix numerotes affiches juste avant l'input
        (les dernieres lignes consecutives du type '1. ...'), ou [] si aucun."""
        # On part de la fin en ignorant les lignes vides.
        lignes = list(self.lignes)
        if self.ligne_courante.strip() != "":
            lignes.append(self.ligne_courante)

        i = len(lignes) - 1
        while i >= 0 and lignes[i].strip() == "":
            i = i - 1

        trouve = []
        while i >= 0:
            m = MOTIF_OPTION.match(lignes[i])
            if not m:
                break
            trouve.append((int(m.group(1)), m.group(2)))
            i = i - 1

        trouve.reverse()
        # Verifier que c'est bien 1, 2, 3, ... sans trou.
        if not trouve:
            return []
        for position in range(len(trouve)):
            if trouve[position][0] != position + 1:
                return []
        return [texte for (_numero, texte) in trouve]

    def flush(self):
        pass


def survol(bouton, normal, survol_couleur):
    """Petit effet : le bouton change de couleur au passage de la souris."""
    bouton.bind("<Enter>", lambda e: bouton.config(bg=survol_couleur))
    bouton.bind("<Leave>", lambda e: bouton.config(bg=normal))


def construire_fenetre():
    root = tk.Tk()
    root.title("Poudlard — L'Art de Coder comme un Sorcier")
    root.geometry("900x680")
    root.configure(bg=FOND)
    root.minsize(720, 520)

    # --- Banniere du haut ---
    entete = tk.Frame(root, bg=FOND)
    entete.pack(fill="x", padx=18, pady=(14, 6))
    tk.Label(
        entete, text="✦  P O U D L A R D  ✦", bg=FOND, fg=OR,
        font=("Georgia", 20, "bold"),
    ).pack()
    tk.Label(
        entete, text="L'Art de Coder comme un Sorcier",
        bg=FOND, fg="#9c93c4", font=("Georgia", 11, "italic"),
    ).pack()
    tk.Frame(root, bg=OR, height=2).pack(fill="x", padx=18, pady=(4, 8))

    # --- Zone d'histoire ---
    zone = scrolledtext.ScrolledText(
        root, wrap="word", bg=FOND_TEXTE, fg=TEXTE,
        font=("Consolas", 13), insertbackground=TEXTE,
        borderwidth=0, padx=18, pady=16, state="disabled",
        spacing1=2, spacing3=4,
    )
    zone.pack(fill="both", expand=True, padx=18)

    for tag, couleur in TAG_VERS_COULEUR.items():
        zone.tag_config(tag, foreground=couleur)
    zone.tag_config("gras", font=("Consolas", 13, "bold"))

    # --- Barre d'interaction (boutons OU champ texte, selon le contexte) ---
    bas = tk.Frame(root, bg=FOND_BAS)
    bas.pack(fill="x", padx=18, pady=(8, 16))

    return root, zone, bas


def main():
    root, zone, bas = construire_fenetre()
    sortie = SortieFenetre(zone)

    # Variable basculee a chaque validation pour debloquer wait_variable.
    attente = tk.IntVar(value=0)
    reponse = {"valeur": ""}

    def repondre(valeur):
        reponse["valeur"] = valeur
        attente.set(attente.get() + 1)

    def vider_bas():
        for widget in bas.winfo_children():
            widget.destroy()

    def montrer_boutons_choix(options):
        """Un bouton dore par option ; renvoie le numero choisi (en texte)."""
        vider_bas()
        for index in range(len(options)):
            numero = index + 1
            bouton = tk.Button(
                bas, text="  " + str(numero) + ".  " + options[index],
                font=("Georgia", 12), anchor="w", justify="left",
                bg="#272140", fg=TEXTE, activebackground=OR,
                activeforeground=FOND, relief="flat", padx=14, pady=9,
                cursor="hand2", wraplength=820,
                command=lambda n=numero: repondre(str(n)),
            )
            bouton.pack(fill="x", pady=3)
            survol(bouton, "#272140", "#3a3160")
            # Raccourci clavier : touche 1..9.
            if numero <= 9:
                root.bind(str(numero), lambda e, n=numero: repondre(str(n)))

    def montrer_bouton_continuer():
        vider_bas()
        bouton = tk.Button(
            bas, text="Continuer  ▶", font=("Georgia", 12, "bold"),
            bg=OR, fg=FOND, activebackground=OR_CLAIR, activeforeground=FOND,
            relief="flat", padx=20, pady=9, cursor="hand2",
            command=lambda: repondre(""),
        )
        bouton.pack(side="right")
        survol(bouton, OR, OR_CLAIR)
        root.bind("<Return>", lambda e: repondre(""))

    def montrer_champ_texte():
        vider_bas()
        champ = tk.Entry(
            bas, bg="#272140", fg=TEXTE, font=("Consolas", 13),
            insertbackground=TEXTE, relief="flat",
        )
        champ.pack(side="left", fill="x", expand=True, ipady=7)
        champ.focus_set()
        bouton = tk.Button(
            bas, text="Valider", font=("Georgia", 11, "bold"),
            bg=OR, fg=FOND, activebackground=OR_CLAIR, activeforeground=FOND,
            relief="flat", padx=18, cursor="hand2",
            command=lambda: repondre(champ.get()),
        )
        bouton.pack(side="left", padx=(8, 0))
        survol(bouton, OR, OR_CLAIR)
        champ.bind("<Return>", lambda e: repondre(champ.get()))

    def desactiver_raccourcis():
        for touche in ["<Return>", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            root.unbind(touche)

    def entree_fenetre(prompt=""):
        texte_prompt = str(prompt)
        prompt_simple = texte_prompt.lower()
        # On detecte les options AVANT d'ecrire le prompt (sinon le prompt
        # "Votre choix : " serait pris pour la derniere ligne).
        options = sortie.options_recentes()

        if "continuer" in prompt_simple:
            # Pause : un simple bouton, pas besoin d'afficher le texte du prompt.
            montrer_bouton_continuer()
        elif options:
            # Choix numerote : les boutons remplacent le "Votre choix :".
            montrer_boutons_choix(options)
        else:
            # Saisie libre (nom, nombre...) : on affiche la question + un champ.
            if texte_prompt:
                sortie.write(texte_prompt)
            montrer_champ_texte()

        try:
            root.wait_variable(attente)   # attend le clic / la touche
        except tk.TclError:
            raise SystemExit              # la fenetre a ete fermee

        desactiver_raccourcis()
        valeur = reponse["valeur"]
        vider_bas()
        # On efface la memoire des options pour ne pas les reutiliser par erreur.
        sortie.lignes = []
        sortie.ligne_courante = ""
        # On affiche dans l'histoire ce que le joueur a choisi/saisi.
        if valeur != "":
            sortie.write("➤ " + valeur + "\n")
        else:
            sortie.write("\n")
        return valeur

    # On branche print et input sur la fenetre.
    sys.stdout = sortie
    builtins.input = entree_fenetre

    def lancer_jeu():
        try:
            lancer_choix_menu()
            sortie.write("\n=== Fin de l'aventure. Tu peux fermer la fenetre. ===\n")
        except SystemExit:
            sortie.write("\n=== Fin du jeu. Tu peux fermer la fenetre. ===\n")
        vider_bas()

    root.after(200, lancer_jeu)
    root.mainloop()


if __name__ == "__main__":
    main()
