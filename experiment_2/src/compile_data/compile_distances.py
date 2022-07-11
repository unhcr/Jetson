import pandas as pd

def collect_dist(src_dir="data/raw/distances",
                admin_level='admin1'):
    '''
    Merges the two distance files together and returns the result:
    - distances_calculated.csv
    - distances_osm.csv  
    
    src_dir   = source directory name
    
    '''
    # Import data
    dist_calc = pd.read_csv(f"{src_dir}/distances_calculated_{admin_level}.csv")
    dist_osm = pd.read_csv(f"{src_dir}/distances_osm_{admin_level}.csv")
    
    dist_calc['distance_straight'] = dist_calc['distance_straight'].round(2)
    dist_osm['distance_driving_km'] = dist_osm['distance_driving_km'].round(2)
    dist_osm['distance_driving_hr'] = dist_osm['distance_driving_hr'].round(2)
    
    # Merge data
    dist = pd.merge(dist_calc, dist_osm, on=['dest_region', 'src_region'], how='outer')
    
    return dist



def aggregate_distances(dist):
    ''' 
    Takes the pairwise OD matrix of distances, 
    and calculates average by ARRIVAL region.
    
    Also confirms no duplicate pairs. 
    '''

    # Ensure that each region pair enters only once
    assert(dist.duplicated(subset=['dest_region', 'src_region']).max() == False)

    # Remove any self-distances
    dist_agg = dist[dist.src_region!=dist.dest_region]

    # Group by region and average (distances) or sum (shared border)
    aggregations = {'distance_straight'  : 'mean', 
                    'shared_border'      : 'sum',
                    'distance_driving_km': 'mean',
                    'distance_driving_hr': 'mean'}

    dist_agg = dist_agg.groupby(['dest_region']).agg(aggregations)
    dist_agg.index.names = ['region']
    return dist_agg



def compile_distances(src_dir="data/raw/distances",
                     target_dir = 'data/clean',
                     sql_engine=""):
    
    ### Administrative level 1
    dist1 = collect_dist(src_dir, admin_level='admin1')
    #dist_agg1 = aggregate_distances(dist1)
    
    #dist1.to_csv(f"{target_dir}/distances_pairwise_admin1.csv", index=False)
    #dist_agg1.to_csv(f"{target_dir}/distances_admin1.csv")
    
        
    #####################
    # Initialize table
    q = '''
    DROP TABLE IF EXISTS pairwise_distances_admin1 CASCADE;

    CREATE TABLE pairwise_distances_admin1 (
        src_region           TEXT,
        dest_region          TEXT,
        distance_straight    FLOAT,
        shared_border        SMALLINT,
        distance_driving_km  FLOAT,
        distance_driving_hr  FLOAT,

        PRIMARY KEY (src_region, dest_region)
    )
    '''
    sql_engine.execute(q)
    
    #####################
    # Write to SQL database
    dist1.to_sql(
      name      = 'pairwise_distances_admin1',    
      con       = sql_engine,                   
      if_exists = "append", 
      index     = False
    )   
    
    
    ### Administrative level 2
    dist2 = collect_dist(src_dir, admin_level='admin2')
    #dist_agg2 = aggregate_distances(dist2)
    
    # Rename "region" to district (currently all files use "region" naming)
    dist2.rename(columns={'dest_region':'dest_district', 
                         'src_region':'src_district'}, inplace=True)
    #dist_agg2.index.names = ['district']
    
    #dist2.to_csv(f"{target_dir}/distances_pairwise_admin2.csv", index=False)
    #dist_agg2.to_csv(f"{target_dir}/distances_admin2.csv")
    
            

    #####################
    # Initialize table
    q = '''
    DROP TABLE IF EXISTS pairwise_distances_admin2 CASCADE;

    CREATE TABLE pairwise_distances_admin2 (
        src_district         TEXT,
        dest_district        TEXT,
        distance_straight    FLOAT,
        shared_border        SMALLINT,
        distance_driving_km  FLOAT,
        distance_driving_hr  FLOAT,

        PRIMARY KEY (src_district, dest_district)
    )
    '''

    sql_engine.execute(q)
    
    #####################
    # Write to SQL database
    
    dist2.to_sql(
      name      = 'pairwise_distances_admin2',    
      con       = sql_engine,                   
      if_exists = "append", 
      index     = False
    )   
    
    
    #####################
    # Create views
    q = '''
    DROP VIEW IF EXISTS distances_admin1 CASCADE;
    CREATE OR REPLACE VIEW distances_admin1 AS (
        SELECT  dest_region AS region,
                AVG(distance_straight) AS distance_straight,
                SUM(shared_border)     AS shared_border,
                AVG(distance_driving_km) AS distance_driving_km,
                AVG(distance_driving_hr) AS distance_driving_hr
        FROM pairwise_distances_admin1
        GROUP BY region
        ORDER BY region
    );

    DROP VIEW IF EXISTS distances_admin2 CASCADE;
    CREATE OR REPLACE VIEW distances_admin2 AS (
        SELECT  dest_district AS district,
                AVG(distance_straight) AS distance_straight,
                SUM(shared_border)     AS shared_border,
                AVG(distance_driving_km) AS distance_driving_km,
                AVG(distance_driving_hr) AS distance_driving_hr
        FROM pairwise_distances_admin2
        GROUP BY district
        ORDER BY district
    )
    '''
    sql_engine.execute(q)  
    
    return
