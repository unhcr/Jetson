from requests import delete
import data_utils
import os, sys
from Landsat8.spectral_vegatation_indices.VCI import calculate_VCI, plot_VCI, classify_VCI
import numpy as np
import datetime
from pathlib import Path
import shutil


def calc_vcis(root_data_dir = "./data/") :
    vci_data = {}
    for (_, dirnames, _) in os.walk(root_data_dir) :
        for region in dirnames:
            print("Calculating Region: " + region)
            data_utils.process_region_folder(region ,root_data_dir)
    
            region_path = root_data_dir + region


def calc_vci_region_year_month(data_dir, region, year, month) :
    '''
    calculates vci for the specified region on the specified year-month pair
    '''
    region_path = os.path.join(data_dir, region)
    target_tif_path = os.path.join(data_dir, region, str(year) + '_' + str(month), str(year) + '_' + str(month) + '.tif')

    # copying rasters from previous years to new folder
    # TODO: change calculate vci to avoid copying again

    previous_dirs = []
    for (dirpath, dirnames, filenames) in os.walk(region_path) :
           for dir in dirnames :
                if int(dir[:4]) < year :
                     previous_dirs.append(dir)

    study_path = os.path.join(data_dir, region, 'study')
    Path(study_path).mkdir(exist_ok=True)

    for dir in previous_dirs :
         prev_year, prev_month = dir.split('_')[0], dir.split('_')[1]
         src_filename = os.path.join(data_dir, region, str(prev_year) + '_' + str(prev_month), str(prev_year) + '_' + str(prev_month) + '.tif')
         dest_filename = study_path + str(prev_year) + '_' + str(prev_month) + '.tif'
         shutil.copyfile(src_filename, dest_filename)

    vci = calculate_VCI(target_tif_path, study_path)
    plot_VCI(vci, region)
    classify_VCI(vci, region)
    shutil.rmtree(study_path)

calc_vci_region_year_month("./data", 'Baki', 2023, 10)