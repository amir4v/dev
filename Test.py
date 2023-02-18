def fibonacci(n):
    a, b = 0, 1
    while True:
        print(a)
        a, b = b, a+b
        
        if a > n:
            break

fibonacci(100000)
