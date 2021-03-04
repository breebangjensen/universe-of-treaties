"""Search and save UN Treaty URLs and metadata

This script outputs tables of UN Treaties, their URLs and some coarse metadata.
Its outputs serve as an input to a follow-on script for scraping treaty details
and treaty text.

Example:
    Simply kick it off from the command line::

        $ python get_treaty_catalog.py

This is adapted from https://github.com/zhiyzuo/UNTC-scraper.  Thanks, @zhiyzuo.

TODOs:
    * Outputs have duplicated rows.  Why?
"""

import os
import time
import calendar
import csv
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup as Soup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Functions
def parse_page(tr_list):
    """Parse search result tables"""
    tmp = list()
    for tr in tr_list:
        tmp.append(list())
        for i, td in enumerate(tr.find_elements_by_tag_name('td')):
            if i == 0:
                tmp[-1].append(td.find_element_by_tag_name('a').get_attribute('href'))
            tmp[-1].append(td.text.strip())
    return tmp
    # return pd.DataFrame(tmp, columns=column_names)

def month_year_iter(start_month, start_year, end_month, end_year):
    """Generator function to return year-month iter
    from https://stackoverflow.com/questions/5734438/how-to-create-a-month-iterator
    """
    ym_start= 12 * start_year + start_month - 1
    ym_end= 12 * end_year + end_month - 1
    for ym in range(ym_start, ym_end):
        y, m = divmod(ym, 12)
        yield y, m+1



# Scrape every month in a range of dates
for y,m in month_year_iter(1, 1998, 12, 2000):
    num_days = calendar.monthrange(y, m)[1]
    from_date = '01/' + str(m).zfill(2) + '/' + str(y)
    to_date = str(num_days) + '/' + str(m).zfill(2) + '/' + str(y)
    print('Searching for all treaties registered in ' + from_date + ' to ' + to_date + '...')

    # Only scrape if it doesn't already exist
    date_range = from_date[6:10] + '-' + from_date[3:5]
    # date_range = from_date[6:10] + from_date[3:5] + from_date[0:2] + '-' + to_date[6:10] + to_date[3:5] + to_date[0:2]
    csv_file_name = 'treaty_catalog_' + date_range + '.csv'
    if csv_file_name in os.listdir('data'):
        print('Skipping %s is already scraped.'%(csv_file_name))
        continue

    # Search criteria
    base_url = 'https://treaties.un.org'
    column_names = ['href', 'title', 'reg_num', 'reg_date', 'type', 'con_date', 'vol']
    tid = 'ctl00_ctl00_ContentPlaceHolder1_ContentPlaceHolderInnerPage_dgTreaty'
    url = 'https://treaties.un.org/Pages/AdvanceSearch.aspx?tab=UNTS&clang=_en'
    
    # Search and scrape UN Treaties webpages
    # everything is nested in a try statement to handle flaky internet
    while True:
        try:
            # Open browser
            chrome_options = webdriver.ChromeOptions()
            # chrome_options.add_argument("--headless")
            browser = webdriver.Chrome(options=chrome_options)
            browser.get(url)

            # Select Treaty filter
            select = Select(browser.find_element_by_name('ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolderInnerPage$drpSearchObj'))
            select.select_by_visible_text('Treaty')
            time.sleep(np.random.randint(4,8))

            # Select Show Only Original Agreements
            browser.find_element_by_id('ctl00_ctl00_ContentPlaceHolder1_ContentPlaceHolderInnerPage_rdbtreaty_2').send_keys(Keys.SPACE)
            select = Select(browser.find_element_by_name('ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolderInnerPage$drpAttribute'))
            time.sleep(np.random.randint(4,8))
            #time.sleep(np.random.randint(10, 15))

            # Select Date of Registration filter
            select = Select(browser.find_element_by_name('ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolderInnerPage$drpAttribute'))
            time.sleep(np.random.randint(4,8))
            select.select_by_visible_text('Date of Registration')

            # Select Date Range filter
            # to date first, then from date.  order is important.
            to_field = browser.find_element_by_name('ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolderInnerPage$txtTo')
            time.sleep(2)
            to_field.click()
            time.sleep(2)
            to_field.clear()
            time.sleep(2)
            to_field.send_keys(to_date)
            from_field = browser.find_element_by_name('ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolderInnerPage$txtFrom')
            from_field.click()
            time.sleep(2)
            from_field.clear()
            time.sleep(2)
            from_field.send_keys(from_date)
            time.sleep(2)
            # then add the query to the search criteria
            browser.find_element_by_name('ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolderInnerPage$btnAdd').send_keys(Keys.SPACE)
            time.sleep(2)

            # Do the Search
            browser.find_element_by_name('ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolderInnerPage$btnSubmit').send_keys(Keys.SPACE)
            time.sleep(8)

            # QAQC
            record_count_elem = browser.find_element_by_id('ctl00_ctl00_ContentPlaceHolder1_ContentPlaceHolderInnerPage_lblMsg').text
            record_count = record_count_elem.split(':')[1].strip()
            print('This query returned ' + record_count + ' treaties.')
            if int(record_count) > 500:
                raise ValueError('Search results are capped at 500 records.  Try smaller date range.')

            # Write to a csv
            csv_file_path = 'data/' + csv_file_name
            out_csv_file = open(csv_file_path, 'w', newline='')
            csv_writer = csv.writer(out_csv_file, delimiter=',')
            _ = csv_writer.writerow(column_names)

            # Iterate over pages and save results
            i = 1
            while True:
                tbody = browser.find_element_by_id(tid).find_element_by_tag_name('tbody')
                tr_list = tbody.find_elements_by_tag_name('tr')
                d = len(tr_list[1].find_elements_by_tag_name('td'))
                if d < 10:
                    s = '0%d'%d
                else:
                    s = str(d)
                id_ = 'ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolderInnerPage$dgTreaty$ctl01$ctl%s'%(s)
                btn = WebDriverWait(browser,
                                    np.random.randint(5,7)).until(EC.presence_of_element_located((By.NAME, id_)))
                for csv_row in parse_page(tr_list[3:-2]):
                    _ = csv_writer.writerow(csv_row)
                print('Parsing page %d of approx %d pages from %s...'%(i, int(record_count)/10, date_range))
                if btn.get_attribute('disabled') is not None:
                    break
                btn.click()
                i += 1
                time.sleep(np.random.randint(20, 25))

        # Handle exception by retrying the month
        except:
            print('Failed to retrieve paged results.  Retrying...')
            browser.close()
            continue

        # Or celebrate success by moving to next month
        out_csv_file.close()
        browser.close()
        break


# browser.find_elements_by_partial_link_text('showDetails')
# deets = browser.find_elements_by_xpath("//a[contains(@href,'showDetails')]")
# for d in deets:
#     print([d.get_attribute('href'), d.text])

