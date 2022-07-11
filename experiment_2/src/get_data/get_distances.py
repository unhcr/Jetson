import pandas as pd
import numpy as np
import geopandas as gp
import itertools
import os.path
import time
from tqdm import tqdm_notebook as tqdm
from shapely.geometry import Polygon, Point, MultiPoint, MultiPolygon
import urllib.request, json


def get_biggest_part(multipolygon):
    ''' Takes the biggest part of a multipolygon shape. '''
    
    if multipolygon.geom_type == 'MultiPolygon':
        areas = [i.area for i in multipolygon]
        max_area = areas.index(max(areas))    
        return multipolygon[max_area]
    else:
        return multipolygon  
    
    
    
def get_distances_calculated(gdf, 
                             data_dir = "data/raw/distances",
                             outfilename = "distances_calculated"):
    '''
    Takes in a geopandas dataframe of admin regions ((multi)/polygons) and calculates two things:
        1. Whether the regions border each other
        2. The MINIMUM distance between ANY TWO POINTS in the regions in kilometers;
           The distance is calculated on the LARGEST polygon of multipart regions
        
    gdf      = A shapefile of regions;
               IMPORTANT: assumed to be indexed by the region name
    data_dir = destination directory name
    
    '''
    
    # Get the admin file projected in meters
    gdf = gdf.to_crs({'proj':'cea'}) # I think this projection occurs in meters
    
    # Get a list of regions
    regions = gdf.index.get_level_values(0).unique().tolist()
    
    # Initialize an empty origin destination dataframe
    distances = pd.DataFrame(
                    index = pd.MultiIndex.from_tuples(
                            list(itertools.product(*[regions, regions])
                            ),
                        names = ['dest_region', 'src_region']),
                        columns= ['distance_straight', 'shared_border'])


    for i in tqdm(regions):
        for j in regions:

            # If same polygon: distance=0, shared border=1
            if i==j:
                distances.loc[(i,j)] = [0,1]

            # Otherwise:
            elif i<j: 

                #  Get the shapes for each region
                shape_i = gdf.loc[i].geometry
                shape_j = gdf.loc[j].geometry

                # If shapes touch: distance=0, shared_border=1
                if shape_i.touches(shape_j):
                    distances.loc[(i,j)] = [0,1]
                    distances.loc[(j,i)] = [0,1]

                # Otherwise: calculate distance, shared border=0
                else:

                    shape_i = get_biggest_part(shape_i)
                    shape_j = get_biggest_part(shape_j)

                    dist = shape_i.distance(shape_j)/1000

                    distances.loc[(i,j)] = [dist,0]
                    distances.loc[(j,i)] = [dist,0]

    distances.to_csv(f"{data_dir}/{outfilename}")
    return distances   




def get_distances_osm(gdf, 
                      data_dir = "data/raw/distances",
                      outfilename="distances_osm"):
    '''
    Takes in a geopandas dataframe of admin regions ((multi)/polygons) and returns two things:
        1. An estimate of driving distance between the region CENTROIDS in KILOMETERS
        2. An estimate of the driving time between the region CENTROIDS in HOURS
           The distance is calculated on the LARGEST polygon of multipart regions
        
    gdf      = A shapefile of regions;
               IMPORTANT: assumed to be indexed by the region name
    data_dir = destination directory name
    
    See also:
    
    http://project-osrm.org/docs/v5.22.0/api/#general-options
    
    OSM router:
    http://router.project-osrm.org/route/v1/driving/-73.9985465,40.7289619;-73.9421432,40.8511419?overview=false


    '''
    
    # Get a list of regions
    regions = gdf.index.get_level_values(0).unique().tolist()

    # Initialize an empty origin destination dataframe
    distances = pd.DataFrame(
                    index = pd.MultiIndex.from_tuples(
                        list(itertools.product(*[regions, regions])
                            ),
                    names = ['dest_region', 'src_region']),
                    columns= ['distance_driving_km', 'distance_driving_hr'])


    # Loop through regions pairwise
    for i in tqdm(regions):
        for j in regions:

            # If same polygon: driving distance is zero
            if i==j:
                distances.loc[(i,j)] = [0,0]

            # Otherwise
            else: 
                # Take the largest part of the multipolygons
                shape_i = get_biggest_part(gdf.loc[i].geometry)
                shape_j = get_biggest_part(gdf.loc[j].geometry)

                # Get the centroids
                x_i, y_i = shape_i.centroid.x, shape_i.centroid.y
                x_j, y_j = shape_j.centroid.x, shape_j.centroid.y


                # Get the driving distance between centroids
                url = f"http://router.project-osrm.org/route/v1/car/{x_i},{y_i};{x_j},{y_j}?overview=false"
                data = json.loads(urllib.request.urlopen(url).read().decode())
                t = data['routes'][0]['weight']/3600
                distance = data['routes'][0]['distance']/1000

                # Store it
                distances.loc[(i,j)] = [distance,t]
                
                time.sleep(1)
    

    distances.to_csv(f"{data_dir}/{outfilename}")
    return distances   





def get_distances_all(fpath = 'data/raw/gis',
                      data_dir= "data/raw/distances", 
                      redownload=False):

    '''
    Takes in a pointer to a shapefile of admin region.    
    For each region pair, calls two functions to generate the following variables:
    
    1. get_distances_calculated
        a. Binary indicator of whether the regions border each other
        b. Minimum euclidean distance between region BORDERS, in KM
    2. get_distances_osm
        a. Estimated driving distance between region CENTROIDS, in KM
        b. Estimated driving time between region CENTROIDS, in hours
    
    fpath        = The name of the stored admin boundary shapefile
    index_col    = The name of the column in the boundary shapefile that has 
                    the region names, which will be used as an index;
                    if FALSE, the file is assumed to be indexed already
    data_dir     = destination directory name
    redownload   = if True, redownload all data 
                   if False, download only files not in repository
    '''
    # Get the admin boundary file
    admin1 = gp.read_file(f"{fpath}/somalia_boundaries/Som_Admbnda_Adm1_UNDP.shp")
    admin2 = gp.read_file(f"{fpath}/somalia_boundaries/Som_Admbnda_Adm2_UNDP.shp")
            
    # If index is supplied to be set, set it
    admin1.set_index('admin1Name', inplace=True)
    admin2.set_index('admin2Name', inplace=True)
    
    
    # Check if distance files exist; if not, make them
    file_list = os.listdir(data_dir)
    
    outfilename=f"distances_calculated_admin1.csv"
    if not outfilename in file_list or redownload==True:        
        get_distances_calculated(admin1, data_dir, outfilename)  
                     
    outfilename=f"distances_calculated_admin2.csv"
    if not outfilename in file_list or redownload==True:        
        get_distances_calculated(admin2, data_dir, outfilename)          
    
    outfilename=f"distances_osm_admin1.csv"
    if not outfilename in file_list or redownload==True:        
        get_distances_osm(admin1, data_dir, outfilename) 
                     
    outfilename=f"distances_osm_admin2.csv"
    if not outfilename in file_list or redownload==True:        
        get_distances_osm(admin2, data_dir, outfilename)        


            
            
            