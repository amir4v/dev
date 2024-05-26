
from sklearn.linear_model import LinearRegression
    fit_intercept: True; Wether to calculate th eintercept for this model.
        is like asking if you want the line to start from the very bottom of the graph or not. If you set it to "True," it means you're allowing the line to start from the bottom, and if you set it to "False," it means the line has to go through the middle of the points. It's like choosing where the line begins on the graph.
    copy_X: True; X will be copied.
    n_jobs: None; the number of jobs to use for the computation.
    positive: False; forces the coefficients to be positive.

from sklearn.linear_model import LogisticRegression
    cross-entropy loss (not a parameter, just an explanation): Now, cross-entropy loss is like a score that tells you how well you drew that line. If your line is really good at separating the red balls from the blue balls, your score is low, which is what you want. But if your line is not so good and mixes up where the red and blue balls are, your score is high, which is not good.
    penalty: l2; None, l2, l1, elasticnet (both l1 and l2 penalty terms are added).
    dual: False.
        If you set "dual" to "True," it's like wearing one pair of glasses that might work better when you have more features (or things to look at). But if you set it to "False," it's like wearing a different pair of glasses that might work better when you have a lot of samples (or examples).
    tol: 1e-4; tolerance for stopping criteria.
        If you set "tol" to a small number, it means you're not willing to wait very long. You want the logistic regression to find a good solution quickly and not spend too much time trying to make it perfect.
    C: 1.0.
        When you set a small value for "C," it's like having a lenient chef who doesn't mind if the ingredients are a bit off. The model might allow more mistakes or misclassifications in the data. helps control how much the model focuses on getting everything just right versus being more flexible with mistakes.
    fit_intercept: True; specifies if a constant (bias or intercept) should be added to the decision function.
        When "fit_intercept" is set to "True," it's like having a special block at the bottom of the tower that helps keep it stable. This block represents the intercept term, which helps the model make better predictions by adjusting the height of the tower. But when "fit_intercept" is set to "False," it's like building the tower without that special block. The tower might still stand, but it might not be as stable or accurate because it doesn't have that extra support.
    intercept_scaling:  1.
        When you increase the "intercept_scaling," it's like making the target bigger. It means you're giving more importance to where the dart lands relative to the center of the target. This can be helpful if you think hitting closer to the center should count more towards your score. But if you decrease the "intercept_scaling," it's like making the target smaller. Now, hitting closer to the center doesn't matter as much, and the dart's position has less impact on your score. So, "intercept_scaling" lets you decide how much weight to give to the center of the target when making predictions.
    class_weight: None; dict or 'balanced', weights associated with classes in the form {'class_label': weight}, if not given, all classes are supposed to have weight one.
        helps logistic regression give fair consideration to different groups or classes in the data, ensuring a balanced prediction.
    random_state: None.
    solver: 'lbfgs'; liblinear, newton-cg, newton-choleski, sag, saga; algorithm to use in th eoptimization problem.
        lets you choose the best tool for building your logistic regression model, depending on the size and complexity of your data.
        - For small datasets, 'liblinear' is a good choice, whereas 'sag' and 'saga' are faster for large ones;
        - For multiclass problems, only 'newton-cg', 'sag', 'saga' and 'lbfgs' handle multinomial loss;
        - 'liblinear' is limited to one-versus-rest schemes.
        - 'newton-cholesky' is a good choice for `n_samples` >> `n_features`,
            especially with one-hot encoded categorical features with rare
            categories. Note that it is limited to binary classification and the
            one-versus-rest reduction for multiclass classification. Be aware that
            the memory usage of this solver has a quadratic dependency on
            `n_features` because it explicitly computes the Hessian matrix.
    max_iter: 100; maximum number of iterations taken for solvers to converge.
    multi_class: auto; auto, ovr, multinomial.
        helps you decide how to handle multiple classes in your logistic regression model, whether by treating each class independently (one-vs-rest) or considering them all together (multinomial).
    verbose: 0.
        When verbose is set to a higher number (e.g., verbose=1 or verbose=2): The model will print out more details about what's happening during the training process. This can be helpful if you want to see progress updates and understand how the model is working step-by-step.
    warm_start: False.
        When warm_start is set to True: The model remembers the previous work and starts from where it left off. This is useful if you want to add more data or tweak the model without starting the training process from scratch.
    n_jobs: None.
        When n_jobs is set to a number: It tells the computer how many CPUs (or workers) to use for the job. For example, n_jobs=2 means using 2 CPUs to speed up the training. Setting n_jobs=-1 uses all available CPUs, making the process as fast as possible.
    l1_ratio: None.
        l1_ratio is used with the ElasticNet penalty, which is a mix of L1 (lasso) and L2 (ridge) penalties:
        When l1_ratio is closer to 1: The model uses more of the lasso penalty, which helps in selecting important features and making others exactly zero.
        When l1_ratio is closer to 0: The model uses more of the ridge penalty, which helps in spreading out the influence among all features, making them small but not zero.
        When l1_ratio is in between (like 0.5): The model balances both penalties to get the benefits of both approaches.

-------------------------------------------------------------------------------

