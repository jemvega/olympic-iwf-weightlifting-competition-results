#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import webscraping_functions as wf


# In[ ]:


website_url = "https://en.wikipedia.org/wiki/World_Weightlifting_Championships"
header_name = "Combined"

df = wf.WikiParser.iwf_competitions_to_dataframe(website_url, header_name)

df.replace("\\n", "", regex=True, inplace=True)
df.replace("\xa0", "", regex=True, inplace=True)

df.columns = ("Comp No. (Men), Comp No. (Women), Year, "
            "Dates, Location, No. Athletes (Men), "
            "No. Countries (Men), No. Athletes (Women), "
            "No. Countries (Women)").split(", ")

df.drop([0,1], inplace=True)

df.reset_index(inplace=True)

df.drop("index", axis=1, inplace=True)

df.to_csv(r'IWF-championships-combined.csv')


# In[ ]:


get_ipython().system('jupyter nbconvert --to script iwf-championships-combined.ipynb')

