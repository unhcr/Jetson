# -*- coding: utf-8 -*-
"""
Calculating Enhanced Vegetation Index (EVI)

EVI is similar to Normalized Difference Vegetation Index (NDVI) and can be used to quantify vegetation greenness.
However, EVI corrects for some atmospheric conditions and canopy background noise and is more sensitive in
areas with dense vegetation. It incorporates an “L” value to adjust for canopy background,
“C” values as coefficients for atmospheric resistance, and values from the blue band (B).
These enhancements allow for index calculation as a ratio between the R and NIR values,
while reducing the background noise, atmospheric noise, and saturation in most cases.

EVI = G * ((NIR - R) / (NIR + C1 * R – C2 * B + L))

- In Landsat 4-7, EVI = 2.5 * ((Band 4 – Band 3) / (Band 4 + 6 * Band 3 – 7.5 * Band 1 + 1)).

- In Landsat 8, EVI = 2.5 * ((Band 5 – Band 4) / (Band 5 + 6 * Band 4 – 7.5 * Band 2 + 1)).

Ref: https://www.usgs.gov/land-resources/nli/landsat/landsat-enhanced-vegetation-index?qt-science_support_page_related_con=0#qt-science_support_page_related_con

"""

from remote_sensing.Landsat8.landsat8_utils import read_band, image_show, image_histogram, image_adjust_brightness
import numpy as np

# """
# Read bands
# """
b2 = read_band(2)
b4 = read_band(4)
b5 = read_band(5)
b6 = read_band(6)


# """
# Calculate EVI
# """

# In Landsat 8, EVI = 2.5 * ((Band 5 – Band 4) / (Band 5 + 6 * Band 4 – 7.5 * Band 2 + 1)).

# EVI = 2.5 * (NIR - RED ) / ( NIR + 6.0 * RED - 7.5 * BLUE+ 1.0 )

EVI = 2.5 * (b5-b4)/(b5 + 6.0 * b4 - 7.5 * b2 + 1.0)

img_ha = image_adjust_brightness(EVI, -0.7695, 1.459,
                                 'RdYlGn',  #find other colourmaps @ https://matplotlib.org/tutorials/colors/colormaps.html
                                 'Enhanced Vegetation Index (EVI)',
                                 to_file='code-generated-EVI-rescaled.png')


