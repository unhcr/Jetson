# -*- coding: utf-8 -*-
"""
Explanation of Landsat 8 bands

Ref: https://nbviewer.jupyter.org/github/HyperionAnalytics/PyDataNYC2014/blob/master/landsat8_bands.ipynb

"""
from drought_prediction.utils.landsat8.landsat8_utils import read_band, image_adjust_brightness


"""
Band 1 - costal aerosol, 433 - 453 nm, resolution 30 m
"""

b1 = read_band(1)
image_adjust_brightness(b1, 10000, 13500, 'Band 1, costal aerosol, 433 - 453 nm, resolution 30 m')


"""
Band 2 blue, 450 - 515 nm, resolution 30 m
Band 3 green, 525 - 600 nm, resolution 30 m
Band 4 red, 630 - 680 nm, resolution 30 m
    These three bands correspond to blue, green, and red colors from the visible spectrum.
    Processing of natural color images is discussed in detail in a separate file titled "landsat8_colour_img_processing.py".
"""


"""
Band 5, near infrared 845 - 885 nm, resolution 30 m 
    This band covers the near infrared (NIR) part of the spectrum. 
    NIR measurements are important for agriculture and ecology because 
    the water in healthy plants efficiently scatters the wavelengths in this range. 
    Used in conjunction with red band, it is possible to estimate the state of green 
    plants using the normalized difference vegetation index (NDVI).
"""

b5 = read_band(5)
image_adjust_brightness(b5, 6000, 23000, 'Band 5, near infrared 845 - 885 nm, resolution 30 m')



"""
Band 7, short wave infrared, 2100 - 2300 nm, resolution 30 m
    The bands cover two different portions of the shortwave infrared (SWIR) spectrum. 
    Bands 6 and 7 are used to assess soil water content, and also distinguish rocks which 
    look very similar in the images formed using other bands. 
    The two bands can also be used to acquire clear images through smoke.
"""


b6 = read_band(6)
b4 = read_band(4)

image_adjust_brightness(b6, 4000, 30000, 'Band 6, short wave infrared, 1560 - 1660 nm, resolution 30 m')

image_adjust_brightness(b4, 8000, 22000, 'Band 4 red, 630 - 680 nm, resolution 30 m')

