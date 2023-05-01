from random import randint

x = int(input('Number>>> '))
n = int(input('Percent>>> '))

low = x - (n * (x/100))
high = x + (n * (x/100))

print('low, high:', low, high)
print('Result:', randint(low, high))
