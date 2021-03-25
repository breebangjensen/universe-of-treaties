""" Scrape metadata details about individual treaties

This script outputs tables of UN Treaty metadata.
It relies on outputs from get_treaty_catalog.py
Its outputs serve as an input to a follow-up script for scraping treaty pdfs.

Example:
    Simply kick it off from the command line::

        $ python get_treaty_details.py

TODOs:
  * there's possibly a problem leading to getting multiple pdfs?
"""

import os
import time
import glob
import csv
import pandas as pd
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup

# Retrieve the treaty catalogs to scrape
catalogs = glob.glob('data/treaty_catalog_[0-9]*.csv')

# Scrape details about each treaty.
# each catalog holds one month of treaties.
for name in catalogs:
    # Only scrape if it doesn't already exist
    date_range = name.split('_')[-1].split('.')[0]
    csv_file_name = 'treaty_details_' + date_range + '.csv'
    print('Searching for all treaties appearing in %s...'%(csv_file_name))
    if csv_file_name in os.listdir('data'):
        print('Skipping %s is already scraped.'%(csv_file_name))
        continue

    # URLs of all treaties in this month
    df = pd.read_csv(name)
    urls=df["href"].to_list()

    # Create CSV to receive outputs
    # save output (will be .csv). try to save one line of csv at a time so the data doesn't get lost if the job crashes. 
    csv_file_path = 'data/' + csv_file_name
    out_csv_file = open(csv_file_path, 'w', newline='')
    csv_writer = csv.writer(out_csv_file, delimiter=',')
    column_names=["reg_num", "title", "reg_year", "type_treaty", "pdf"]
    _ = csv_writer.writerow(column_names)
    # then write the column names into the csv

    # Get treaty metadata
    print('There are %d treaties to retrieve'%(len(df.index)))
    for url in urls:
        print('Retrieving ' + url)
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')

        # Scrape valuable data
        towrite = {}
        ## registration number (appears as <span id="lblRegNum1">20</span>)
        towrite['reg_num'] = soup.find("span", {"id": "lblRegNum1"}).text
        ##title
        towrite['title'] = soup.find("span", {"id": "lblTitle1"}).text
        #registration date
        towrite['reg_year'] = soup.find("span", {"id": "lblRegDate1"}).text
        #type
        towrite['type_treaty'] = soup.find("span", {"id": "lblAgreementType1"}).text
        ## pdf path
        towrite['pdf'] = soup.find("a", {"id": "0"})["href"]
        _ = csv_writer.writerow(towrite.values())
        time.sleep(5)

out_csv_file.close()
