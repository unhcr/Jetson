# -*- coding: utf-8 -*-
"""Utilities related to Landsat 8 image processing.
"""

import glob, os
import re
import numpy as np
from skimage import io, exposure
from matplotlib import pyplot as plt
import earthpy as et
import earthpy.spatial as es
import earthpy.plot as ep
import rasterio as rio
from tqdm import trange
import calendar



from glob import glob  # File manipulation



def image_adjust_brightness(img, limit_left, limit_right, color_map, title, to_file):
    """Adjust image brightness and plot the image
    # Arguments
        img: 2D array of uint16 type
        limit_left: integer
        limit_right: integer
        color_map: string
        title: string
        to_file: file name of the figure to be saved

     # Returns
        Image array after rescaling its intensity. This image is the same dtype as the input image.

    """
    img_ha = exposure.rescale_intensity(img, (limit_left, limit_right))
    fig = plt.figure(figsize=(10, 10))
    fig.set_facecolor('white')
    plt.imshow(img_ha, cmap=color_map)
    plt.title(title)
    plt.show()
    fig.savefig(to_file)

    return img_ha


def read_band(n):
    """Load Landsat 8 band. Raw images must be in the form of 'Bn.tif'
    # Arguments
        n: integer in the range 1-11
    # Returns
        2D image array of uint16 type
    """
    if n in range(1, 12):
        tif_list = glob.glob("*.tif")
        band_name = 'B' + str(n) + '.tif'
        img_idx = [idx for idx, band_string in enumerate(tif_list) if band_name in band_string]
        img = io.imread(tif_list[img_idx[0]])
        return img
    else:
        print('Band number has to be in the range 1-11!')


def image_show(img, color_map, title):
    """Show image
    # Arguments
        img: 2D array of uint16 type
        color_map: string
        title: string
    """
    fig = plt.figure(figsize=(10, 10))
    fig.set_facecolor('white')
    plt.imshow(img, cmap=color_map)
    plt.title(title)
    plt.show()

def color_image_show(img, title):
    """Show colour image
    # Arguments
        img: 3D array of uint16 type
        color_map: string
        title: string
    """
    fig = plt.figure(figsize=(10, 10))
    fig.set_facecolor('white')
    plt.imshow(img/65535)
    plt.title(title)
    plt.show()


def image_histogram(img):
    """Plot image histogram
    # Arguments
        img: 2D array of uint16 type
    """
    co, ce = exposure.histogram(img)

    fig = plt.figure(figsize=(10, 7))
    fig.set_facecolor('white')
    plt.plot(ce[1::], co[1::])
    plt.show()


def get_gain_bias_angle(n):
    """Get band reflectance gain, bias, and Sun elevation angle
    # Arguments
        n: integer in the range 1-11
    # Returns
        gain: float
        bias: float
    """
    if n in range(1, 10):
        n_str = str(n)
        s_g = 'REFLECTANCE_MULT_BAND_' + n_str + ' = '
        s_b = 'REFLECTANCE_ADD_BAND_' + n_str + ' = '

        fn = glob.glob("*._ML.txt")
        fn = glob.glob("*.txt")

        f = open(fn[0], 'r+')

        search_str_g = '(?<=' + s_g + ').*'
        search_str_b = '(?<=' + s_b + ').*'
        search_str_a = '(?<=' + 'SUN_ELEVATION = ' + ').*'

        for line in f:
            s0 = re.search(search_str_a, line)
            s1 = re.search(search_str_g, line)
            s2 = re.search(search_str_b, line)
            if s0:
                angle = float(s0.group(0))
            elif s1:
                gain = float(s1.group(0))
            elif s2:
                bias = float(s2.group(0))

        f.close()

        return gain, bias, angle
    else:
        print('Band number has to be in the range 1-9!')



