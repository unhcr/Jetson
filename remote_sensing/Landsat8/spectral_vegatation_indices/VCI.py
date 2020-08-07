# -*- coding: utf-8 -*-
"""
Calculating Vegetation Condition Index (VCI)

The Vegetation Condition Index (VCI) is used to monitor vegetation condition.

Vegetation Condition Index (VCI): per pixel NDVI value re-scaled according to the
minimum and maximum values observed over the whole time series (Kogan, 1990)

VCI definition:
Kogan proposed a Vegetation Condition Index (VCI) based on the relative Normalized Difference Vegetation Index (NDVI)
change with respect to minimum historical NDVI value. The VCI therefore compares the current Vegetation Index (VI)
such as NDVI or Enhanced Vegetation Index (EVI) to the values observed in the same period in previous years within a specific pixel.

Reference: Kogan, F. N. F. Remote sensing of weather impacts on vegetation in non-homogeneous areas.
           International Journal of Remote Sensing 1990, 11, 1405–1419.

Code based on 'Step by step: Drought monitoring using the Vegetation Condition Index (VCI) in Python'
http://www.un-spider.org/advisory-support/recommended-practices/recommended-practice-drought-monitoring-vci-python

"""
import os
import numpy as np
import random

from remote_sensing.Landsat8.spectral_vegatation_indices.NDVI import calculate_NDVI
import earthpy.plot as ep
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

from remote_sensing.Landsat8.spectral_vegatation_indices.calculate_VCI import calculate_VCI as calc_VCI

import rasterio as rio
import matplotlib.colors as colors


def calculate_VCI(selected_full_filename,
                  study_dir_of_stacked_raster):
    """
    Calculate current Vegetation Index (NDVI)
    """

    print("[INFO] Start calculating NDVI for the selected '%s' \n " % selected_full_filename)

    current_ndvi = calculate_NDVI(selected_full_filename)

    row_NDVI, col_NDVI = current_ndvi.shape

    print("[INFO] Start calculating min and max historical NDVI values for the selected study period\n ")

    for dirName, subdirList, fileList in os.walk(study_dir_of_stacked_raster, topdown=True):
        number_of_subdirs = len(subdirList)

        # os.walk without hidden folders
        files = [f for f in fileList if not f[0] == '.']

        """
        Two instances of NDVI arrays are required to calculate min and max historical NDVI values, 
        so we need to have a temporary NDVI calculated. 
    
        A random integer can be generated for that purpose - fileList[random_num], but we go with the first element of the list files[0]
        """

        # random_num = random.randint(0, (len(files)-1))

        tmp_full_filename = os.path.join(study_dir_of_stacked_raster, files[0])

        tmp_ndvi = calculate_NDVI(tmp_full_filename)

        tmp_row, tmp_col = tmp_ndvi.shape

        """
        Pad the arrays for instances that do not have the same size with the NDVI of the selected date (current_ndvi)
        """

        if row_NDVI != tmp_row:

            if row_NDVI > tmp_row:  # NDVI array of selected date has more rows that the historical NDVI array, apply padding
                tmp_row_dif = row_NDVI - tmp_row
                tmp_ndvi = np.pad(tmp_ndvi, ((0, tmp_row_dif), (0, 0)), 'edge')
            else:  # NDVI array of selected date has fewer rows that the historical NDVI array, so padding cannot be applied
                tmp_row_dif = tmp_row - row_NDVI
                print(
                    "[WARNING] Historical NDVI array has lower number of rows compared to the NVDI array of the selected date")
                break

        if col_NDVI != tmp_col:

            if col_NDVI > tmp_col:
                tmp_col_dif = col_NDVI - tmp_col
                tmp_ndvi = np.pad(tmp_ndvi, ((0, 0), (0, tmp_col_dif)), 'edge')
            else:
                tmp_col_dif = tmp_col - col_NDVI
                print(
                    "[WARNING] Historical NDVI array has lower number of columns compared to the NVDI array of the selected date")

        for file in files:

            # the first element of the files list, files[0], has been already utilised for NDVI calculation,
            # so there's no need to calculate it again.
            # if file == files[0]:
            #     print("[WARNING] Skipping iteration")
            #     continue

            print("    ‣ Calculating NDVI for '%s'" % file)

            running_full_filename = os.path.join(study_dir_of_stacked_raster, file)

            running_ndvi = calculate_NDVI(running_full_filename)

            # print("Historival NDVI shape:", running_ndvi.shape)

            row, col = running_ndvi.shape

            if row == row_NDVI and col == col_NDVI:
                min_ = np.minimum.reduce([tmp_ndvi, running_ndvi])
                max_ = np.maximum.reduce([tmp_ndvi, running_ndvi])
                tmp_ndvi = running_ndvi
            else:
                print(
                    "        [WARNING] Historical NDVI array of '%s' is not the same shape with the calculated NDVI of the selected date" % file)

                """
                Pad the arrays for instances that do not have the same size with the NDVI of the selected date (current_ndvi)
                """

                if row_NDVI != row:

                    if row_NDVI > row:

                        row_dif = row_NDVI - row
                        running_ndvi = np.pad(running_ndvi, ((0, row_dif), (0, 0)), 'edge')
                    else:
                        row_dif = row - row_NDVI
                        break

                if col_NDVI != col:

                    if col_NDVI > col:
                        col_dif = col_NDVI - col
                    else:
                        col_dif = col - col_NDVI

                    running_ndvi = np.pad(running_ndvi, ((0, 0), (0, col_dif)), 'edge')

                rowxxx, colxxx = running_ndvi.shape

                min_ = np.minimum.reduce([tmp_ndvi, running_ndvi])
                max_ = np.maximum.reduce([tmp_ndvi, running_ndvi])
                tmp_ndvi = running_ndvi

    print("\n")

    print("[INFO] Calculating the actual Vegetation Condition Index (VCI) \n")

    # Calculate the VCI

    vci = calc_VCI(current_ndvi, min_, max_)

    return vci


