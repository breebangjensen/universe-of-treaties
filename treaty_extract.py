#!/usr/bin/env python
import os
import re
import sys
import itertools

from bs4 import BeautifulSoup
from requests_html import HTMLSession
import PyPDF2

def convert_to_txt(pdf_file):
    pdf_reader = PyPDF2.PdfFileReader(pdf_file)
    txt_file = os.path.splitext(pdf_file)[0] +'.txt'
    with open (txt_file,'w', encoding('ascii', 'ignore')) as pdf_output:
        for page in range(pdf_reader.getNumPages()):
            data = pdf_reader.getPage(page).extractText()
            pdf_output.write(data)
    with open(txt_file, 'r') as pdf_content:
        pdf_content.read().replace('\n', ' ')

data_path = '/Users/josehernandez/Documents/eScience/projects/universe-of-treaties/data/'

for pdf in os.listdir(data_path):
    convert_to_txt(data_path+pdf)

# test regex
# begins with [No. #####] d{5}
