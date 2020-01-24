#!/usr/bin/env python
# coding: utf-8

# In[4]:


import re
import requests
from bs4 import BeautifulSoup
import webscraping_functions as wf
import time
import concurrent.futures


# In[5]:


url_domain = "https://en.wikipedia.org"
website_url = "https://en.wikipedia.org/wiki/World_Weightlifting_Championships"
header_name = "Combined"

# Scrape the competition urls from the World_Weightlifting_Championships page on Wikipedia
competition_urls = [
    url_domain + elem for elem in wf.WikiParser.iwf_links(
        website_url, header_name, wf.years_list
                    )]

# Use threading to grab the results url from every weightclass and append it to a list
with concurrent.futures.ThreadPoolExecutor() as executor:
    weightclass_urls = list(executor.map(wf.WikiParser.process_urls, competition_urls))
    comp_urls = []
    for index in range(len(weightclass_urls)):
        for elem in weightclass_urls[index]:
            comp_urls.append(url_domain + elem) 

# Use threading to write the results tables for every weightclass from 1996+ and write to .csv files
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = []
    file_names = executor.map(wf.datatable_cleanup.results_table, comp_urls)
    for names in file_names:
        futures.append(names)
        
# A function to concate all of the above .csv files into one file
file_name = "IWF-championships-total-results-1996-2019"
wf.datatable_cleanup.concat_csv(file_name)


# In[ ]:





# In[ ]:


import pdb; pdb.set_trace()
for elem in comp_urls:
    wf.datatable_cleanup.results_table(elem)


# In[ ]:


for elem in comp_urls:
    wf.datatable_cleanup.results_table(elem)


# In[ ]:





# In[ ]:


# import csv 
# with open(..., 'w', newline='') as myfile:
#      wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
#      wr.writerow(mylist)


# In[ ]:


import pandas as pd
iwf_list_links = pd.DataFrame(comp_urls)


# In[ ]:


iwf_list_links.to_csv("iwf_links_list.csv")


# In[ ]:





# In[ ]:





# In[ ]:


import pdb; pdb.set_trace()
for elem in iwf_links_list:
    wf.datatable_cleanup.results_table(elem)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


website_url = "https://en.wikipedia.org/wiki/2003_World_Weightlifting_Championships_%E2%80%93_Men%27s_69_kg"
header_name = "Results"

df = wf.WikiParser.results_to_dataframe(website_url, header_name)
df


# In[ ]:


# df.replace("None", "", regex=True, inplace=True)
df.fillna("NaN", inplace=True)
df


# In[ ]:


df[12].values.tolist()


# In[ ]:





# In[ ]:





# In[ ]:





# In[1]:


import re
import requests
from bs4 import BeautifulSoup
import webscraping_functions as wf
import time
import concurrent.futures


# In[2]:


import pandas as pd
iwf_urls_list = pd.read_csv("iwf_urls_list.csv")
iwf_urls_list.drop("Unnamed: 0", axis=1, inplace=True)
iwf_urls_list.head()


# In[ ]:


iwf_urls_list.head()


# In[ ]:


iwf_urls_list["0"]


# In[3]:


import pdb; pdb.set_trace()
for elem in iwf_urls_list["0"].values.tolist():
    wf.datatable_cleanup.results_table(elem)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


website_url = "https://en.wikipedia.org/wiki/2019_World_Weightlifting_Championships_%E2%80%93_Women%27s_59_kg"
header_name = "Results"

df = wf.WikiParser.results_to_dataframe(website_url, header_name)
df


# In[ ]:


