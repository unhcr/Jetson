import pandas as pd
import json

def compile_public_prmn(sql_engine=""):
    ''' Cleans and reshapes PRMN from UNHCR website (2016 - present) '''
    
    #### ADMIN 1
    #prmn = pd.read_csv("data/raw/prmn/prmn_public.csv", parse_dates=['Month End'])
    
    # Extract month from date
    #prmn['date'] = prmn['Month End'].dt.to_period('M')

    # Count monthly arrivals/departures by region
    #arrivals   = prmn.groupby(['Current (Arrival) Region',    'date']).sum()[['Number of Individuals']]
    #departures = prmn.groupby(['Previous (Departure) Region', 'date']).sum()[['Number of Individuals']]

    # Clean up the dataframes
    #arrivals.columns   = ['arrivals']
    #departures.columns = ['departures']

    #arrivals.index.names   = ['region', 'date']
    #departures.index.names = ['region', 'date']

    # Merge
    #prmn = arrivals.merge(departures, left_index=True, right_index=True, how='outer')

    #prmn.to_csv("data/clean/prmn_public_admin1.csv")
    
    
    
    #### ADMIN 2
    #prmn = pd.read_csv("data/raw/prmn/prmn_public.csv", parse_dates=['Month End'])
    
    # Extract month from date
    #prmn['date'] = prmn['Month End'].dt.to_period('M')

    # Count monthly arrivals/departures by region
    #arrivals   = prmn.groupby(['Current (Arrival) Region', 'Current (Arrival) District',    
    #                           'date']).sum()[['Number of Individuals']]
    #departures = prmn.groupby(['Previous (Departure) Region', 'Previous (Departure) District', 
    #                            'date']).sum()[['Number of Individuals']]

    # Clean up the dataframes
    #arrivals.columns   = ['arrivals']
    #departures.columns = ['departures']

    #arrivals.index.names   = ['region', 'district', 'date']
    #departures.index.names = ['region', 'district', 'date']

    # Merge
    #prmn = arrivals.merge(departures, left_index=True, right_index=True, how='outer')
    
    
    
    #prmn.to_csv("data/clean/prmn_public_admin2.csv")
    
    
    ###################
    # Compile public prmn
    prmn = pd.read_csv("data/raw/prmn/prmn_public.csv", parse_dates=['Month End'])

    # Extract month from date
    prmn['date'] = pd.to_datetime(prmn['Month End'].dt.to_period('M').astype(str) + "-01")

    # Rename columns
    prmn.rename(columns = { 'Current (Arrival) Region'     : 'arrival_region',
                            'Current (Arrival) District'   : 'arrival_district', 
                            'Previous (Departure) Region'  : 'previous_region',
                            'Previous (Departure) District': 'previous_district',
                            'Number of Individuals'        : 'n'}, 
                inplace=True)
    
    
    # Clean up region names
    admin1_map = json.load(open('src/admin1_map.json'))
    admin2_map = json.load(open('src/admin2_map.json'))
    prmn['arrival_region']    = prmn.arrival_region.replace(admin1_map)
    prmn['previous_region']   = prmn.previous_region.replace(admin1_map)
    prmn['arrival_district']  = prmn.arrival_district.replace(admin2_map)
    prmn['previous_district'] = prmn.previous_district.replace(admin2_map)

    # Collapse
    prmn = prmn.groupby(['arrival_region', 'arrival_district', 'previous_region', 'previous_district', 'date']).sum()[['n']]
    
    
    ####################
    # Initialize table
    q = '''
    DROP TABLE IF EXISTS monthly_prmn CASCADE;

    CREATE TABLE monthly_prmn (
        arrival_region    TEXT,
        arrival_district  TEXT,
        previous_region   TEXT,
        previous_district TEXT,
        date              DATE,
        n                 FLOAT,

        PRIMARY KEY (arrival_region, arrival_district, previous_region, previous_district, date)
    )
    '''
    sql_engine.execute(q)
    
    ####################
    # Write to SQL database

    prmn.reset_index().to_sql(
      name      = 'monthly_prmn',    
      con       = sql_engine,                   
      if_exists = "append", 
      index     = False
    )   
    
    

    ####################
    # Create views
    q = '''
    DROP VIEW IF EXISTS prmn_admin1 CASCADE;
        CREATE OR REPLACE VIEW prmn_admin1 AS (
            SELECT 
                arr.region, arr.date, arrivals, departures       
            FROM
                (SELECT arrival_region AS region,
                        date,
                        SUM(n)         AS arrivals           
                    FROM monthly_prmn
                    GROUP BY region, date) AS arr
            FULL OUTER JOIN
                (SELECT previous_region AS region,
                        date,
                        SUM(n)         AS departures           
                    FROM monthly_prmn
                    GROUP BY region, date) AS dep
            ON arr.region = dep.region AND arr.date = dep.date
            WHERE arr.region in (
                'Lower Shabelle', 'Galgaduud', 'Banadir', 'Hiraan', 'Bakool',
                'Lower Juba', 'Togdheer', 'Bari', 'Sanaag', 'Woqooyi Galbeed',
                'Awdal', 'Middle Juba', 'Sool', 'Middle Shabelle', 'Gedo', 'Bay',
                'Nugaal', 'Mudug')
            ORDER BY arr.region, arr.date
        );

    DROP VIEW IF EXISTS prmn_admin2 CASCADE;
        CREATE OR REPLACE VIEW prmn_admin2 AS (
            SELECT 
                arr.region, arr.district, arr.date, arrivals, departures       
            FROM
                (SELECT arrival_region AS region,
                        arrival_district AS district,
                        date,
                        SUM(n)         AS arrivals           
                    FROM monthly_prmn
                    GROUP BY region, district, date) AS arr
            FULL OUTER JOIN
                (SELECT previous_region AS region,
                        previous_district AS district,
                        date,
                        SUM(n)         AS departures           
                    FROM monthly_prmn
                    GROUP BY region, district, date) AS dep
            ON arr.region = dep.region AND arr.district = dep.district AND arr.date = dep.date
            WHERE arr.region in (
                'Lower Shabelle', 'Galgaduud', 'Banadir', 'Hiraan', 'Bakool',
                'Lower Juba', 'Togdheer', 'Bari', 'Sanaag', 'Woqooyi Galbeed',
                'Awdal', 'Middle Juba', 'Sool', 'Middle Shabelle', 'Gedo', 'Bay',
                'Nugaal', 'Mudug')
            ORDER BY arr.region, arr.district, arr.date
        ); 
    '''
    sql_engine.execute(q)  
    
    return

    
    
    