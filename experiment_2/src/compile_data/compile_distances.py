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
                     target_dir = 'data/clean'):
    
    ### Administrative level 1
    dist1 = collect_dist(src_dir, admin_level='admin1')
    dist_agg1 = aggregate_distances(dist1)
    
    dist1.to_csv(f"{target_dir}/distances_pairwise_admin1.csv", index=False)
    dist_agg1.to_csv(f"{target_dir}/distances_admin1.csv")
                      
    
    ### Administrative level 2
    dist2 = collect_dist(src_dir, admin_level='admin2')
    dist_agg2 = aggregate_distances(dist2)
    
    # Rename "region" to district (currently all files use "region" naming)
    dist2.rename(columns={'dest_region':'dest_district', 
                         'source_region':'source_district'}, inplace=True)
    dist_agg2.index.names = ['district']
    
    dist2.to_csv(f"{target_dir}/distances_pairwise_admin2.csv", index=False)
    dist_agg2.to_csv(f"{target_dir}/distances_admin2.csv")
    
    
    