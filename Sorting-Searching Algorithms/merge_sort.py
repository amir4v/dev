def merge_sort(data):
    if len(data) <= 1:
        return data
    
    left_data = data[: len(data)//2 ]
    right_data = data[ len(data)//2 :]
    left = merge_sort(left_data)
    right = merge_sort(right_data)
    
    print(left, right)
    print(merge(left, right))
    print('=' * 80)
    
    return merge(left, right)

def merge(left, right):
    result = []
    i = 0
    j = 0
    
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    while i < len(left):
        result.append(left[i])
        i += 1
    
    while j < len(right):
        result.append(right[j])
        j += 1
    
    return result

print(
    merge_sort([1,5,2,4,3,34,99,11,555,0,333333])
)
