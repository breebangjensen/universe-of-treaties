#Objective of script
#The goal of this script is to pick up where the script get_treaty_catalogue.py leaves off and to scrape through those treaty urls to harvest treaty specific metadata and the URLs
#for each volume and for each treaty .txt or .pdf file.

#packages to import

#read in output from get_treaty_catalogue.py. Output is a .csv file. 

#Use .csv file to find and open first URL. Tell program which column to find the URL in. 

#go to URL and "read" data from table. 
#listing for self, sections of the table we need
#Registration Number, Title, Places/dates of conclusion, Subject terms, Agreement type, UNTS Volume Number, Publication format, Text document(s), Volume In PDF, Map(s), #Corrigendum/Addendum, Participant 

# save output (will be csv)

#close url?

#loop process so as to cycle through each row in the .csv file.  Maybe the script for this should go at the beginning and not at the end (or both). 

#next steps
#The output for this script will be used in a third script that will grab the text from all the text document URLS. 
