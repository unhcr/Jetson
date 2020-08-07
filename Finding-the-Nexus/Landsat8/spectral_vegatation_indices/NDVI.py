# -*- coding: utf-8 -*-
"""
Calculating Normalized Difference Vegetation Index (NDVI)

The normalized difference vegetation index (NDVI) is used to assess the state of vegetation.
In living plants chlorophyll-A, from the photosynthetic machinery, strongly absorbs red color;
on the other hand, near-infrared light is strongly reflected.
Live, healthy vegetation reflects around 8% of red light and 50% of near-infrared light.
Dead, unhealthy, or sparse vegetation reflects approximately 30% of red light and 40% of near-infrared light.

By its formulation, NDVI ranges from -1 to +1. In practice, an area of an image containing living vegetation will have NDVI in the range 0.3 to 0.8.
High water content clouds and snow will have negative values of the index. Bodies of water, having low reflectance in both Band 4 and 5,
exhibit very low positive or negative index. Soil, having slightly higher reflectance in near-infrared than in red, will produce low positive values of the index.

- In Landsat 8, NDVI = (Band 5 – Band 4) / (Band 5 + Band 4).

Ref: https://nbviewer.jupyter.org/github/HyperionAnalytics/PyDataNYC2014/blob/master/ndvi_calculation.ipynb



"""


from matplotlib import pyplot as plt
import earthpy.spatial as es
import rasterio as rio
import numpy as np
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
import earthpy.plot as ep
import os

from Landsat8.landsat8_utils import get_list_of_data
import argparse
from Landsat8.landsat8_utils import create_raster_stack

from utils import splitall


# def get_args():
#     parser = argparse.ArgumentParser()
#
#     parser.add_argument("--root_dir", type = str, help = 'main working directory of previously stacked data')
#
#     parser.add_argument("--product_id", type = str, help = 'Landsat 8 product identifier')
#
#     args = parser.parse_args()
#     return args
#
#
# args = get_args()
#
# filename = args.product_id + '.tif'
#
# landsat_post_process_path = os.path.join(args.root_dir, 'raster_stack', filename)


# def calculate_NDVI(root_dir,
#                    raster_stacked_filename):
#     landsat_post_process_path = os.path.join(root_dir, 'raster_stack', raster_stacked_filename)
#
#     # Once you have stacked your data, you can import it and work with it as you need to!
#     with rio.open(landsat_post_process_path) as src:
#         landsat_stacked_data = src.read(masked=True)  # stacked raster (NumPy array) with each "layer" representing a single band
#
#     nir_band = landsat_stacked_data[5]
#     red_band = landsat_stacked_data[4]
#
#     # Calculate normalized difference vegetation index
#     ndvi = es.normalized_diff(b1=nir_band, b2=red_band)
#
#     return ndvi


# def calculate_NDVI(root_dir,
#                    raster_stacked_filename):
#     landsat_post_process_path = os.path.join(root_dir, 'raster_stack', raster_stacked_filename)
#
#     # Once you have stacked your data, you can import it and work with it as you need to!
#     with rio.open(landsat_post_process_path) as src:
#         landsat_stacked_data = src.read(masked=True)  # stacked raster (NumPy array) with each "layer" representing a single band
#
#     nir_band = landsat_stacked_data[5]
#     red_band = landsat_stacked_data[4]
#
#     # Calculate normalized difference vegetation index
#     ndvi = es.normalized_diff(b1=nir_band, b2=red_band)
#
#     return ndvi



def calculate_NDVI(full_filename):
    """Calculates Normalized Difference Vegetation Index (NDVI)

    # Arguments
        full_filename: /path/where/image/stack/is/stored/xxxx.tif
        to_file: filename given to the plot
        mask_missing_values: whether to mask invalid or missing values in the output
    """

    with rio.open(full_filename) as src:
        landsat_stacked_data = src.read(masked=True)

    nir_band = landsat_stacked_data[5]
    red_band = landsat_stacked_data[4]

    # Calculate normalized difference vegetation index
    ndvi = es.normalized_diff(b1=nir_band, b2=red_band)

    return ndvi




# def calculate_NDVI_manually(root_dir,
#                             raster_stacked_filename):
#     landsat_post_process_path = os.path.join(root_dir, 'raster_stack', raster_stacked_filename)
#
#     # Once you have stacked your data, you can import it and work with it as you need to!
#     with rio.open(landsat_post_process_path) as src:
#         landsat_stacked_data = src.read(masked=True)  # stacked raster (NumPy array) with each "layer" representing a single band
#
#     print (landsat_stacked_data.shape)
#
#     nir_band = landsat_stacked_data[5]
#     red_band = landsat_stacked_data[4]
#
#
#     # Calculate normalized difference vegetation index
#     ndvi = (nir_band-red_band)/(nir_band+red_band)
#
#     return ndvi