def get_list_of_data(path,
                     create_stacked_raster = False):
    """Get list of all downloaded data and sort the data, and finally convert a list of raster paths into a raster stack numpy darray.
        Stacking the Landsat 8 bands creates a numpy array with each "layer" representing a single band.

        Adapted from:: https://www.earthdatascience.org/courses/use-data-open-source-python/multispectral-remote-sensing/landsat-in-Python/

    # Arguments
        path: where the .tif files are stored
    # Returns
        land_stack: N-dimensional array created by stacking the raster files provided.
        land_meta: A rasterio profile object containing the updated spatial metadata for the stacked numpy array.
        landsat_post_process_path: directory of the created stacked raster with all bands
    """

    # Get list of all data and sort the data
    all_landsat_post_bands = glob(path + "/*band*.tif")
    all_landsat_post_bands.sort()

    tmp_path = os.path.join(path, "outputs")

    if not os.path.exists(tmp_path):
        print ('Creating new path..')
        os.makedirs(tmp_path)

    # Create an output array of all the landsat data stacked
    landsat_post_process_path = os.path.join(path, "outputs", "landsat_post.tif")

    # This will create a new stacked raster with all bands
    # This creates a numpy array with each "layer" representing a single band
    land_stack, land_meta = es.stack(all_landsat_post_bands,
                                     landsat_post_process_path)


    return land_stack, land_meta, landsat_post_process_path


def create_raster_stack(rootDir,
                        region_name):
    """Gets list of all downloaded data, sorts the data, and finally converts a list of raster paths into a raster stack numpy darray.
        Stacking the Landsat 8 bands creates a numpy array with each "layer" representing a single band.
        A new directory with the name "raster_stack" is created that will contain all raster stack numpy arrays from the raw data.

        Adapted from:: https://www.earthdatascience.org/courses/use-data-open-source-python/multispectral-remote-sensing/landsat-in-Python/

    # Arguments
        rootDir: main working directory (represents a whole region)

        Assumes directory structure:
        rootDir/
                LC081610532016112201T1-SC20200512113013/
                                                       xxx_band1.tif
                                                       xxx_band2.tif
                                                       ...
                LC081610532017082101T1-SC20200512113005/
                                                       xxx_band1.tif
                                                       xxx_band2.tif
                                                       ...

        region_name: name given by the user, indicating the region to be studied

    """


    tmp_path = os.path.join(rootDir, "raster_stack")

    if not os.path.exists(tmp_path):
        print("[INFO] 'raster_stack' subdirectory successfully created")
        os.makedirs(tmp_path)


    # Start traversing the root directory

    for dirName, subdirList, fileList in os.walk(rootDir):
        number_of_subdirs = len(subdirList)
        if 'raster_stack' in subdirList:
            subdirList.remove('raster_stack')

        # print('Found subdirectory: %s' % subdirList)
        # for fname in fileList:
        #     print('\t%s' % fname)

        for current_folder in subdirList:
            # print('number of subdirs: ', len(subdirList))

            current_working_dir = dirName + '/' + current_folder


            # print("[INFO] Processing ", current_working_dir, " folder")

            # Get list of all data and sort the data
            all_landsat_post_bands = glob(current_working_dir + "/*B*.TIF")
            #all_landsat_post_bands.sort()

            # CHANGE THIS TO EXCLUDE EXTRA BANDS BEYOND 7
            all_landsat_post_bands = [band for band in all_landsat_post_bands if "B10" not in band and "B11" not in band and "B9" not in band and "B8" not in band]
            #all_landsat_post_bands = all_landsat_post_bands[:-2]
            #print(all_landsat_post_bands)

            formatted_filename = format_landsat_product_identifier(current_folder,region_name)
            # print ('formatted_filename: ',formatted_filename)

            print("[INFO] Processing ", formatted_filename)

            # basename = os.path.basename(formatted_name) + '.tif'
            #
            # print('basename: ', basename)



            # Create an output array of all the landsat data stacked
            new_raster_stack_path = os.path.join(rootDir, "raster_stack", formatted_filename)

            print ("[INFO] New raster stack created as '",new_raster_stack_path,"'")

            # This will create a new stacked raster with all bands
            # This creates a numpy array with each "layer" representing a single band
            land_stack, land_meta = es.stack(all_landsat_post_bands,
                                             new_raster_stack_path,
                                             9999)


    print("[INFO] Raster stack numpy arrays have been successfully created")



