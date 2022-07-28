from requests import delete
import data_utils
import os, sys
from Landsat8.spectral_vegatation_indices.VCI import calculate_VCI
import numpy as np


def calc_vcis(root_data_dir = "./data/") :
    vci_data = {}
    for (_, dirnames, _) in os.walk(root_data_dir) :
        for region in dirnames:
            print("Calculating Region: " + region)
            data_utils.process_region_folder(region ,root_data_dir)
    
            region_path = root_data_dir + region
            

           
    
calc_vcis()