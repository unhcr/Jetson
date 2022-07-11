import pandas as pd
import jetson_configs as jcfg

first_month = jcfg.first_month

def compile_master(sql_engine=""):
    
    ##############
    # ADMIN 1
    
    q = f'''
    DROP VIEW IF EXISTS master_admin1 CASCADE;
    CREATE OR REPLACE VIEW master_admin1 AS (
        SELECT 
                COALESCE(p.region, a.region, f.region, e.region, d.region) AS region,
                COALESCE(p.date, a.date, f.date, e.date, r.date) AS date,
                arrivals,
                awd_cholera_cases,
                awd_cholera_deaths,
                charcoal50kg,
                cost_of_minimum_basket_cmb,
                dailylaborrate,
                departures,
                distance_driving_hr,
                distance_driving_km,
                distance_straight,
                fatalities,
                firewoodbundle,
                goatlocalquality,
                importedredrice1kg,
                incidents,
                maize_prices,
                malaria_cases,
                measles_cases,
                new_admissions_gam,
                petrol1litre,
                rainfall,
                redsorghum1kg,
                river_baardheere,
                river_belet_weyne,
                river_buaale,
                river_bulo_burto,
                river_doolow,
                river_jowhar,
                river_luuq,
                shared_border,
                somalishillingtousd,
                tot_goat_to_cereals,
                tot_wage_to_cereals,
                vegetation_cover_ndvi,
                waterdrum,
                wheatflour1kg
        FROM prmn_admin1 p
        FULL OUTER JOIN acled_admin1   a ON a.date = p.date                           AND a.region = p.region
        FULL OUTER JOIN fsnau_admin1   f ON f.date = COALESCE(p.date, a.date)         AND f.region = COALESCE(a.region, p.region)
        FULL OUTER JOIN ew_ea_admin1   e ON e.date = COALESCE(p.date, a.date, f.date) AND e.region = COALESCE(a.region, p.region, f.region)
        LEFT JOIN distances_admin1     d ON                                               d.region = COALESCE(a.region, p.region, f.region, e.region)
        LEFT JOIN monthly_ew_ea_rivers r ON r.date = COALESCE(p.date, a.date, f.date, e.date) 
        WHERE p.date>='{first_month}-01' OR a.date>='{first_month}-01' OR f.date>='{first_month}-01' OR e.date>='{first_month}-01' 
        ORDER BY region, date
        );'''
    sql_engine.execute(q)
    
    ##############
    # ADMIN 2
    
    # Todo: reconcile competing names
    q = f'''
    DROP VIEW IF EXISTS master_admin2 CASCADE;
    CREATE OR REPLACE VIEW master_admin2 AS (
        SELECT 
                COALESCE(p.region,   a.region,   f.region,   e.region)   AS region,
                COALESCE(p.district, a.district, f.district, e.district, d.district) AS district,
                COALESCE(p.date, a.date, f.date, e.date, r.date) AS date,
                arrivals,
                awd_cholera_cases,
                awd_cholera_deaths,
                charcoal50kg,
                cost_of_minimum_basket_cmb,
                dailylaborrate,
                departures,
                distance_driving_hr,
                distance_driving_km,
                distance_straight,
                fatalities,
                firewoodbundle,
                goatlocalquality,
                importedredrice1kg,
                incidents,
                maize_prices,
                malaria_cases,
                measles_cases,
                new_admissions_gam,
                petrol1litre,
                rainfall,
                redsorghum1kg,
                river_baardheere,
                river_belet_weyne,
                river_buaale,
                river_bulo_burto,
                river_doolow,
                river_jowhar,
                river_luuq,
                shared_border,
                somalishillingtousd,
                tot_goat_to_cereals,
                tot_wage_to_cereals,
                vegetation_cover_ndvi,
                waterdrum,
                wheatflour1kg
        FROM prmn_admin2 p
        FULL OUTER JOIN acled_admin2   a ON  a.date     = p.date                           
                                         AND a.region   = p.region                              
                                         AND a.district = p.district
        FULL OUTER JOIN fsnau_admin2   f ON  f.date     = COALESCE(a.date,     p.date)         
                                         AND f.region   = COALESCE(a.region,   p.region)      
                                         AND f.district = COALESCE(a.district, p.district)
        FULL OUTER JOIN ew_ea_admin2   e ON  e.date     = COALESCE(a.date,     p.date,     f.date)       
                                         AND e.region   = COALESCE(a.region,   p.region,   f.region)      
                                         AND e.district = COALESCE(a.district, p.district, f.district)
        LEFT JOIN distances_admin2     d ON  d.district = COALESCE(a.district, p.district, f.district, e.district)
        LEFT JOIN monthly_ew_ea_rivers r ON  r.date     = COALESCE(a.date,     p.date,     f.date,     e.date) 
        WHERE p.date>='{first_month}-01' OR a.date>='{first_month}-01' OR f.date>='{first_month}-01' OR e.date>='{first_month}-01'
        ORDER BY region, district, date
        ); '''
    sql_engine.execute(q)

    return

    
