from pulp import *


def solv(K, n, bLa, bLb, bLs, bCa, bCb, bCs):
    prob = LpProblem("KakuroSolv", LpMinimize)

    x = LpVariable.dicts("x", (range(int(n)), (range(n)), (range(1, 10))), cat="Binary")

    # prob += (lpSum([x[for i in range(0,n), for j in range (0,n),for u in range (1, 10)]]))

    # contraintes

    # contr_1
    for i in range(n):
        for j in range(n):
            prob += lpSum([x[i][j][u] for u in range(1, 10)]) == 1

    # ctr0
    for i in range(n):
        for k in range(K):
            for j in range(bLa[i][k], bLb[i][k] + 1):
                if bLs[i][k] != 0:
                    prob += lpSum([x[i][j][u] for u in range(1, 10)]) * bLs[i][k] >= bLs[i][k]

    # ctr1
    for i in range(n):
        for k in range(K):
            if bLs[i][k] != 0:
                prob += lpSum([x[i][j][u] * u for u in range(1, 10) for j in range(bLa[i][k], bLb[i][k]+1)]) == bLs[i][k]

    # ctr2
    for i in range(n):
        for k in range(K):
            for u in range(1, 10):
                if bLs[i][k] != 0 :
                    prob += lpSum([x[i][j][u] for j in range(bLa[i][k], bLb[i][k]+1)]) <= 1

    # ctr3
    for j in range(n):
        for k in range(K):
            if bCs[j][k] != 0:
                prob += lpSum([x[i][j][u] * u for u in range(1, 10) for i in range(bCa[j][k], bCb[j][k]+1)]) == bCs[j][k]

    # ctr4
    for j in range(n):
        for k in range(K):
            for u in range(1, 10):
                if bCs[j][k] != 0:
                    prob += lpSum([x[i][j][u] for i in range(bCa[j][k], bCb[j][k]+1)]) <= 1

    # The problem data is written to an .lp file
    prob.writeLP("Sudoku.lp")

    # The problem is solved using PuLP's choice of Solver
    prob.solve()

    # The status of the solution is printed to the screen
    print("Status:", LpStatus[prob.status])

    for i in range(1, n):
        for j in range(1, n):
            for u in range(1, 10):
                if value(x[i][j][u]) == 1:
                    print(i, j, u)
