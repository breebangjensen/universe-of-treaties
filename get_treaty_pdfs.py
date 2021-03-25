""" Scrape treaty pdf files

This script outputs pdf files of treaties
It relies on outputs from get_treaty_details.py

Example:
    Simply kick it off from the command line::

        $ python get_treaty_pdfs.py

TODOs:

"""

import os
import glob
import pandas as pd
import requests
import urllib.request


# Build set of all treaty URLs to be scraped
pdfs_to_get = set()
for file in glob.glob('data/treaty_details_[0-9]*.csv'):
    print(file)

    # URLs of all pdfs in this month
    df = pd.read_csv(file)
    pdfs_to_get.update(df["pdf"].to_list())

# Get pdf if it isn't already scraped
print('There are %d treaty pdfs to retrieve'%(len(pdfs_to_get)))
for p in pdfs_to_get:
    pdf_name = p.lstrip('/').replace('/', '-')
    pdf_path = 'data/pdfs/' + pdf_name
    if pdf_name in os.listdir('data/pdfs/'):
        print('Skipping %s is already scraped.'%(pdf_name))
        continue
        print('Skipping %s is already scraped.'%(pdf_name))
    url = 'https://treaties.un.org' + p
    print('Scraping %s'%(url))
    urllib.request.urlretrieve(url, pdf_path)


