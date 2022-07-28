# Measuring Drought 
In order to analyse the impact of drought in the internal displacments and conflicts of Somalia, we first need to be able to quantify it. The state of vegetation is theorized to be a strong indicator of drought within a region and is possible to calculate from image data.

## Normalized Difference Vegetation Index 
The normalized difference vegetation index (NDVI) is used to assess the state of vegetation.
In living plants chlorophyll-A, from the photosynthetic machinery, strongly absorbs red color;
on the other hand, near-infrared light is strongly reflected.
Live, healthy vegetation reflects around 8% of red light and 50% of near-infrared light.
Dead, unhealthy, or sparse vegetation reflects approximately 30% of red light and 40% of near-infrared light.

By its formulation, NDVI ranges from -1 to +1. In practice, an area of an image containing living vegetation will have NDVI in the range 0.3 to 0.8.
High water content clouds and snow will have negative values of the index. Bodies of water, having low reflectance in both Band 4 and 5,
exhibit very low positive or negative index. Soil, having slightly higher reflectance in near-infrared than in red, will produce low positive values of the index.

## Vegetation Condition Index
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


# Data

## Satellite Imagery
In Landsat 8, the Normalized Difference Vegetation Index of an area can be calculated as NDVI = (Band 5 – Band 4) / (Band 5 + Band 4), where the bands are channels in TIF format file. Given the NVDI for the relevant time-series, the calculation of VCI can also be performed.

## Dataset and Collection
The Landsat 8 dataset utilized in this experiment is the collection 2 level 1: Landsat 8-9 OLI/TIRS C2 L1. For each Somalia region we download the scenes that contain the region utilizing the machine-to-machine functionality of the USGS service. 

## Pre-Processing
Each scene data is received as a bundle of all satellite bands as a TAR compressed file. A raster stack is a TIF file composed of several bands. A KML file defines one or many polygons in TIF files, delimiting an area.

The processing of data before computing VCI is as follows:
- Bundle data downloaded as a TAR compressed file 
- Extract data
- Create raster stack from bands 1 to 7
- Clip raster stack to only contain the relevant region by utilizing a KML file
- Clipped raster stack is ready for NVDI and VCI calculation

This process is applied to all scenes for every Somalia region over the selected time period.
