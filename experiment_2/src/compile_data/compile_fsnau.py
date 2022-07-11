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
    fsnau['date'] = pd.to_datetime(fsnau.month + " " + fsnau.year.astype(str)).dt.to_period("M")
    fsnau['date'] = pd.to_datetime(fsnau['date'].astype(str) + "-01")

    # Properly case the regions
    fsnau['region'] = fsnau.region.str.title()
    fsnau['district'] = fsnau.district.str.title()
    fsnau['market'] = fsnau.market.str.title()
    

    # Clean up region names
    admin1_map = json.load(open('src/admin1_map.json'))
    admin2_map = json.load(open('src/admin2_map.json'))
    fsnau['region']   = fsnau.region.replace(admin1_map)
    fsnau['district'] = fsnau.district.replace(admin2_map)

    # Drop columns that are not prices or for index
    fsnau.drop(columns = ['market_type', 'year', 'month'], inplace=True)
    
    # Remove observations with missing region
    fsnau.dropna(subset=['region'], inplace=True)

    # Set the index
    fsnau.set_index(["region", "district",'market', 'date'], inplace=True)
    
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
                   'somalishillingtousd',
                   'importedredrice1kg']]
    
    return fsnau


def compile_fsnau(source_dir = "data/raw/fsnau", \
                  target_dir = "data/clean",
                  sql_engine = ""):
    
    fsnau = collect_fsnau(source_dir)
    fsnau = clean_fsnau(fsnau)
    
    # Average prices over all markets in region
    #fsnau1 = fsnau.groupby(level=[0,2]).mean().round(0)
    #fsnau2 = fsnau.groupby(level=[0,1,2]).mean().round(0)
    fsnau = fsnau.groupby(['region', 'district', 'date']).mean().round(0)
    
    ####################
    # Initialize table 
    
    q = '''
    DROP TABLE IF EXISTS monthly_fsnau CASCADE;

    CREATE TABLE monthly_fsnau (
        region         TEXT,
        district       TEXT,
        date           DATE,
        wheatflour1kg  FLOAT,
        waterdrum      FLOAT,
        goatlocalquality FLOAT,
        redsorghum1kg  FLOAT,
        petrol1litre   FLOAT,
        charcoal50kg   FLOAT,
        firewoodbundle FLOAT,
        dailylaborrate FLOAT,
        somalishillingtousd FLOAT,
        importedredrice1kg FLOAT,

        PRIMARY KEY (region, district, date)
    )
    '''

    sql_engine.execute(q)
    
    ####################
    # Write to SQL database
    fsnau.reset_index().to_sql(
      name      = 'monthly_fsnau',    
      con       = sql_engine,                   
      if_exists = "append", 
      index     = False
    )   
    
    ####################
    # Create views
    q = '''
    DROP VIEW IF EXISTS fsnau_admin2 CASCADE;
    CREATE OR REPLACE VIEW fsnau_admin2 AS (
        SELECT region,
               district,
               date,
               AVG(wheatflour1kg)            AS  wheatflour1kg, 
               AVG(waterdrum)                AS  waterdrum, 
               AVG(goatlocalquality)         AS  goatlocalquality, 
               AVG(redsorghum1kg)            AS  redsorghum1kg, 
               AVG(petrol1litre)             AS  petrol1litre, 
               AVG(charcoal50kg)             AS  charcoal50kg, 
               AVG(firewoodbundle)           AS  firewoodbundle, 
               AVG(dailylaborrate)           AS  dailylaborrate, 
               AVG(somalishillingtousd)      AS  somalishillingtousd, 
               AVG(importedredrice1kg)       AS  importedredrice1kg
        FROM monthly_fsnau
        GROUP BY region, district, date
        ORDER BY region, district, date
    );


    DROP VIEW IF EXISTS fsnau_admin1 CASCADE;
    CREATE OR REPLACE VIEW fsnau_admin1 AS (
        SELECT region,
               date,
               AVG(wheatflour1kg)            AS  wheatflour1kg, 
               AVG(waterdrum)                AS  waterdrum, 
               AVG(goatlocalquality)         AS  goatlocalquality, 
               AVG(redsorghum1kg)            AS  redsorghum1kg, 
               AVG(petrol1litre)             AS  petrol1litre, 
               AVG(charcoal50kg)             AS  charcoal50kg, 
               AVG(firewoodbundle)           AS  firewoodbundle, 
               AVG(dailylaborrate)           AS  dailylaborrate, 
               AVG(somalishillingtousd)      AS  somalishillingtousd, 
               AVG(importedredrice1kg)       AS  importedredrice1kg
        FROM monthly_fsnau
        GROUP BY region, date
        ORDER BY region, date
    );
    '''
    sql_engine.execute(q)  
    
    return
    # Save
    #fsnau1.to_csv(f"{target_dir}/fsnau_admin1.csv")
    #fsnau2.to_csv(f"{target_dir}/fsnau_admin2.csv")
    
    