from sklearn.svm import SVC
    verbose: Controls the amount of printed output during training. Higher numbers show more details. Options include 0, 1, 2.
    C: Controls the trade-off between a smooth decision boundary and correctly classifying training points. Larger values focus more on correct classification. Common values are 0.1, 1, 10.
    kernel: Specifies the shape of the decision boundary. Options include 'linear', 'poly', 'rbf', 'sigmoid'.
    degree: Specifies the degree of the polynomial kernel function. Used only when kernel='poly'. Common values are 2, 3, 4.
    gamma: Determines how far the influence of a single training example reaches. Common settings are 'scale', 'auto', or a float value like 0.001, 0.01.
    coef0: Independent term in kernel function for 'poly' and 'sigmoid'. Acts like a bias in the model. Common values are 0, 0.1, 1.
    probability: Enables probability estimates. Slows down training but allows the model to output probabilities. Options are True, False.
    shrinking: Uses the shrinking heuristic to speed up training. Usually set to True. Options are True, False.
    tol: Tolerance for stopping criteria. Smaller values make the model more precise but slower to converge. Common values are 0.001, 0.01, 0.1.
    class_weight: Balances the weights of different classes. Useful for handling imbalanced datasets. Options are 'balanced' or a dictionary like {0: 1, 1: 10}.
    max_iter: Limits the number of iterations. -1 means no limit, allowing the model to run until convergence. Common values are 100, 1000, -1.

from sklearn.svm import SVR
    verbose: Controls the amount of printed output during training. Higher numbers show more details. Options include 0, 1, 2.
    C: Controls the trade-off between a smooth decision boundary and correctly fitting training data. Larger values focus more on minimizing errors. Common values are 0.1, 1, 10.
    kernel: Specifies the shape of the decision boundary. Options include 'linear', 'poly', 'rbf', 'sigmoid'.
    degree: Specifies the degree of the polynomial kernel function. Used only when kernel='poly'. Common values are 2, 3, 4.
    gamma: Determines how far the influence of a single training example reaches. Common settings are 'scale', 'auto', or a float value like 0.001, 0.01.
    coef0: Independent term in kernel function for 'poly' and 'sigmoid'. Acts like a bias in the model. Common values are 0, 0.1, 1.
    shrinking: Uses the shrinking heuristic to speed up training. Usually set to True. Options are True, False.
    tol: Tolerance for stopping criteria. Smaller values make the model more precise but slower to converge. Common values are 0.001, 0.01, 0.1.
    epsilon: Specifies the epsilon-tube within which no penalty is associated in the training loss function with points predicted within a distance epsilon from the actual value. Common values are 0.1, 0.2, 0.5.
    max_iter: Limits the number of iterations. -1 means no limit, allowing the model to run until convergence. Common values are 100, 1000, -1.

-------------------------------------------------------------------------------

from sklearn.tree import DecisionTreeClassifier
    criterion: The function to measure the quality of a split. Options include 'gini' for Gini impurity and 'entropy' for information gain.
    splitter: The strategy used to choose the split at each node. Options are 'best' to choose the best split and 'random' to choose a random split.
    max_depth: The maximum depth of the tree. Common values are None for no limit, or an integer like 5, 10, 20.
    min_samples_split: The minimum number of samples required to split an internal node. Common values are 2, 10, 20.
    min_samples_leaf: The minimum number of samples required to be at a leaf node. Common values are 1, 5, 10.
    min_weight_fraction_leaf: The minimum weighted fraction of the sum total of weights required to be at a leaf node. Common values are 0.0, 0.1, 0.2.
    max_features: The number of features to consider when looking for the best split. Options include None, 'auto', 'sqrt', 'log2', or an integer.
    random_state: Controls the randomness of the estimator. Can be an integer for reproducible results or None for random.
    max_leaf_nodes: Grow a tree with max_leaf_nodes in best-first fashion. Common values are None for unlimited, or an integer like 10, 20, 100.
    min_impurity_decrease: A node will be split if this split induces a decrease of the impurity greater than or equal to this value. Common values are 0.0, 0.1, 0.2.
    class_weight: Weights associated with classes. Useful for handling imbalanced datasets. Options are None, 'balanced', or a dictionary like {0: 1, 1: 10}.
    ccp_alpha: Complexity parameter used for Minimal Cost-Complexity Pruning. The larger the value, the more the tree is pruned. Common values are 0.0, 0.1, 0.2.

from sklearn.tree import DecisionTreeRegressor
    criterion: The function to measure the quality of a split. Options include 'mse' for mean squared error, 'friedman_mse' for Friedman’s improvement score, and 'mae' for mean absolute error.
    splitter: The strategy used to choose the split at each node. Options are 'best' to choose the best split and 'random' to choose a random split.
    max_depth: The maximum depth of the tree. Common values are None for no limit, or an integer like 5, 10, 20.
    min_samples_split: The minimum number of samples required to split an internal node. Common values are 2, 10, 20.
    min_samples_leaf: The minimum number of samples required to be at a leaf node. Common values are 1, 5, 10.
    min_weight_fraction_leaf: The minimum weighted fraction of the sum total of weights required to be at a leaf node. Common values are 0.0, 0.1, 0.2.
    max_features: The number of features to consider when looking for the best split. Options include None, 'auto', 'sqrt', 'log2', or an integer.
    random_state: Controls the randomness of the estimator. Can be an integer for reproducible results or None for random.
    max_leaf_nodes: Grow a tree with max_leaf_nodes in best-first fashion. Common values are None for unlimited, or an integer like 10, 20, 100.
    min_impurity_decrease: A node will be split if this split induces a decrease of the impurity greater than or equal to this value. Common values are 0.0, 0.1, 0.2.
    ccp_alpha: Complexity parameter used for Minimal Cost-Complexity Pruning. The larger the value, the more the tree is pruned. Common values are 0.0, 0.1, 0.2.

