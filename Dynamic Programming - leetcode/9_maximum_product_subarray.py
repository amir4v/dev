def maximum_product_subarray(nums):
    res = max(nums)
    cur_min, cur_max = 1, 1
    
    for n in nums:
        if n == 0:
            cur_min, cur_max = 1, 1
            continue
        
        tmp_cur_max = cur_max
        cur_max = max(n*cur_min, n*cur_max, n)
        cur_min = max(n*cur_min, n*tmp_cur_max, n)
        res = max(res, cur_max)
    
    return res
