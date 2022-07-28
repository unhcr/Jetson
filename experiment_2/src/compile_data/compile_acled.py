import os
import pandas as pd
import dask.dataframe as dd


def collect_acled(source_dir = "data/raw/acled"):
    ''' Read in the ACLED monthly files to a single dataframe'''
    
    acled = dd.read_csv(f'{source_dir}/acled_*.csv', dtype={'admin3': 'object'}, parse_dates=['event_date']).compute() 

    return acled

def clean_acled(acled):
    ''' Cleans the ACLED dataframe;
    - Removes strategic developments
    - Fills missing values with zeroes 
    - Aggregates to count of incidents and fatalities by admin level
    '''
    
    # Remove empty rows, columns
    acled.dropna(axis=1, how='all', inplace=True)
    acled.dropna(axis=0, how='all', inplace=True)

    # Remove strategic developments
    acled = acled[(acled.event_type!="Strategic developments")].copy()

    # Create month variable
    acled['month_year'] = acled.event_date.dt.to_period("M")

    # Sort
    acled.sort_values(['admin1', 'admin2', 'month_year'], inplace=True)

    # Get count of fatalities and violent incidents
    acled_fatalities = acled.groupby(['admin1', \
                                      'admin2', \
                                      'month_year']).sum()[['fatalities']]
    acled_incidents  = acled.groupby(["admin1", \
                                      'admin2', \
                                      'month_year']).count()[['data_id']]
    acled_incidents.columns = ['incidents']

    # Merge into final dataset
    acled = acled_incidents.merge(acled_fatalities, right_index=True, left_index=True)
    acled.index.names = ['region', 'district', 'date']

    # Fill missing values
    acled = acled.unstack(level=2).fillna(0).stack()
    
    return acled


def compile_acled(source_dir = "data/raw/acled", \
                   target_dir = "data/clean"):
    
    acled = collect_acled(source_dir)
    acled = clean_acled(acled)
    
    # Save 
    acled.to_csv(f"{target_dir}/acled_admin2.csv")
    acled = acled.groupby(level=[0,2]).sum()
    acled.to_csv(f"{target_dir}/acled_admin1.csv")
    
    