-------------------------------------------------------------------------------

from sklearn.ensemble import GradientBoostingRegressor
    loss: The loss function to be optimized. Options include 'ls' for least squares regression, 'lad' for least absolute deviation, 'huber' for Huber loss, 'quantile' for quantile regression.
    learning_rate: The shrinkage parameter to control the contribution of each tree. Common values are 0.1, 0.01, 0.001.
    n_estimators: The number of boosting stages (trees) to be used. Common values are 100, 500, 1000.
    subsample: The fraction of samples to be used for fitting the individual base learners. Common values are 0.5, 0.8, 1.0.
    criterion: The function to measure the quality of a split. Options include 'friedman_mse' for Friedman’s improvement score, 'mse' for mean squared error, 'mae' for mean absolute error.
    min_samples_split: The minimum number of samples required to split an internal node. Common values are 2, 5, 10.
    min_samples_leaf: The minimum number of samples required to be at a leaf node. Common values are 1, 2, 5.
    min_weight_fraction_leaf: The minimum weighted fraction of the sum total of weights required to be at a leaf node. Common values are 0.0, 0.1, 0.2.
    max_depth: The maximum depth of the individual regression estimators. Common values are None for no limit, or an integer like 3, 5, 10.
    min_impurity_decrease: A node will be split if this split induces a decrease of the impurity greater than or equal to this value. Common values are 0.0, 0.1, 0.2.
    max_features: The number of features to consider when looking for the best split. Options include 'auto', 'sqrt', 'log2', or an integer.
    alpha: The L1 regularization term on weights. Common values are 0.0, 0.1, 0.5.
    random_state: Controls the randomness of the estimator. Can be an integer for reproducible results or None for random.

from sklearn.ensemble import GradientBoostingClassifier
    loss: The loss function to be optimized. Options include 'deviance' for logistic regression with probabilistic outputs, 'exponential' for AdaBoost.
    learning_rate: The shrinkage parameter to control the contribution of each tree. Common values are 0.1, 0.01, 0.001.
    n_estimators: The number of boosting stages (trees) to be used. Common values are 100, 500, 1000.
    subsample: The fraction of samples to be used for fitting the individual base learners. Common values are 0.5, 0.8, 1.0.
    criterion: The function to measure the quality of a split. Options include 'friedman_mse' for Friedman’s improvement score, 'mse' for mean squared error, 'mae' for mean absolute error.
    min_samples_split: The minimum number of samples required to split an internal node. Common values are 2, 5, 10.
    min_samples_leaf: The minimum number of samples required to be at a leaf node. Common values are 1, 2, 5.
    min_weight_fraction_leaf: The minimum weighted fraction of the sum total of weights required to be at a leaf node. Common values are 0.0, 0.1, 0.2.
    max_depth: The maximum depth of the individual regression estimators. Common values are None for no limit, or an integer like 3, 5, 10.
    min_impurity_decrease: A node will be split if this split induces a decrease of the impurity greater than or equal to this value. Common values are 0.0, 0.1, 0.2.
    max_features: The number of features to consider when looking for the best split. Options include 'auto', 'sqrt', 'log2', or an integer.
    random_state: Controls the randomness of the estimator. Can be an integer for reproducible results or None for random.
    alpha: The L1 regularization term on weights. Common values are 0.0, 0.1, 0.5.
    verbose: Controls the amount of printed output during training. Higher numbers show more details. Options include 0, 1, 2.
    max_leaf_nodes: Grow a tree with max_leaf_nodes in best-first fashion. Common values are None for unlimited, or an integer like 10, 20, 100.

from sklearn.ensemble import RandomForestClassifier
    n_estimators: The number of trees in the forest. Common values are 100, 500, 1000.
    criterion: The function to measure the quality of a split. Options include 'gini' for Gini impurity and 'entropy' for information gain.
    max_depth: The maximum depth of the trees. Common values are None for no limit, or an integer like 5, 10, 20.
    min_samples_split: The minimum number of samples required to split an internal node. Common values are 2, 5, 10.
    min_samples_leaf: The minimum number of samples required to be at a leaf node. Common values are 1, 2, 5.
    min_weight_fraction_leaf: The minimum weighted fraction of the sum total of weights required to be at a leaf node. Common values are 0.0, 0.1, 0.2.
    max_features: The number of features to consider when looking for the best split. Options include 'auto', 'sqrt', 'log2', or an integer.
    max_leaf_nodes: Grow trees with max_leaf_nodes in best-first fashion. Common values are None for unlimited, or an integer like 10, 20, 100.
    min_impurity_decrease: A node will be split if this split induces a decrease of the impurity greater than or equal to this value. Common values are 0.0, 0.1, 0.2.
    bootstrap: Whether bootstrap samples are used when building trees. Options are True or False.
    oob_score: Whether to use out-of-bag samples to estimate the generalization accuracy. Options are True or False.
    random_state: Controls the randomness of the estimator. Can be an integer for reproducible results or None for random.
    verbose: Controls the amount of printed output during training. Higher numbers show more details. Options include 0, 1, 2.
    class_weight: Weights associated with classes. Useful for handling imbalanced datasets. Options are None, 'balanced', or a dictionary like {0: 1, 1: 10}.

