import geopandas as gp
import os.path

def get_gis_all(data_dir ='data/raw/gis', redownload=False):
    ''' 
    Downloads Somalia admin boundaries.
    
    data_dir   = destination directory name
    redownload   = if True, redownload all data 
                   if False, download only if not in repository
    
    '''
    
    url1 = "https://data.humdata.org/dataset/ec140a63-5330-4376-a3df-c7ebf73cfc3c/resource/0353bb25-919e-40d7-be7d-831376bc4f76/download/som_admbnda_adm1_undp.zip"
    
    
    url2 = "https://data.humdata.org/dataset/ec140a63-5330-4376-a3df-c7ebf73cfc3c/resource/a58ba039-7423-4241-b2cb-0534c46f295d/download/som_admbnda_adm2_undp.zip"
    
    fname1= 'somalia_boundaries_admin1'
    fname2= 'somalia_boundaries_admin2'
    
    # Download the file if it doesn't exist or redownload is requested
    for fname,url in [[fname1, url1],
                      [fname2, url2]]:
        
        if not os.path.exists(f'{data_dir}/{fname}/{fname}.shp') or redownload==True:

            admin = gp.read_file(url)
            admin.to_file(
                f'{data_dir}/{fname}', 
                driver='ESRI Shapefile')

            print(f"Redownloaded: {fname}")

    
    
    
    
    