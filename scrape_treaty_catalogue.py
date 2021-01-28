
from bs4 import BeautifulSoup
import requests
import csv



#read in output from get_treaty_catalogue.py. Output is a .csv file. will be multiple tables so actually need to loop thru them.
## need to create set of treaties that have already been scraped, so we don't keep scraping the same ones. 
# need to put the file name below in a loop
# Currently, no loops

url = "https://treaties.un.org/Pages/showDetails.aspx?objid=0800000280165965&clang=_en"
#Use .csv file to find and open first URL. Tell program which column to find the URL in. Column is called "href". 
r = requests.get(url)
soup= BeautifulSoup(r.text, 'html.parser')


#scraping tables on url/extract data
tables = soup.findAll("table")

for table in tables:
        row_data = []
        for row in table.find_all('tr'):
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            column_names=["Registration Number", "Title", "Participants", "Submittor", 
                          "Places/dates of conclusion", "EIF information", "Authentic texts",
                          "Attachments", "ICJ Information", "Despository", "Registration Date", 
                          "Subject terms", "Agreement type", "UNTS Volume Number", "Publication Format",
                          "Certificate of Registration", "Text Document(s)", "Volume in PDF", 
                          "Map(s)", "Corrigendum/Addendum", "Participant", "Action", "Date of Notification/Deposit",
                          "Date of Effect"]
            row_data.append(cols)
            print(row_data)
 
# save output (will be .csv). try to save one line of csv at a time so the data doesn't get lost if the job crashes. 
csv_file_name = 'treaty_links'
out_csv_file = open(csv_file_name, 'w', newline='')
csv_writer = csv.writer(out_csv_file, delimiter=',')
_ = csv_writer.writerow(column_names)
_ = csv_writer.writerow(row_data)

#close url? close csv? 
out_csv_file.close()