from sklearn.ensemble import RandomForestRegressor
    n_estimators: The number of trees in the forest. Common values are 100, 500, 1000.
    criterion: The function to measure the quality of a split. Options include 'mse' for mean squared error and 'mae' for mean absolute error.
    max_depth: The maximum depth of the trees. Common values are None for no limit, or an integer like 5, 10, 20.
    min_samples_split: The minimum number of samples required to split an internal node. Common values are 2, 5, 10.
    min_samples_leaf: The minimum number of samples required to be at a leaf node. Common values are 1, 2, 5.
    min_weight_fraction_leaf: The minimum weighted fraction of the sum total of weights required to be at a leaf node. Common values are 0.0, 0.1, 0.2.
    max_features: The number of features to consider when looking for the best split. Options include 'auto', 'sqrt', 'log2', or an integer.
    max_leaf_nodes: Grow trees with max_leaf_nodes in best-first fashion. Common values are None for unlimited, or an integer like 10, 20, 100.
    min_impurity_decrease: A node will be split if this split induces a decrease of the impurity greater than or equal to this value. Common values are 0.0, 0.1, 0.2.
    bootstrap: Whether bootstrap samples are used when building trees. Options are True or False.
    oob_score: Whether to use out-of-bag samples to estimate the generalization accuracy. Options are True or False.
    random_state: Controls the randomness of the estimator. Can be an integer for reproducible results or None for random.
    verbose: Controls the amount of printed output during training. Higher numbers show more details. Options include 0, 1, 2.

from sklearn.ensemble import BaggingRegressor
    base_estimator: The base estimator to fit on random subsets of the dataset. Commonly used estimators include DecisionTreeRegressor, RandomForestRegressor, etc.
    n_estimators: The number of base estimators (trees) to be used. Common values are 100, 500, 1000.
    max_samples: The number of samples to draw from X to train each base estimator. Common values are 0.5, 0.8, 1.0.
    max_features: The number of features to draw from X to train each base estimator. Options include 'auto', 'sqrt', 'log2', or an integer.
    bootstrap: Whether bootstrap samples are used when building base estimators. Options are True or False.
    bootstrap_features: Whether features are drawn with replacement when building base estimators. Options are True or False.
    oob_score: Whether to use out-of-bag samples to estimate the generalization accuracy. Options are True or False.
    warm_start: When set to True, reuse the solution of the previous call to fit and add more estimators to the ensemble.
    n_jobs: The number of jobs to run in parallel for both fit and predict. -1 means using all processors.
    random_state: Controls the randomness of the estimator. Can be an integer for reproducible results or None for random.
    verbose: Controls the amount of printed output during training. Higher numbers show more details. Options include 0, 1, 2.

from sklearn.ensemble import BaggingClassifier
    base_estimator: The base estimator to fit on random subsets of the dataset. Commonly used estimators include DecisionTreeClassifier, RandomForestClassifier, etc.
    n_estimators: The number of base estimators (trees) to be used. Common values are 100, 500, 1000.
    max_samples: The number of samples to draw from X to train each base estimator. Common values are 0.5, 0.8, 1.0.
    max_features: The number of features to draw from X to train each base estimator. Options include 'auto', 'sqrt', 'log2', or an integer.
    bootstrap: Whether bootstrap samples are used when building base estimators. Options are True or False.
    bootstrap_features: Whether features are drawn with replacement when building base estimators. Options are True or False.
    oob_score: Whether to use out-of-bag samples to estimate the generalization accuracy. Options are True or False.
    warm_start: When set to True, reuse the solution of the previous call to fit and add more estimators to the ensemble.
    n_jobs: The number of jobs to run in parallel for both fit and predict. -1 means using all processors.
    random_state: Controls the randomness of the estimator. Can be an integer for reproducible results or None for random.
    verbose: Controls the amount of printed output during training. Higher numbers show more details. Options include 0, 1, 2.

-------------------------------------------------------------------------------

from sklearn.cluster import KMeans
    n_clusters: The number of clusters to form. Common values are determined based on domain knowledge or using techniques like the elbow method.
    init: The method used to initialize centroids. Options include 'k-means++' for smart initialization or 'random' for random initialization.
    n_init: The number of times the algorithm will be run with different centroid seeds. The final results will be the best output of n_init consecutive runs in terms of inertia.
    max_iter: The maximum number of iterations for each run.
    tol: The relative tolerance with regards to inertia to declare convergence.
    algorithm: The algorithm used to compute the centroids. Options include 'auto', 'full', 'elkan'.
    random_state: Controls the randomness of the algorithm. Can be an integer for reproducible results or None for random.
    n_jobs: The number of jobs to run in parallel. -1 means using all processors.

from sklearn.cluster import DBSCAN
    eps: The maximum distance between two samples for them to be considered as in the same neighborhood. Common values depend on the dataset and need experimentation.
    min_samples: The number of samples in a neighborhood for a point to be considered as a core point. Common values are determined based on the density of the dataset.
    metric: The distance metric used to measure distance between points. Options include 'euclidean', 'manhattan', 'cosine', etc.
    metric_params: Additional keyword arguments for the metric function.
    algorithm: The algorithm used to compute nearest neighbors. Options include 'auto', 'ball_tree', 'kd_tree', 'brute'.
    leaf_size: Leaf size passed to BallTree or KDTree.
    p: The power parameter for the Minkowski metric.
    n_jobs: The number of parallel jobs to run. -1 means using all processors.

-------------------------------------------------------------------------------

