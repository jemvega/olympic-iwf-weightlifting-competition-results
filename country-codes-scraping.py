#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import pandas as pd


# In[96]:


def iso_country_codes(website_url):
    code_text = []
    url = requests.get(website_url)
    page = BeautifulSoup(url.text, 'lxml')
    wiki_table = page.find("div", class_= "plainlist")
    code_data = wiki_table.find_all(["span", "a"])
    for text in code_data:
        code_text.append(text.get_text())
    return code_text


# In[30]:


def ioc_country_codes(website_url, header_name):
    # parse html; find table; find table rows
    url = requests.get(website_url)
    page = BeautifulSoup(url.text, 'lxml')
    header_id = page.find("span", id=header_name)
    wiki_table = header_id.parent.find_next_sibling("table", class_="wikitable")
    table_cells = wiki_table.find('td')
    table_rows = wiki_table.find_all("tr")
    # Iterate through rows and load text into a list
    results_table = []
    for row in table_rows:
        table_tags = row.find_all(["th", "td"])
        td = list(item.text for item in table_tags)
        results_table.append(td)
    results_df = pd.DataFrame(results_table)
    return results_df


# In[97]:


website_url = "https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3"
table_data = iso_country_codes(website_url)

table_data[457] = "Taiwan, Province of China"

table_data.pop(458)

code_names = []
country_names = []
for elem in table_data:
    if len(elem) == 3:
        code_names.append(elem)
    else: 
        country_names.append(elem)

iso_code_list = list(zip(code_names, country_names))
iso_code_dataframe = pd.DataFrame(code_country_list)
iso_code_dataframe.columns = ["Alpha-3 code", "Country"]
iso_code_dataframe.to_csv("country-codes-alpha-3-only.csv")


# In[109]:


website_url1 = "https://en.wikipedia.org/wiki/List_of_IOC_country_codes"
header_name1 = "Current_NOCs"
ioc_dataframe = ioc_country_codes(website_url1, header_name1)

ioc_dataframe.drop(3, axis=1, inplace=True)
ioc_dataframe.columns = ["IOC code", "Country", "Other codes used"]
ioc_dataframe.replace("\n", "", regex=True, inplace=True)
new_col = ioc_dataframe["Country"].str.split("[", 1, expand=True)
ioc_dataframe["Country"] = new_col[0]
ioc_dataframe.drop(0, inplace=True)
ioc_dataframe.reset_index(inplace=True)
ioc_dataframe.drop("index", axis=1, inplace=True)
ioc_dataframe.iloc[0].values[0] = ioc_dataframe.iloc[0].values[0].split("}")[1]

ioc_dataframe.to_csv("country-codes-ioc.csv")



ioc_dataframe


# In[94]:


website_url1 = "https://en.wikipedia.org/wiki/List_of_IOC_country_codes"
header_name1 = "Current_NOCs"
ioc_dataframe = ioc_country_codes(website_url1, header_name1)

ioc_dataframe.drop(3, axis=1, inplace=True)
ioc_dataframe.columns = ["IOC code", "Country", "Other codes used"]
ioc_dataframe.replace("\n", "", regex=True, inplace=True)
ioc_dataframe.replace("\xa0", "", regex=True, inplace=True)
new_col = ioc_dataframe["Country"].str.split("[", 1, expand=True)
ioc_dataframe["Country"] = new_col[0]
ioc_dataframe.drop(0, inplace=True)
ioc_dataframe.reset_index(inplace=True)
ioc_dataframe.drop("index", axis=1, inplace=True)
ioc_dataframe.iloc[0].values[0] = ioc_dataframe.iloc[0].values[0].split("}")[1]

ioc_dataframe.to_csv("country-codes-ioc.csv")


# In[111]:


get_ipython().system('jupyter nbconvert --to script country-codes-scraping.ipynb')

