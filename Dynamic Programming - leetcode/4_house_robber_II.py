from .house_robber import house_robber

def house_robber_II(nums):
    return max(
        nums[0], # in case of only one item
        house_robber(nums[1:]),
        house_robber(nums[:-1]),
    )
