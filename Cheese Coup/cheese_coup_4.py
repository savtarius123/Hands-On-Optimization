import pulp as pl


def cheese_coup(cheese, cuttable, pieces, weight, value, small_capacity, k):
    """
    Parameters:
    - cheese: list of cheese types
    - cuttable: list of cheese types which are cuttable
    - pieces[cheese]: number of pieces von Due can steal
    - weight[cheese]
    - value[cheese]
    - small_capacity: capacity of one pouch
    - k: number of pouches
    """

    total_attainable = first_model(
        cheese, cuttable, pieces, weight, value, small_capacity, k
    )
    print(total_attainable)
    minimal_unevenness = second_model(
        cheese, cuttable, pieces, weight, value, small_capacity, k, total_attainable
    )
    print(minimal_unevenness)
    third_model(
        cheese, cuttable, pieces, weight, value, small_capacity, k, minimal_unevenness
    )


def first_model(cheese, cuttable, pieces, weight, value, small_capacity, k):
    noncuttable = list(set(cheese) - set(cuttable))
    pouch = list(range(k))

    X = pl.LpVariable.dicts("x", (cuttable, pouch), lowBound=0)
    Y = pl.LpVariable.dicts("x", (noncuttable, pouch), lowBound=0, cat=pl.LpInteger)

    prob = pl.LpProblem("cheese_coup_4a", pl.LpMaximize)
    prob += pl.lpSum(X[c][p] * value[c] for c in cuttable for p in pouch) + pl.lpSum(
        Y[c][p] * value[c] for c in noncuttable for p in pouch
    )

    for p in pouch:
        prob += (
            pl.lpSum(X[c][p] * weight[c] for c in cuttable)
            + pl.lpSum(Y[c][p] * weight[c] for c in noncuttable)
            <= small_capacity
        )
    for c in cuttable:
        prob += pl.lpSum(X[c][p] for p in pouch) <= pieces[c]
    for c in noncuttable:
        prob += pl.lpSum(Y[c][p] for p in pouch) <= pieces[c]

    # call the solver
    status = prob.solve()

    return prob.objective.value()


def second_model(
    cheese, cuttable, pieces, weight, value, small_capacity, k, total_attainable
):
    noncuttable = list(set(cheese) - set(cuttable))
    pouch = list(range(k))

    X = pl.LpVariable.dicts("x", (cuttable, pouch), lowBound=0)
    Y = pl.LpVariable.dicts("x", (noncuttable, pouch), lowBound=0, cat=pl.LpInteger)
    uplus = pl.LpVariable.dicts("plus", pouch, lowBound=0)
    uminus = pl.LpVariable.dicts("minus", pouch, lowBound=0)

    prob = pl.LpProblem("cheese_coup_4b", pl.LpMinimize)
    prob += pl.lpSum(uplus[p] + uminus[p] for p in pouch)

    for p in pouch:
        prob += (
            pl.lpSum(X[c][p] * weight[c] for c in cuttable)
            + pl.lpSum(Y[c][p] * weight[c] for c in noncuttable)
            <= small_capacity
        )
    for c in cuttable:
        prob += pl.lpSum(X[c][p] for p in pouch) <= pieces[c]
    for c in noncuttable:
        prob += pl.lpSum(Y[c][p] for p in pouch) <= pieces[c]

    prob += (
        pl.lpSum(X[c][p] * value[c] for c in cuttable for p in pouch)
        + pl.lpSum(Y[c][p] * value[c] for c in noncuttable for p in pouch)
        >= 0.9 * total_attainable
    )

    for p in pouch:
        prob += uplus[p] - uminus[p] == pl.lpSum(
            X[c][p] * weight[c] for c in cuttable
        ) + pl.lpSum(Y[c][p] * weight[c] for c in noncuttable) - pl.lpSum(
            X[c][q] * weight[c] / k for c in cuttable for q in pouch
        ) - pl.lpSum(
            Y[c][q] * weight[c] / k for c in noncuttable for q in pouch
        )

    # call the solver
    status = prob.solve()

    return prob.objective.value()