from sklearn.impute import SimpleImputer
    missing_values: The placeholder for missing values. Common values include np.nan, 0, etc.
    strategy: The imputation strategy. Options include 'mean', 'median', 'most_frequent', 'constant'.
    fill_value: The value used to replace missing values when strategy='constant'.
    verbose: Controls the amount of printed output during imputation. Higher numbers show more details. Options include 0, 1, 2.
    copy: Whether to create a copy of the data. If False, imputation will be done in-place.

-------------------------------------------------------------------------------

from sklearn.feature_extraction.text import CountVectorization
    input: The input data to be vectorized. It can be 'content' for a sequence of strings, 'filename' to read the input from the given file path, or 'file' to read from the given file object.
    encoding: The encoding to use when reading from files. Common values include 'utf-8', 'latin-1', etc.
    decode_error: Specifies what to do if encountering decoding errors. Options include 'strict', 'ignore', 'replace'.
    strip_accents: Whether to remove accents and perform Unicode normalization. Options include 'ascii', 'unicode', None.
    lowercase: Whether to convert all characters to lowercase before tokenizing.
    preprocessor: Custom pre-processing function applied to each document prior to tokenization and encoding.
    tokenizer: Custom tokenizer for tokenization. If None, default tokenizer is used.
    stop_words: Specifies stop words to be removed during tokenization. Options include 'english', a list of words, or None.
    token_pattern: Regular expression pattern for tokenization.
    ngram_range: Specifies the lower and upper boundary of the range of n-values for different n-grams to be extracted.
    max_df: Specifies the maximum document frequency of terms to be included in the vocabulary.
    min_df: Specifies the minimum document frequency of terms to be included in the vocabulary.
    max_features: Limits the number of features to be extracted.
    vocabulary: Custom vocabulary mapping.
    binary: Whether to use binary encoding instead of frequency counts.

-------------------------------------------------------------------------------

from sklearn.neighbors import KNeighborsClassifier
    n_neighbors: The number of neighbors to use for classification. Common values are integers like 3, 5, 10.
    weights: The weight function used in prediction. Options include 'uniform' for all points in each neighborhood to be weighted equally, or 'distance' for points to be weighted by the inverse of their distance.
    algorithm: The algorithm used to compute the nearest neighbors. Options include 'auto', 'ball_tree', 'kd_tree', 'brute'.
    leaf_size: Leaf size passed to BallTree or KDTree.
    p: The power parameter for the Minkowski metric.
    metric: The distance metric used to measure distance between points. Options include 'euclidean', 'manhattan', 'chebyshev', 'minkowski', etc.
    metric_params: Additional keyword arguments for the metric function.
    n_jobs: The number of parallel jobs to run. -1 means using all processors.

from sklearn.neighbors import KNeighborsRegressor
    n_neighbors: The number of neighbors to use for regression. Common values are integers like 3, 5, 10.
    weights: The weight function used in prediction. Options include 'uniform' for all points in each neighborhood to be weighted equally, or 'distance' for points to be weighted by the inverse of their distance.
    algorithm: The algorithm used to compute the nearest neighbors. Options include 'auto', 'ball_tree', 'kd_tree', 'brute'.
    leaf_size: Leaf size passed to BallTree or KDTree.
    p: The power parameter for the Minkowski metric.
    metric: The distance metric used to measure distance between points. Options include 'euclidean', 'manhattan', 'chebyshev', 'minkowski', etc.
    metric_params: Additional keyword arguments for the metric function.
    n_jobs: The number of parallel jobs to run. -1 means using all processors.

-------------------------------------------------------------------------------

from sklearn.naive_bayes import GaussianNB
    priors: Prior probabilities of the classes. If specified, the priors are not adjusted based on the data.
    var_smoothing: Portion of the largest variance of all features added to variances for calculation stability. Common values are small positive numbers like 1e-9, 1e-10.

from sklearn.naive_bayes import BernoulliNB
    alpha: Additive (Laplace/Lidstone) smoothing parameter. Common values are small positive numbers like 1.0, 0.1, 0.01.
    binarize: Threshold for binarizing (mapping to 0 or 1) of sample features. If None, no binarization is performed.
    fit_prior: Whether to learn class prior probabilities from the data. If False, a uniform prior will be used.
    class_prior: Prior probabilities of the classes. If specified, the priors are not adjusted based on the data.

-------------------------------------------------------------------------------

from sklearn.decomposition import PCA
    n_components: The number of components to keep. If None, all components are kept.
    whiten: Whether to whiten the data. Whitening removes the mean and scales the data to have a unit variance.
    svd_solver: The solver to use for the computation of the principal components. Options include 'auto', 'full', 'arpack', 'randomized'.
    tol: Tolerance for singular values if svd_solver='arpack'.
    iterated_power: Number of iterations for the power method if svd_solver='randomized'.
    random_state: Controls the randomness of the estimator. Can be an integer for reproducible results or None for random.

-------------------------------------------------------------------------------

from sklearn.metrics import accuracy_score
    y_true: The true labels or ground truth.
    y_pred: The predicted labels.

from sklearn.metrics import confusion_matrix
    y_true: The true labels or ground truth.
    y_pred: The predicted labels.

from sklearn.metrics import classification_metrics
    y_true: The true labels or ground truth.
    y_pred: The predicted labels.
    labels: The set of labels to include when calculating metrics. If None, metrics are calculated for all labels in y_true and y_pred.
    sample_weight: Sample weights used when calculating metrics. It can be None (default) or an array-like of shape (n_samples,) containing the weight for each sample.
    average: The averaging strategy used for multiclass classification. Options include 'micro', 'macro', 'weighted', or None.
    zero_division: Value to use for division when there is 0 precision or recall. It can be 'warn', 0, or 'raise'.

