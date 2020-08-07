# -*- coding: utf-8 -*-
"""
Calculating Normalized Difference Water Index (NDWI)

Normalized Difference Water Index (NDWI) is use for the water bodies analysis. The index uses Green and Near infra-red bands of remote sensing images.
The NDWI can enhance water information efficiently in most cases. It is sensitive to build-up land and result in over-estimated water bodies.
The NDWI products can be used in conjunction with NDVI change products to assess context of apparent change areas.

NDWI = (NIR – SWIR) / (NIR + SWIR)

- For Landsat 7 data, NDWI = (Band 4 – Band 5) / (Band 4 + Band 5)

- For Landsat 8 data, NDWI = (Band 5 – Band 6) / (Band 5 + Band 6)


Ref: https://www.linkedin.com/pulse/ndvi-ndbi-ndwi-calculation-using-landsat-7-8-tek-bahadur-kshetri/

"""

from remote_sensing.Landsat8.landsat8_utils import image_adjust_brightness, read_band

# """
# Read bands
# """
b3 = read_band(3)
b4 = read_band(4)
b5 = read_band(5)
b6 = read_band(6)


# """
# Calculate NDWI
# """

# For Landsat 8 data, NDWI = (Band 5 – Band 6) / (Band 5 + Band 6)

NDWI = (b5 - b6)/(b5 + b6)

img_ha = image_adjust_brightness(NDWI, -0.7695, 1.459, 'Blues', 'Normalized Difference Water Index (NDWI)',
                                 'code-generated-NDWI.png') #find other colourmaps https://matplotlib.org/tutorials/colors/colormaps.html



