from pulp import *

prob = LpProblem("KakuroSolv", LpMinimize)

# variables
# nb max de sommes par lignes et colonnes
K = 3
# nb case max par ligne et colonnes
n = 10

bLa = ("i", 0, n, "Integer"), ("k", 0, K, "Integer")
bLb = ("i", 0, n, "Integer"), ("k", 0, K, "Integer")
bLs = ("i", 0, n, "Integer"), ("k", 0, K, "Integer")
bCa = ("j", 0, n, "Integer"), ("k", 0, K, "Integer")
bCb = ("j", 0, n, "Integer"), ("k", 0, K, "Integer")
bCs = ("j", 0, n, "Integer"), ("k", 0, K, "Integer")

x = LpVariable.dicts("x", ((range(int(n))), (range(n)), (range(10)), 'Binary'))

# prob += (lpSum([x[for i in range(0,n), for j in range (0,n),for u in range (0,9)]]))

# contraintes

# contr_1
for i in range(n):
    for j in range(n):
        prob += lpSum([x[i][j][u] for u in range(10)]) == 1

# ctr0
for i in range(n):
    for k in range(K):
        for j in range(bLa[i][k], bLb[i][k] + 1):
            prob += lpSum([x[i][j][u] for u in range(10)]) * bLs[i][k] >= bLs[i][k]

# ctr1
for i in range(n):
    for k in range(K):
        prob += lpSum([x[i][j][u]*u for u in range(10) for j in range(bLa[i][k], bLb[i][k])]) == bLs[i][k]

# ctr2
for i in range(n):
    for k in range(K):
        for u in range(10):
            prob += lpSum([x[i][j][u] for j in range(bLa[i][k], bLb[i][k])]) <= 1

# ctr3
for j in range(n):
    for k in range(K):
        prob += lpSum([x[i][j][u]*u for u in range(10) for i in range(bCa[j][k], bCb[j][k])]) == bCs[j][k]

# ctr4
for j in range(n):
    for k in range(K):
        for u in range(10):
            prob += lpSum([x[i][j][u] for i in range(bCa[i][k], bCb[i][k])]) <= 1

# solve
prob.solve()
