import http.cookiejar as cookielib
import pandas as pd
import mechanize
import calendar
import os
import time
from bs4 import BeautifulSoup
import numpy as np


def get_ew_ea_monthly(month, ew_ea_user, ew_ea_pass, data_dir = "data/raw/ew_ea"):
    
    ''' 
    Get monthly data from the FSNAU early-warning early-action dashboard. 
    http://dashboard.fsnau.org/
    
    month      = month of interest ("YYYY-MM)
    ew_ea_user = EW EA dashboard user name
    ew_ea_pass = EW EA dashboard password
    data_dir   = destination directory name
    '''
    
    # Get the year and three-letter month name
    y, m = [int(i) for i in month.split("-")]
    m = calendar.month_abbr[m]
   
    
    # Setup to log in
    cj = cookielib.CookieJar()
    br = mechanize.Browser()
    br.set_cookiejar(cj)

    # Open the page
    br.open(f"http://dashboard.fsnau.org/dashboard/index/01-{m}-{y}")

    # Supply credentials
    br.select_form(nr=0)
    br.form['username'] = ew_ea_user
    br.form['password'] = ew_ea_pass
    br.submit()

    # Get the response
    res = br.response().read()
    soup = BeautifulSoup(res, 'lxml')

    # Extract the table
    tbl = soup.find('table') 
    envdata = pd.read_html(tbl.prettify())[0]
    
    # Store the source month
    envdata['date'] = month
    
    #if 'Severe Acute Malnutrion (SAM)' not in envdata.columns:
    #    envdata['Severe Acute Malnutrion (SAM)'] = np.nan  
        
    #envdata.sort_index(axis=1, inplace=True)
    
    # Return results
    envdata.to_csv(f"{data_dir}/ew_ea_{month}.csv", index=False)
    return envdata


def get_ew_ea_rivers_monthly(month, ew_ea_user, ew_ea_pass, data_dir = "data/raw/ew_ea"):
    
    ''' 
    Get monthly RIVER data from the FSNAU early-warning early-action dashboard.
    http://dashboard.fsnau.org/climate/river-levels
    
    month      = month of interest ("YYYY-MM)
    ew_ea_user = EW EA dashboard user name
    ew_ea_pass = EW EA dashboard password
    data_dir   = destination directory name
    '''
    
    # Get the year and three-letter month name
    y, m = [int(i) for i in month.split("-")]
    m = calendar.month_abbr[m]
   
    
    # Setup to log in
    cj = cookielib.CookieJar()
    br = mechanize.Browser()
    br.set_cookiejar(cj)

    # Open the page
    br.open(f"http://dashboard.fsnau.org/climate/river_levels/28-{m}-{y}")

    # Supply credentials
    br.select_form(nr=0)
    br.form['username'] = ew_ea_user
    br.form['password'] = ew_ea_pass
    br.submit()

    # Get the response
    res = br.response().read()
    soup = BeautifulSoup(res, 'lxml')

    # Extract the table
    tbl = soup.find('table') 
    riverdata = pd.read_html(tbl.prettify())[0]
    
    # Tidy up and reshape the data frame
    riverdata.drop(columns=['#'], inplace=True)
    riverdata = pd.DataFrame(riverdata.set_index(['Region', 'District']).stack(), 
                             columns = ['depth_in_meters'])
    riverdata.index.names = ['region', 'district', 'date']
    riverdata.reset_index(inplace=True)
    
    # Return results
    riverdata.to_csv(f"{data_dir}/ew_ea_rivers_{month}.csv", index=False)
    return riverdata




def get_ew_ea_all( start_month, end_month, ew_ea_user, ew_ea_pass, data_dir= "data/raw/ew_ea", redownload=False):
    ''' 
    Loops over all months in range and calls `get_ew_ea_monthly` to download the data.  
    
    start_month  = start month of interest ("MM-YYYY")
    end_month    = end month of interest ("MM-YYYY")
    ew_ea_user = EW EA dashboard user name
    ew_ea_pass = EW EA dashboard password
    data_dir     = destination directory name
    redownload   = if True, redownload all data 
                   if False, download only months not in repository
    '''
    downloaded = []
    file_list = os.listdir(data_dir)
    
    periods = pd.period_range(start=start_month, end=end_month, freq='M')
    
    for month in periods:
        
        file_exists = (f"ew_ea_{month}.csv" in file_list)
        
        if not file_exists or \
           redownload==True:
            
            get_ew_ea_monthly(str(month), ew_ea_user, ew_ea_pass, data_dir)
            downloaded.append(month)
            time.sleep(2)
            
        else:
            pass
        
    print("The following files were downloaded:",  [str(i) for i in downloaded])
            
    

def get_ew_ea_rivers_all( start_month, end_month, ew_ea_user, ew_ea_pass, data_dir= "data/raw/ew_ea", redownload=False):
    ''' 
    Loops over all months in range and calls `get_ew_ea_rivers_monthly` to download the data.  
    
    start_month  = start month of interest ("MM-YYYY")
    end_month    = end month of interest ("MM-YYYY")
    ew_ea_user = EW EA dashboard user name
    ew_ea_pass = EW EA dashboard password
    data_dir     = destination directory name
    redownload   = if True, redownload all data 
                   if False, download only months not in repository
    '''
    downloaded = []
    file_list = os.listdir(data_dir)
    
    periods = pd.period_range(start=start_month, end=end_month, freq='M')
    
    for month in periods:
        
        file_exists = (f"ew_ea_rivers_{month}.csv" in file_list)
        
        if not file_exists or \
           redownload==True:
            
            get_ew_ea_rivers_monthly(str(month), ew_ea_user, ew_ea_pass, data_dir)
            downloaded.append(month)
            time.sleep(2)
            
        else:
            pass
        
    print("The following files were downloaded:",  [str(i) for i in downloaded])    
    
    
    
    
    