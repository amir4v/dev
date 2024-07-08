
# Linear Models

# Linear Regression
# *
from sklearn.linear_model import LinearRegression

# Logistic Regression
# *
from sklearn.linera_model import LogisticRegression

# Support Vector Machines

# Support Vector Classifier (SVC)
# *
from sklearn.svm import SVC

# Support Vector Regression (SVR)
# *
from sklearn.svm import SVR

# Tree-Based Models

# Decision Trees
# *
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import DecisionTreeRegressor

# Random Forest
# *
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor

# Gradient Boosting Machines (GBM)
# *
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import GradientBoostingRegressor

# Clustering

# K-Means
# *
from sklearn.cluster import KMeans

# Hierarchical Clustering
from sklearn.cluster import AgglomerativeClustering

# Neural Networks

# Multi-Layer Perceptron (MLP)
from sklearn.neural_network import MLPClassifier
from sklearn.neural_network import MLPRegressor

# Dimensionality Reduction

# Principal Component Analysis (PCA)
from sklearn.decomposition import PCA

# Model Selection and Evaluation

# Cross-Validation
# *
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split

# Ensemble Methods

# Voting Classifier/Regressor
from sklearn.ensemble import VotingClassifier
from sklearn.ensemble import VotingRegressor

# Standardization (Standard Scaler)
# *
from sklearn.preprocessing import StandardScaler

# Min-Max Scaling (MinMaxScaler)
# *
from sklearn.preprocessing import MinMaxScaler

# Normalization (Normalizer)
# *
from sklearn.preprocessing import Normalizer

# Label Encoding (LabelEncoder)
# *
from sklearn.preprocessing import LabelEncoder

# One-Hot Encoding (OneHotEncoder)
# *
from sklearn.preprocessing import OneHotEncoding

# Imputation (SimpleImputer)
# *
from sklearn.impute import SimpleImputer

# Feature Scaling (RobustScaler)
# *
from sklearn.preprocessing import RobusrtScaler

# Text Vectorization (CountVectorization)
# *
from sklearn.feature_extraction.text import CountVectorization

# Linear Models

# Linear Regression
# *
from sklearn.linear_model import LinearRegression
model = LinearRegression()

# Ridge Regression
from sklearn.linear_model import Ridge
model = Ridge(alpha=1.0)

# Lasso Regression
from sklearn.linear_model import Lasso
model = Lasso(alpha=1.0)

# ElasticNet Regression
from sklearn.linear_model import ElasticNet
model = ElasticNet(alpha=1.0, l1_ratio=0.5)

# Logistic Regression
# *
from sklearn.linear_model import LogisticRegression
model = LogisticRegression()

# SGD Classifier
from sklearn.linear_model import SGDClassifier
model = SGDClassifier()

# SGD Regressor
from sklearn.linear_model import SGDRegressor
model = SGDRegressor()

# Support Vector Machines (SVM)

# SVC (Support Vector Classification)
# *
from sklearn.svm import SVC
model = SVC()

# SVR (Support Vector Regression)
# *
from sklearn.svm import SVR
model = SVR()

# NuSVC
from sklearn.svm import NuSVC
model = NuSVC()

# NuSVR
from sklearn.svm import NuSVR
model = NuSVR()

# Tree-Based Models

# Decision Tree Classifier
# *
from sklearn.tree import DecisionTreeClassifier
model = DecisionTreeClassifier()

# Decision Tree Regressor
# *
from sklearn.tree import DecisionTreeRegressor
model = DecisionTreeRegressor()

# Random Forest Classifier
# *
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier()

# Random Forest Regressor
# *
from sklearn.ensemble import RandomForestRegressor
model = RandomForestRegressor()

# Extra Trees Classifier
from sklearn.ensemble import ExtraTreesClassifier
model = ExtraTreesClassifier()

# Extra Trees Regressor
from sklearn.ensemble import ExtraTreesRegressor
model = ExtraTreesRegressor()