def third_model(
    cheese, cuttable, pieces, weight, value, small_capacity, k, minimal_unevenness
):
    noncuttable = list(set(cheese) - set(cuttable))
    pouch = list(range(k))

    X = pl.LpVariable.dicts("x", (cuttable, pouch), lowBound=0)
    Y = pl.LpVariable.dicts("x", (noncuttable, pouch), lowBound=0, cat=pl.LpInteger)
    uplus = pl.LpVariable.dicts("plus", pouch, lowBound=0)
    uminus = pl.LpVariable.dicts("minus", pouch, lowBound=0)

    prob = pl.LpProblem("cheese_coup_4c", pl.LpMaximize)
    prob += pl.lpSum(X[c][p] * value[c] for c in cuttable for p in pouch) + pl.lpSum(
        Y[c][p] * value[c] for c in noncuttable for p in pouch
    )

    for p in pouch:
        prob += (
            pl.lpSum(X[c][p] * weight[c] for c in cuttable)
            + pl.lpSum(Y[c][p] * weight[c] for c in noncuttable)
            <= small_capacity
        )
    for c in cuttable:
        prob += pl.lpSum(X[c][p] for p in pouch) <= pieces[c]
    for c in noncuttable:
        prob += pl.lpSum(Y[c][p] for p in pouch) <= pieces[c]

    for p in pouch:
        prob += uplus[p] - uminus[p] == pl.lpSum(
            X[c][p] * weight[c] for c in cuttable
        ) + pl.lpSum(Y[c][p] * weight[c] for c in noncuttable) - pl.lpSum(
            X[c][q] * weight[c] / k for c in cuttable for q in pouch
        ) - pl.lpSum(
            Y[c][q] * weight[c] / k for c in noncuttable for q in pouch
        )

    prob += pl.lpSum(uplus[p] + uminus[p] for p in pouch) <= minimal_unevenness

    # call the solver
    status = prob.solve()

    # print solution
    print(pl.LpStatus[status])

    for p in pouch:
        cut = ", ".join([f"{pl.value(X[c][p])} of {c}" for c in cuttable])
        ncut = ", ".join([f"{pl.value(Y[c][p])} of {c}" for c in noncuttable])
        print(f"Put in pouch {p}: {cut}, {ncut}")


cheese = ["Brie", "Camembert", "Reblochon", "Handkaese", "Roquefort"]
cuttable = ["Brie", "Camembert", "Reblochon"]
pieces = [1, 1, 1, 30, 1]
weight = [15, 9, 10, 0.4, 10]
value = [1800, 1200, 1300, 50, 2200]
small_capacity = 11
k = 9

cheese_coup(
    cheese,
    cuttable,
    dict(zip(cheese, pieces)),
    dict(zip(cheese, weight)),
    dict(zip(cheese, value)),
    small_capacity,
    k,
)


# 8000
# Put in pouch 0: 0.0 of Brie, 0.0 of Camembert, 0.0 of Reblochon, 0.0 of Handkaese, 1.0 of Roquefort
# Put in pouch 1: 0.14074074 of Brie, 0.0 of Camembert, 0.37777778 of Reblochon, 0.0 of Handkaese, 0.0 of Roquefort
# Put in pouch 2: 0.014814815 of Brie, 0.0 of Camembert, 0.0 of Reblochon, 15.0 of Handkaese, 0.0 of Roquefort
# Put in pouch 3: 0.41481481 of Brie, 0.0 of Camembert, 0.0 of Reblochon, 0.0 of Handkaese, 0.0 of Roquefort
# Put in pouch 4: 0.0 of Brie, 0.30864198 of Camembert, 0.0 of Reblochon, 0.0 of Handkaese, 0.0 of Roquefort
# Put in pouch 5: 0.41481481 of Brie, 0.0 of Camembert, 0.0 of Reblochon, 0.0 of Handkaese, 0.0 of Roquefort
# Put in pouch 6: 0.0 of Brie, 0.0 of Camembert, 0.62222222 of Reblochon, 0.0 of Handkaese, 0.0 of Roquefort
# Put in pouch 7: 0.0 of Brie, 0.69135802 of Camembert, 0.0 of Reblochon, 0.0 of Handkaese, 0.0 of Roquefort
# Put in pouch 8: 0.014814815 of Brie, 0.0 of Camembert, 0.0 of Reblochon, 15.0 of Handkaese, 0.0 of Roquefort