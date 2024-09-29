import pulp as pq

x1 = pq.LpVariable("x1", lowBound=0) # produced quantity of process 1
x2 = pq.LpVariable("x2", lowBound=0) # produced quantity of process 2


# problem definition and objective function
prob = pq.LpProblem("Crude_Oil", pq.LpMinimize)
prob += 30 * x1 + 50 * x2


# constraints
prob += 2*x1 + x2 >= 3
prob += 2*x1 + 2*x2 >= 5
prob += x1 + 4*x2 >= 4

# call the solver
status = prob.solve()

# print solution
print(pq.LpStatus[status])
print(f"Die minimale Kosten für diese Bestellung wäre durch:")
print(f"Prozess 1 = {pq.value(x1)}")
print(f"Prozess 2 = {pq.value(x2)}")
print(f"Optimal objective value = {pq.value(prob.objective)}")


