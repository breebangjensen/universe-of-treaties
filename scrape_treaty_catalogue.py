
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 15:25:02 2021

@author: Bree
"""
##
from bs4 import BeautifulSoup
import requests
import csv
import pandas


##read columns and file
col_list = ["href", "title", "reg_num", "reg_date", "type", "con_date", "vol"]
df = pandas.read_csv("treaty_catalog_1947.csv", usecols=col_list)
urls=(df["href"])

for url in urls: 
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
##attempt to fix overwriting issue, does not fix
    return _=csv_writer.writerow(row_to_write)


# Instantiate CSV
# save output (will be .csv). try to save one line of csv at a time so the data doesn't get lost if the job crashes. 
    csv_file_name = 'treaty_links_2.csv'
    out_csv_file = open(csv_file_name, 'w', newline='')
    csv_writer = csv.writer(out_csv_file, delimiter=',')
    column_names=["reg_num", "title", "reg_year", "type_treaty", "pdf"]
    _ = csv_writer.writerow(column_names)
# then write the column names into the csv

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

   



# #scraping tables on url/extract data
# tables = soup.findAll("table")

# table = tables[0]
# row_data = []
# for row in table.find_all('tr'):
#     cols = row.find_all('td')
#     print("===========================")
#     print(cols)



#     cols = [ele.text.strip() for ele in cols]
#     column_names=["Registration Number", "Title", "Participants", "Submittor", 
#                     "Places/dates of conclusion", "EIF information", "Authentic texts",
#                     "Attachments", "ICJ Information", "Despository", "Registration Date", 
#                     "Subject terms", "Agreement type", "UNTS Volume Number", "Publication Format",
#                     "Certificate of Registration", "Text Document(s)", "Volume in PDF", 
#                     "Map(s)", "Corrigendum/Addendum", "Participant", "Action", "Date of Notification/Deposit",
#                     "Date of Effect"]
#     row_data.append(cols)
#     print(row_data)
 
# _ = csv_writer.writerow(column_names)
# _ = csv_writer.writerow(row_data)

#close url? close csv? 
out_csv_file.close()
