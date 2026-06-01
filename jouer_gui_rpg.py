# VERSION GRAPHIQUE RPG (BONUS) — Poudlard
# Style Undertale : grande image en haut, boite de texte en bas.
# Quand afficher_art("nom") est appele, l'image du haut change.
# Le texte s'affiche lettre par lettre dans la boite du bas.
# Lancer : python jouer_gui_rpg.py

import sys
import os
import builtins
import re
import tkinter as tk
from tkinter import font as tkfont
from PIL import Image, ImageTk

# Se placer dans le dossier du projet pour que open("data/...") fonctionne
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from menu import lancer_choix_menu
import utils.art

# Codes ANSI -> couleur texte
CODE_VERS_COULEUR = {
    "91": "#ff6b6b", "92": "#5af78e", "93": "#f3f99d",
    "94": "#57c7ff", "95": "#ff6ac1", "96": "#9aedfe",
    "90": "#9aa0a6", "97": "#ffffff",
}
MOTIF_ANSI   = re.compile(r"\x1b\[([0-9;]*)m")
MOTIF_OPTION = re.compile(r"^\s*(\d+)\.\s+(.+?)\s*$")

# Palette
NOIR    = "#000000"
GRIS_F  = "#111111"
BLANC   = "#ffffff"
OR      = "#d4af37"
OR_C    = "#f0d979"
BORDURE = "#ffffff"   # bordure blanche style Undertale


