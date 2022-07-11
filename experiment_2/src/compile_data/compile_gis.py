import pandas as pd
import geopandas as gp
from geoalchemy2      import Geometry, WKTElement

def compile_gis(src_dir="data/raw/gis",
                     target_dir = 'data/clean',
                     sql_engine=""):
    
    ########################
    # Prepare geodataframes
    
    crs=4326

    admin1 = gp.read_file("data/raw/gis/somalia_boundaries/Som_Admbnda_Adm1_UNDP.shp")
    admin2 = gp.read_file("data/raw/gis/somalia_boundaries/Som_Admbnda_Adm2_UNDP.shp")

    admin1.rename(columns={'admin1Name':'region'}, inplace=True)
    admin2.rename(columns={'admin2Name':'district', 'admin1Name':'region'}, inplace=True)
    
    admin1['geometry']   = admin1['geometry'].apply(lambda x: WKTElement(x.wkt, srid=crs))
    admin2['geometry']   = admin2['geometry'].apply(lambda x: WKTElement(x.wkt, srid=crs))
    
    admin1.sort_values(['region'],             inplace=True)
    admin2.sort_values(['region', 'district'], inplace=True)
    
    ########################
    # Initialize tables
    
    q = '''
    DROP TABLE IF EXISTS geo_admin2;

    CREATE TABLE geo_admin2 (
        region   VARCHAR(50), 
        district VARCHAR(50), 
        geometry GEOMETRY,

        PRIMARY KEY (region, district)
    );


    DROP TABLE IF EXISTS geo_admin1;

    CREATE TABLE geo_admin1 (
        region   VARCHAR(50), 
        geometry GEOMETRY,

        PRIMARY KEY (region)
    );
    '''
    sql_engine.execute(q)  
    
    
    ########################
    # Insert data

    admin1[['region','geometry']].to_sql(
          name      = 'geo_admin1',    
          con       = sql_engine,                   
          if_exists = "append", 
          index     = False,
          dtype     = {'geometry': Geometry('GEOMETRY', srid=crs)}
        )


    admin2[['region','district','geometry']].to_sql(
          name      = 'geo_admin2',    
          con       = sql_engine,                   
          if_exists = "append", 
          index     = False,
          dtype     = {'geometry': Geometry('GEOMETRY', srid=crs)}
        )

    return

    
