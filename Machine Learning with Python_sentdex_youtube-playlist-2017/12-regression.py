import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import random

style.use('fivethirtyeight')

# x = np.array([1,2,3,4,5,6], dtype=np.float64)
# y = np.array([5,4,6,5,6,7], dtype=np.float64)

def best_fit_slope_and_intercept(x, y):
    m = ( ((x.mean() * y.mean()) - ((x * y).mean())) /
          ((x.mean() ** 2) - ((x ** 2).mean()))
        )
    b = y.mean() - m * x.mean()
    return m, b

def squared_error(y_pred, y_true):
    return ((y_pred - y_true) ** 2).sum()

def coefficient_of_determination(y_pred, y_true):
    y_mean_line = [y_true.mean() for _ in y_true]
    squared_error_regr = squared_error(y_pred, y_true)
    squared_error_y_mean = squared_error(y_mean_line, y_true)
    return 1 - (squared_error_regr / squared_error_y_mean)

def create_dataset(hm, variance, step=2, correlation=False):
    val = 1
    y = []
    for i in range(hm):
        y.append(val + random.randrange(-variance, variance))
        if correlation == 'pos':
            val += step
        elif correlation == 'neg':
            val -+ step
    x = [i for i in range(len(y))]
    return np.array(x, dtype=np.float64), np.array(y, dtype=np.float64)

x, y = create_dataset(40, 10, 2, correlation=False)

m, b = best_fit_slope_and_intercept(x, y)

y_true = y
y_pred = m*x+b

r_squared__coefficient_of_determination = coefficient_of_determination(y_pred, y_true)

print(r_squared__coefficient_of_determination)

plt.scatter(x, y)
plt.plot(x, m*x+b)
plt.show()
