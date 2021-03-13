#!/usr/bin/env python
import os
import re
import sys
import itertools

import PyPDF2

from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

import time 

def convert_to_txt_pypdf(pdf_file):
    pdf_reader = PyPDF2.PdfFileReader(pdf_file)
    txt_file = os.path.splitext(pdf_file)[0] +'.txt'
    with open (txt_file,'w', encoding('ascii', 'ignore')) as pdf_output:
        for page in range(pdf_reader.getNumPages()):
            data = pdf_reader.getPage(page).extractText()
            pdf_output.write(data)
    with open(txt_file, 'r') as pdf_content:
        pdf_content.read().replace('\n', ' ')

# Adapted from https://pdfminersix.readthedocs.io/en/latest/tutorial/composable.html
def convert_to_txt_miner(pdf_path):
    txt_file = os.path.splitext(file_path)[0] +'.txt'
    output_string = StringIO()
    with open(pdf_path, 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
        text = output_string.getvalue()
    with open (txt_file,'w', encoding="utf-8") as pdf_output:
        pdf_output.write(text)

file_path = '/Users/josehernandez/Documents/eScience/projects/universe-of-treaties/data/v1.pdf'

t = time.time() 
convert_to_txt_pypdf(file_path)
time.time() - t
# 5.05s

t = time.time() 
convert_to_txt_miner(file_path)
time.time() - t
# 18.38s!! Yikes!