from sklearn.metrics import classification_report
    y_true: The true labels or ground truth.
    y_pred: The predicted labels.
    labels: The set of labels to include when calculating metrics. If None, metrics are calculated for all labels in y_true and y_pred.
    target_names: Optional display names matching the labels.
    sample_weight: Sample weights used when calculating metrics. It can be None (default) or an array-like of shape (n_samples,) containing the weight for each sample.
    digits: Number of digits for formatting output floating point values.
    output_dict: If True, the return value will be a dictionary of the classification report. Otherwise, it will be a string.
    zero_division: Value to use for division when there is 0 precision or recall. It can be 'warn', 0, or 'raise'.

from sklearn.metrics import f1_score
    y_true: The true labels or ground truth.
    y_pred: The predicted labels.
    labels: The set of labels to include when calculating metrics. If None, metrics are calculated for all labels in y_true and y_pred.
    average: The averaging strategy used for multiclass classification. Options include 'micro', 'macro', 'weighted', or None.
    sample_weight: Sample weights used when calculating metrics. It can be None (default) or an array-like of shape (n_samples,) containing the weight for each sample.
    zero_division: Value to use for division when there is 0 precision or recall. It can be 'warn', 0, or 'raise'.

from sklearn.metrics import r2_score
    y_true: The true target values.
    y_pred: The predicted target values.
    sample_weight: Sample weights used when calculating metrics. It can be None (default) or an array-like of shape (n_samples,) containing the weight for each sample.
    multioutput: Defines aggregating of multiple output scores. Options include 'raw_values', 'uniform_average', 'variance_weighted'. If 'raw_values', returns individual scores for each output. If 'uniform_average', computes the unweighted mean across all outputs. If 'variance_weighted', computes the mean squared error weighted by the variance of each individual output.
    squared: Whether to compute the squared error. Default is True.

from sklearn.metrics import mean_absolute_error
    y_true: The true target values.
    y_pred: The predicted target values.
    sample_weight: Sample weights used when calculating metrics. It can be None (default) or an array-like of shape (n_samples,) containing the weight for each sample.

from sklearn.metrics import mean_squared_error
    y_true: The true target values.
    y_pred: The predicted target values.
    sample_weight: Sample weights used when calculating metrics. It can be None (default) or an array-like of shape (n_samples,) containing the weight for each sample.
    squared: Whether to compute the squared error. Default is True.

from sklearn.metrics import precision_score
    y_true: The true labels or ground truth.
    y_pred: The predicted labels.
    labels: The set of labels to include when calculating metrics. If None, metrics are calculated for all labels in y_true and y_pred.
    pos_label: The class to report if average='binary' and the data is binary. If None, the positive label will be determined automatically.
    average: The averaging strategy used for multiclass classification. Options include 'micro', 'macro', 'weighted', 'samples', or None.
    sample_weight: Sample weights used when calculating metrics. It can be None (default) or an array-like of shape (n_samples,) containing the weight for each sample.
    zero_division: Value to use for division when there is 0 precision or recall. It can be 'warn', 0, or 'raise'.

from sklearn.metrics import recall_score
    y_true: The true labels or ground truth.
    y_pred: The predicted labels.
    labels: The set of labels to include when calculating metrics. If None, metrics are calculated for all labels in y_true and y_pred.
    pos_label: The class to report if average='binary' and the data is binary. If None, the positive label will be determined automatically.
    average: The averaging strategy used for multiclass classification. Options include 'micro', 'macro', 'weighted', 'samples', or None.
    sample_weight: Sample weights used when calculating metrics. It can be None (default) or an array-like of shape (n_samples,) containing the weight for each sample.
    zero_division: Value to use for division when there is 0 precision or recall. It can be 'warn', 0, or 'raise'.

-------------------------------------------------------------------------------

from sklearn.preprocessing import RobusrtScaler
    with_centering: Whether to center the data before scaling. Default is True.
    with_scaling: Whether to scale the data after centering. Default is True.
    quantile_range: Tuple (q_min, q_max) where q_min and q_max are floats representing the lower and upper quantile range for the scaling. Default is (25.0, 75.0).
    copy: Whether to make a copy of the input data. Default is True.

from sklearn.preprocessing import StandardScaler
    copy: Whether to make a copy of the input data. Default is True.
    with_mean: Whether to center the data before scaling. Default is True.
    with_std: Whether to scale the data to unit variance. Default is True.

from sklearn.preprocessing import MinMaxScaler
    feature_range: Tuple (min, max) specifying the range of transformed features. Default is (0, 1).
    copy: Whether to make a copy of the input data. Default is True.

from sklearn.preprocessing import MaxAbsScaler
    copy: Whether to make a copy of the input data. Default is True.

from sklearn.preprocessing import RobustScaler
    with_centering: Whether to center the data before scaling. Default is True.
    with_scaling: Whether to scale the data after centering. Default is True.
    quantile_range: Tuple (q_min, q_max) representing the lower and upper quantile range for the scaling. Default is (25.0, 75.0).
    copy: Whether to make a copy of the input data. Default is True.

from sklearn.preprocessing import Normalizer
    norm: The normalization norm to use. Options include 'l1', 'l2', 'max', or None. Default is 'l2'.
    copy: Whether to make a copy of the input data. Default is True.

