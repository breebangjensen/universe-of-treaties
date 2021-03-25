# universe-of-treaties
Exploring the design of publicly registered international treaties.


## Scrape UN Treaties

Code here will create a collection of information about multinational treaties contain in the UN Treaty Series.  The process is divided into three parts that must be run in sequence:

1. Use `get_treaty_catalog.py` to search for treaties by month of treaty registration date.
2. Use `get_treaty_details.py` to gather metadata about individual treaties, including the path to the pdf file containing the treaty text.
3. Use `get_treaty_pdfs.py` to download every pdf file that contains a treaty.
   
These scripts need to read and write from a directory called `data/pdfs`.


## Team Members:
Bree Bang-Jensen (Ph.D. Candidate, Political Science, University of Washington)
Jose Hernandez (Data Scientist, eScience Institute, University of Washington)
Spencer Wood (Research Scientist, eScience Institute, University of Washington)

Thanks to Kray Nguyen and Huy Nguyen for their work in developing the scraping script. 
