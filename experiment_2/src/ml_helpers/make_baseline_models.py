import pandas as pd
import numpy as np

def naive(series, lag = 1):
    ''' Shifts the series by the lag '''
    pred = series.shift(lag)
    return pred

def historical_mean(series, window_size=12, horizon=1):
    ''' Shifts the series by the lag, and takes the historical mean of the shifted series '''
    
    naiive = series.shift(horizon)
    pred = naiive.rolling(window=window_size, center=False, min_periods=1).mean()
    
    return pred

def expanding_mean(series, horizon=1):
    ''' Shifts the series by the lag, and takes the expanding mean of the shifted series.
        In other words, the mean of all observations that have come before '''
    
    naiive = series.shift(horizon)
    pred = naiive.expanding(center=False, min_periods=1).mean()
    
    return pred

def exponentially_weighted_mean(series, span=12, horizon=1):
    ''' Shifts the series by the lag, and takes the exponentially weighted mean 
    of the shifted series '''
    naiive = series.shift(horizon)
    pred = naiive.ewm(span=span, ignore_na=True).mean()
    
    return pred

### CHECK THESE
def naive_plus_last_diff(series, horizon = 1):
    ''' Shifts the series by the lag, and adds this to the previous month-on-month change '''
    naiive = series.shift(horizon)
    diff   = naiive - naiive.shift(1)

    pred = naiive + diff

    return pred

def naive_plus_mean_diff(series, window_size=12, horizon = 1):
    ''' Shifts the series by the lag, and adds this to the previous month-on-month change '''
    naiive = series.shift(horizon)
    diff   = naiive - naiive.shift(1)
    mean_diff = diff.rolling(window=window_size, center=False, min_periods=1).mean()

    pred = naiive + mean_diff

    return pred