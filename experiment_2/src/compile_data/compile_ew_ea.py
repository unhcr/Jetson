import os
import pandas as pd
import dask.dataframe as dd
import json
import numpy as np

def collect_ew_ea(source_dir = "data/raw/ew_ea"):
    ''' Read in the Early Warning Early Action monthly files to a single dataframe'''
   
    source_dir = "data/raw/ew_ea"

    ew_ea = dd.read_csv(f'{source_dir}/ew_ea_2*.csv', dtype='object').compute() 
    
    ew_ea = ew_ea.replace("NaN", np.nan)
    
    for c in ew_ea.columns:
        ew_ea[c] = ew_ea[c].astype(float, errors="ignore")
    
    return ew_ea


def clean_ew_ea(ew_ea):
    ''' Cleans the Early Warning Early Action dataframe;
    - Renames columns
    '''
    
    # Clean column names
    ew_ea.columns = [i.lower()
                     .replace(" ", "_")
                     .replace("(", "")
                     .replace(")", "")
                     .replace("/", "_") for i in ew_ea.columns]

    ew_ea.rename(columns={"regions"  : "region"  }, inplace=True)
    ew_ea.rename(columns={"districts": "district"}, inplace=True)
    
    # Clean up region names
    admin1_map = json.load(open('src/admin1_map.json'))
    admin2_map = json.load(open('src/admin2_map.json'))
    ew_ea['region']   = ew_ea.region.replace(admin1_map)
    ew_ea['district'] = ew_ea.district.replace(admin2_map)
    
    # Date
    ew_ea['date'] = ew_ea['date'] + "-01"

    
    # Fill zeroes
    for v in ['malaria_cases', 'awd_cholera_cases', 'awd_cholera_deaths', 'measles_cases', 'new_admissions_gam']:
        
        # If no observation but data collection has started, fill NA with 0
        ew_ea[v] = np.where(ew_ea[v].isna()
                             & (ew_ea['date']>=ew_ea[~ew_ea[v].isna()]['date'].min())
                             & (ew_ea['date']<=ew_ea[~ew_ea[v].isna()]['date'].max()),
                            0, 
                            ew_ea[v])
    
        print(ew_ea[~ew_ea[v].isna()]['date'].min())
        print(ew_ea[~ew_ea[v].isna()]['date'].max())
        
        
    # Keep only relevant columns
    keepcols = ['region', 
                'district', 
                'date',
                'awd_cholera_deaths', 
                'awd_cholera_cases',
                'malaria_cases', 
                'measles_cases',
                'new_admissions_gam',
                'cost_of_minimum_basket_cmb', 
                'maize_prices', 
                'rainfall', 
                'tot_goat_to_cereals',
                'tot_wage_to_cereals', 
                'vegetation_cover_ndvi']
    
    ew_ea = ew_ea[keepcols].copy()
    
    return ew_ea


