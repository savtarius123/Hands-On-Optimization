import pulp as pl


def cheese_empire(location, factory, demand, production_cost, capacity, factory_location):
    """
    Parameters:
    - location: list of cities
    - factories: list of factory names
    - demand[location]: cheese demand in tons per month for each location
    - production_cost[factory]: production cost per ton in each factory
    - capacity[factory]: maximum number of tons which can be produced in one month in each factory
    - factory_location[factory]: the location of each factory
    """

    # variable definitions
    ship = pl.LpVariable.dicts("ship", (factory, location), lowBound=0)

    # problem definition and objective function
    prob = pl.LpProblem("cheese_empire_1", pl.LpMinimize)
    prob += pl.lpSum(production_cost[f] * ship[f][l] for f in factory for l in location)

    # constraints
    for f in factory:
        prob += pl.lpSum(ship[f][l] for l in location) <= capacity[f]
        
        for l in location:
            if factory_location[f] != l:
                prob += ship[f][l] <= 0
    
    for l in location:
        prob += pl.lpSum(ship[f][l] for f in factory) >= demand[l]

    # call the solver
    status = prob.solve()

    # print solution
    print(pl.value(prob.objective))
    print(pl.LpStatus[status])
    for f in factory:
        s = ", ".join([f"{pl.value(ship[f][l])} to {l}" for l in location])
        print(f"Ship from {f} to {s}")



location = ["Zuerich", "Genf", "Basel", "Lausanne", "Bern", "Luzern"]
factory = ["Zuerich1", "Zuerich2", "Genf1", "Genf2", "Basel", "Lausanne", "Bern", "Luzern"]
demand = [20, 15, 4, 8, 13, 9]
factory_location = ["Zuerich", "Zuerich", "Genf", "Genf", "Basel", "Lausanne", "Bern", "Luzern"]
production_cost = [8, 5, 6, 6, 3, 5, 10, 7]
capacity = [17, 9, 9, 9, 9, 9, 17, 9]

cheese_empire(
    location,
    factory,
    dict(zip(location, demand)),
    dict(zip(factory, production_cost)),
    dict(zip(factory, capacity)),
    dict(zip(factory, factory_location)),
)
