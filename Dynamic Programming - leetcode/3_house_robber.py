def house_robber(nums: list):
    rob1, rob2 = 0, 0
    
    for n in nums:
        temp = max(rob1+n, rob2)
        rob1, rob2 = rob2, temp
    
    return rob2
