# -*- coding: utf-8 -*-
"""
Calculating Modified Normalized Difference Water Index (MNDWI)

MNDWI = (Green – SWIR) / (Green + SWIR)

- For Landsat 7 data, NDWI = (Band 2 – Band 5) / (Band 2 + Band 5)

- For Landsat 8 data, NDWI = (Band 3 – Band 6) / (Band 3 + Band 6)


Ref: https://www.linkedin.com/pulse/ndvi-ndbi-ndwi-calculation-using-landsat-7-8-tek-bahadur-kshetri/

"""

from drought_prediction.utils.landsat8.landsat8_utils import read_band,image_show, image_histogram, image_adjust_brightness, get_gain_bias_angle

# """
# Read bands
# """
b3 = read_band(3)
b4 = read_band(4)
b5 = read_band(5)
b6 = read_band(6)


# """
# Calculate MNDWI
# """


# For Landsat 8 data, MNDWI = (Band 3 – Band 6) / (Band 3 + Band 6)

MNDWI = (b3 - b6)/(b3 + b6)

img_ha = image_adjust_brightness(MNDWI,
                                 -0.7695, 1.459,
                                 'Blues',  #find other colourmaps https://matplotlib.org/tutorials/colors/colormaps.html
                                 'Modified Normalized Difference Water Index (MNDWI)',
                                 to_file='code-generated-MNDWI.png')


