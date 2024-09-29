# Several (I)LP models for graph coloring on complete graphs
import pulp as pl

def graph_coloring1(n):
    nodes = list(range(n))
    colors = list(range(n))

    # variable definitions
    X = pl.LpVariable.dicts("x", (nodes, colors), cat=pl.LpBinary)
    Y = pl.LpVariable.dicts("y", colors, cat=pl.LpBinary)

    # problem definition and objective function
    prob = pl.LpProblem("graph_coloring", pl.LpMinimize)
    prob += pl.lpSum(Y[c] for c in colors)

    # constraints
    for i in nodes:
        prob += pl.lpSum(X[i][c] for c in colors) == 1

        for c in colors:
            prob += X[i][c] <= Y[c]

    for c in colors:
        for i in nodes:
            for j in nodes: 
                if i != j:
                    prob += X[i][c] + X[j][c] <= 1

    #solver = pl.CPLEX_CMD()
    #solver = pl.GLPK()
    #prob.solve(solver)
    
    prob.solve()


# Alternative (I)LP model
def graph_coloring2(n):
    nodes = list(range(n))

    N = 2 * n
    X = pl.LpVariable.dicts("x", nodes, cat=pl.LpInteger, lowBound= 1,upBound= n)
    Y = pl.LpVariable.dicts("y", (nodes,nodes), cat=pl.LpBinary)
    Z = pl.LpVariable("z",lowBound=0) 

    prob = pl.LpProblem("graph_coloring", pl.LpMinimize)
    prob += Z
    
    for i in nodes:
        for j in nodes:
            if i != j:
                prob += (X[i] - X[j]) + Y[i][j] * N >= 1
                prob += -(X[i] - X[j]) + (1-Y[i][j]) * N >= 1



    for i in nodes:
        prob += X[i] <= Z    

    #solver = pl.CPLEX_CMD()
    #solver = pl.GLPK()
    #prob.solve(solver)
    
    prob.solve()


# The same as the second model but without variable upper limits
def graph_coloring3(n):
    nodes = list(range(n))

    N = 2 * n
    X = pl.LpVariable.dicts("x", nodes, cat=pl.LpInteger, lowBound= 1)
    Y = pl.LpVariable.dicts("y", (nodes,nodes), cat=pl.LpBinary)
    Z = pl.LpVariable("z",lowBound=0) 

    prob = pl.LpProblem("graph_coloring", pl.LpMinimize)
    prob += Z
    
    for i in nodes:
        for j in nodes:
            if i != j:
                prob += (X[i] - X[j]) + Y[i][j] * N >= 1
                prob += -(X[i] - X[j]) + (1-Y[i][j]) * N >= 1



    for i in nodes:
        prob += X[i] <= Z    

    #solver = pl.CPLEX_CMD()
    #solver = pl.GLPK()
    #prob.solve(solver)

    prob.solve()







graph_coloring1(8)
#graph_coloring2(8)   
#graph_coloring3(8)
