def min_cost_climbing_stairs(cost: list):
    cost.append(0)
    cost.reverse()
    
    for i in range(len(cost)-3):
        cost[i] += min(cost[i+1], cost[i+2])
    
    cost.reverse()
    return min(cost[0], cost[1])
