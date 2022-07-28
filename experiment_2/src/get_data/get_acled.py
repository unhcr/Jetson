#!/usr/bin/env python3

import urllib.request, json
import pandas as pd
import os
import time


def get_acled_monthly(month, iso='706', data_dir = "data/raw/acled"):
    ''' 
    Page through the Acled API and download all query results to csv. 
    https://www.acleddata.com/wp-content/uploads/dlm_uploads/2017/10/API-User-Guide-11.pdf
    
    month      = month of interest ("YYYY-MM")
    iso        = three-digit country ISO ('NNN')
    data_dir   = destination directory name
    '''
       
    start_date = month + '-01'
    end_date   = month + '-31' # It doesn't throw an error, even for short months
    
    p = 1

    # Page through the API response as long as results are still being returned
    while True:

        # API query
        url = f"https://api.acleddata.com/acled/read?terms=accept&" + \
                f"iso={iso}&event_date={start_date}|{end_date}&" + \
                f"event_date_where=BETWEEN&page={p}"
                
        resp = json.loads(urllib.request.urlopen(url).read().decode())
        
        if p == 1:
            # Convert json response to dataframe
            acled = pd.DataFrame(resp['data'])

        else:
            # Append json response
            new_acled = pd.DataFrame(resp['data'])
            acled = acled.append(new_acled)

            # When there is nothing left to append (last page in pagination...)
            if new_acled.shape[0]==0:
                break

        #print(p, end=" ")
        p+=1          
    
    acled['month'] = month
    acled.to_csv(f"{data_dir}/acled_{month}.csv", index=False)
    return acled



def get_acled_all( start_month, end_month, data_dir= "data/raw/acled", redownload=False):
    ''' 
    Loops over all months in range and calls `get_acled_monthly` to download the data.  
    
    start_month  = start month of interest ("MM-YYYY")
    end_month    = end month of interest ("MM-YYYY")
    data_dir     = destination directory name
    redownload   = if True, redownload all data 
                   if False, download only months not in repository
    '''
    downloaded = []
    file_list = os.listdir(data_dir)
    
    periods = pd.period_range(start=start_month, end=end_month, freq='M')
    
    for month in periods:
        
        file_exists = (f"acled_{month}.csv" in file_list)
        
        if not file_exists or \
           redownload==True:
            
            get_acled_monthly(str(month), '706', data_dir)
            downloaded.append(month)
            time.sleep(2)
            
        else:
            pass
        
    print("The following files were downloaded:", [str(i) for i in downloaded])
            








