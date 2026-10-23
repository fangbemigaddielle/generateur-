

import tkinter as tk
from tkinter import ttk
import secrets
import string
import re

# =========================
# CONFIGURATION
# =========================

BG = "#101827"
PANEL = "#1C293B"
GREEN = "#56D6A0"
WHITE = "#F3F6FC"
MUTED = "#AAB7C8"

# =========================
# FONCTIONS
# =========================

def generer():
    try:
        longueur = int(longueur_var.get())
        if not 8 <= longueur <= 128:
            raise ValueError
    except ValueError:
        statut.set("Choisis une longueur entre 8 et 128.")
        return

    groupes = []

    if maj.get():
        groupes.append(string.ascii_uppercase)
    if minusc.get():
        groupes.append(string.ascii_lowercase)
    if chiffres.get():
        groupes.append(string.digits)
    if symboles.get():
        groupes.append("!@#$%&*?-_+")

    if not groupes:
        statut.set("Coche au moins un type de caractère.")
        return

    if longueur < len(groupes):
        statut.set("Longueur trop courte pour ces options.")
        return

    alphabet = "".join(groupes)

    mot = [secrets.choice(groupe) for groupe in groupes]
    mot += [
        secrets.choice(alphabet)
        for _ in range(longueur - len(mot))
    ]

    secrets.SystemRandom().shuffle(mot)
    mot = "".join(mot)

    resultat.set(mot)
    statut.set("Mot de passe généré avec succès.")

    # Afficher aussi son niveau de robustesse
    analyser(mot)


def analyser(mot=None):
    """Vérifie un mot de passe et actualise l'interface."""

    if mot is None:
        mot = saisie.get()

    if not mot or not mot.strip():
        niveau.set("Robustesse : en attente")
        conseil.set("Saisis un mot de passe, puis clique sur Vérifier.")
        barre["value"] = 0
        barre.configure(style="Weak.Horizontal.TProgressbar")
        return

    score = 0

    # Longueur
    if len(mot) >= 12:
        score += 1
    if len(mot) >= 16:
        score += 1

    # Diversité des caractères
    if re.search(r"[a-z]", mot):
        score += 1
    if re.search(r"[A-Z]", mot):
        score += 1
    if re.search(r"\d", mot):
        score += 1
    if re.search(r"[^a-zA-Z0-9]", mot):
        score += 1

    mots_communs = {
        "password", "motdepasse", "12345678",
        "azerty", "qwerty", "admin"
    }

    # Résultats pédagogiques, pas une garantie de sécurité
    if len(mot) < 8 or mot.lower() in mots_communs:
        score = min(score, 1)

    pourcentage = score / 6 * 100
    barre["value"] = pourcentage

    if score <= 2:
        niveau.set("Robustesse : FAIBLE")
        barre.configure(style="Weak.Horizontal.TProgressbar")
        conseil.set(
            "Conseil : utilise au moins 12 à 16 caractères "
            "et varie les types de caractères."
        )

    elif score <= 4:
        niveau.set("Robustesse : MOYENNE")
        barre.configure(style="Medium.Horizontal.TProgressbar")
        conseil.set(
            "Conseil : allonge le mot de passe et évite "
            "les suites prévisibles ou les informations personnelles."
        )

    else:
        niveau.set("Robustesse : FORTE")
        barre.configure(style="Strong.Horizontal.TProgressbar")
        conseil.set(
            "Bonne diversité ! Utilise un mot de passe unique "
            "pour chaque compte."
        )


def copier():
    mot = resultat.get()

    if not mot:
        statut.set("Génère d'abord un mot de passe.")
        return

    fenetre.clipboard_clear()
    fenetre.clipboard_append(mot)
    fenetre.update()
    statut.set("Mot de passe copié !")


def basculer_affichage():
    entree.config(show="" if visible.get() else "*")


def vider_verificateur():
    saisie.set("")
    niveau.set("Robustesse : en attente")
    conseil.set("Saisis un mot de passe, puis clique sur Vérifier.")
    barre["value"] = 0
    barre.configure(style="Weak.Horizontal.TProgressbar")


# =========================
# FENÊTRE PRINCIPALE
# =========================

fenetre = tk.Tk()
fenetre.title("PasswordSecure")
fenetre.geometry("560x790")
fenetre.minsize(520, 740)
fenetre.configure(bg=BG)

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "TCheckbutton",
    background=PANEL,
    foreground=WHITE,
    font=("Segoe UI", 10)
)

style.configure(
    "Weak.Horizontal.TProgressbar",
    troughcolor=BG,
    background="#FF5C69",
    thickness=14
)

style.configure(
    "Medium.Horizontal.TProgressbar",
    troughcolor=BG,
    background="#FFC857",
    thickness=14
)

style.configure(
    "Strong.Horizontal.TProgressbar",
    troughcolor=BG,
    background=GREEN,
    thickness=14
)

# =========================
# TITRE
# =========================

tk.Label(
    fenetre,
    text="PASSWORD SECURE",
    bg=BG,
    fg=GREEN,
    font=("Segoe UI", 23, "bold")
).pack(pady=(18, 3))

tk.Label(
    fenetre,
    text="Génère et vérifie tes mots de passe",
    bg=BG,
    fg=MUTED,
    font=("Segoe UI", 10)
).pack(pady=(0, 12))

