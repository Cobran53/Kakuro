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

#contr_1
for i in range(n) :
    for j in range (n) :
        prob += lpSum([x[i][j][u] for u in range(10)]) == 1

#ctr0
for i in range (n) :
    for k in range (K):
        for j in range (bLa[i,k], bLb[i,k]+1):
            prob += lpSum([x[i][j][u] for u in range(10)])*bLs[i,k] >= bLs[i,k]

constraint_2 = LpConstraint()
constraint_3 = LpConstraint()
constraint_4 = Lpconstraint()

#solve