class AppRPG:
    def __init__(self, root):
        self.root = root
        self.root.title("Poudlard")
        self.root.configure(bg=NOIR)
        self.root.geometry("1100x800")
        self.root.minsize(800, 600)

        # ── Zone image (haut, prend tout l'espace disponible) ──────────────
        self.cadre_img = tk.Frame(root, bg=NOIR)
        self.cadre_img.pack(fill="both", expand=True, padx=0, pady=0)

        self.label_img = tk.Label(self.cadre_img, bg=NOIR)
        self.label_img.place(relx=0.5, rely=0.5, anchor="center")

        self._photo_actuelle = None  # garde la reference pour eviter le GC
        self._charger_image_defaut()

        # ── Boite de texte style RPG (bas) ─────────────────────────────────
        cadre_bas = tk.Frame(root, bg=NOIR)
        cadre_bas.pack(fill="x", padx=16, pady=(0, 16))

        # Bordure blanche comme Undertale
        bordure = tk.Frame(cadre_bas, bg=BORDURE, padx=3, pady=3)
        bordure.pack(fill="x")

        interieur = tk.Frame(bordure, bg=GRIS_F)
        interieur.pack(fill="x")

        # Zone de texte (3 lignes visibles, police grande et lisible)
        police = tkfont.Font(family="Courier New", size=16)
        self.zone_texte = tk.Text(
            interieur, height=4, bg=GRIS_F, fg=BLANC,
            font=police, wrap="word", borderwidth=0,
            padx=16, pady=12, state="disabled",
            insertbackground=BLANC,
        )
        self.zone_texte.pack(fill="x")
        self.zone_texte.tag_config("gras", font=tkfont.Font(family="Courier New", size=16, weight="bold"))
        for code, couleur in CODE_VERS_COULEUR.items():
            self.zone_texte.tag_config(code, foreground=couleur)

        # Zone des boutons (sous la boite de texte)
        self.cadre_boutons = tk.Frame(cadre_bas, bg=NOIR)
        self.cadre_boutons.pack(fill="x", pady=(6, 0))

        # ── Etat interne ────────────────────────────────────────────────────
        self.attente      = tk.IntVar(value=0)
        self.reponse      = {"valeur": ""}
        self.couleur_texte = None
        self.gras          = False
        self.lignes        = []
        self.ligne_courante = ""
        self._file_lettres  = []   # file d'attente pour l'effet machine a ecrire
        self._en_cours      = False

    # ── Image ───────────────────────────────────────────────────────────────

    def _charger_image_defaut(self):
        # Fond noir avec titre au demarrage
        self.label_img.config(image="", text="✦  P O U D L A R D  ✦",
                              fg=OR, font=("Georgia", 28, "bold"))

    def afficher_image(self, nom):
        chemin = "data/art/" + nom + ".png"
        try:
            img = Image.open(chemin)
            # Prend la taille reelle du cadre image pour s'adapter
            self.root.update_idletasks()
            larg = max(self.cadre_img.winfo_width(), 800)
            haut = max(self.cadre_img.winfo_height(), 400)
            img.thumbnail((larg, haut), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self._photo_actuelle = photo
            self.label_img.config(image=photo, text="")
        except Exception:
            pass  # si l'image manque on garde l'ancienne

    # ── Texte (machine a ecrire) ─────────────────────────────────────────────

    def _inserer_char(self, char, tags):
        self.zone_texte.config(state="normal")
        self.zone_texte.insert(tk.END, char, tuple(tags))
        self.zone_texte.see(tk.END)
        self.zone_texte.config(state="disabled")

    def _process_file(self):
        if not self._file_lettres:
            self._en_cours = False
            self.zone_texte.update_idletasks()
            return
        char, tags = self._file_lettres.pop(0)
        self._inserer_char(char, tags)
        # 18ms par lettre = ~55 caracteres/s, suffisamment rapide
        self.root.after(18, self._process_file)

    def ecrire(self, texte):
        # Parse les codes ANSI et met les caracteres en file
        pos = 0
        for m in MOTIF_ANSI.finditer(texte):
            avant = texte[pos:m.start()]
            if avant:
                self._enqueue(avant)
            self._appliquer_codes(m.group(1))
            pos = m.end()
        reste = texte[pos:]
        if reste:
            self._enqueue(reste)
        # Mettre a jour la memoire des lignes (pour detecter les choix)
        texte_brut = MOTIF_ANSI.sub("", texte)
        for c in texte_brut:
            if c == "\n":
                self.lignes.append(self.ligne_courante)
                self.ligne_courante = ""
            else:
                self.ligne_courante += c
        if len(self.lignes) > 60:
            self.lignes = self.lignes[-60:]
        # Si trop de texte en attente (inventaire, stats...) on affiche d'un coup
        if len(self._file_lettres) > 120:
            self._attendre_fin_ecriture()
        elif not self._en_cours:
            self._en_cours = True
            self._process_file()

    def _enqueue(self, texte):
        tags = []
        if self.couleur_texte:
            tags.append(self.couleur_texte)
        if self.gras:
            tags.append("gras")
        for char in texte:
            self._file_lettres.append((char, list(tags)))

    def _appliquer_codes(self, codes):
        parties = codes.split(";")
        i = 0
        while i < len(parties):
            c = parties[i]
            if c in ("", "0"):
                self.couleur_texte = None
                self.gras = False
            elif c == "1":
                self.gras = True
            elif c in CODE_VERS_COULEUR:
                self.couleur_texte = c
            i += 1

    def vider_texte(self):
        self.zone_texte.config(state="normal")
        self.zone_texte.delete("1.0", tk.END)
        self.zone_texte.config(state="disabled")
        self.lignes = []
        self.ligne_courante = ""
        self._file_lettres = []
        self._en_cours = False

    def flush(self):
        pass

    def write(self, texte):
        self.ecrire(texte)

    # ── Detection des choix ─────────────────────────────────────────────────

    def options_recentes(self):
        lignes = list(self.lignes)
        if self.ligne_courante.strip():
            lignes.append(self.ligne_courante)
        i = len(lignes) - 1
        while i >= 0 and not lignes[i].strip():
            i -= 1
        trouve = []
        while i >= 0:
            m = MOTIF_OPTION.match(lignes[i])
            if not m:
                break
            trouve.append((int(m.group(1)), m.group(2)))
            i -= 1
        trouve.reverse()
        if not trouve:
            return []
        for idx in range(len(trouve)):
            if trouve[idx][0] != idx + 1:
                return []
        return [t for _, t in trouve]

    # ── Boutons ─────────────────────────────────────────────────────────────

    def _vider_boutons(self):
        for w in self.cadre_boutons.winfo_children():
            w.destroy()

    def _repondre(self, valeur):
        # Annule l'effet machine a ecrire restant et repond
        self._file_lettres = []
        self._en_cours = False
        self.reponse["valeur"] = valeur
        self.attente.set(self.attente.get() + 1)

    def montrer_boutons_choix(self, options):
        self._vider_boutons()
        nb = len(options)
        for idx, texte in enumerate(options):
            n = idx + 1
            b = tk.Button(
                self.cadre_boutons,
                text="❯  " + texte,
                font=("Courier New", 14), anchor="w",
                bg=GRIS_F, fg=BLANC,
                activebackground=OR, activeforeground=NOIR,
                relief="flat", padx=12, pady=7,
                cursor="hand2", wraplength=860,
                command=lambda n=n: self._repondre(str(n)),
            )
            b.pack(fill="x", pady=2)
            b.bind("<Enter>", lambda e, b=b: b.config(bg="#222222", fg=OR))
            b.bind("<Leave>", lambda e, b=b: b.config(bg=GRIS_F, fg=BLANC))
            if n <= 9:
                self.root.bind(str(n), lambda e, n=n: self._repondre(str(n)))

    def montrer_continuer(self):
        self._vider_boutons()
        b = tk.Button(
            self.cadre_boutons,
            text="▼  Continuer",
            font=("Courier New", 14, "bold"),
            bg=NOIR, fg=OR,
            activebackground=OR, activeforeground=NOIR,
            relief="flat", padx=12, pady=7,
            cursor="hand2",
            command=lambda: self._repondre(""),
        )
        b.pack(side="right")
        b.bind("<Enter>", lambda e: b.config(fg=OR_C))
        b.bind("<Leave>", lambda e: b.config(fg=OR))
        self.root.bind("<Return>", lambda e: self._repondre(""))
        self.root.bind("<space>",  lambda e: self._repondre(""))

    def montrer_champ(self):
        self._vider_boutons()
        champ = tk.Entry(
            self.cadre_boutons,
            bg="#1a1a1a", fg=BLANC,
            font=("Courier New", 13),
            insertbackground=BLANC, relief="flat",
        )
        champ.pack(side="left", fill="x", expand=True, ipady=7)
        champ.focus_set()
        b = tk.Button(
            self.cadre_boutons,
            text="OK",
            font=("Courier New", 11, "bold"),
            bg=OR, fg=NOIR,
            activebackground=OR_C, activeforeground=NOIR,
            relief="flat", padx=16, cursor="hand2",
            command=lambda: self._repondre(champ.get()),
        )
        b.pack(side="left", padx=(6, 0))
        champ.bind("<Return>", lambda e: self._repondre(champ.get()))

    def _debind(self):
        for k in ["<Return>", "<space>"] + [str(i) for i in range(1, 10)]:
            self.root.unbind(k)

    # ── Entree utilisateur (remplace input()) ───────────────────────────────

    def entree(self, prompt=""):
        # On attend que la file de lettres soit vide avant d'afficher les boutons
        self._attendre_fin_ecriture()

        options = self.options_recentes()
        prompt_s = str(prompt).lower()

        if "continuer" in prompt_s or "entree" in prompt_s or prompt_s.strip() in ("", "[entree...]"):
            self.montrer_continuer()
        elif options:
            self.montrer_boutons_choix(options)
        else:
            if prompt:
                self.ecrire(str(prompt))
                self._attendre_fin_ecriture()
            self.montrer_champ()

        try:
            self.root.wait_variable(self.attente)
        except tk.TclError:
            raise SystemExit

        self._debind()
        valeur = self.reponse["valeur"]
        self._vider_boutons()
        self.lignes = []
        self.ligne_courante = ""
        if valeur:
            self.ecrire("❯ " + valeur + "\n")
        else:
            self.ecrire("\n")
        return valeur

    def _attendre_fin_ecriture(self):
        # Vide la file de lettres d'un coup (pas d'attente)
        while self._file_lettres:
            char, tags = self._file_lettres.pop(0)
            self._inserer_char(char, tags)
        self._en_cours = False
        self.zone_texte.update_idletasks()


def main():
    root = tk.Tk()
    app = AppRPG(root)

    # Branche sys.stdout et builtins.input sur l'app
    sys.stdout = app
    builtins.input = app.entree

    # Remplace afficher_art par la version qui met a jour l'image du haut
    def afficher_art_rpg(nom):
        app.afficher_image(nom)
        app.vider_texte()   # nouvelle scene = on efface le texte precedent

    utils.art.afficher_art = afficher_art_rpg

    def lancer():
        try:
            lancer_choix_menu()
            app.ecrire("\n=== Fin de l'aventure. Tu peux fermer la fenetre. ===\n")
        except SystemExit:
            pass
        app._vider_boutons()

    root.after(200, lancer)
    root.mainloop()


if __name__ == "__main__":
    main()
