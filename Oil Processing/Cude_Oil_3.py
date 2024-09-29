import pulp as pq

def Crude_oil (Bestellung, OilTypes, Kosten):
    
    # variable definitions
    X = pq.LpVariable.dicts("x", Bestellung, lowBound=0)
    
    print(X)
    
    # problem definition and objective function
    prob = pq.LpProblem("Crude_oil", pq.LpMaximize)
    prob += pq.lpSum(X[t] * Kosten[t] for t in OilTypes)
    
     # call the solver
    status = prob.solve()

    # print solution
    print(pq.LpStatus[status])
    for t in OilTypes:
        print(f"Produce {pq.value(X[t])} of {t}")
        
    OilTypes = ["heavy", "medium", "light"]
    
    Bestellung = [30, 50, 40]
    Kosten = [30, 50]
    
    Crude_oil(
    Bestellung,
    dict(zip(OilTypes, Kosten)),
    
    
)