year = wf.datatable_cleanup.insert_year(website_url)
gender = wf.datatable_cleanup.insert_gender(website_url)
event = wf.datatable_cleanup.insert_gender(website_url)
url_header = wf.WikiParser.get_h1_text(website_url)
header_name = "Results"
snatch_cols = ["Snatch 1 (kg)", "Snatch 2 (kg)", "Snatch 3 (kg)"] 
clean_cols = ["C/J 1 (kg)", "C/J 2 (kg)", "C/J 3 (kg)"]
df = wf.WikiParser.results_to_dataframe(website_url, header_name)
wf.ResultsCleanup.column_row_cleanup(df)
wf.ResultsCleanup.data_cleanup(df)
wf.ResultsCleanup.lift_rankings(df, snatch_cols, "Max Snatch", "Snatch Rank")
wf.ResultsCleanup.lift_rankings(df, clean_cols, "Max C/J", "C/J Rank")
df.insert(0,"Year", year)
df.insert(1, "Event", event)
df.insert(2, "Gender", gender)
file_name = url_header + ".csv"
df.to_csv(file_name)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


website_url = "https://en.wikipedia.org/wiki/2019_World_Weightlifting_Championships_%E2%80%93_Women%27s_59_kg"
header_name = "Results"

df = wf.WikiParser.results_to_dataframe(website_url, header_name)


# In[ ]:


results_dataframe = df
results_dataframe


# In[ ]:


if not "Rank\n" in results_dataframe.iloc[1].values:
    results_dataframe.insert(9, "Snatch Rank", 0)
    results_dataframe.insert(14, "C/J Rank", 0)
    results_dataframe
else:
    results_dataframe.rename({9: "Snatch Rank", 14: "C/J Rank"})
# #     results_dataframe.iloc[columns=9].column = "Snatch Rank"
# #     results_dataframe.iloc[columns=14].column = "C/J Rank"
#     results_dataframe.drop(columns=[8, 14], inplace = True)
    results_dataframe


# In[ ]:


wf.CheckFunctions.check_group(results_dataframe)
results_dataframe


# In[ ]:


wf.CheckFunctions.check_bodyweight(results_dataframe)
results_dataframe


# In[ ]:


wf.CheckFunctions.check_nation(results_dataframe)
results_dataframe


# In[ ]:


df = wf.WikiParser.results_to_dataframe(website_url, header_name)


# In[ ]:


wf.CheckFunctions.check_max_lift(results_dataframe)
results_dataframe


# In[ ]:


wf.CheckFunctions.check_rank(results_dataframe)
results_dataframe


# In[ ]:


results_dataframe


# In[ ]:


column_names = (
                "Comp Rank, Athlete Name, Nationality, Group, Body Weight (kg), "
                "Snatch 1 (kg), Snatch 2 (kg), Snatch 3 (kg), Max Snatch, Snatch Rank, "
                "C/J 1 (kg), C/J 2 (kg), C/J 3 (kg), Max C/J, C/J Rank, Total"
                ).split(", ")
results_dataframe.columns = column_names


# In[ ]:


results_dataframe


# In[ ]:


results_dataframe.drop([0,1], inplace=True)
results_dataframe.reset_index(inplace=True)
results_dataframe.drop("index", axis=1, inplace=True)
# Change country name to country code for consistency
for country in results_dataframe["Nationality"].values.tolist():
    if country in wf.country_codes["Country"].values.tolist():
        index = wf.country_codes["Country"].values.tolist().index(country)
        code = wf.country_codes["Alpha-3 code"][index]
        results_dataframe["Nationality"][index] = code
    else:
        pass


# In[ ]:





# In[ ]:


results_dataframe


# In[ ]:


wf.ResultsCleanup.column_row_cleanup(df)


# In[ ]:


wf.ResultsCleanup.data_cleanup(df)
wf.ResultsCleanup.lift_rankings(df, snatch_cols, "Max Snatch", "Snatch Rank")
wf.ResultsCleanup.lift_rankings(df, clean_cols, "Max C/J", "C/J Rank")
df.insert(0,"Year", year)
df.insert(1, "Gender", gender)
file_name = url_header + ".csv"
df.to_csv(file_name)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


get_ipython().system('jupyter nbconvert --to script iwf-championships-results-scraping.ipynb')

