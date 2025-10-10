import numpy as np
import time
import pandas as pd
import matplotlib.pyplot as plt

# ==========================
# 1️⃣ Classe compteur
# ==========================
class Compteur:
    def __init__(self):
        self.comparaisons = 0
    def inc(self):
        self.comparaisons += 1


# ==========================
# 2️⃣ Fonctions de recherche
# ==========================

# Recherche séquentielle simple
def recherche_seq_simple(tab, x, compteur):
    for i, val in enumerate(tab):
        compteur.inc()
        if val == x:
            return i
    return -1


# Recherche séquentielle optimisée (arrêt si val > x)
def recherche_seq_optimisee(tab, x, compteur):
    for i, val in enumerate(tab):
        compteur.inc()
        if val == x:
            return i
        if val > x:
            return -1
    return -1


# Recherche binaire itérative
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


# Recherche binaire récursive
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


# ==========================
# 3️⃣ Expérimentation
# ==========================

def test_algorithmes():
    tailles = [10**4, 10**5, 10**6]   # أحجام الجداول
    essais = 30                       # عدد التكرارات
    resultats = []
    rng = np.random.default_rng(42)

    algorithmes = {
        "Séquentielle simple": recherche_seq_simple,
        "Séquentielle optimisée": recherche_seq_optimisee,
        "Binaire itérative": recherche_binaire_iterative,
        "Binaire récursive": lambda t, x, c: recherche_binaire_recursive(t, x, 0, len(t)-1, c)
    }

    for n in tailles:
        print(f"\n=== Taille du tableau : {n} ===")
        tab = np.sort(rng.integers(0, 10**6, n))
        for nom, algo in algorithmes.items():
            comparaisons, temps = [], []
            for _ in range(essais):
                # 50% احتمال أن القيمة موجودة
                if rng.random() < 0.5:
                    x = tab[rng.integers(0, n)]
                else:
                    x = rng.integers(-10**6, 2*10**6)
                c = Compteur()
                debut = time.perf_counter()
                algo(tab, x, c)
                fin = time.perf_counter()
                comparaisons.append(c.comparaisons)
                temps.append(fin - debut)

            resultats.append({
                "Algorithme": nom,
                "Taille": n,
                "Comparaisons_moy": np.mean(comparaisons),
                "Temps_moy (s)": np.mean(temps)
            })
            print(f"{nom:<25} | Comp. moy: {np.mean(comparaisons):8.2f} | Temps moy: {np.mean(temps):.6f}s")

    df = pd.DataFrame(resultats)
    return df


# ==========================
# 4️⃣ Exécution et affichage
# ==========================
df = test_algorithmes()

# Affichage du tableau de résultats
print("\n=== Résumé des résultats ===")
print(df)

# ==========================
# 5️⃣ Graphiques comparatifs
# ==========================
plt.figure(figsize=(10,5))
for alg in df["Algorithme"].unique():
    sous_df = df[df["Algorithme"] == alg]
    plt.plot(sous_df["Taille"], sous_df["Comparaisons_moy"], marker='o', label=alg)
plt.xlabel("Taille du tableau")
plt.ylabel("Comparaisons moyennes")
plt.title("Comparaison du nombre de comparaisons")
plt.legend()
plt.grid()
plt.show()

plt.figure(figsize=(10,5))
for alg in df["Algorithme"].unique():
    sous_df = df[df["Algorithme"] == alg]
    plt.plot(sous_df["Taille"], sous_df["Temps_moy (s)"], marker='o', label=alg)
plt.xlabel("Taille du tableau")
plt.ylabel("Temps moyen (s)")
plt.title("Comparaison du temps d’exécution")
plt.legend()
plt.grid()
plt.show()
