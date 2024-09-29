import pulp as pl
from math import sqrt, pow


def cheese_empire(
    location,
    factory,
    demand,
    production_cost,
    capacity,
    factory_location,
    x,
    y,
    leakage=0.001,
    pipeline_cap=3,
    heating_cost=0.02,
    construction_cost=0.2,
):
    """
    Parameters:
    - location: list of cities
    - factories: list of factory names
    - demand[location]: cheese demand in tons per month for each location
    - production_cost[factory]: production cost per ton in each factory
    - capacity[factory]: maximum number of tons which can be produced in one month in each factory
    - factory_location[factory]: the location of each factory
    - x[location]: x coordinates
    - y[location]: y coordinates
    """

    distance = dict(zip(location, [dict.fromkeys(location) for _ in location]))
    loss = dict(zip(factory, [dict.fromkeys(location) for _ in factory]))
    for l in location:
        for k in location:
            distance[l][k] = sqrt(pow(abs(x[l] - x[k]), 2) + pow(abs(y[l] - y[k]), 2))

    for l in location:
        for f in factory:
            loss[f][l] = distance[factory_location[f]][l] * leakage

    # variable definitions
    ship = pl.LpVariable.dicts("ship", (factory, location), lowBound=0)
    build = pl.LpVariable.dicts("build", (location, location), cat=pl.LpBinary)
    produce = pl.LpVariable.dicts("produce", factory, lowBound=0)

    # problem definition and objective function
    prob = pl.LpProblem("cheese_empire_2", pl.LpMinimize)
    prob += (
        24 * pl.lpSum(production_cost[f] * produce[f] for f in factory)
        + (
            24
            * heating_cost
            * pl.lpSum(
                ship[f][l] * distance[factory_location[f]][l]
                for f in factory
                for l in location
            )
        )
        + construction_cost
        * pl.lpSum(build[l][k] * distance[l][k] for l in location for k in location)
    )

    # constraints
    for f in factory:
        prob += pl.lpSum(ship[f][l] for l in location) <= produce[f]
        prob += produce[f] <= capacity[f]

    for l in location:
        prob += pl.lpSum((1 - loss[f][l]) * ship[f][l] for f in factory) >= demand[l]

    for l in location:
        for k in location:
            if l != k:
                prob += (
                    pl.lpSum(ship[f][k] for f in factory if factory_location[f] == l)
                    <= pipeline_cap * build[l][k]
                )

    # call the solver
    status = prob.solve()

    # print solution
    print(pl.LpStatus[status])
    print(prob.objective.value())
    for l in location:
        for k in location:
            if pl.value(build[l][k]):
                s = ", ".join(
                    [
                        f"{pl.value(ship[f][k])} from {f}"
                        for f in factory
                        if factory_location[f] == l and pl.value(ship[f][k]) > 0
                    ]
                )
                print(f"Build {l} -> {k} and ship {s}")


location = ["Zuerich", "Genf", "Basel", "Lausanne", "Bern", "Luzern"]
factory = [
    "Zuerich1",
    "Zuerich2",
    "Genf1",
    "Genf2",
    "Basel",
    "Lausanne",
    "Bern",
    "Luzern",
]
demand = [20, 15, 4, 8, 13, 9]
factory_location = [
    "Zuerich",
    "Zuerich",
    "Genf",
    "Genf",
    "Basel",
    "Lausanne",
    "Bern",
    "Luzern",
]
production_cost = [8, 5, 6, 6, 3, 5, 10, 7]
capacity = [17, 9, 9, 9, 9, 9, 17, 9]
x = [8.5, 6.1, 7.6, 6.6, 7.4, 8.3]
y = [47.4, 46.2, 47.6, 66.6, 47, 47.1]


cheese_empire(
    location,
    factory,
    dict(zip(location, demand)),
    dict(zip(factory, production_cost)),
    dict(zip(factory, capacity)),
    dict(zip(factory, factory_location)),
    dict(zip(location, x)),
    dict(zip(location, y)),
)
