from pulp import *


# Exercise 3

def chips_factory(chips, prices, processes, process_durations, max_times):

    x = LpVariable.dicts("x", chips, lowBound=0)

    prob = LpProblem("chips factory", LpMaximize)

    prob += lpSum(prices[c] * x[c] for c in chips)

    for p in processes:
        prob += lpSum(process_durations[p][c] * x[c] for c in chips) <= max_times[p]

    prob.solve()

    for c in chips:
        print(f"{c}: {value(x[c])}")


chips = ["potato", "mexican"]
processes = ["slice", "fry", "pack"]

prices = [2, 1.5]
process_times = [[2,4], [4,5], [4,2]]
max_times = [345,480,330]


chips_factory(
    chips,
    dict(zip(chips,prices)),
    processes,
    dict([(p, dict(zip(chips, process_times[i]))) for i, p in enumerate(processes)]),
    dict(zip(processes, max_times))
)