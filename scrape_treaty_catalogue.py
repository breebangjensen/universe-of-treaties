#import packages
import pandas as pd
from bs4 import Beautifulsoup
import time
import os
import glob
import csv
import requests
from urllib.parse import urlparse


# Instantiate CSV
# save output (will be .csv). try to save one line of csv at a time so the data doesn't get lost if the job crashes. 
csv_file_name = 'treaty_links.csv'
out_csv_file = open(csv_file_name, 'w', newline='')
csv_writer = csv.writer(out_csv_file, delimiter=',')
column_names=["reg_num", "title", "reg_year", "type_treaty", "pdf"]
_ = csv_writer.writerow(column_names)
# then write the column names into the csv


#outer loop to go through the csv 
# need step to check scraped files

print('\nNamed with wildcard ranges:') 

# glob.glob returns a list of the matched files see it here 
glob.glob('data/treaty_catalog_[1946:2019]*.csv')


for name in glob.glob('/data/treaty_catalog_*[1946:2019]*.csv'): 
##read columns and file
# let's assume that you are inside the glob loop for now and the first file needs to be open 
#some redundancy with the above to clean up 
        df = pd.read_csv(name)
  
   
urls=(df["href"].to_list())
   

# set up for tracking urls scraped
url_example = 'https://treaties.un.org/Pages/showDetails.aspx?objid=0800000280164909&clang=_en'
# url parser
test = urlparse(url_example).path
os.path.basename(urlparse(url_example).path)

##get pdfs
for url in urls:
  pdf_from_link = os.path.basename(urlparse(url).path)
  if pdf_from_link is not in pdf_files:
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')


# Scrape valuable data
## registration number (appears as <span id="lblRegNum1">20</span>)
    reg = soup.find("span", {"id": "lblRegNum1"}).text

##title
    title=soup.find("span", {"id": "lblTitle1"}).text

#registration date
    reg_year=soup.find("span", {"id": "lblRegDate1"}).text


#type
    type_treaty =soup.find("span", {"id": "lblAgreementType1"}).text

## pdf path
##possible problem--getting multiple pdfs
    pdf = soup.find("a", {"id": "0"})["href"]


    row_to_write = [reg, title, reg_year, type_treaty, pdf]

    _=csv_writer.writerow(row_to_write)
   
    time.sleep(2)


close csv? 
out_csv_file.close()
