# Installing Packages
- Run setup/setup.py

# Files
- Place "location_data.json" in /remote_sensing/
- Place the kml file (e.g. "Somalia_Adminstrative_Boundaries.kml") in /remote_sensing/ 

# Folder Setup
- Run folder_creation.py

# Downloading Data
- Run download_data.py 
    - if no region name is passed as shell argument: download all regions
    - if region name is passed: download data only for that region

# Calculating VCIs#
## DO NOT TRY YET, WORKING ON IT - BRUNO
- Run calculate_vcis.py 
    - if no region name is passed as shell argument: calculate for all regions
    - if region name is passed: calculate only for that region
