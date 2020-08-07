# -*- coding: utf-8 -*-
"""Band Combinations of Landsat 8.

Ref: https://www.harrisgeospatial.com/Learn/Blogs/Blog-Details/ArtMID/10198/ArticleID/15691/The-Many-Band-Combinations-of-Landsat-8

"""
import numpy as np
from matplotlib import pyplot as plt
from skimage import io, exposure

from Landsat8.landsat8_utils import read_band,color_image_show, image_show, image_adjust_brightness

band_1 = read_band(1)
band_2 = read_band(2)
band_3 = read_band(3)
band_4 = read_band(4)
band_5 = read_band(5)
band_6 = read_band(6)
band_7 = read_band(7)

natural_colour_img = np.dstack((band_4, band_3, band_2))

color_image_show(natural_colour_img, title='Natural Color Image (4-3-2)')



traditional_colour_infrared = np.dstack((band_5, band_4, band_3))

image_show(traditional_colour_infrared, 'OrRd', 'Traditional Color Infrared (CIR) (5-4-3)')


# color_image_show(traditional_colour_infrared, title='Traditional Color Infrared (CIR) (5-4-3)')
#
#
# false_colour = np.dstack((band_7, band_6, band_4))
#
# color_image_show(traditional_colour_infrared, title='False Color (CIR) (7-6-4)')

