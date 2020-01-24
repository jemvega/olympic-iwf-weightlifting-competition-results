#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import re
import requests
from bs4 import BeautifulSoup
import webscraping_functions as wf
import time
import concurrent.futures


# In[ ]:


url_domain = "https://en.wikipedia.org"
website_url = "https://en.wikipedia.org/wiki/Weightlifting_at_the_Summer_Olympics"
div_id = "mw-content-text"

# Scrape the competition urls from the Summer Olympic Weightlifting page on Wikipedia
competition_urls = [
    url_domain + elem for elem in wf.WikiParser.oly_links(
        website_url, div_id, wf.olympic_years_list
                    )]

# Use threading to grab the results url from every weightclass and append it to a list
with concurrent.futures.ThreadPoolExecutor() as executor:
    weightclass_urls = list(executor.map(wf.WikiParser.process_urls, competition_urls))
    comp_urls = []
    for index in range(len(weightclass_urls)):
        for elem in weightclass_urls[index]:
            comp_urls.append(url_domain + elem)

# Pop off the links that prevent the function from continuing
for elem in comp_urls:
    if "Qualification" in elem:
        index = comp_urls.index(elem)
        comp_urls.pop(index)
    else: 
        pass

# Use threading to write the results tables for every weightclass from 1996+ and write to .csv files
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = []
    file_names = executor.map(wf.datatable_cleanup.results_table, comp_urls)
    for names in file_names:
        futures.append(names)

# A function to concate all of the above .csv files into one file
file_name = "Olympic-Weightlifting-total-results-1980-2016"
wf.datatable_cleanup.concat_csv(file_name)


# In[ ]:


get_ipython().system('jupyter nbconvert --to script olympic-weightlifting-results-scraping.ipynb')

