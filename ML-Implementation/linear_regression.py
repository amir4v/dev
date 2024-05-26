import numpy as np


class LinearRegression:
    def __init__(self, lr=.01, n_iters=1000):
        self.lr = lr
        self.n_iters = n_iters
    
    def w_gradient(self, X, y_pred, y):
        slope = np.dot(X.T, (y_pred - y)) / len(y)
        return slope
    
    def b_gradient(self, X, y_pred, y):
        slope = np.sum(y_pred - y) / len(y)
        return slope
    
    def fit(self, X, y):
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        self.bias = 0
        
        for _ in range(self.n_iters):
            y_pred = np.dot(self.weights, X.T) + self.bias
            
            dw = self.w_gradient(X, y_pred, y)
            db = self.b_gradient(X, y_pred, y)
            
            self.weights = self.weights - self.lr * dw
            self.bias = self.bias - self.lr * db
    
    def predict(self, X):
        y_pred = np.dot(self.weights, X.T) + self.bias
        return y_pred


# Test

from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

X, y = make_regression(1000, 1)

# plt.scatter(X[:, 0], y)
# plt.show()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2, random_state=42)

reg = LinearRegression()
reg.fit(X_train, y_train)
y_pred = reg.predict(X_test)

def mse(y_test, y_pred):
    return np.mean((y_test - y_pred)**2)

plt.scatter(X_train[:, 0], y_train)
plt.scatter(X_test[:, 0], y_test)
plt.plot(X[:, 0], reg.predict(X))
plt.show()

print(mse(y_test, y_pred))
