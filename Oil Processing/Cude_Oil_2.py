import pulp as pq

def Crude_oil (OilTypes, Bestellung, Kosten):



    #problem definition and objective function
    prob = pq.LpProblem("Crude_oil", pq.LpMinimize)
    prob += pq.lpDot(X, Kosten)
    
    X = [pq.LpVariable(OilTypes, lowBound=0) for OilTypes in Bestellung]
    
    # call the solver
    status = prob.solve()
    
    
    # print solution
    print(pq.LpStatus[status])
    for x in X:
        print(f"Produce {pq.value(x)} of {x}")
        

Crude_oil(
    ["heavy", "medium", "light"],
    [3, 5, 4],
    [
        [2, 2],
        [2, 2],
        [1, 4],
      
    ],
    [30, 50],
)
