# -*- coding: utf-8 -*-
"""
Calculating Vegetation Condition Index (VCI)

The Vegetation Condition Index (VCI) is used to monitor vegetation condition.

VCI definition:
Kogan proposed a Vegetation Condition Index (VCI) based on the relative Normalized Difference Vegetation Index (NDVI)
change with respect to minimum historical NDVI value. The VCI therefore compares the current Vegetation Index (VI)
such as NDVI or Enhanced Vegetation Index (EVI) to the values observed in the same period in previous years within a specific pixel.

Reference: Kogan, F. N. F. Remote sensing of weather impacts on vegetation in non-homogeneous areas.
           International Journal of Remote Sensing 1990, 11, 1405–1419.

Code based on 'Step by step: Drought monitoring using the Vegetation Condition Index (VCI) in Python'
http://www.un-spider.org/advisory-support/recommended-practices/recommended-practice-drought-monitoring-vci-python

"""



def calculate_VCI(current_VI,
                  min_,
                  max_):
    """Calculate the Vegetation Condition Index (VCI).
        The VCI is calculated using the following formula:
        VCI = ((VI - min(VI)) / (max(VI) - min(VI))) * 100

    # Arguments
        current_VI: masked (subclass of ndarray designed to manipulate numerical arrays with missing data) numpy array containing the geotiff processing results
                    current Vegetation Index (VI), such as NDVI or Enhanced Vegetation Index (EVI)

        min_: Minimum values of a Vegetation Index (VI) computed in the time series
        max_: Maximum values of a Vegetation Index (VI) computed in the time series

     # Returns
        vci: masked array which has had its values replaced in-place with the VCI values

    """

    # Calculate the VCI
    vci = current_VI
    vci -= min_
    max_ -= min_
    vci /= max_
    vci *= 100

    return vci