from sklearn.preprocessing import OneHotEncoding
    categories: Specifies the categories of each feature. If 'auto', categories will be inferred automatically. Default is 'auto'.
    drop: Whether to drop one of the categories for each feature to avoid collinearity. Default is 'first'.
    sparse: Whether to return sparse matrix. Default is True. If set to False, the output will be a dense array.
    dtype: Data type of the output array. Default is numpy.float64.

from sklearn.preprocessing import LabelEncoder
    None.

from sklearn.preprocessing import OrdinalEncoder
    categories: Specifies the categories of each feature. If 'auto', categories will be inferred automatically. Default is 'auto'.
    dtype: Data type of the output array. Default is numpy.float64.
    handle_unknown: Specifies how to handle unknown categories. Options include 'error', 'use_encoded_value', or 'ignore'. Default is 'error'.
    unknown_value: The value to use for unknown categories if handle_unknown='use_encoded_value'. Default is np.nan.

from sklearn.preprocessing import LabelBinarizer
    neg_label: The value to represent the negative class. Default is 0.
    pos_label: The value to represent the positive class. Default is 1.
    sparse_output: Whether to return a sparse matrix. Default is False. If set to True, the output will be a sparse matrix in CSR format.

from sklearn.preprocessing import MultiLabelBinarizer
    classes: The explicit classes to use for binarization. If None, classes will be inferred from the input data. Default is None.
    sparse_output: Whether to return a sparse matrix. Default is False. If set to True, the output will be a sparse matrix in CSR format.

from sklearn.preprocessing import FunctionTransformer
    func: The function to apply to the data. This function should accept and return 2D arrays. It can also be set to 'log' to apply natural logarithm transformation or 'exp' to apply exponential transformation.
    inverse_func: The inverse function to apply to the transformed data. If None, the inverse transformation is not available.
    validate: Whether to validate input array X before applying the function. Default is False.

-------------------------------------------------------------------------------

from sklearn.model_selection import KFold
    n_splits: The number of folds. Default is 5.
    shuffle: Whether to shuffle the data before splitting into folds. Default is False.
    random_state: Controls the randomness of the shuffling. Default is None.
    fold_generator: An optional function that generates the train/test indices for each fold. If None, the default KFold splitter will be used.

from sklearn.model_selection import ShuffleSplit
    n_splits: The number of re-shuffling & splitting iterations. Default is 10.
    test_size: The proportion of the dataset to include in the test split. It can be an integer (number of samples) or float (proportion of the dataset). Default is 0.1.
    train_size: The proportion of the dataset to include in the train split. It can be an integer (number of samples) or float (proportion of the dataset). Default is None, which means the complement of the test_size.
    random_state: Controls the randomness of the splitting. Default is None.

from sklearn.model_selection import GroupShuffleSplit
    n_splits: The number of re-shuffling & splitting iterations. Default is 10.
    test_size: The proportion of the dataset to include in the test split. It can be an integer (number of samples) or float (proportion of the dataset). Default is 0.1.
    train_size: The proportion of the dataset to include in the train split. It can be an integer (number of samples) or float (proportion of the dataset). Default is None, which means the complement of the test_size.
    random_state: Controls the randomness of the splitting. Default is None.
    groups: The group labels for the samples. Each group will be split separately.

from sklearn.model_selection import TimeSeriesSplit
    n_splits: The number of splits. Default is 5.
    max_train_size: The maximum size of the training set. Default is None, which means it will be set to the size of the training set in the first split.
    test_size: The size of the test set. Default is None, which means it will be set to the size of the training set in the next split.
    gap: The gap between train and test. Default is 0.

from sklearn.model_selection import GridSearchCV
    estimator: The estimator object. This is assumed to implement the scikit-learn estimator interface. Either estimator needs to provide a score function, or scoring must be passed.
    param_grid: The parameter grid as a dictionary or list of dictionaries. Each dictionary maps parameter names to sequences of values to search over.
    scoring: The scoring method to use for evaluation. This can be a string (e.g., 'accuracy', 'precision', 'recall') or a callable that returns a scalar score. Default is None.
    cv: The cross-validation strategy. This can be an integer (e.g., 5 for 5-fold cross-validation) or a cross-validation splitter object. Default is 5-fold cross-validation.
    n_jobs: The number of parallel jobs to run. Default is 1.
    verbose: Controls the verbosity: the higher, the more messages. Default is 0.
    refit: Whether to refit the best estimator on the whole dataset. Default is True.

from sklearn.model_selection import RandomizedSearchCV
    estimator: The estimator object. This is assumed to implement the scikit-learn estimator interface. Either estimator needs to provide a score function, or scoring must be passed.
    param_distributions: The parameter distributions as a dictionary or list of dictionaries. Each dictionary maps parameter names to distributions or lists of parameters to sample from.
    n_iter: The number of parameter settings that are sampled. Default is 10.
    scoring: The scoring method to use for evaluation. This can be a string (e.g., 'accuracy', 'precision', 'recall') or a callable that returns a scalar score. Default is None.
    n_jobs: The number of parallel jobs to run. Default is 1.
    cv: The cross-validation strategy. This can be an integer (e.g., 5 for 5-fold cross-validation) or a cross-validation splitter object. Default is 5-fold cross-validation.
    verbose: Controls the verbosity: the higher, the more messages. Default is 0.
    refit: Whether to refit the best estimator on the whole dataset. Default is True.

from sklearn.model_selection import ParameterGrid
    param_grid: The parameter grid as a dictionary or list of dictionaries. Each dictionary maps parameter names to sequences of values to search over.

