from collections import Counter

import numpy as np


def euclidean_distance(x1, x2):
    distance = np.sqrt(np.sum((x1-x2)**2))
    return distance


class KNN:
    def __init__(self, k=3):
        self.k = k
    
    def fit(self, X, y):
        self.X_train = X
        self.y_train = y
    
    def predict(self, X):
        predictions = [self._predict(x) for x in X]
        return predictions
    
    def _predict(self, x):
        # compute the distances
        distances = [euclidean_distance(x, x_train) for x_train in self.X_train]
        
        # get the closest k
        k_nearest_indices = np.argsort(distances)[:self.k]
        k_nearest_labels = [self.y_train[i] for i in k_nearest_indices]
                
        # majority vote
        most_common = Counter(k_nearest_labels).most_common(1)[0][0]
        
        return most_common


# Testing

from sklearn.datasets import load_iris

iris = load_iris()
X, y = iris.data, iris.target

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2, random_state=42)

knn = KNN(3)

knn.fit(X_train, y_train)
y_pred = knn.predict(X_test)

print(
    accuracy_score(y_test, y_pred)
)
