import os
import pandas as pd
import dask.dataframe as dd
import json
import numpy as np


def collect_fsnau(source_dir = "data/raw/fsnau"):
    ''' Read in the FSNAU monthly files'''
    
    fsnau = dd.read_csv(f'{source_dir}/fsnau_*.csv', 
                          dtype={'GoatLocalQuality':  'object',
                                'Salt':               'object',
                                'Soap1Bar':           'object',
                                'Sugar':              'object',
                                'TeaLeaves':          'object',
                                'VegetableOil1litre': 'object',
                                'WheatFlour1kg':      'object'}).compute() 
    return fsnau


def clean_fsnau(fsnau):
    ''' Cleans the FSNAU dataset;
    - Pulls out relevant columns
    - Cleans up region names
    '''
    
   # Lowercase the columns
    fsnau.columns = [i.lower().replace(" ", "_") for i in fsnau.columns]

    # Replace missing values
    fsnau = fsnau.replace("-", np.nan)

    # Create year month variable
    fsnau['year_month'] = pd.to_datetime(fsnau.month + " " + fsnau.year.astype(str)).dt.to_period("M")

    # Properly case the regions
    fsnau['region'] = fsnau.region.str.title()
    fsnau['district'] = fsnau.district.str.title()

    # Clean up region names
    admin1_map = json.load(open('src/admin1_map.json'))
    fsnau['region'] = fsnau.region.replace(admin1_map)

    # Drop columns that are not prices or for index
    fsnau.drop(columns = ['market', 'market_type', 'year', 'month'], inplace=True)

    # Set the index
    fsnau.set_index(["region", "district", 'year_month'], inplace=True)
    fsnau.index.names = ['region', 'district', 'date']

    # Convert remaining price columns to float
    fsnau = fsnau.astype(float)

    # Keep relevant commodities
    fsnau = fsnau[['wheatflour1kg',  
                   'waterdrum', 
                   'goatlocalquality', 
                   'redsorghum1kg', 
                   'petrol1litre',
                   'charcoal50kg',   
                   'firewoodbundle', 
                   'dailylaborrate', 
                   'somalishillingtousd']]
    
    return fsnau


def compile_fsnau(source_dir = "data/raw/fsnau", \
                   target_dir = "data/clean"):
    
    fsnau = collect_fsnau(source_dir)
    fsnau = clean_fsnau(fsnau)
    
     # Average prices over all markets in region
    fsnau1 = fsnau.groupby(level=[0,2]).mean().round(0)
    fsnau2 = fsnau.groupby(level=[0,1,2]).mean().round(0)
    
    # Save
    fsnau1.to_csv(f"{target_dir}/fsnau_admin1.csv")
    fsnau2.to_csv(f"{target_dir}/fsnau_admin2.csv")
    
    