from sklearn.model_selection import ParameterSampler
    param_distributions: The parameter distributions as a dictionary or list of dictionaries. Each dictionary maps parameter names to distributions or lists of parameters to sample from.
    n_iter: The number of parameter settings that are sampled. Default is 10.
    random_state: Controls the randomness of the parameter sampling. Default is None.

from sklearn.model_selection import train_test_split
    arrays: The input data arrays to be split. They can be lists, numpy arrays, scipy-sparse matrices, or pandas dataframes.
    test_size: The proportion of the dataset to include in the test split. It can be an integer (number of samples) or float (proportion of the dataset). Default is 0.25.
    train_size: The proportion of the dataset to include in the train split. It can be an integer (number of samples) or float (proportion of the dataset). Default is None, which means the complement of the test_size.
    random_state: Controls the randomness of the splitting. Default is None.

from sklearn.model_selection import cross_val_score
    estimator: The estimator object. This is assumed to implement the scikit-learn estimator interface.
    X: The feature matrix.
    y: The target values.
    groups: The group labels for the samples. Each group will be used for splitting the dataset in cross-validation.
    scoring: The scoring method to use for evaluation. This can be a string (e.g., 'accuracy', 'precision', 'recall') or a callable that returns a scalar score.
    cv: The cross-validation strategy. This can be an integer (e.g., 5 for 5-fold cross-validation) or a cross-validation splitter object.
    n_jobs: The number of parallel jobs to run. Default is 1.
    verbose: Controls the verbosity: the higher, the more messages. Default is 0.
    fit_params: Additional parameters to pass to the fit method of the estimator.

from sklearn.model_selection import cross_val_predict
    estimator: The estimator object. This is assumed to implement the scikit-learn estimator interface.
    X: The feature matrix.
    y: The target values.
    groups: The group labels for the samples. Each group will be used for splitting the dataset in cross-validation.
    cv: The cross-validation strategy. This can be an integer (e.g., 5 for 5-fold cross-validation) or a cross-validation splitter object.
    n_jobs: The number of parallel jobs to run. Default is 1.

from sklearn.model_selection import cross_validate
    estimator: The estimator object. This is assumed to implement the scikit-learn estimator interface.
    X: The feature matrix.
    y: The target values.
    groups: The group labels for the samples. Each group will be used for splitting the dataset in cross-validation.
    scoring: The scoring method(s) to use for evaluation. This can be a string (e.g., 'accuracy', 'precision', 'recall') or a list of strings.
    cv: The cross-validation strategy. This can be an integer (e.g., 5 for 5-fold cross-validation) or a cross-validation splitter object.
    n_jobs: The number of parallel jobs to run. Default is 1.
    verbose: Controls the verbosity: the higher, the more messages. Default is 0.
    fit_params: Additional parameters to pass to the fit method of the estimator.

from sklearn.model_selection import validation_curve
    estimator: The estimator object. This is assumed to implement the scikit-learn estimator interface.
    X: The feature matrix.
    y: The target values.
    param_name: The name of the parameter to vary.
    param_range: The range of parameter values to use.
    groups: The group labels for the samples. Each group will be used for splitting the dataset in cross-validation.
    cv: The cross-validation strategy. This can be an integer (e.g., 5 for 5-fold cross-validation) or a cross-validation splitter object.
    scoring: The scoring method to use for evaluation. This can be a string (e.g., 'accuracy', 'precision', 'recall') or a callable that returns a scalar score.
    n_jobs: The number of parallel jobs to run. Default is 1.
    pre_dispatch: Controls the number of batches of parallel jobs. Default is 'all'.

from sklearn.model_selection import learning_curve
    estimator: The estimator object. This is assumed to implement the scikit-learn estimator interface.
    X: The feature matrix.
    y: The target values.
    train_sizes: The sizes of the training set to use. It can be an array-like of shape (n_ticks,) or float (proportion of the dataset).
    cv: The cross-validation strategy. This can be an integer (e.g., 5 for 5-fold cross-validation) or a cross-validation splitter object.
    scoring: The scoring method to use for evaluation. This can be a string (e.g., 'accuracy', 'precision', 'recall') or a callable that returns a scalar score.
    n_jobs: The number of parallel jobs to run. Default is 1.
    verbose: Controls the verbosity: the higher, the more messages. Default is 0.

-------------------------------------------------------------------------------

from sklearn.datasets import make_blobs
from sklearn.datasets import make_regression
from sklearn.datasets import make_classification
    n_samples: The number of samples to generate.
    n_features: The number of features (i.e., independent variables) in the dataset.
    n_classes: The number of classes (i.e., target variable categories) in the dataset.
    n_clusters_per_class: The number of clusters per class.
    weights: The proportions of samples assigned to each class. Default is None, which means all classes have equal weights.
    flip_y: The probability of flipping the class label for each sample. Default is 0.01.
    class_sep: The separation between classes. Larger values result in more separable classes.
    hypercube: If True, samples are uniformly distributed in a hypercube. If False, samples are drawn from a Gaussian distribution.
    shift: The shift applied to each class center to make the classes linearly separable. Default is 0.0.
    scale: The scale applied to each class center to make the classes linearly separable. Default is 1.0.
    shuffle: Whether to shuffle the samples. Default is True.
    random_state: Controls the randomness of the dataset generation. Default is None.
X, y = make_classification(
    n_samples,
    n_features,
    n_classes,
    n_informative,
    random_state,
)

-------------------------------------------------------------------------------
