def bubble_sort(data):
    for i in range(len(data)):
        for j in range(i+1, len(data)):
            if data[i] > data[j]:
                data[i], data[j] = data[j], data[i]
    return data

items = [1,5,4,3,2,0,33,11,5,6666,7777,4,3,2,1]
print(
    bubble_sort(items)
)