# =========================
# GÉNÉRATEUR
# =========================

generation = tk.Frame(
    fenetre, bg=PANEL, padx=18, pady=12
)
generation.pack(fill="x", padx=22, pady=6)

tk.Label(
    generation,
    text="1. GÉNÉRATEUR",
    bg=PANEL,
    fg=GREEN,
    font=("Segoe UI", 12, "bold")
).pack(anchor="w")

ligne = tk.Frame(generation, bg=PANEL)
ligne.pack(fill="x", pady=8)

tk.Label(
    ligne,
    text="Longueur (8 à 128) :",
    bg=PANEL,
    fg=WHITE
).pack(side="left")

longueur_var = tk.StringVar(value="20")

tk.Spinbox(
    ligne,
    from_=8,
    to=128,
    textvariable=longueur_var,
    width=6,
    font=("Segoe UI", 11)
).pack(side="right")

maj = tk.BooleanVar(value=True)
minusc = tk.BooleanVar(value=True)
chiffres = tk.BooleanVar(value=True)
symboles = tk.BooleanVar(value=True)

for texte, variable in [
    ("Majuscules A-Z", maj),
    ("Minuscules a-z", minusc),
    ("Chiffres 0-9", chiffres),
    ("Symboles spéciaux", symboles)
]:
    ttk.Checkbutton(
        generation,
        text=texte,
        variable=variable
    ).pack(anchor="w", pady=1)

resultat = tk.StringVar()

tk.Entry(
    generation,
    textvariable=resultat,
    font=("Consolas", 12),
    justify="center",
    bg=WHITE,
    fg=BG
).pack(fill="x", pady=(10, 7), ipady=5)

tk.Button(
    generation,
    text="Générer un mot de passe",
    command=generer,
    bg=GREEN,
    fg=BG,
    font=("Segoe UI", 11, "bold"),
    relief="flat",
    pady=8,
    cursor="hand2"
).pack(fill="x")

tk.Button(
    generation,
    text="Copier le mot de passe",
    command=copier,
    bg="#30425A",
    fg=WHITE,
    font=("Segoe UI", 10),
    relief="flat",
    pady=6,
    cursor="hand2"
).pack(fill="x", pady=(6, 0))

# =========================
# VÉRIFICATEUR
# =========================

verification = tk.Frame(
    fenetre, bg=PANEL, padx=18, pady=12
)
verification.pack(fill="x", padx=22, pady=8)

tk.Label(
    verification,
    text="2. VÉRIFICATEUR DE ROBUSTESSE",
    bg=PANEL,
    fg=GREEN,
    font=("Segoe UI", 12, "bold")
).pack(anchor="w")

saisie = tk.StringVar()
visible = tk.BooleanVar(value=False)

entree = tk.Entry(
    verification,
    textvariable=saisie,
    show="*",
    font=("Segoe UI", 12),
    bg=WHITE,
    fg=BG
)
entree.pack(fill="x", pady=9, ipady=5)

tk.Checkbutton(
    verification,
    text="Afficher le mot de passe",
    variable=visible,
    command=basculer_affichage,
    bg=PANEL,
    fg=WHITE,
    selectcolor=BG,
    activebackground=PANEL,
    activeforeground=WHITE
).pack(anchor="w")

boutons = tk.Frame(verification, bg=PANEL)
boutons.pack(fill="x", pady=8)

tk.Button(
    boutons,
    text="Vérifier",
    command=analyser,
    bg=GREEN,
    fg=BG,
    font=("Segoe UI", 10, "bold"),
    relief="flat",
    pady=7,
    cursor="hand2"
).pack(side="left", fill="x", expand=True, padx=(0, 4))

tk.Button(
    boutons,
    text="Effacer",
    command=vider_verificateur,
    bg="#30425A",
    fg=WHITE,
    font=("Segoe UI", 10),
    relief="flat",
    pady=7,
    cursor="hand2"
).pack(side="left", fill="x", expand=True, padx=(4, 0))

niveau = tk.StringVar(value="Robustesse : en attente")

tk.Label(
    verification,
    textvariable=niveau,
    bg=PANEL,
    fg=WHITE,
    font=("Segoe UI", 12, "bold")
).pack(anchor="w", pady=(5, 7))

barre = ttk.Progressbar(
    verification,
    maximum=100,
    value=0,
    style="Weak.Horizontal.TProgressbar"
)
barre.pack(fill="x")

conseil = tk.StringVar(
    value="Saisis un mot de passe, puis clique sur Vérifier."
)

tk.Label(
    verification,
    textvariable=conseil,
    bg=PANEL,
    fg=MUTED,
    font=("Segoe UI", 9),
    wraplength=450,
    justify="left"
).pack(anchor="w", pady=(8, 0))

# =========================
# MESSAGE EN BAS
# =========================

statut = tk.StringVar(value="Application prête.")

tk.Label(
    fenetre,
    textvariable=statut,
    bg=BG,
    fg=GREEN,
    font=("Segoe UI", 9),
    wraplength=480
).pack(pady=7)

tk.Label(
    fenetre,
    text="Conseil : un mot de passe différent pour chaque compte.",
    bg=BG,
    fg=MUTED,
    font=("Segoe UI", 9)
).pack(pady=(0, 10))

# =========================
# LANCEMENT
# =========================

fenetre.mainloop()