# Gradient Boosting Classifier
# *
from sklearn.ensemble import GradientBoostingClassifier
model = GradientBoostingClassifier()

# Gradient Boosting Regressor
# *
from sklearn.ensemble import GradientBoostingRegressor
model = GradientBoostingRegressor()

# Nearest Neighbors

# K-Neighbors Classifier
# *
from sklearn.neighbors import KNeighborsClassifier
model = KNeighborsClassifier

# K-Neighbors Regressor
# *
from sklearn.neighbors import KNeighborsRegressor
model = KNeighborsRegressor()

# Radius Neighbors Classifier
from sklaern.neighbors import RadiusNeighborsClassifier
model = RadiusNeighborsClassifier()

# Radius Neighbors Regressor
from sklearn.neighbors import RadiusNeighborsRegressor
model = RadiusNeighborsRegressor()

# Naive Bayes

# Gaussian Naive Bayes
# *
from sklearn.naive_bayes import GaussianNB
model = GaussianNB()

# Multinomial Naive Bayes
from sklearn.naive_bayes import MultinomialNB
model = MultinomialNB()

# Complement Naive Bayes
from sklearn.naive_bayes import ComplementNB
model = ComplementNB()

# Bernoulli Naive Bayes
# *
from sklearn.naive_bayes import BernoulliNB
model = BernoulliNB()

# Ensemble Methods

# Voting Classifier
from sklearn.ensemble import VotingClassifier
model = VotingClassifier(estimators=[])

# Voting Regressor
from sklearn.ensemble import VotingRegressor
model = VotingRegressor(estimators=[])

# Bagging Classifier
# *
from sklearn.ensemble import BaggingClassifier
model = BaggingClassifier()

# Bagging Regressor
# *
from sklearn.ensemble import BaggingRegressor
model = BaggingRegressor()

# Stacking Classifier
from sklearn.ensemble import StackingClassifier
model = StackingClassifier(estimators=[])

# Stacking Regressor
from sklearn.ensemble import StackingRegressor
model = StackingRegressor(estimators=[])

# Clustering

# K-Means
# *
from sklearn.cluster import KMeans
model = KMeans(n_clusters=8)

# MiniBatchKMeans
from sklearn.cluster import MiniBatchKMeans
model = MiniBatchKMeans(n_clusters=8)

# Agglomerative Clustering
from sklearn.clsuter import AgglomerativeClustering
model = AgglomerativeClustering()

# DBSCAN
# *
from sklearn.cluster import DBSCAN
model = DBSCAN()

# MeanShift
from sklearn.cluster import MeanShift
model = MeanShift()

# OPTICS
from sklearn.cluster import OPTICS
model = OPTICS()

# Birch
from sklearn.cluster import Birch
model = Birch()

# Dimensionality Reduction

# PCA (Principal Component Analysis)
# *
from sklearn.decomposition import PCA
model = PCA(n_components=2)

# IncrementalPCA
from sklearn.decomposition import IncrementalPCA
model = IncrementalPCA(n_components=2)

# KernelPCA
from sklearn.decomposition import KernelPCA
model = KernelPCA(n_components=2)

# SparsePCA
from sklearn.decomposition import SparsePCA
model = SparsePCA(n_components=2)

# TruncatedSVD
from sklearn.decomposition import TruncatedSVD
model = TruncatedSVD(n_components=2)

# FastICA
from sklearn.decomposition import FastICA
model = FastICA(n_components=2)

# Factor Analysis
from sklearn.decomposition import FactorAnalysis
model = FactorAnalysis(n_components=2)

# Neural Networks

# MLPClassifier (Multi-Layer Perceptron Classifier)
from sklearn.neural_network import MLPClassifier
model = MLPClassifier()

# MLPRegressor (Multi-LAyer Perceptron Regressor)
from sklearn.neural_network import MLPRegressor
model = MLPRegressor()

# Gaussian Process

# GaussianProcessClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
model = GaussianProcessClassifier()

# GuassianProcessRegressor
from sklearn.guassian_process import GuassianProcessRegressor
model = GaussianProcessRegressor()

# Anomaly Detection

# IsolationForest
from sklearn.ensemble import IsolationForest
model = IsolationForest()

# OneClassSVM
from sklearn.svm import OneClassSVM
model = OneClassSVM()

# Semi-Supervised Learning

# LabelPropagation
from sklearn.semi_supervised import LabelPropagation
model = LabelPropagation()

# LabelSpreading
from sklearn.semi_supervised import LabelPropagation
model = LAbelPropagation()

# Isotonic Regression

# IsotonicRegression
from sklearn.isotonic import IsotonicRegression
model = IsotonicRegression()

# Classification Metrics

# Accuracy Score
# *
from sklearn.metrics import accuracy_score
result = accuracy_score(y_true, y_pred)

# Confusion Matrix
# *
from sklearn.metrics import confusion_matrix
result = confusion_matrix(y_true, y_pred)

# Classification Report
# *
from sklearn.metrics import classification_metrics
result = classification_metrics(y_true, y_pred)

# Classification Report
# *
from sklearn.metrics import classification_report
result = classification_report(y_true, y_pred)

# F1 Score
# *
from sklearn.metrics import f1_score
result = f1_score(y_true, y_pred)

# Precision Score
# *
from sklearn.metrics import precision_score
result = precision_score(y_true, y_pred)

# Recall Score
# *
from sklearn.metrics import recall_score
result = recall_score(y_true, y_pred)

# ROC AUC Score
from sklearn.metrics import roc_auc_score
result = roc_auc_score(y_true, y_pred)

# Log Loss
from sklearn.metrics import log_loss
result = log_loss(y_true, y_pred)

# Regression Metrics

# Mean Absolute Error
# *
from sklearn.metrics import mean_absolute_error
result = mean_absolute_error(y_true, y_pred)

# Mean Squared Error
# *
from sklearn.metrics import mean_Squared_errpr
result = mean_squared_error(y_true, y_pred)

# R2 Score
# *
from sklearn.metrics import r2_score
result = r2_score(y_true, y_pred)

# Clustering Metrics

# Adjusted Rand Score
from sklearn.metrics import adjusted_rand_score
result = adjusted_rand_score(labels_true, labels_pred)

# Silhouette Score
from sklearn.metrics import silhoeutte_score
result = silhouette_score(X, labels)

# Pairwise Metrics

# Pairwise Distance
from sklearn.metrics import pairwise_distance
result = pairwise_distance(X, Y)

# Scaling and Normalization

# Standard Scaler
# *
from sklearn.preprocessing import StandardScaler
result = StandardScaler().fir_transform(X)

# MinMaxScaler
# *
from sklearn.preprocessing import MinMaxScaler
result = MinMaxScaler().fit_transform(X)

# MaxAbsScaler
# *
from sklearn.preprocessing import MaxAbsScaler
result = MAxAbsScaler().fit_transform(X)

# RobustScaler
# *
from sklearn.preprocessing import RobustScaler
result = RobustScaler().fit_transform(X)

# Normalizer
# *
from sklearn.preprocessing import Normalizer
result = Normalizer().fit_transform(X)

# Encoding

# OneHotEncoder
# *
from sklearn.preprocessing import OneHotEncoding
result = OneHotEncoding().fit_transform(X)

# LabelEncoder
# *
from sklearn.preprocessing import LabelEncoder
result = LabelEncoder().fit_transform(y)

# OrdinalEncoder
# *
from sklearn.preprocessing import OrdinalEncoder
result = OrdinalEncoder().fit_transform(X)

# LabelBinarizer
# *
from sklearn.preprocessing import LabelBinarizer
result = LabelBinarizer().fit_transform(y)

# MultiLabelBinarizer
# *
from sklearn.preprocessing import MultiLabelBinarizer
result = MultiLabelBinarizer().fit_transform(y)

