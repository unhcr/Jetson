import pandas as pd
import numpy as np
from dateutil.relativedelta import *
import os


def make_ml_features(current_month, admin_level):
    '''
    Starts from the compiled dataset for the given admin level and month. 
    Does the following steps:
    
    1. Replaces zero arrivals/departures with missing values.
    2. Adds dummy variables for region and month
    3. Creates a linear variable for months since 2010
    4. For each observation, adds in observations across all other regions.
    5. One-hot encodes the missing values
    6. Shortens the time horizon from 2011-01-01 to the `current month`.
    7. Drops columns that are all missing or never varying.
    8. Saves a column called "true" in the "output data" for all models.
    
    '''
    # add shifts? horizon range?
    
    ################################
    ### Read in the data
    df = pd.read_csv(f"data/compiled/master_{admin_level}.csv", 
                     parse_dates=['date'], 
                     index_col=['date', 'region'])

    if admin_level=='admin1':
        admin_unit='region'

    current_month = pd.to_datetime(current_month)

    df.sort_index(inplace=True)
    
    ################################
    ## Handle zero arrivals as missing
    df['arrivals']   = np.where(df['arrivals']   == 0, np.nan, df['arrivals'])
    df['departures'] = np.where(df['departures'] == 0, np.nan, df['departures'])
    

    ################################
    ### Create features
    constant_cols     = ['distance_straight', 
                         'shared_border',
                         'distance_driving_km', 
                         'distance_driving_hr'] 
    river_cols        = [i for i in df.columns if "river_" in i ]
    varying_cols      = [i for i in df.columns if i not in constant_cols and i not in river_cols]

    ################################
    ### First, add features that don't need to be shifted

    # Initialize dataframe with constant columns
    learn_df = df.copy()

    # One-hot encode the regions and months
    learn_df['region_dummies'] = learn_df.index.get_level_values(admin_unit).astype(str)
    learn_df['month_dummies']  = learn_df.index.get_level_values('date'  ).month.astype(str)
    learn_df = pd.get_dummies(learn_df)

    # Linear time var
    learn_df['months_since_2010'] = (learn_df.index.get_level_values('date').to_period('M') - 
                                                pd.to_datetime('2010-01-01').to_period('M'))
    '''
    ################################
    ### Then, add in the observations for other regions
    
    # Get a dataframe of other region observations
    other_regions = learn_df[varying_cols].unstack(level=admin_unit)
    other_regions.columns = ['_'.join(col).strip() for col in other_regions.columns.values]

    # Merge on to the existing dataframe
    learn_df.reset_index(level=admin_unit, inplace=True)        
    learn_df = pd.concat([learn_df, other_regions], axis=1, join='outer')
    learn_df.set_index(admin_unit, inplace=True, append=True)
    '''
    ################################
    ###  One-hot encode the missing values
    for c in learn_df.columns:
        if learn_df[c].isna().max()==True:
            learn_df[f'miss_{c}'] = np.where(learn_df[c].isna(),1,0)


    ################################
    ## Pare down dataset 
    
    # Since 2011-01-01
    start_prmn = pd.to_datetime('2011-01-01')
    learn_df = learn_df.loc[start_prmn:current_month]
    
    # Remove columns which are completely missing
    column_list = learn_df.columns
    learn_df.dropna(axis=1, how='all', inplace=True)    
    print("Dropped entirely missing columns: ", [i for i in column_list if i not in learn_df.columns])

    # Remove columns which never vary
    keep = [c for c in learn_df.columns if len(learn_df[c].unique()) > 1]
    learn_df = learn_df[keep]

    # Remove columns which are duplicated
    column_list = learn_df.columns
    learn_df = learn_df.T.drop_duplicates().T    
    print("Dropped duplicate columns: ", [i for i in column_list if i not in learn_df.columns])
        
    ################################
    ## Make the shifts of the target variable for prediction
    #for i in range(1,13):
    #    learn_df[f'arrivals_t+{i}'] = learn_df.groupby(level=['region']).arrivals.shift(-i)

    ################################
    ## Save
    learn_df.to_csv(f"ml/input_data/learn_df_{admin_level}.csv")

    for lag in range(1,13):
        if not os.path.exists(f"ml/output_data/{admin_level}_lag{lag}/"):
            os.mkdir(f"ml/output_data/{admin_level}_lag{lag}/")

        learn_df[[f'arrivals']].to_csv(f'ml/output_data/{admin_level}_lag{lag}/true.csv')
        
        
    '''
    # Verify the columns we expect were created
    learn_df.columns.tolist()

    # Verify that imputing of neighboring regions worked 
    learn_df.xs('Awdal', level='region')[['rainfall', 'rainfall_Awdal',  'rainfall_Nugaal', 'rainfall_Sanaag', 'rainfall_Sool']]

    # Verify that the shifting occurred without a problem:
    learn_df.xs('Awdal', level='region')[['arrivals', 'arrivals_t+1', 'arrivals_t+2']]
    '''
    return learn_df


def fill_missing_values(learn_df, X_cols):
    '''
    Fills missing values for the input features
    
    '''
    
    learn_df.sort_index(level='date', inplace=True)

    # Fill missing values 
    learn_df[X_cols] = learn_df.groupby(level=['region'])[X_cols].transform(lambda x: x.ffill())
    learn_df[X_cols] = learn_df[X_cols].fillna(0)
    
    return learn_df


def shift_input_features(learn_df, X_cols, y_col, horizon, current_month, admin_unit = 'region'):
    
    '''
    Shifts the features by the amount of the lag
    '''

    ### Add blank rows with future periods to the dataframe
    # Get list of current and future months
    current_month = pd.to_datetime(current_month)
    future_months = [ current_month + relativedelta(months=i) for i in range(1, horizon+1)]

    # Insert extra regions and dates for lagged predictions
    regions = learn_df.index.get_level_values(admin_unit)

    for d in future_months:
        for r in regions:
            learn_df.ix[(d, r), :] = np.nan

    ### Shift the X features back according to the horizon
    # Concatenate
    learn_df = pd.concat([
            learn_df[y_col],
            learn_df.groupby(level='region')[X_cols].shift(horizon)
        ], axis=1, join='outer')
    
    return learn_df



