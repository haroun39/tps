# Exemple d'utilisation
import numpy as np
import time
from Compteur import Compteur, recherche_binaire_recursive, recherche_seq_optimisee, recherche_seq_simple, recherche_binaire_iterative
# Génération d’un tableau trié
tab = np.sort(np.random.randint(0, 100, 20))
x = 42  # valeur à rechercher
print("Tableau :", tab)

# Création du compteur
c = Compteur()

# Exemple 1 : Recherche séquentielle simple
start_time = time.time()
pos = recherche_seq_simple(tab, x, c)
end_time = time.time()
execution_time = (end_time - start_time) * 1000  # en millisecondes
print("Résultat (séquentielle simple):", pos, "| Comparaisons:", c.comparaisons, "| Temps:", f"{execution_time:.6f} ms")

# Exemple 2 : Recherche binaire itérative
c = Compteur()
start_time = time.time()
pos = recherche_binaire_iterative(tab, x, c)
end_time = time.time()
execution_time = (end_time - start_time) * 1000  # en millisecondes
print("Résultat (binaire itérative):", pos, "| Comparaisons:", c.comparaisons, "| Temps:", f"{execution_time:.6f} ms")

# Exemple 3 : Recherche binaire récursive
c = Compteur()
start_time = time.time()
pos = recherche_binaire_recursive(tab, x, 0, len(tab) - 1, c)
end_time = time.time()
execution_time = (end_time - start_time) * 1000  # en millisecondes
print("Résultat (binaire récursive):", pos, "| Comparaisons:", c.comparaisons, "| Temps:", f"{execution_time:.6f} ms")

# Exemple 4 : Recherche séquentielle optimisée
c = Compteur()
start_time = time.time()
pos = recherche_seq_optimisee(tab, x, c)
end_time = time.time()
execution_time = (end_time - start_time) * 1000  # en millisecondes
print("Résultat (séquentielle optimisée):", pos, "| Comparaisons:", c.comparaisons, "| Temps:", f"{execution_time:.6f} ms")