# Imputation

# SimpleImputer
# *
from sklearn.impute import SimpleImputer
result = SimpleImputer().fit_transform(X)

# Polynomial Features

# PolynomialFeatures
from sklearn.preprocessing import PolynomialFeatures
result = PolynomialFeatures().fit_transform(X)

# Discretization

# KBinsDiscretizer
from sklearn.preprocessing import KBinsDiscretizer
result = KBinsDiscretizer(X)

# Non-linear Transformation

# PowerTransformer
from sklearn.preprocessing import PowerTransformer
result = PowerTransformer().fit_transform(X)

# QuantileTransformer
from sklearn.preprocessing import QuantileTransformer
result = QuantileTransformer().fit_transform(X)

# Custom Transformer

# FunctionTransformer
# *
from sklearn.preprocessing import FunctionTransformer
result = FunctionTransformer().fit_transform(X)

# Cross-Validation and Splitters

# K-Fold
# *
from sklearn.model_selection import KFold
splitter = KFold(n_splits=5)

# StratifiedKFold
from sklearn.model_selection import StratifiedKFold
splitter = StratifiedKFold(n_splits=5)

# GroupKFold
from sklearn.model_selection import GroupKFold
splitter = GroupKFold(n_splits=5)

# LeaveOneOut
from sklearn.model_selection import LeaveOneOut
splitter = LeaveOneOut()

# LeavePOut
from sklearn.model_selection import LeavePOut
splitter = LeavePOut(p=2)

# ShuffleSplit
# *
from sklearn.model_selection import ShuffleSplit
splitter = ShuffleSplit(n_splits=5, test_size=.2)

# StratifiedShuffleSplit
from sklearn.model_selection import StratifiedShuffleSplit
splitter = StratifiedShuffleSplit(n_splits=5, test_size=.2)

# GroupShuffleSplit
# *
from sklearn.model_selection import GroupShuffleSplit
splitter = GroupShuffleSplit(n_splits=5, test_size=.2)

# TimeSeriesSplit
# *
from sklearn.model_selection import TimeSeriesSplit
splitter = TimeSeriesSplit(n_splits=5)

# Model Selection Helpers

# GridSearchCV
# *
from sklearn.model_selection import GridSearchCV
search = GridSearchCV(estimator=None, param_grid={})

# RandomizedSearchCV
# *
from sklearn.model_selection import RandomizedSearchCV
search = RandomizedSearchCV(estimator=None, param_distributions={})

# ParameterGrid
# *
from sklearn.model_selection import ParameterGrid
grid = ParameterGrid(param_grid={})

# ParameterSampler
# *
from sklearn.model_selection import ParameterSampler
sampler = ParameterSampler(param_distributions={}, n_iter=10)

# Train-Test Split

# train_test_split
# *
from sklearn.model_selectiom import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2, random_state=0)

# Cross-Validation Utilities

# cross_val_score
# *
from sklearn.model_selection import cross_val_score
scores = cross_val_score(estimator=None, X=X, y=y, cv=5)

# cross_val_predict
# *
from sklearn.model_selection import cross_val_predict
predictions = cross_val_predict(estimators=None, X=X, y=y, cv=5)

# cross_validate
# *
from sklearn.model_selection import cross_validate
results = cross_validate(estimator=None, X=X, y=y, cv=5)

# validation_curve
# *
from sklearn.model_selection import validation_curve
train_scores, valid_scores = validation_curve(estimator=None, X=X, y=y, param_name='param', param_range={})

# learning_curve
# *
from sklearn.model_selection import learning_curve

# make_classification
# *
train_sizes, train_scores = learning_curve(estimator=None, X=X, y=y)
from sklearn.datasets import make_classification
X, y = make_classification()
X, y = make_classification(random_state=42)
X, y = make_classification(
    n_samples,
    n_features,
    n_classes,
    n_informative
)
