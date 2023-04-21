def quick_sort(items):
    if len(items) <= 1:
        return items
    
    pivot = items[0]
    lt = []
    gt = []
    
    for item in items[1:]:
        if item < pivot:
            lt.append(item)
        else:
            gt.append(item)

    return quick_sort(lt) + [pivot] + quick_sort(gt)    

print(
    quick_sort([1,6,2,5,3,4])
)
