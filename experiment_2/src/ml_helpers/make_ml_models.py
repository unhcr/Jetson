import numpy as np
from xgboost                 import XGBRegressor 
from sklearn.linear_model    import LinearRegression, Lasso, Ridge
from sklearn.svm             import SVR
from sklearn.neural_network  import MLPRegressor
from sklearn.ensemble        import RandomForestRegressor, AdaBoostRegressor
from sklearn.tree            import DecisionTreeRegressor

from sklearn.model_selection import TimeSeriesSplit, GridSearchCV


def make_ridge(cv, scoring):
    
    return GridSearchCV(
                Ridge(normalize=False, fit_intercept=True), #, copy_X=True),
                { 
                    'alpha': np.logspace(-7, 2, 10)
                }, 
                cv=cv,
                scoring=scoring)

def make_lasso(cv, scoring):

    return GridSearchCV(
               Lasso(normalize=False, fit_intercept=True, tol=0.01, max_iter=2000), #copy_X=True), 
               { 
                   'alpha': np.logspace(-10, 0, 6) # When zero, equivalent to OLS
               },  
               cv=cv,
                scoring=scoring)

def make_svm(cv, scoring):

    return GridSearchCV(
                SVR(gamma='auto'),
                {    
                    'kernel'       : ['linear', 'poly', 'rbf'],
                    'degree'       : [2,3,4,5],
                    'C'            : [1, 10, 100],
                    'gamma'        : np.logspace(-2, 2, 3)
                }, 
                cv=cv,
                scoring=scoring)

def make_adaboost(cv, scoring):
    return GridSearchCV( 
                AdaBoostRegressor(loss='square'),
                {
                    'n_estimators':   [10, 25, 50, 100, 250], 
                    'learning_rate' : [0.01, 0.03, 0.05, 0.07, 0.1], #, 0.5, 1
                    #'loss' :          ['linear', 'square', 'exponential']
                    },
                cv=cv,
                scoring=scoring)

def make_randomforest(cv, scoring):

    return GridSearchCV(
                RandomForestRegressor(min_samples_leaf=5, criterion='mse'), 
                {  
                    'n_estimators': [10, 100,  200, 300, 400, 500],
                    'max_depth'   : [None,5,10,15,20],
                    'max_features': ['sqrt', 'log2'] # None, 
                },
                 cv=cv,
                scoring=scoring)

def make_decisiontree(cv, scoring):
    
    return GridSearchCV(
                DecisionTreeRegressor(min_samples_leaf=5, criterion='mse'), 
                { 
                    'max_depth'   : [None,3,4,5,6,7,10,15,20],
                    'max_features': ['sqrt', 'log2'] # None,
                },
                cv=cv,
                scoring=scoring)


def make_perceptron(cv, scoring):
    return GridSearchCV(
                MLPRegressor(max_iter=1000), #  alpha=0.05)
                { 
                    'alpha': np.logspace(-10, -4, 7), #np.logspace(-10, -2, 5) ,
                    'hidden_layer_sizes': [ (200,), (300,)], # (25,), (50,), (100,),
                    'activation': [ 'relu'] #'logistic',
                },
                cv=cv,
                scoring=scoring)

def make_xgboost(cv, scoring):
    return GridSearchCV(
                XGBRegressor(max_iter=1000), #  alpha=0.05)
                { 
                    'n_estimators':   [10, 25, 50], #100, 250], 
                    'learning_rate' : [0.01, 0.03, 0.05, 0.07, 0.1], #[0.01, 0.05, 0.1, 0.5, 1],
                },
                cv=cv,
                scoring=scoring)







