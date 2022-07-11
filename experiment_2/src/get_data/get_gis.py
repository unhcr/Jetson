import geopandas as gp
import os
import urllib.request
import zipfile

def get_gis_all(data_dir ='data/raw/gis', redownload=False):
    ''' 
    Downloads Somalia admin boundaries.
    
    data_dir   = destination directory name
    redownload   = if True, redownload all data 
                   if False, download only if not in repository
    
    '''
    
    url = "https://data.humdata.org/dataset/ec140a63-5330-4376-a3df-c7ebf73cfc3c/resource/6f42e9ce-bbca-4c0d-a3e6-85efc9298c3c/download/som_adm_undp_shp.zip"
    
    fname= 'somalia_boundaries'
    
    # Download the file if it doesn't exist or redownload is requested
    if not os.path.isdir(f'{data_dir}/{fname}/') or redownload==True:
            
            cwd = os.getcwd().replace("\\", "/")
            
            urllib.request.urlretrieve(url, f"{cwd}/{data_dir}/{fname}.zip")
            
            zip_ref = zipfile.ZipFile(f"{data_dir}/{fname}.zip", 'r')
            zip_ref.extractall(f"{data_dir}/{fname}/")
            zip_ref.close()
            os.remove(f"{cwd}/{data_dir}/{fname}.zip")

            print(f"Redownloaded: {fname}")

    
    
    
    
    