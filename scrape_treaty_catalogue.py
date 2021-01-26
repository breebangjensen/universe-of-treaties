

#Objective of script
#The goal of this script is to pick up where the script get_treaty_catalogue.py leaves off and to scrape through those treaty urls to harvest treaty specific metadata and the URLs
#for each volume and for each treaty .txt or .pdf file.

#packages to import
import bs4
import requests

#read in output from get_treaty_catalogue.py. Output is a .csv file. will be multiple tables so actually need to loop thru them.
## need to create set of treaties that have already been scraped, so we don't keep scraping the same ones. 
# need to put the file name below in a loop
for i in range(1946:2019):  
            file_object("data/treaty_catalog_' + str(i) + '.csv'")
 #this is not an connected or functional loop 
for URL in file_object
#Use .csv file to find and open first URL. Tell program which column to find the URL in. Column is called "href". 
            def open_page(url):
    r = requests.get(url)
    return BeautifulSoup(r.text, 'html.parser')


#scraping tables on url/extract data
tables = soup.findAll("table")

for table in tables:
        row_data = []
        for row in table.find_all('tr'):
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            row_data.append(cols)
        print(row_data)
 
# save output (will be .csv). try to save one line of csv at a time so the data doesn't get lost if the job crashes. 
csv_file_name = 'data/treaty_links'
out_csv_file = open(csv_file_name, 'w', newline='')
csv_writer = csv.writer(out_csv_file, delimiter=',')
_ = csv_writer.writerow(column_names)

#close url? close csv? 
out_csv_file.close()

#loop process so as to cycle through each table  Maybe the script for this should go at the beginning and not at the end (or needs to envelope the whole process). 

#next steps
#The output for this script will be used in a third script that will grab the text from all the text document URLS. 
