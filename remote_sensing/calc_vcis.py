from Landsat8.landsat8_utils import create_raster_stack
from osgeo import gdal
from Landsat8.spectral_vegatation_indices.VCI import calculate_VCI, plot_VCI, classify_VCI
from utils import splitall
import os
import numpy as np
import pandas as pd

vci_data = {}
for (dirpath, dirnames, filenames) in os.walk("./data/") :
    for region in dirnames :
        region_path = "./data/" + region
        kml_path = region_path + "/" + region + ".kml"
        create_raster_stack(region_path, region)
        os.mkdir(region_path + "/raster_stack/clipped/")

        for (dirpath, dirnames, filenames) in os.walk(region_path + "/raster_stack") :
            for stack in filenames:
                OutTile = gdal.Warp(region_path  + "/raster_stack/clipped/" + stack, 
                    region_path + "/raster_stack/" + stack, 
                    cutlineDSName=kml_path,
                    cropToCutline=True,
                    dstNodata = 0)

                OutTile = None
        
        for (dirpath, dirnames, filenames) in os.walk(region_path  + "/raster_stack/clipped/") :
            region_vci_data = {}
            for stack in filenames:
                vci = calculate_VCI(region_path  + "/raster_stack/clipped/" +stack, region_path  + "/raster_stack/clipped/")
                region_vci_data[stack.replace(".tif", "").replace(region + "-", "")] = np.average(vci)
        
        vci_data[region] = vci_data


df = pd.DataFrame(vci_data)
df.to_excel("VCI.xlsx")