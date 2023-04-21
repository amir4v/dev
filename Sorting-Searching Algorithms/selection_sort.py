def selection_sort(items: list):
    sorted = []
    for i in range(len(items)):
        min = 0
        
        for j in range(len(items)):
            if items[j] < items[min]:
                min = j
        sorted.append(items.pop(min))
    
    return sorted


import random

items = random.sample([x for x in range(30000)], k=100)
print(
    selection_sort(items)
)
