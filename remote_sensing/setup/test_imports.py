import platform 
import os 
import sys 

# Get operative system name
op_sys = platform.system()

# Get python version
python_version = str(sys.version_info[0]) + "." + str(sys.version_info[1])

print("Platform: " + op_sys + " Python Version: " + python_version)

print("importing skimage")
import skimage

print("importing rasterio")
import rasterio

print("importing skimage")
import skimage

print("importing matplotlib")
import matplotlib

print("importing earthpy")
import earthpy

print("importing geopandas")
import geopandas

print("importing landsatexplore")
import landsatxplore


