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
    ew_ea['region'] = ew_ea.region.replace(admin1_map)
    
    return ew_ea


def compile_ew_ea(source_dir = "data/raw/ew_ea", 
                  target_dir = "data/clean"):
    
    ew_ea = collect_ew_ea(source_dir)
    ew_ea = clean_ew_ea(ew_ea)
    
    
    # Data that needs to be summed by region
    sum_vars = ['awd_cholera_deaths', 
                'awd_cholera_cases',
                'malaria_cases', 
                'measles_cases',
                'new_admissions_gam']

    # Data that needs to be averaged by region
    mean_vars = ['cost_of_minimum_basket_cmb', 
                 'local_goat_prices',
                 'maize_prices', 
                 'price_of_water', 
                 'rainfall', 
                 'red_rice_prices',
                 'sorghum_prices', 
                 'tot_goat_to_cereals',
                 'tot_wage_to_cereals', 
                 'vegetation_cover_ndvi', 
                 'wage_labor']

    # Make a dataframe with instructions for aggregation
    aggs = {}

    for s in sum_vars:
        aggs[s] = 'sum'

    for m in mean_vars:
        aggs[m] = 'mean'
        
    # Collapse to region level
    ew_ea1 = ew_ea.groupby(['date', 'region']).agg(aggs)
    ew_ea2 = ew_ea.groupby(['date', 'region', 'district']).agg(aggs)

    ew_ea1.to_csv(f"{target_dir}/ew_ea_admin1.csv")
    ew_ea2.to_csv(f"{target_dir}/ew_ea_admin2.csv")

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
    
    ew_ea_rivers.index = ew_ea_rivers.index.to_period("M")
    

    return ew_ea_rivers   



def compile_ew_ea_rivers(source_dir = "data/raw/ew_ea", \
                  target_dir = "data/clean"):
    
    ew_ea_rivers = collect_ew_ea_rivers(source_dir)
    ew_ea_rivers = clean_ew_ea_rivers(ew_ea_rivers)
    ew_ea_rivers.to_csv(f"{target_dir}/ew_ea_rivers.csv")
    
    return
    
    
    