# Poudlard

## Auteurs

- Andre Alan
- El-Abassi Sara
- Rhilane Basma

**Groupe : G2**

## L'histoire

Un jeu d'aventure interactif inspiré de l'univers de Harry Potter. Tu incarnes
un·e nouvel·le élève qui, dès le Poudlard Express, rejoint la bande de Harry,
Ron et Hermione — une histoire alternative où tu vis la saga à leurs côtés.

L'aventure se déroule en 4 chapitres : l'arrivée dans le monde magique, le
voyage vers Poudlard et la répartition, les premiers cours, puis l'épreuve
finale de Quidditch.

## Comment lancer le jeu

Trois façons de jouer, **avec exactement la même histoire** :

### 1. Version terminal (version officielle, notée)

```
python main.py
```

N'utilise que les bibliothèques autorisées (`random` et `json`). Les couleurs
sont gérées par des codes ANSI (de simples chaînes de caractères, sans import).
À lancer dans un terminal moderne (Windows Terminal, VS Code) pour un bon rendu.

### 2. Version graphique classique — BONUS

```
python jouer_gui.py
```

Ouvre une fenêtre avec une zone de texte scrollable et des boutons cliquables
pour les choix. Utilise `tkinter` (hors bibliothèques autorisées) — bonus uniquement.

### 3. Version graphique RPG — BONUS

```
python jouer_gui_rpg.py
```

Interface style jeu de rôle : grande image en haut qui change à chaque scène,
boîte de dialogue en bas avec effet machine à écrire. Même principe technique
que la version 2 — `print` et `input` redirigés vers la fenêtre.

## Structure du projet

```
poudelard/
├── main.py            # point d'entrée — version terminal
├── jouer_gui.py       # point d'entrée — version graphique (bonus tkinter)
├── menu.py
├── univers/
│   ├── __init__.py
│   ├── personnage.py
│   └── maison.py
├── chapitres/
│   ├── __init__.py
│   ├── chapitre_1.py
│   ├── chapitre_2.py
│   ├── chapitre_3.py
│   ├── chapitre_4.py
│   └── chapitre_5_extension.py
├── utils/
│   ├── __init__.py
│   ├── input_utils.py
│   └── couleurs.py    # palette ANSI partagée (constantes, sans import)
├── data/
│   ├── inventaire.json
│   ├── maisons.json
│   ├── sorts.json
│   ├── quiz_magie.json
│   └── equipes_quidditch.json
└── README.md
```
