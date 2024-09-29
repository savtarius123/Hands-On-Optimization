import pulp as pl


def cheese_coup(cheese, pieces, weight, value, capacity):
    """
    Parameters:
    - cheese: list of cheese types
    - pieces[cheese]: number of pieces von Due can steal
    - weight[cheese]
    - value[cheese]
    - capacity: capacity of von Due's knapsack
    """

    # variable definitions
    X = pl.LpVariable.dicts("x", cheese, lowBound=0)

    # problem definition and objective function
    prob = pl.LpProblem("cheese_coup_1", pl.LpMaximize)
    prob += pl.lpSum(X[c] * value[c] for c in cheese)

    # constraints
    prob += pl.lpSum(X[c] * weight[c] for c in cheese) <= capacity
    for c in cheese:
        prob += X[c] <= pieces[c]

    # call the solver
    status = prob.solve()

    # print solution
    print(pl.LpStatus[status])
    for x in X.values():
        print(f"Steal {pl.value(x)} of cheese {x}")


cheese = ["Brie", "Camembert", "Reblochon"]
pieces = [1, 1, 1]
weight = [15, 9, 10]
value = [1800, 1200, 1300]
capacity = 30

cheese_coup(
    cheese,
    dict(zip(cheese, pieces)),
    dict(zip(cheese, weight)),
    dict(zip(cheese, value)),
    capacity,
)

# Objective value 3820
# Steal 0.73333333 of cheese x_Brie
# Steal 1.0 of cheese x_Camembert
# Steal 1.0 of cheese x_Reblochon
