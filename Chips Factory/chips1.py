from pulp import *

# Exercise 1

xp = LpVariable("xp", lowBound=0)
xm = LpVariable("xm", lowBound=0)

prob = LpProblem("chips factory", LpMaximize)

prob += 2 * xp + 1.5 * xm

prob += 2 * xp + 4 *xm <= 345
prob += 4 * xp + 5 *xm <= 480
prob += 4 * xp + 2 *xm <= 330

print(prob)

prob.solve()

print(f"xp = {value(xp)}")
print(f"xm = {value(xm)}")

