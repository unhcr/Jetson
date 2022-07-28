import numpy as np
from xgboost                 import XGBRegressor 
from sklearn.linear_model    import LinearRegression, Lasso, Ridge
from sklearn.svm             import SVR
from sklearn.neural_network  import MLPRegressor
from sklearn.ensemble        import RandomForestRegressor, AdaBoostRegressor
from sklearn.tree            import DecisionTreeRegressor

from sklearn.model_selection import TimeSeriesSplit, GridSearchCV


def make_ridge(cv):
    
    return GridSearchCV(
                Ridge(normalize=False, fit_intercept=True), #, copy_X=True),
                { 
                    'alpha': np.logspace(-10, -2, 5) 
                }, 
                cv=cv)

def make_lasso(cv):

    return GridSearchCV(
               Lasso(normalize=False, fit_intercept=True, tol=0.01, max_iter=2000), #copy_X=True), 
               { 
                   'alpha': np.logspace(-10, 0, 6) # When zero, equivalent to OLS
               },  
               cv=cv)

def make_svm(cv):

    return GridSearchCV(
                SVR(gamma='auto'),
                {    
                    'kernel'       : ['linear', 'poly', 'rbf'],
                    'degree'       : [2,3,4,5],
                    'C'            : [1, 10, 100],
                    'gamma'        : np.logspace(-2, 2, 3)
                }, 
                cv=cv)

def make_adaboost(cv):
    return GridSearchCV( 
                AdaBoostRegressor(),
                {
                    'n_estimators':   [50, 500], 
                    'learning_rate' : [0.01,0.1,1],
                    'loss' :          ['linear', 'square', 'exponential']
                    },
                cv=cv)

def make_randomforest(cv):

    return GridSearchCV(
                RandomForestRegressor(min_samples_leaf=5), 
                {  
                    'n_estimators': [100, 250, 500],
                    'max_depth'   : [5,10],
                    'max_features': ['sqrt', 'log2'],
                    #'loss'       : ['mse', 'mae'],
                    #'criterion'  :['gini', 'entropy']
                },
                 cv=cv)

def make_decisiontree(cv):
    return GridSearchCV(
                DecisionTreeRegressor(min_samples_leaf=5),  #max_depth=10
                { 
                    'criterion'   : ['mse', 'mae'],
                    'max_depth'   : [5,10],
                    'max_features': ['sqrt', 'log2']
                },
                cv=cv)


def make_perceptron(cv):
    return GridSearchCV(
                MLPRegressor(max_iter=1000), #  alpha=0.05)
                { 
                    'alpha': np.logspace(-10, -2, 5) 
                },
                cv=cv)

def make_xgboost(cv):
    return XGBRegressor(cv)








