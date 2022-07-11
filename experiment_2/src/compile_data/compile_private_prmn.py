import pandas as pd
import json
import jetson_configs as jcfg

def compile_private_prmn(sql_engine=""):
    ''' Cleans and reshapes internal PRMN from local desktop '''
    
    # Compile public prmn
    prmn = pd.read_csv(jcfg.prmn_path, parse_dates=['date'])
    
    # Keep only observations prior to 2016, when the public PRMN kicks in
    prmn = prmn[prmn.date<pd.to_datetime('2016-01-01')].copy()

    # Extract month from date
    prmn['date'] = pd.to_datetime(prmn['date'].dt.to_period('M').astype(str) + "-01")

    # Rename columns
    prmn.rename(columns = { 'dest_region'   : 'arrival_region',
                            'dest_district' : 'arrival_district', 
                            'src_region'    : 'previous_region',
                            'src_district'  : 'previous_district',
                            'arrivals'      : 'n'}, 
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

    # Write to SQL database
    # NOTE: ASSUMES THE TABLE ALREADY EXISTS BECAUSE PUBLIC PRMN HAS BEEN WRITTEN

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
            ORDER  by arr.region, arr.date
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
            ORDER  by arr.region, arr.district, arr.date
        ); 
    '''
    sql_engine.execute(q)  
    
    return

    
