from pulp import *;

def maintenance(
        trucks,
        weeks,
        past,
        future,
        last_maintenance,
        maintenance_cost,
        inter_maintenance_time,
        min_truck_total,
        total_capacity,
        unavailable_during_maintenance
    ):
    """
    Parameters:
    - trucks: list of trucks
    - weeks: all relevant weeks [-15,...,51]
    - past: relevant weeks of past year [-15,...,-1]
    - future: weeks in this year [0,51]
    - last_maintenance[trucks]: number of weeks since the last maintenance (e.g. 1 means that the truck was maintained in the last week of the previous year)
    - maintenance cost: cost for one truck maintenance
    - min_truck_total: the minimum number of truck which must be available during each week.
    - total_capacity: total number of maintenances every week.
    - unavailable_during_maintenance: the fraction of a week which is required for maintenance (e.g. 0.5 for half of a week)
    """

    x = LpVariable.dicts("x", (trucks,weeks), cat=LpBinary)
    av = LpVariable.dicts("available", (trucks,weeks), lowBound=0,upBound=1,cat=LpContinuous)

    prob = LpProblem("maintenance_1", LpMinimize)

    prob += lpSum(x)

    
    for t in trucks:
        for w in past:
            if w == -last_maintenance[t]:
                prob += x[t][w] == 1
            else:
                prob += x[t][w] == 0
    
    for w in future:
        prob += lpSum(av[t][w] for t in trucks) >= min_truck_total
    
    #make sure that trucks are unavailable if no maintenance was done in time
    for t in trucks:
        for w in future:
            prob += av[t][w] <= lpSum(x[t][wp] for wp in range(w-inter_maintenance_time+1,w+1))

    #truck partly available when in maintenance
    for t in trucks:
        for w in future:
            prob += av[t][w] <= 1 - unavailable_during_maintenance * x[t][w]

    for w in future:
        prob += lpSum(unavailable_during_maintenance * x[t][w] for t in trucks) <= total_capacity
        # should x[t][w] times unavail_during_maintenance?

    status = prob.solve()
    print(LpStatus[status])
    for w in future:
        print(f"Week {w}: {",".join([str(t) for t in trucks if value(x[t][w]) == 1])}")



number_of_trucks = 85
number_of_weeks = 52
 
maintenance_cost = 250
inter_maintenance_time = 15
min_truck_total = 75
total_capacity = 6
unavailable_during_maintenance = 0.5

last_maintenance = [1, 1, 2, 2, 3, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 1, 1, 1, 1, 2, 2, 3, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 1, 1, 1, 2, 2, 3, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 1, 1, 2, 2, 3, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 1, 1, 2, 2, 3, 3, 4, 5, 6, 7, 8, 9, 10, 11] 

maintenance(
    trucks=list(range(0,number_of_trucks)),
    weeks=list(range(-15,number_of_weeks)),
    past=list(range(-15,0)),
    future=list(range(0,number_of_weeks)),
    last_maintenance=dict(zip(range(0,number_of_trucks),last_maintenance)),
    maintenance_cost=maintenance_cost,
    inter_maintenance_time=inter_maintenance_time,
    min_truck_total=min_truck_total,
    total_capacity=total_capacity,
    unavailable_during_maintenance=unavailable_during_maintenance,
)
