try:
    from sklearn.externals import joblib
except:
    import joblib
    
import pandas as pd
import numpy as np
from dateutil.relativedelta import *
from src.ml_helpers.make_baseline_models import *
from tqdm import tqdm_notebook as tqdm


def fit_baseline_models(learn_df, admin_level, horizon):
    
    sequences = learn_df['arrivals'].unstack(level='region').astype(float) #.interpolate()
    regions = learn_df.index.get_level_values('region').unique()
    
    # Initialize the dataframe for storing results
    predictions = pd.DataFrame(columns = sequences.index,
                             index = pd.MultiIndex(levels =[[],[]], 
                                                   codes =[[],[]], 
                                                   names=['model_parameters', 'region']))
    
    # For each region, fit all models
    for r in tqdm(sequences.columns):
        series = sequences[r]

        # True value
        predictions.loc[("true", r), sequences.index] = series

        # Naive 
        for lag in range(1,24):
            if lag>=horizon:
                pred = naive(series, lag)
                predictions.loc[(f"naive_{lag:02.0f}", r), pred.index] = pred

        # Historical mean
        for window in range(1,24):
            pred = historical_mean(series, window, horizon)
            predictions.loc[(f'hm_{window:02.0f}', r), pred.index] = pred


        # Exponentially weighted mean
        for span in range(1,24):
            pred = exponentially_weighted_mean(series, span, horizon)
            predictions.loc[(f'ewm_{span:02.0f}', r), pred.index] = pred

        # Expanding mean
        pred = expanding_mean(series, horizon)
        predictions.loc[('em', r), pred.index] = pred

        '''
        # Naive + diff
        pred = naive_plus_last_diff(series, 1)
        predictions.loc[('naive+lastdiff', r), pred.index] = pred


        # Naive + mean diff
        pred = naive_plus_mean_diff(series, 12, 1)
        predictions.loc[('naive+meandiff', r), pred.index] = pred
        '''

    # Ensure predictions are greater than zero
    predictions = predictions.mask(predictions<0, 0)     

    # Reshape and export
    predictions = predictions.unstack(level='region').T.sort_index()
    predictions.index = predictions.index.swaplevel()
    predictions.to_csv(f'ml/output_data/{admin_level}_lag{horizon}/results_baseline.csv')
    
    return predictions