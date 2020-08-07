# -*- coding: utf-8 -*-
"""
Processing Landsat 8 colour images

[1] Load RGB Bands
[2] Histogram Equalization
[3] Contrast and Color Balance Adjustment

Ref: https://nbviewer.jupyter.org/github/HyperionAnalytics/PyDataNYC2014/blob/master/color_image_processing.ipynb
Video: https://www.youtube.com/watch?v=4QpwcjD2Lpw

"""

from drought_prediction.utils.landsat8.landsat8_utils import read_band,color_image_show

import numpy as np
from skimage import exposure
from matplotlib import pyplot as plt

"""
Load RGB Bands 
    Landsat 8 bands corresponding to RGB are 4-3-2. Data is loaded as 2D uint16 arrays, then stacked into NumPy 3D array of the same type, and imaged.
    Please note that matplotlib cannot display RGB uint16 arrays. Data is transformed to float64 in range 0-1.
"""
b2 = read_band(2)
b3 = read_band(3)
b4 = read_band(4)

img432 = np.dstack((b4, b3, b2))

color_image_show(img432, 'RGB (4-3-2) image')

"""
Histogram Equalization
    Histograms of RGB colors corresponding to raw data show that the data is not utilizing full 16-bit range (0-65535) afforded by the detector. 
    Limits for all three colors are picked and data is rescaled. This results in apparent brightening of the image.
"""
fig = plt.figure(figsize=(10, 7))
fig.set_facecolor('white')

for color, channel in zip('rgb', np.rollaxis(img432, axis=-1)):
    counts, centers = exposure.histogram(channel)
    plt.plot(centers[1::], counts[1::], color=color)

plt.show()

img432_ha = np.empty(img432.shape, dtype='uint16')
lims = [(0,4000), (0,4000), (0,4000)]
for lim, channel in zip(lims, range(3)):
    img432_ha[:, :, channel] = exposure.rescale_intensity(img432[:, :, channel], lim)

color_image_show(img432_ha, 'RGB (4-3-2) image, histogram equilised')

"""
Contrast and Color Balance Adjustment
    Adjusting contrast and color balance of an image to their "right" levels is an iterative process. 
    It involves the knowledge of how images at the same latitude and longitude look at a particular time of year. 
    Users can draw on previous experience or search for images of the similar scenes on the Internet to get appropriate contrast and color balance. 
    In this case, we will adjust balance of green and blue colors by shifting them to partially "brighter" values using gamma adjustment.
"""
img432_ha[:, :, 1] = exposure.adjust_gamma(img432_ha[:, :, 1], 0.65)
img432_ha[:, :, 2] = exposure.adjust_gamma(img432_ha[:, :, 2], 0.75)
color_image_show(img432_ha, 'RGB (4-3-2) image, histogram equilized, color gamma adjusted')