def plot_VCI(vci,
             selected_full_filename):

    average_VCI = np.average(vci)

    print('    ‣ Average VCI: ', round(average_VCI, 2), '\n')

    print("[INFO] Start plotting the data \n")

    titles = ["[Landsat 8] Vegetation Condition Index (VCI) - %s" % os.path.splitext(os.path.basename(selected_full_filename))[0]]

    ep.plot_bands(vci,
                  cmap="RdYlGn",
                  cols=1,
                  title=titles,
                  scale=False,
                  vmin=0, vmax=100
                  )


def classify_VCI(vci,
                 selected_full_filename):
    # Create classes and apply to NDVI results
    vci_class_bins = [0.4, 0.5, 0.7, 0.95]
    vci_landsat_class = np.digitize(vci, vci_class_bins)

    # Apply the nodata mask to the newly classified NDVI data
    vci_landsat_class = np.ma.masked_where(np.ma.getmask(vci), vci_landsat_class)
    np.unique(vci_landsat_class)

    # print (type(vci_landsat_class))

    """
    Plot Classified NDVI With Categorical Legend - EarthPy Draw_Legend()
    """

    # Define color map
    # https://loading.io/color/feature/RdYlGn-9/
    nbr_colors = ["#d7191c", "#fdae61", "#ffffbf", "#a6d96a", "#1a9641"]

    nbr_cmap = ListedColormap(nbr_colors)

    vci_cat_names = [
        "Very Low Vegetation",
        "Low Vegetation",
        "Average Vegetation",
        "High Vegetation",
        "Very High Vegetation",
    ]

    # Get list of classes
    classes = np.unique(vci_landsat_class)
    classes = classes.tolist()
    # The mask returns a value of none in the classes. remove that
    classes = classes[0:5]

    # Plot your data
    fig, ax = plt.subplots(figsize=(12, 12))
    im = ax.imshow(vci_landsat_class, cmap=nbr_cmap)

    # print("List of classes: ", classes)

    ep.draw_legend(im_ax=im, classes=classes, titles=vci_cat_names)
    ax.set_title('VCI distribution in the area of %s' % os.path.splitext(os.path.basename(selected_full_filename))[0],
                 fontsize=14)

    ax.set_axis_off()

    # Auto adjust subplot to fit figure size
    plt.tight_layout()

    plt.show()

    plot_filename = os.path.splitext(os.path.basename(selected_full_filename))[0] + '.pdf'

    name_to_file = plot_filename

    fig.savefig(name_to_file)
