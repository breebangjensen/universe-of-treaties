# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 11:20:04 2021

@author: Bree
"""
##The purpose of this script is to go through the links to the treaty pdfs and download 
##those pdfs.  The Volume and Treaty pdfs will be intermingled.

##import packages
import os
import pandas as pd
import time
import wget
from urllib.parse import urlparse
import os.path


##create new folder to store treaties
newpath = r'\data\treaty_pdfs' 
if not os.path.exists(newpath):
    os.makedirs(newpath)

##open csv
df = pd.read_csv("treaty_links")

pdf_files = glob.glob('/data/treaty_pdfs/*.pdf') # assumption list of files that exists
# os.path parse to just get the file 

urls=(df["pdf"].to_list())

# assume you're inside the loop of urls 
url_example = 'https://treaties.un.org/doc/Publication/UNTS/Volume%2011/v11.pdf'
# url parser
test = urlparse(url_example).path
os.path.basename(urlparse(url_example).path)

##get pdfs
for url in urls:
  pdf_from_link = os.path.basename(urlparse(url).path)
  if pdf_from_link is not in pdf_files:
    # here we check if it exists if not in the list do the wget 
    wget.download(url)
  
time.sleep(2)