def compile_ew_ea(source_dir = "data/raw/ew_ea", 
                  target_dir = "data/clean",
                  sql_engine = ""):
    
    ew_ea = collect_ew_ea(source_dir)
    ew_ea = clean_ew_ea(ew_ea)
    
    # Data that needs to be summed by region
    '''sum_vars = ['awd_cholera_deaths', 
                'awd_cholera_cases',
                'malaria_cases', 
                'measles_cases',
                'new_admissions_gam']'''

    # Data that needs to be averaged by region
    '''mean_vars = ['cost_of_minimum_basket_cmb', 
                 'local_goat_prices',
                 'maize_prices', 
                 'price_of_water', 
                 'rainfall', 
                 'red_rice_prices',
                 'sorghum_prices', 
                 'tot_goat_to_cereals',
                 'tot_wage_to_cereals', 
                 'vegetation_cover_ndvi', 
                 'wage_labor']'''

    # Make a dataframe with instructions for aggregation
    '''aggs = {}

    for s in sum_vars:
        aggs[s] = 'sum'

    for m in mean_vars:
        aggs[m] = 'mean'
        
    # Collapse to region level
    ew_ea1 = ew_ea.groupby(['date', 'region']).agg(aggs)
    ew_ea2 = ew_ea.groupby(['date', 'region', 'district']).agg(aggs)

    ew_ea1.to_csv(f"{target_dir}/ew_ea_admin1.csv")
    ew_ea2.to_csv(f"{target_dir}/ew_ea_admin2.csv")'''
    
    ####################
    # Initialize table
    q = '''
    DROP TABLE IF EXISTS monthly_ew_ea CASCADE;

    CREATE TABLE monthly_ew_ea (
        region         TEXT,
        district       TEXT,
        date           DATE,
        rainfall       FLOAT,
        vegetation_cover_ndvi FLOAT,
        maize_prices          FLOAT,
        tot_goat_to_cereals   FLOAT,
        tot_wage_to_cereals   FLOAT,
        cost_of_minimum_basket_cmb FLOAT,
        new_admissions_gam    FLOAT,
        measles_cases         FLOAT,
        awd_cholera_cases     FLOAT,
        awd_cholera_deaths    FLOAT,
        malaria_cases         FLOAT,

        PRIMARY KEY (region, district, date)
    )
    '''
    sql_engine.execute(q)
    
    
    ####################
    # Write to SQL database
    
    ew_ea.to_sql(
      name      = 'monthly_ew_ea',    
      con       = sql_engine,                   
      if_exists = "append", 
      index     = False
    )   
    
    
    ####################
    # Create views
    
    q = '''
    DROP VIEW IF EXISTS ew_ea_admin2 CASCADE;
    CREATE OR REPLACE VIEW ew_ea_admin2 AS (
        SELECT region, 
            district,
            date,
            SUM(awd_cholera_deaths)         AS awd_cholera_deaths, 
            SUM(awd_cholera_cases)          AS awd_cholera_cases, 
            SUM(malaria_cases)              AS malaria_cases, 
            SUM(measles_cases)              AS measles_cases, 
            SUM(new_admissions_gam)         AS new_admissions_gam, 
            AVG(rainfall)                   AS rainfall, 
            AVG(vegetation_cover_ndvi)      AS vegetation_cover_ndvi, 
            AVG(maize_prices)               AS maize_prices, 
            AVG(tot_goat_to_cereals)        AS tot_goat_to_cereals, 
            AVG(tot_wage_to_cereals)        AS tot_wage_to_cereals, 
            AVG(cost_of_minimum_basket_cmb)       AS cost_of_minimum_basket_cmb
        FROM monthly_ew_ea
        GROUP BY region, district, date
        ORDER BY region, district, date
    );

    DROP VIEW IF EXISTS ew_ea_admin1 CASCADE;
    CREATE OR REPLACE VIEW ew_ea_admin1 AS (
        SELECT region, 
            date,
            SUM(awd_cholera_deaths)         AS awd_cholera_deaths, 
            SUM(awd_cholera_cases)          AS awd_cholera_cases, 
            SUM(malaria_cases)              AS malaria_cases, 
            SUM(measles_cases)              AS measles_cases, 
            SUM(new_admissions_gam)         AS new_admissions_gam, 
            AVG(rainfall)                   AS rainfall, 
            AVG(vegetation_cover_ndvi)      AS vegetation_cover_ndvi, 
            AVG(maize_prices)               AS maize_prices, 
            AVG(tot_goat_to_cereals)        AS tot_goat_to_cereals, 
            AVG(tot_wage_to_cereals)        AS tot_wage_to_cereals, 
            AVG(cost_of_minimum_basket_cmb)       AS cost_of_minimum_basket_cmb
        FROM monthly_ew_ea
        GROUP BY region, date
        ORDER BY region, date
    )
    '''
    sql_engine.execute(q)  
    
    return
    
################################################   
    

def collect_ew_ea_rivers(source_dir = "data/raw/ew_ea"):
    ''' Read in the Early Warning Early Action monthly RIVER files to a single dataframe'''
   
    source_dir = "data/raw/ew_ea"

    ew_ea_rivers = dd.read_csv(f'{source_dir}/ew_ea_rivers*.csv').compute() 

    return ew_ea_rivers



def clean_ew_ea_rivers(ew_ea_rivers):
    ''' Cleans the Early Warning Early Action dataframe;
    - Renames columns
    '''
    # Remove duplicates
    ew_ea_rivers.drop_duplicates(inplace=True)
    
    # Fix the date column
    ew_ea_rivers['date'] = pd.to_datetime(ew_ea_rivers['date'])
                                                           
    # Reshape
    ew_ea_rivers = ew_ea_rivers.set_index(['date', 'district']).unstack(level='district')['depth_in_meters']
    
    # Fix column names
    ew_ea_rivers.columns = ["river_"+ i.lower().replace(" ", "_").replace("'","") for i in ew_ea_rivers.columns]
    
    ew_ea_rivers.index = pd.to_datetime(ew_ea_rivers.index.to_period("M").astype(str) + "-01")
    

    return ew_ea_rivers   



def compile_ew_ea_rivers(source_dir = "data/raw/ew_ea", \
                  target_dir = "data/clean",
                  sql_engine=""):
    
    ew_ea_rivers = collect_ew_ea_rivers(source_dir)
    ew_ea_rivers = clean_ew_ea_rivers(ew_ea_rivers)
    
    # Write to SQL database
    q = '''
    DROP TABLE IF EXISTS monthly_ew_ea_rivers CASCADE;

    CREATE TABLE monthly_ew_ea_rivers (
        date              DATE,
        river_baardheere  FLOAT,
        river_belet_weyne FLOAT,
        river_buaale      FLOAT,
        river_bulo_burto  FLOAT,
        river_doolow      FLOAT,
        river_jowhar      FLOAT,
        river_luuq        FLOAT,

        PRIMARY KEY (date)
    )
    '''

    sql_engine.execute(q)
    
    ew_ea_rivers.reset_index().to_sql(
      name      = 'monthly_ew_ea_rivers',    
      con       = sql_engine,                   
      if_exists = "append", 
      index     = False
    )   
        
    #ew_ea_rivers.to_csv(f"{target_dir}/ew_ea_rivers.csv")
    
    return
    
    
    