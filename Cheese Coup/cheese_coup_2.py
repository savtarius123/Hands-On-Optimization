import pulp as pl


def cheese_coup(cheese, cuttable, pieces, weight, value, capacity):
    """
    Parameters:
    - cheese: list of cheese types
    - cuttable: list of cheese types which are cuttable
    - pieces[cheese]: number of pieces von Due can steal
    - weight[cheese]
    - value[cheese]
    - capacity: capacity of von Due's knapsack
    """

    noncuttable = list(set(cheese) - set(cuttable))

    # variable definitions
    X = pl.LpVariable.dicts("x", cuttable, lowBound=0)
    Y = pl.LpVariable.dicts("x", noncuttable, lowBound=0, cat=pl.LpInteger)

    # problem definition and objective function
    prob = pl.LpProblem("cheese_coup_2", pl.LpMaximize)
    prob += pl.lpSum(X[c] * value[c] for c in cuttable) + pl.lpSum(
        Y[c] * value[c] for c in noncuttable
    )

    # constraints
    prob += (
        pl.lpSum(X[c] * weight[c] for c in cuttable)
        + pl.lpSum(Y[c] * weight[c] for c in noncuttable)
        <= capacity
    )
    for c in cuttable:
        prob += X[c] <= pieces[c]
    for c in noncuttable:
        prob += Y[c] <= pieces[c]

    # call the solver
    status = prob.solve()

    # print solution
    print(pl.LpStatus[status])
    for x in X.values():
        print(f"Steal {pl.value(x)} of cheese {x}")
    for x in Y.values():
        print(f"Steal {pl.value(x)} of cheese {x}")


cheese = ["Brie", "Camembert", "Reblochon", "Handkaese", "Roquefort"]
cuttable = ["Brie", "Camembert", "Reblochon"]
pieces = [1, 1, 1, 30, 1]
weight = [15, 9, 10, 0.4, 10]
value = [1800, 1200, 1300, 50, 2200]
capacity = 30

cheese_coup(
    cheese,
    cuttable,
    dict(zip(cheese, pieces)),
    dict(zip(cheese, weight)),
    dict(zip(cheese, value)),
    capacity,
)

# 4824
# Steal 0.013333333 of cheese x_Brie
# Steal 1.0 of cheese x_Camembert
# Steal 1.0 of cheese x_Reblochon
# Steal 2.0 of cheese x_Handkaese
# Steal 1.0 of cheese x_Roquefort