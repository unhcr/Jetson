import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
from   statsmodels.formula.api import ols
from dateutil.relativedelta import *
import os


def make_baseline(current_month, lag, admin_level='admin1'):
    
    if admin_level=='admin1':
        admin_unit='region'
    
    # Get full range of dates
    current_month = pd.to_datetime(current_month)
    future_months = [ current_month + relativedelta(months=i) for i in range(1, lag+1)]
    
    
    ## Import data
    true = pd.read_csv(f"ml/output_data/{admin_level}_lag{lag}/true.csv", parse_dates=['date'], index_col=['date', 'region'])
    
    true.sort_values(['region', 'date'], inplace=True)
    true.columns=['true']

    # Insert extra regions and dates for three-month predictions
    regions = true.index.get_level_values(admin_unit)
    for d in future_months:
        for r in regions:
            true.ix[(d, r), :] = np.nan
            
    
    #################################
    ### Make Last Observation Carried Forward predictions
    
    true[f'locf'] = true.groupby(admin_unit)['true'].shift(lag)

    #################################
    ### Make Historical Mean (12 month) predictions

    # Get the rolling mean <- need to specify dropna=False because rolling mean is missing for future periods
    hm= true[['true']].unstack(level=admin_unit).rolling(window=12, center=False, min_periods=1).mean().stack(dropna=False)
    hm.columns = ['rolling_mean']

    # Shift it backwards
    hm[f'hm'] = hm.groupby(admin_unit)['rolling_mean'].shift(lag)
    true = true.merge(hm[[f'hm']], left_index=True, right_index=True, how='outer')

    #################################
    ### Make expanding mean predictions

    # Get the expanding mean
    em= true[['true']].unstack(level=admin_unit).expanding(min_periods=1).mean().stack()
    em.columns = ['expanding_mean']

    # Shift it backwards
    em[f'em'] = em.groupby(admin_unit)['expanding_mean'].shift(lag)
    true = true.merge(em[[f'em']], left_index=True, right_index=True, how='outer')

    #################################
    ### Make exponential weighted mean predictions

    # Get the exponentially weighted mean
    ewm= true[['true']].unstack(level=admin_unit).ewm(span=12, ignore_na=True).mean().stack()
    ewm.columns = ['exponential_mean']

    # Shift it backwards
    ewm[f'ewm'] = ewm.groupby(admin_unit)['exponential_mean'].shift(lag)
    true = true.merge(ewm[[f'ewm']], left_index=True, right_index=True, how='outer')

    #################################
    ## Export
    true.to_csv(f"ml/output_data/{admin_level}_lag{lag}/compiled_baseline.csv")
    
    
    