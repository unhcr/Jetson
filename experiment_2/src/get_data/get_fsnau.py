import http.cookiejar as cookielib
import pandas as pd
import mechanize
import calendar
import os
import time
from io import StringIO
from bs4 import BeautifulSoup


def get_fsnau_monthly(month,
                      fsnau_user,
                      fsnau_pass,
                      data_dir = "data/raw/fsnau"):
    
    ''' 
    Get monthly data from the FSNAU price database. 
    http://www.fsnau.org/ids/dashboard.php
    
    month      = month of interest ("YYYY-MM)
    fsnau_user = FSNAU database user name
    fsnau_pass = FSNAU database password
    data_dir   = destination directory name
    '''
    
    # Get the year and three-letter month name
    y, m = [str(int(i)) for i in month.split("-")]
    
    # Setup to log in
    cj = cookielib.CookieJar()
    br = mechanize.Browser()
    br.set_cookiejar(cj)

    br.open('http://www.fsnau.org/ids/dashboard.php')

    # Supply credentials
    br.select_form(nr=0)
    br.form['username'] = fsnau_user
    br.form['password'] = fsnau_pass
    br.submit()

    # Open the main dashboard page
    br.open('http://www.fsnau.org/ids/dashboard.php')

    # Go to the data export page
    data_export_url = [i for i in br.links() if 'exportdata' in i.attrs[0][1]][0]
    request = br.click_link(data_export_url)
    response = br.follow_link(data_export_url)
    br.response()

    # Fill in the form
    res = br.response().read()
    br.select_form("frmExporter")

    # Identify the form elements that control month and year
    monthcontrol = br.form.find_control("month")
    yearcontrol = br.form.find_control("year")
    criteriacontrol = br.form.find_control("criteria")
    startyearcontrol = br.form.find_control("start_year")
    endyearcontrol = br.form.find_control("end_year")
    
    # Set the month andyear values we want
    monthcontrol.value = [m]
    yearcontrol.value = [y]
    startyearcontrol.value = [y]
    endyearcontrol.value = [y]
    criteriacontrol.value = ['month_year']
    
    ## A bit hacky: we can't disable the year control, 
    ## so we just set all years to be the same    
    #startyearcontrol.disabled = True
    #endyearcontrol.disabled = True

    # Retrieve the dataset
    br.method = "POST"
    response = br.submit()
    data = response.get_data()

    # Get into a csv
    s=str(data,'utf-8')
    data = StringIO(s) 
    df=pd.read_csv(data)

    # Store the source month
    #df['date'] = month
    
    # Return results
    df.to_csv(f"{data_dir}/fsnau_{month}.csv", index=False)
    return df




def get_fsnau_all( start_month, 
                  end_month, 
                  fsnau_user,
                  fsnau_pass,                  
                  data_dir= "data/raw/fsnau", 
                  redownload=False):
    ''' 
    Loops over all months in range and calls `get_fsnau_monthly` to download the data.  
    
    start_month  = start month of interest ("MM-YYYY")
    end_month    = end month of interest ("MM-YYYY")
    fsnau_user   = FSNAU database user name
    fsnau_pass   = FSNAU database password
    data_dir     = destination directory name
    redownload   = if True, redownload all data 
                   if False, download only months not in repository
    '''
    downloaded = []
    file_list = os.listdir(data_dir)
    
    periods = pd.period_range(start=start_month, end=end_month, freq='M')
    
    for month in periods:
        
        file_exists = (f"fsnau_{month}.csv" in file_list)
        
        if not file_exists or \
           redownload==True:
            
            get_fsnau_monthly(str(month), fsnau_user, fsnau_pass, data_dir)
            downloaded.append(month)
            time.sleep(2)
            
        else:
            pass
        
    print("The following files were downloaded:",  [str(i) for i in downloaded])