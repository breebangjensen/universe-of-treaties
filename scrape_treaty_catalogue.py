#import packages
import pandas as pd
from bs4 import Beautifulsoup
import time
import os
import glob
import csv
import requests


# Instantiate CSV
# save output (will be .csv). try to save one line of csv at a time so the data doesn't get lost if the job crashes. 
csv_file_name = 'treaty_links.csv'
out_csv_file = open(csv_file_name, 'w', newline='')
csv_writer = csv.writer(out_csv_file, delimiter=',')
column_names=["reg_num", "title", "reg_year", "type_treaty", "pdf"]
_ = csv_writer.writerow(column_names)
# then write the column names into the csv

##create file dictionary
file_dictionary={}

#outer loop to go through the csv 
# need step to check scraped files

print('\nNamed with wildcard ranges:') 

# glob.glob returns a list of the matched files see it here 
glob.glob('data/treaty_catalog_[1946:2019]*.csv')


for name in glob.glob('/data/treaty_catalog_*[1946:2019]*.csv'): 
    print (name) # print the first one
    #check if name in dictionary
    if name in file_dictionary:
        print("yes")
    else:
        df = pd.read_csv(name)
    ##append name to dictionary 
        file_dictionary={name}

##read columns and file
# let's assume that you are inside the glob loop for now and the first file needs to be open 
#some redundancy with the above to clean up 
        df = pd.read_csv(name)
    name = 'data/treaty_catalog_1947.csv'
   

    urls=(df["href"].to_list())
# so now your loop should start here with the urls let's try the first one
    urls = urls[0] # this will pass only one entry, get rid of this line when you're ready for the full list
# This is the inner loop 
for url in urls: 
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