def format_landsat_product_identifier(folder,
                                      region_name):

    # format filename to extract collection date
    year = folder[17:21]
    month = folder[21:23]
    date = folder[23:25]

    print(year, month, date)

    month_name = calendar.month_name[int(month)]
    month_name_abbr = calendar.month_abbr[int(month)]

    formatted_filename = region_name + '-' + year + '-' + month_name_abbr + '-' + date + '.tif'


    return formatted_filename


def plot_RGB_composite_image(path,
                             to_file,
                             mask_missing_values=True):



    """Adapted from https://earthpy.readthedocs.io/en/latest/gallery_vignettes/plot_rgb.html#sphx-glr-gallery-vignettes-plot-rgb-py

    To plot band combinations and create composite images using plot_rgb(),
    the bands of a satellite image such as those from Landsat, need to be stacked into one file.
    With EarthPy, you can create an image stack from all of the Landsat .tif files (one per band)
    in a directory using the stack() function from the earthpy.spatial module.

    # Arguments
        path: main working directory, where all bands have been extracted
        to_file: filename given to the plot
        mask_missing_values: whether to mask invalid or missing values in the output

    """


    # Get list of all data and sort the data
    all_landsat_post_bands = glob(path + "/*band*.tif")

    # print (all_landsat_post_bands)
    all_landsat_post_bands.sort()

    tmp_path = os.path.join(path, "RGB_composite_image")

    if not os.path.exists(tmp_path):
        print ('[INFO] Creating new path...')
        os.makedirs(tmp_path)

    # Create an output array of all the landsat data stacked
    landsat_post_process_path = os.path.join(path, "RGB_composite_image", "stacked_landsat.tif")

    if mask_missing_values:
        # Create image stack and apply nodata value for Landsat
        land_stack, land_meta = es.stack(band_paths=all_landsat_post_bands,
                                         out_path=landsat_post_process_path,
                                         nodata=-9999)
    else:
        # Create image stack and apply nodata value for Landsat
        land_stack, land_meta = es.stack(band_paths=all_landsat_post_bands,
                                         out_path=landsat_post_process_path)



    # Create figure with one plot
    fig, ax = plt.subplots(figsize=(12, 12))

    # Plot red, green, and blue bands, respectively
    ep.plot_rgb(land_stack, rgb=(3, 2, 1), ax=ax, title="Landsat 8 RGB Image")
    plt.show()




    fig.savefig(to_file)


def plot_RGB_composite_image_from_stack(full_filename,
                                        to_file):
    """Adapted from https://earthpy.readthedocs.io/en/latest/gallery_vignettes/plot_rgb.html#sphx-glr-gallery-vignettes-plot-rgb-py

    To plot band combinations and create composite images using plot_rgb(),
    the bands of a satellite image such as those from Landsat, need to be stacked into one file.
    With EarthPy, you can create an image stack from all of the Landsat .tif files (one per band)
    in a directory using the stack() function from the earthpy.spatial module.

    # Arguments
        full_filename: /path/where/image/stack/is/stored/xxxx.tif
        to_file: filename given to the plot
    """

    with rio.open(full_filename) as src:
        landsat_stacked_data = src.read(masked=True)  # stacked raster (NumPy array) with each "layer" representing a single band


    # Create figure with one plot
    fig, ax = plt.subplots(figsize=(12, 12))

    # Plot red, green, and blue bands, respectively
    ep.plot_rgb(landsat_stacked_data, rgb=(3, 2, 1), ax=ax, title="Landsat 8 RGB Image")
    plt.show()

    fig.savefig(to_file)

