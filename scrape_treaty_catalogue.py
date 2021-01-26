#Objective of script
#The goal of this script is to pick up where the script get_treaty_catalogue.py leaves off and to scrape through those treaty urls to harvest treaty specific metadata and the URLs
#for each volume and for each treaty .txt or .pdf file.

#packages to import
import bs4

#read in output from get_treaty_catalogue.py. Output is a .csv file. will be multiple tables so actually need to loop thru them.
## need to create set of treaties that have already been scraped, so we don't keep scraping the same ones. 
# need to put the file name below in a loop
file_object("data/treaty_catalog_' + str(search_year) + '.csv'", 

#Use .csv file to find and open first URL. Tell program which column to find the URL in. Column is called "href". 

#go to URL and "read" data from table. 
#find table on page 
#listing for self, sections of the table we would like: 
#Registration Number, Title, Places/dates of conclusion, Subject terms, Agreement type, UNTS Volume Number, Publication format, Text document(s), Volume In PDF, Map(s), #Corrigendum/Addendum, Participant 
#Question: Is it an added challenge that "Participants" is in a subtable on the bottom? Can drop. 

# save output (will be .csv). try to save one line of csv at a time so the data doesn't get lost if the job crashes. 
csv_file_name = 'data/treaty_links'
out_csv_file = open(csv_file_name, 'w', newline='')
csv_writer = csv.writer(out_csv_file, delimiter=',')
_ = csv_writer.writerow(column_names)

#close url?

#loop process so as to cycle through each table  Maybe the script for this should go at the beginning and not at the end (or needs to envelope the whole process). 

#next steps
#The output for this script will be used in a third script that will grab the text from all the text document URLS. 
