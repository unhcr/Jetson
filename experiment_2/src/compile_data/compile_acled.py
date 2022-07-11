import os
import json
import pandas as pd
import dask.dataframe as dd

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists, drop_database


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
    acled['month_year'] = pd.to_datetime(acled.event_date.dt.to_period("M").astype(str)+"-01")

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
    
    # Fix region names
    admin1_map = json.load(open('src/admin1_map.json'))
    admin2_map = json.load(open('src/admin2_map.json'))
    acled['admin1'] = acled.admin1.replace(admin1_map)
    acled['admin2'] = acled.admin2.replace(admin2_map)

    # Merge into final dataset
    acled = acled_incidents.merge(acled_fatalities, right_index=True, left_index=True)
    acled.index.names = ['region', 'district', 'date']
       

    # Fill missing values
    acled = acled.unstack(level=2).fillna(0).stack()
    
    return acled



def compile_acled(source_dir = "data/raw/acled", 
                  target_dir = "data/clean",
                  sql_engine = ""):
    
    acled = collect_acled(source_dir)
    acled = clean_acled(acled)
    
    #####################
    # Initialize table
    q = '''
    DROP TABLE IF EXISTS monthly_acled CASCADE;

    CREATE TABLE monthly_acled (
        region         TEXT,
        district       TEXT,
        date           DATE,
        incidents      FLOAT,
        fatalities     FLOAT,

        PRIMARY KEY (region, district, date)
    )
    '''
    sql_engine.execute(q)
    
    
    #####################
    # Write to database
    acled.reset_index().to_sql(
      name      = 'monthly_acled',    
      con       = sql_engine,                   
      if_exists = "append", 
      index     = False
    )   
    
    #####################
    # Create views
    q = '''
    DROP VIEW IF EXISTS acled_admin1 CASCADE;
    CREATE OR REPLACE VIEW acled_admin1 AS (
        SELECT region,
               date,
               SUM(incidents) as incidents,
               SUM(fatalities) as fatalities
        FROM monthly_acled
        GROUP BY region, date
        ORDER BY region, date
    );


    DROP VIEW IF EXISTS acled_admin2 CASCADE;
    CREATE OR REPLACE VIEW acled_admin2 AS (
        SELECT * FROM monthly_acled
        ORDER BY region, district, date
    );
    '''
    sql_engine.execute(q)  
    
    return
    
    # Save 
    #acled.to_csv(f"{target_dir}/acled_admin2.csv")
    #acled = acled.groupby(level=[0,2]).sum()
    #acled.to_csv(f"{target_dir}/acled_admin1.csv")
    
    