import os
import sys
import platform

# Get operative system name
op_sys = platform.system()

# Get python version
python_version = str(sys.version_info[0]) + str(sys.version_info[1])

# Installing for Windows 64-bit 
# Only Python 3.7+ is supported
# Need to install wheels from binaries
if op_sys == "Windows" :

    # Upgrading pip
    print("upgrading pip")
    os.system("python -m pip install --upgrade pip")

    # Installing scikit-image
    print("Installing scikit-image package")
    os.system("pip install scikit-image")

    # Installing matplotlib
    print("Installing matplotlib package")
    os.system("pip install matplotlib")

    # Installing wheel
    print("Installing wheel package")
    os.system("pip install wheel")

    # Installing gdal binaries
    print("Installing gdal binaries")
    os.system("pip install ./wheels/GDAL-3.3.2-cp" + python_version + "-cp" + python_version + "-win_amd64.whl")

    # Installing rasterio binaries
    print("Installing rasterio binaries")
    os.system("pip install ./wheels/rasterio-1.2.9-cp" + python_version + "-cp" + python_version + "-win_amd64.whl")

    # Installing fiona binaries
    print("Installing fiona binaries")
    os.system("pip install ./wheels/Fiona-1.8.20-cp" + python_version + "-cp" + python_version + "-win_amd64.whl")

    # Installing geopandas
    print("Installing geopandas package")
    os.system("pip install geopandas")

    # Installing earthpy
    print("Installing earthpy package")
    os.system("pip install earthpy")

# Installing for Linux (Ubuntu based)
# Requires sudo password
# TODO test this script
if op_sys == "Linux":
    # Installing gdal
    os.system("sudo add-apt-repository ppa:ubuntugis/ppa && sudo apt-get update")
    os.system("sudo apt-get update")
    os.system("sudo apt-get install gdal-bin")
    os.system("sudo apt-get install libgdal-dev")
    os.system("export CPLUS_INCLUDE_PATH=/usr/include/gdal")
    os.system("export C_INCLUDE_PATH=/usr/include/gdal")
    os.system("pip install GDAL")

    # Installing rasterio
    os.system("sudo add-apt-repository ppa:ubuntugis/ppa")
    os.system("sudo apt-get update")
    os.system("sudo apt-get install python-numpy gdal-bin libgdal-dev") # hopefully already installed from previous
    os.system("pip install rasterio")

    # Installing Fiona
    os.system("pip install fiona")

    # Installing geopandas
    os.system("pip install geopandas")

    # Installing earthpy
    os.system("pip install earthpy")

# Installing for Mac
# Assumes brew is installed
# TODO test this script
if op_sys == "Darwin":

    # Installing gdal
    os.system("brew install gdal --HEAD")
    os.system("brew install gdal")
    os.system("pip3 install — upgrade pip")
    os.system("pip3 install gdal==2.4.4")
    
    # Installing rasterio 
    os.system("pip install rasterio")

    # Installing Fiona
    os.system("pip install fiona")

    # Installing geopandas
    os.system("pip install geopandas")

    # Installing earthpy
    os.system("pip install earthpy")
    