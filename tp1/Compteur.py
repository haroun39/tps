# ===========================================
# Implémentation des algorithmes de recherche
# ===========================================

# Classe pour compter le nombre de comparaisons
class Compteur:
    def __init__(self):
        self.comparaisons = 0
    def inc(self):
        self.comparaisons += 1


# 1️⃣ Recherche séquentielle simple
def recherche_seq_simple(tab, x, compteur):
    for i, val in enumerate(tab):
        compteur.inc()
        if val == x:
            return i
    return -1


# 2️⃣ Recherche séquentielle optimisée
# (on s'arrête dès que la valeur courante dépasse x)
def recherche_seq_optimisee(tab, x, compteur):
    for i, val in enumerate(tab):
        compteur.inc()
        if val == x:
            return i
        if val > x:
            return -1
    return -1


# 3️⃣ Recherche binaire (itérative)
def recherche_binaire_iterative(tab, x, compteur):
    gauche = 0
    droite = len(tab) - 1
    while gauche <= droite:
        milieu = (gauche + droite) // 2
        compteur.inc()
        if tab[milieu] == x:
            return milieu
        elif tab[milieu] < x:
            gauche = milieu + 1
        else:
            droite = milieu - 1
    return -1


# 4️⃣ Recherche binaire (récursive)
def recherche_binaire_recursive(tab, x, gauche, droite, compteur):
    if gauche > droite:
        return -1
    milieu = (gauche + droite) // 2
    compteur.inc()
    if tab[milieu] == x:
        return milieu
    elif tab[milieu] < x:
        return recherche_binaire_recursive(tab, x, milieu + 1, droite, compteur)
    else:
        return recherche_binaire_recursive(tab, x, gauche, milieu - 1, compteur)
