# -*- coding: utf-8 -*-
"""
Calculate change in NDVI over time

- In Landsat 8, NDVI = (Band 5 – Band 4) / (Band 5 + Band 4).

Ref: https://geohackweek.github.io/raster/04-workingwithrasters/

"""
from drought_prediction.utils.landsat8.landsat8_utils import read_band,image_show, image_histogram, image_adjust_brightness, get_gain_bias_angle



# """
# Read bands
# """
b4 = read_band(4)
b5 = read_band(5)

# """
# Get reflectance gain and bias, and Sun elevation angle; calculate top-of-atmosphere reflectance
# """
#
#
# b4_gain, b4_bias, angle = get_gain_bias_angle(4)
# b5_gain, b5_bias, angle = get_gain_bias_angle(5)
#
# b4_lambda_refl  = (b4_gain * b4 + b4_bias) / np.sin(angle)
# b5_lambda_refl  = (b5_gain * b5 + b5_bias) / np.sin(angle)
#
#
# """
# Calculate NDVI
# """
#
# ndvi = (b5_lambda_refl - b4_lambda_refl) / (b5_lambda_refl + b4_lambda_refl)
# img_ha = image_adjust_brightness(ndvi, -0.7695, 1.459, 'OrRd', 'NDVI')

# In Landsat 8, NDVI = (Band 5 – Band 4) / (Band 5 + Band 4).

ndvi = (b5-b4)/(b5+b4)
img_ha = image_adjust_brightness(ndvi,
                                 -0.7695, 1.459,
                                 'RdYlGn',  #find other colourmaps https://matplotlib.org/tutorials/colors/colormaps.html
                                 'Normalized Difference Vegetation Index (NDVI)',
                                 to_file='code-generated-NDVI2.png')


