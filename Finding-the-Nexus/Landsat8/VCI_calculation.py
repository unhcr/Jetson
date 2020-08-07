# -*- coding: utf-8 -*-
"""
Calculating Vegetation Condition Index (VCI)

The Vegetation Condition Index (VCI) is used to monitor vegetation condition.

Definition of the VCI
Kogan proposed a Vegetation Condition Index (VCI) based on the relative Normalized Difference Vegetation Index (NDVI)
change with respect to minimum historical NDVI value. The VCI therefore compares the current Vegetation Index (VI)
such as NDVI or Enhanced Vegetation Index (EVI) to the values observed in the same period in previous years within a specific pixel.

In Detail: Recommended Practice drought monitoring using the Vegetation Condition Index (VCI)
http://www.un-spider.org/advisory-support/recommended-practices/recommended-practice-agricultural-drought-monitoring/in-detail

Recommended Practice: Drought monitoring using the Vegetation Condition Index (VCI)
http://www.un-spider.org/advisory-support/recommended-practices/recommended-practice-agricultural-drought-monitoring

"""
from matplotlib import pyplot as plt
import earthpy as et
import earthpy.spatial as es
import earthpy.plot as ep
import rasterio as rio
from skimage import io, exposure


from Landsat8.landsat8_utils import get_list_of_data


land_stack, \
land_meta, \
landsat_post_process_path = get_list_of_data('/Users/gkalliatakis/Desktop/Gedo/LC081650582018022501T1-SC20200416194144')


# Once you have stacked your data, you can import it and work with it as you need to!
with rio.open(landsat_post_process_path) as src:
    landsat_stacked_data = src.read(masked=True)
    csf_meta = src.meta


# print('Metadata: ', csf_meta)

# Image Raster Data Values - Next, examine the raster’s min and max values.
# View min and max value
print('Image Raster MIN value: ',landsat_stacked_data.min())
print('Image Raster MAX value: ',landsat_stacked_data.max())

# The .ravel method turns an 2-D numpy array into a 1-D vector
# https://www.earthdatascience.org/courses/use-data-open-source-python/intro-raster-data-python/fundamentals-raster-data/plot-raster-histograms/
print('Raster 2-D numpy array shape: ',landsat_stacked_data.shape)
print('Raster 1-D vector shape: ',landsat_stacked_data.ravel().shape)


# View shape of the data
# print (landsat_stacked_data.shape)

# Calculate NDVI using regular numpy array math
nir_band = landsat_stacked_data[5]
red_band = landsat_stacked_data[4]
ndvi = es.normalized_diff(b1=nir_band, b2=red_band)

print('NDVI 2-D numpy array shape: ',ndvi.shape)
print('NDVI 1-D vector shape: ',ndvi.ravel().shape)
print('NDVI min value: ',ndvi.min())
print('NDVI max value: ',ndvi.max())

# 1D version of NDVI
ndvi_ravel = ndvi.ravel()

print('NDVI-1D min value: ',ndvi_ravel.min())
print('NDVI-1D max value: ',ndvi_ravel.max())



# # Finally plot the data.
# # Note below that the vmin= and vmax= arguments are used to stretch the colorbar across the full possible range of NDVI values (-1 to 1)
# ep.plot_bands(ndvi,
#               cmap='RdYlGn',
#               scale=False,
#               vmin=-1, vmax=1,
#               title="Derived NDVI")
# plt.show()
#
# img_ha = exposure.rescale_intensity(ndvi, (-0.7695, 1.459))
#
# ep.plot_bands(img_ha,
#               cmap='RdYlGn',
#               scale=False,
#               vmin=-1, vmax=1,
#               title="Derived NDVI - adjusted brightness")
# plt.show()
