import data_utils
import os 
import sys

def download_data(user , psswd, region = None, root_data_dir = "./data/", location_file = "location_data.json") :
    if region == None : # no region specified = download all data
        for (_, dirnames, _) in os.walk(root_data_dir) :
            for region in dirnames:
                print("Downloading region: " + region)
                data_utils.download_region_data(region, user, psswd, root_data_dir, location_file)
            break
    
    else :
        print("Downloading region: " + region)
        data_utils.download_region_data(region, user, psswd, root_data_dir, location_file)


args = sys.argv
if len(args) == 2 :
    region = args[1].capitalize()
else :
    region = None
download_data("barcanjo", "Guitarra915641448", region)