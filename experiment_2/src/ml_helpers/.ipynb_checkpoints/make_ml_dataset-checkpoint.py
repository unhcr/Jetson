import pandas as pd
import numpy as np
from dateutil.relativedelta import *
import os


def make_ml_dataset(df, current_month, lag=3, admin_level='admin1', shifts=[3,4,5,6,12]):
    
    ################################
    ### Read in the data
    df = pd.read_csv(f"data/compiled/master_{admin_level}.csv", parse_dates=['date'], index_col=['date', 'region'])
    
    if admin_level=='admin1':
        admin_unit='region'

    ################################
    ### Set up the month lags
    
    # Get list of current and future months
    current_month = pd.to_datetime(current_month)
    future_months = [ current_month + relativedelta(months=i) for i in range(1, lag+1)]
    
    # Insert extra regions and dates for lagged predictions
    regions = df.index.get_level_values(admin_unit)

    for d in future_months:
        for r in regions:
            df.ix[(d, r), :] = np.nan
            
    # df.dropna(subset=['arrivals'], inplace=True)
    df.sort_index(inplace=True)
    
    ################################
    ### Create features
    constant_cols     = ['distance_straight', 
                         'shared_border',
                         'distance_driving_km', 
                         'distance_driving_hr'] #i for i in df.columns if "riverlevel" in i or 'distance' in i or 'shared_border' in i]
    river_cols        = [i for i in df.columns if "river_" in i ]
    varying_cols      = [i for i in df.columns if i not in constant_cols and i not in river_cols]
    
    ################################
    ### First, add features that don't need to be shifted

    # Initialize dataframe with constant columns
    learn_df = df[['arrivals']].copy()

    # One-hot encode the regions and months
    learn_df['region_dummies'] = learn_df.index.get_level_values(admin_unit).astype(str)
    learn_df['month_dummies']  = learn_df.index.get_level_values('date'  ).month.astype(str)
    learn_df = pd.get_dummies(learn_df)

    # Linear time var
    learn_df['months_since_2010'] = (learn_df.index.get_level_values('date').to_period('M') - 
                                                pd.to_datetime('2010-01-01').to_period('M'))
    
    ################################
    ### Then, add the shift for the target region
    for n in shifts:
        
        shifted_df = df.groupby(level=admin_unit).shift(n)
        shifted_df.columns = [i + "_lag" + str(n) for i in shifted_df.columns]
        learn_df = pd.concat([learn_df, shifted_df], axis=1, join='outer')

        
    ################################
    ### And, add the historical mean values (with a shift of n) for the target region
    hm= df.unstack(level=admin_unit).rolling(window=12, center=False).mean().stack(dropna=False)
    hm.columns = [i+f'_hm{lag}' for i in hm.columns]

    # Shift it backwards
    hm = hm.groupby(admin_unit).shift(lag)
    learn_df = pd.concat([learn_df, hm], axis=1, join='outer')

    
    ### Shifted values of the data <- for all other regions
    for n in shifts:

        shift = df[varying_cols].copy()
        shift.columns = [i + "_lag" + str(n) for i in shift.columns]
        shift = shift.unstack(level=admin_unit).shift(n)
        shift.columns = ['_'.join(col).strip() for col in shift.columns.values]

        learn_df.reset_index(level=admin_unit, inplace=True)        
        learn_df = pd.concat([learn_df, shift], axis=1, join='outer')
        learn_df.set_index(admin_unit, inplace=True, append=True)

        
    ################################
    ###  One-hot encode the missing values
    cols = [i for i in learn_df.columns if i!='arrivals']

    for c in cols:
        if learn_df[c].isna().max()==True:
            learn_df[f'miss_{c}'] = np.where(learn_df[c].isna(),1,0)
            #learn_df[c] = learn_df[c].fillna(0)


    ## Pare down dataset    
    # Since 2011-01-01
    start_prmn = pd.to_datetime('2011-01-01')
    start_df = start_prmn + pd.DateOffset(months=lag)
    learn_df = learn_df.loc[start_df:]

    # Remove columns which are completely missing
    learn_df.dropna(axis=1, how='all', inplace=True)
    
    # Remove columns which never vary
    keep = [c for c in learn_df.columns if len(learn_df[c].unique()) > 1]
    learn_df = learn_df[keep]
    
    
    # Remove columns which are missing the target variable (arrivals) and are in the past    
    learn_df = learn_df[
        (learn_df.arrivals.isna() &
        (learn_df.index.get_level_values('date') <= current_month))==False
            ].copy()
        
    ## Save
    learn_df.to_csv(f"ml/input_data/learn_df_{admin_level}_lag{lag}.csv")
    
    if not os.path.exists(f"ml/output_data/{admin_level}_lag{lag}/"):
        os.mkdir(f"ml/output_data/{admin_level}_lag{lag}/")
    
    learn_df[['arrivals']].to_csv(f'ml/output_data/{admin_level}_lag{lag}/true.csv')
    
    return






