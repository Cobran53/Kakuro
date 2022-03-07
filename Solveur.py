from pulp import *

prob = LpProblem("KakuroSolv", LpMinimize)

# variables
# nb max de sommes par lignes et colonnes
K = LpVariable(3)
# nb case max par ligne et colonnes
n = LpVariable(9)

bLa = LpVariable(("i", 1, n, "Integer"), ("k", 1, K, "Integer"))
bLb = LpVariable(("i", 1, n, "Integer"), ("k", 1, K, "Integer"))
bLs = LpVariable(("i", 1, n, "Integer"), ("k", 1, K, "Integer"))
bCa = LpVariable(("j", 1, n, "Integer"), ("k", 1, K, "Integer"))
bCb = LpVariable(("j", 1, n, "Integer"), ("k", 1, K, "Integer"))
bCs = LpVariable(("j", 1, n, "Integer"), ("k", 1, K, "Integer"))

x = LpVariable.dicts("x",(("i" in range (1,n)), ("j" in range(1,n)), ("u" in range(1,9)) , "Binary"))

prob += LpMinimize(Sum([x]))

#contraintes
for "i" in range(1,n) :
    for "j" in range (1,n) :
        prob += lpSum([x[i,j,u] for ])


constraint_2 = LpConstraint()
constraint_3 = LpConstraint()
constraint_4 = Lpconstraint()

#solve