# def plot_NDVI(root_dir,
#               raster_stacked_filename):
#
#     landsat_post_process_path = os.path.join(root_dir, 'raster_stack', raster_stacked_filename)
#
#     # Once you have stacked your data, you can import it and work with it as you need to!
#     with rio.open(landsat_post_process_path) as src:
#         landsat_stacked_data = src.read(
#             masked=True)  # stacked raster (NumPy array) with each "layer" representing a single band
#
#     nir_band = landsat_stacked_data[5]
#     red_band = landsat_stacked_data[4]
#
#     # Calculate normalized difference vegetation index
#     ndvi = es.normalized_diff(b1=nir_band, b2=red_band)
#
#
#     titles = ["Bari - %s - Normalized Difference Vegetation Index (NDVI)" % raster_stacked_filename]
#
#     # Turn off bytescale scaling due to float values for NDVI
#     ep.plot_bands(ndvi,
#                   cmap="RdYlGn",
#                   cols=1,
#                   title=titles,
#                   scale=False,
#                   vmin=-1, vmax=1
#                   )



def plot_NDVI(ndvi,
              raster_stacked_filename):

    titles = ["Bari - %s - Normalized Difference Vegetation Index (NDVI)" % raster_stacked_filename]

    # Turn off bytescale scaling due to float values for NDVI
    ep.plot_bands(ndvi,
                  cmap="RdYlGn",
                  cols=1,
                  title=titles,
                  scale=False,
                  vmin=-1, vmax=1
                  )


def classify_NDVI(ndvi,
                  raster_stacked_filename):
    """
    Classify NDVI - Categorise (or classify) the NDVI results into useful classes.
    Values under 0 will be classified together as no vegetation.
    Additional classes will be created for bare area and low, moderate, and high vegetation areas.
    """
    #
    # landsat_post_process_path = os.path.join(root_dir, 'raster_stack', raster_stacked_filename)
    #
    # # Once you have stacked your data, you can import it and work with it as you need to!
    # with rio.open(landsat_post_process_path) as src:
    #     landsat_stacked_data = src.read(
    #         masked=True)  # stacked raster (NumPy array) with each "layer" representing a single band
    #
    # nir_band = landsat_stacked_data[5]
    # red_band = landsat_stacked_data[4]
    #
    # # Calculate normalized difference vegetation index
    # ndvi = es.normalized_diff(b1=nir_band, b2=red_band)

    # Create classes and apply to NDVI results
    ndvi_class_bins = [-np.inf, 0, 0.1, 0.25, 0.4, np.inf]
    ndvi_landsat_class = np.digitize(ndvi, ndvi_class_bins)

    # Apply the nodata mask to the newly classified NDVI data
    ndvi_landsat_class = np.ma.masked_where(np.ma.getmask(ndvi), ndvi_landsat_class)
    np.unique(ndvi_landsat_class)

    """
    Plot Classified NDVI With Categorical Legend - EarthPy Draw_Legend()
    """

    # Define color map
    nbr_colors = ["gray", "y", "yellowgreen", "g", "darkgreen"]
    nbr_cmap = ListedColormap(nbr_colors)

    # Define class names
    ndvi_cat_names = [
        "No Vegetation",
        "Bare Area",
        "Low Vegetation",
        "Moderate Vegetation",
        "High Vegetation",
    ]

    # Get list of classes
    classes = np.unique(ndvi_landsat_class)
    classes = classes.tolist()
    # The mask returns a value of none in the classes. remove that
    classes = classes[0:5]

    # Plot your data
    fig, ax = plt.subplots(figsize=(12, 12))
    im = ax.imshow(ndvi_landsat_class, cmap=nbr_cmap)

    print("List of classes: ", classes)

    ep.draw_legend(im_ax=im, classes=classes, titles=ndvi_cat_names)
    ax.set_title("%s - Normalized Difference Vegetation Index (NDVI) Classes" % raster_stacked_filename,
                 fontsize=14)

    ax.set_axis_off()

    # Auto adjust subplot to fit figure size
    plt.tight_layout()

    plt.show()

    name_to_file = raster_stacked_filename + '.pdf'

    fig.savefig(name_to_file)

    # print('NDVI 2-D numpy array shape: ',ndvi.shape)
    # print('NDVI 1-D vector shape: ',ndvi.ravel().shape)
    # print('NDVI min value: ', ndvi.min())
    # print('NDVI max value: ', ndvi.max())



if __name__ == '__main__':

    full_filename = '/Users/gkalliatakis/Desktop/espa-gkallia@essex.ac.uk-0102006107904/raster_stack/Hiraan-2017-Apr-20.tif'

    allparts, raster_stacked_filename = splitall(full_filename)


    ndvi=calculate_NDVI(full_filename)

    plot_NDVI(ndvi,raster_stacked_filename)

    classify_NDVI(ndvi,raster_stacked_filename)

