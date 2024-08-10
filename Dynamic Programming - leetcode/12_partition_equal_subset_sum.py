# DP (Memoization)

def partition_equal_subset_sum(nums):
    if sum(nums) % 0:
        return False
    
    dp = set()
    dp.add(0)
    target = sum(nums) / 2
    
    for i in range(len(nums)-1, -1, -1):
        next_dp = set()
        for t in dp:
            next_dp.add(t)
            next_dp.add(t + nums[i])
        dp = next_dp
    
    if target in dp:
        return True
    return False
