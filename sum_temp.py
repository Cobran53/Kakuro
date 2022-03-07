# -*- coding: cp1252 -*-
# décomposer n
from copy import deepcopy

n = 46

solutions = []  # contiendra l'ensemble des solutions
for i in range(0, n + 1):
    solutions.append([])  # liste vide partout pour commencer

solutions[0] = []  # pour le total 0
solutions[1] = [[1]]  # pour le total 1


# la récurrence est amorcée, car on a toutes les décompositions pour 1
# on va pouvoir y aller

def decomposition_partielle(k):
    # construit les solutions pour k+1 à partir de celles pour k
    print(k)  # pour voir la progression
    sol_precedentes = deepcopy(solutions[k])  # récupérer les solutions précédentes
    sol_nouvelles = []  # pour recevoir les nouvelles solutions
    for i in range(0, len(sol_precedentes)):
        sol_avant = sol_precedentes[i]
        for j in range(0, len(sol_avant)):  # récupérer les solutions une par une
            sol_actuelle = deepcopy(sol_avant)
            sol_actuelle[j] = sol_actuelle[j] + 1  # ajout d'une unité
            if (j > 0) and sol_actuelle[j - 1] < sol_actuelle[j]:  # on conserve l'ordre décroissant
                break
            else:
                if sol_actuelle not in sol_nouvelles:  # s'il s'agit d'une nouvelle possibilité
                    sol_nouvelles.append(sol_actuelle)  # l'ajouter à celles trouvées précédemment
    sol_nouvelles.append([1] * (k + 1))  # pour finir rien que des 1
    solutions[k + 1] = sol_nouvelles  # mise à jour en vue du traitement suivant
    return


def decomposition_totale():
    # itération de la fonction précédente
    global n
    for k in range(1, n):
        decomposition_partielle(k)
    return


def corrections_kakuro():
    """
    On retire les résultats qui ne servent pas pour le kakuro, c'est-à-dire ceux avec une répétition,
    et ceux où on utilise pas que des chiffres.
    """
    global solutions
    solutions_corrigees = []  # contiendra les solutions après correction
    for nombre in range(n):
        solutions_corrigees.append([])  # contient les solutions corrigés pour le nombre actuel
        for sol in solutions[nombre]:
            if len(sol) <= 1:  # s'il n'y a qu'une solution ou 0
                continue  # on arrete
            if sol[0] > 9:  # on vérifie si c'est bien un chiffre
                continue  # si c'est pas le cas on arrête, sinon on c'est que ils sont tous entre 1 et 9 car c'est
                # décroissant
            else:
                for chiffre in range(len(sol) - 1):
                    if sol[chiffre] == sol[chiffre + 1]:  # pas deux fois le même chiffre
                        break
                else:  # for-else : si il n'y a pas eu de break, alors :
                    solutions_corrigees[nombre].append(sol)  # la sol est valide et on l'ajoute
    solutions = deepcopy(solutions_corrigees)


def sauvegarder_dans_fichier():
    # sauvegarde dans le fichier decompo.csv
    global n
    f = open("decompo.csv", 'w')
    for nombre in range(n):
        f.write(str(nombre) + ": ")
        for i in range(0, len(solutions[nombre])):
            ligne = solutions[nombre][i]  # on prend toutes les solutions pour le nombre
            for j in range(0, len(ligne) - 1):
                f.write(str(ligne[j]) + ",")
            f.write(str(ligne[len(ligne) - 1]) + ";")  # on met un ; pour le dernier
            f.write("\n")
        f.write("\n")  # On laisse une ligne vide quand on change de nombre
    f.close()
    return


decomposition_totale()
corrections_kakuro()
sauvegarder_dans_fichier()
