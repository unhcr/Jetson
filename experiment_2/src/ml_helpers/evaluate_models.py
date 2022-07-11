import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from math import sqrt
from tqdm import tqdm_notebook as tqdm

from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error


def rmse(true, pred):
    return np.sqrt(mse(pred,true))

def mse(true, pred):
    return ((true-pred)**2).mean()

def mae(true,pred):
    return np.abs(true-pred).mean()

def mape(true,pred):
    return (np.abs(pred-true)/true).mean()


def evaluate_predictions(predictions, train_dates, test_dates, admin_level, horizon):
    
    # Reshape the predictions for facility
    predictions = predictions.unstack(level='date').stack(level='model_parameters')
    
    # Extract the name of the models and regions
    models  = predictions.index.get_level_values("model_parameters").unique()
    regions = predictions.index.get_level_values('region').unique().tolist()

    # Initalize a dataframe for results
    results = pd.DataFrame(columns = regions,
                          index = pd.MultiIndex(levels =[[],[],[]], 
                                                codes =[[],[],[]], 
                                                names=['model_parameters', 'metric', 'dataset']))

    ##############################
    ### Score by region - train, test, and all

    # Loop over all models+parameters and regions
    for region, model in tqdm(predictions.index):

        # Get the true and predicted series
        pred = predictions.loc[region, model]
        true = predictions.loc[region, 'true']

        # Loop over all metrics
        for metric, metricname in [(mse,  'mse'), 
                                   (rmse, 'rmse'), 
                                   (mae,  'mae'), 
                                   (mape, 'mape')]:

            # Score the full dataset, train dataset, and test dataset
            results.loc[(model, metricname, "both"),  region] = metric(true,              pred)
            results.loc[(model, metricname, "train"), region] = metric(true[train_dates], pred[train_dates])
            results.loc[(model, metricname, "test"),  region] = metric(true[test_dates],  pred[test_dates])

    ##############################
    ### Score over whole dataset - train, test, and all

    # Loop over all models+parameters
    for model in tqdm(models):

        # Get the true and predicted series; make a single series with multiple obs per date
        pred = predictions.xs(model,  level='model_parameters').stack(dropna=False).reset_index(level='region', drop=True).sort_index()
        true = predictions.xs("true", level='model_parameters').stack(dropna=False).reset_index(level='region', drop=True).sort_index()

        # Loop over all metrics
        for metric, metricname in [(mse,  'mse'), 
                                   (rmse, 'rmse'), 
                                   (mae,  'mae'), 
                                   (mape, 'mape')]:

            # Score the full dataset, train dataset, and test dataset
            results.loc[(model, metricname, "both"),  'all' ] = metric(true,              pred)
            results.loc[(model, metricname, "train"), 'all' ] = metric(true[train_dates], pred[train_dates])
            results.loc[(model, metricname, "test"), 'all'  ] = metric(true[test_dates],  pred[test_dates])
        
    results.to_csv(f"ml/results/{admin_level}_lag{horizon}/scored_baseline_models.csv")
    return results