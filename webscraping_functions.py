#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
import concurrent.futures
import os
from glob import glob


# In[ ]:


years_list = [1996 + x for x in range(24)]

olympic_years_list = [1980 + x for x in range(0, 40, 4)]

country_codes = pd.read_html("https://www.iban.com/country-codes")[0]

class CheckFunctions():
    
    @staticmethod
    def check_group(results_dataframe):
#         try: 
        if not "Group\n" in results_dataframe.iloc[0].values:
            results_dataframe.insert(2, "Group", "A")
            return results_dataframe
        else: 
            return results_dataframe

    @staticmethod
    def check_bodyweight(results_dataframe):
        if not "Bodyweight\n" in results_dataframe.iloc[0].values:
            if not "Body weight\n" in results_dataframe.iloc[0].values:
                    if not "Body Weight\n" in results_dataframe.iloc[0].values:
                        results_dataframe.insert(3, "Body Weight (kg)", "NaN")
                        return results_dataframe
        else:
            return results_dataframe

    @staticmethod
    def check_nation(results_dataframe):
        if not "Nation\n" in results_dataframe.iloc[0].values:
            new_cols = results_dataframe[1].str.split("(", 1, expand=True)
            results_dataframe[1] = new_cols[0]
            results_dataframe.insert(2, "Nationality", new_cols[1])
            results_dataframe["Nationality"] = results_dataframe["Nationality"].str.strip(")")
            return results_dataframe
        else:
            return results_dataframe
            
    @staticmethod
    def check_max_lift(results_dataframe):
        if not "Result\n" in results_dataframe.iloc[1].values:
            results_dataframe.insert(8, "Max Snatch", 0)
            results_dataframe.insert(13, "Max C/J", 0)
            return results_dataframe
        else:
            return results_dataframe

    @staticmethod
    def check_rank(results_dataframe):
        if not "Rank\n" in results_dataframe.iloc[1].values:
            results_dataframe.insert(9, "Snatch Rank", 0)
            results_dataframe.insert(14, "C/J Rank", 0)
            return results_dataframe
        else:
            results_dataframe.rename({9: "Snatch Rank", 14: "C/J Rank"})
            return results_dataframe
            
class WikiParser():
    
    @staticmethod
    def get_h1_text(website_url):
        url = requests.get(website_url)
        page = BeautifulSoup(url.text, 'lxml')
        header_id = page.find("h1", id="firstHeading").get_text()
        return header_id
    
    @staticmethod
    # Create a function to grab all of the results urls from each weight class of the competition year
    def process_urls(url):
        website_url = requests.get(url)
        page = BeautifulSoup(website_url.text, "lxml")
        results_urls = []
        for link in page.find_all("a", attrs={"href": re.compile(f"^{url[24:]}_")}):
            results_urls.append(link.get('href'))
        return results_urls
    
    @staticmethod
    def iwf_competitions_to_dataframe(website_url, header_name):
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
    
    @staticmethod
    def iwf_links(website_url, header_name, years_list):
        # parse html; find table; find table rows
        url = requests.get(website_url)
        page = BeautifulSoup(url.text, 'lxml')
        header_id = page.find("span", id=header_name)
        wiki_table = header_id.parent.find_next_sibling("table", class_="wikitable")
        # Iterate through rows and load text into a list
        links_list = []
        for link in wiki_table.find_all("a"):
            for year in years_list:
                if f"{year}" in link.get_text():
                    links_list.append(link.get("href"))
        return links_list
    
    @staticmethod
    def oly_links(website_url, div_id, years_list):
        # parse html; find table; find table rows
        url = requests.get(website_url)
        page = BeautifulSoup(url.text, 'lxml')
        page_details = page.find("div", id=div_id)
        oly_years_table = page_details.find("table", class_="infobox")
        # Iterate through rows and load text into a list
        links_list = []
        for link in oly_years_table.find_all("a"):
            for year in olympic_years_list:
                if f"{year}" in link.get_text():
                    links_list.append(link.get("href"))
        return links_list
    
    @staticmethod
    def results_to_dataframe(website_url, header_name):
        # parse html; find table; find table rows
        url = requests.get(website_url)
        page = BeautifulSoup(url.text, 'lxml')
        header_id = page.find("span", id=header_name)
        wiki_table = header_id.parent.find_next_sibling("table", class_="wikitable")
        table_cells = wiki_table.find('td')
        table_rows = wiki_table.find_all("tr")
        # Iterate through rows and load text into a list
        results_table = []
        for elem in table_rows:
            strikethrough = elem.find_all("s")
            bold = elem.find_all("b")
            for string in strikethrough:
                negative = "".join(f"-{string.get_text()}")
                string.replace_with(negative)
            for string in bold:
                non_bold = "".join(f"{string.get_text()}")
                string.replace_with(non_bold)
        for tag in table_rows:
            table_tags = tag.find_all(["th", "td"])
            td = []
            for text in table_tags:
                td.append(text.get_text())
            results_table.append(td)
        results_df = pd.DataFrame(results_table)
        return results_df
    
class ResultsCleanup():
    
    @staticmethod
    def column_row_cleanup(results_dataframe):
        CheckFunctions.check_group(results_dataframe)
        CheckFunctions.check_bodyweight(results_dataframe)
        CheckFunctions.check_nation(results_dataframe)
        CheckFunctions.check_max_lift(results_dataframe)
        CheckFunctions.check_rank(results_dataframe)
        column_names = (
                "Comp Rank, Athlete Name, Nationality, Group, Body Weight (kg), "
                "Snatch 1 (kg), Snatch 2 (kg), Snatch 3 (kg), Max Snatch, Snatch Rank, "
                "C/J 1 (kg), C/J 2 (kg), C/J 3 (kg), Max C/J, C/J Rank, Total"
                        ).split(", ")
        results_dataframe.columns = column_names
        results_dataframe.drop([0,1], inplace=True)
        results_dataframe.reset_index(inplace=True)
        results_dataframe.drop("index", axis=1, inplace=True)
        # Change country name to country code for consistency
        CheckFunctions.change_nation_code(results_dataframe)
        return results_dataframe

    @staticmethod
    def check_float(string):
        try:
            float(string)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def string_to_float(converted_list):
        for elem in converted_list:
            if ResultsCleanup.check_float(elem):
                rational = float(elem)
                index = converted_list.index(elem)
                converted_list.pop(index)
                converted_list.insert(index, rational)
            elif ResultsCleanup.check_float(elem) == False:
                index = converted_list.index(elem)
                converted_list.pop(index)
                converted_list.insert(index, 0)
            else:
                print("error")
        return converted_list
    
    @staticmethod
    def lift_rankings(results_dataframe, lift_col_names, max_lift, lift_rank):
        """Note: lift_col_names = ["Snatch 1 (kg)", "Snatch 2 (kg)", "Snatch 3 (kg)"] 
                                or ["C/J 1 (kg)", "C/J 2 (kg)", "C/J 3 (kg)"]
        Note: max_lift = 'Max Snatch' or 'Max C/J' 
        Note: lift_rank = 'Snatch Rank' or 'C/J Rank'"""
        temp_list = results_dataframe[lift_col_names].values.tolist()
        max_weight = []
        for elem in temp_list:
            ResultsCleanup.string_to_float(elem)
        results_dataframe[lift_col_names] = temp_list
        for row in temp_list:
            row.sort()
        for row in range(len(temp_list)):
            max_weight.append(temp_list[row][-1])
        # Sort the indices of the max lifts to get comp rank (overall place)
        max_lift_rankings = list(sorted(max_weight, reverse=True).index(num) + 1 for num in max_weight)
        results_dataframe[max_lift] = max_weight
        results_dataframe[lift_rank] = max_lift_rankings
        return results_dataframe

    @staticmethod
    def data_cleanup(results_dataframe):
        podium = [1, 2, 3]
        for i in range(len(podium)):
            results_dataframe["Comp Rank"][i] = podium[i]
        results_dataframe.replace("\n", "", regex=True, inplace = True)
        results_dataframe.replace("\xa0", "", regex=True, inplace=True)
        results_dataframe.replace("None", "", regex=True, inplace=True)
        results_dataframe.fillna("NaN", inplace = True)
        # Some cells have "OR" or "=OR" to indicate Olympic Record.
        # The following .split() func delete any data after the digit
        results_dataframe["Snatch 1 (kg)"] = results_dataframe["Snatch 1 (kg)"].str.split().str[0]
        results_dataframe["Snatch 2 (kg)"] = results_dataframe["Snatch 2 (kg)"].str.split().str[0]
        results_dataframe["Snatch 3 (kg)"] = results_dataframe["Snatch 3 (kg)"].str.split().str[0]
        results_dataframe["C/J 1 (kg)"] = results_dataframe["C/J 1 (kg)"].str.split().str[0]
        results_dataframe["C/J 2 (kg)"] = results_dataframe["C/J 2 (kg)"].str.split().str[0]
        results_dataframe["C/J 3 (kg)"] = results_dataframe["C/J 3 (kg)"].str.split().str[0]
        results_dataframe["Total"] = results_dataframe["Total"].astype(str).str.split().str[0]
        results_dataframe["Body Weight (kg)"] = ResultsCleanup.string_to_float(results_dataframe["Body Weight (kg)"].values.tolist())
        results_dataframe["Comp Rank"] = ResultsCleanup.string_to_float(results_dataframe["Comp Rank"].values.tolist())
        results_dataframe["Total"] = ResultsCleanup.string_to_float(results_dataframe["Total"].values.tolist())
        return results_dataframe

class datatable_cleanup():
    
    @staticmethod
    def insert_year(website_url):
        if website_url[30:43] == "Weightlifting":
            year = website_url[51:55]
            return year
        else:
            year = website_url[30:34]
            return year 
    
    @staticmethod
    def insert_gender(website_url):
        if website_url[79:82] == "Men":
            gender = "M"
            return gender
        elif website_url[79:84] == "Women":
            gender = "W"
            return gender
        elif website_url[82:85] == "Men":
            gender = "M"
            return gender
        elif website_url[82:87] == "Women":
            gender = "W"
            return gender
        
    @staticmethod
    def country_code_cleanup(dataframe):
        iso_country_codes = pd.read_csv("country-codes-alpha-3-only.csv")
        iso_country_codes.drop("Unnamed: 0", axis=1, inplace=True)
        ioc_country_codes = pd.read_csv("country-codes-ioc.csv")
        ioc_country_codes.drop("Unnamed: 0", axis=1, inplace=True)
        for country in dataframe["Nationality"].values.tolist():
            if country in iso_country_codes["Country"].values.tolist():
                iso_dataframe_index = dataframe["Nationality"].values.tolist().index(country)
                iso_code_index = iso_country_codes["Country"].values.tolist().index(country)
                iso_code = iso_country_codes["Alpha-3 code"][iso_code_index]
                dataframe["Nationality"][iso_dataframe_index] = iso_code
            elif country in ioc_country_codes["Country"].values.tolist():
                ioc_dataframe_index = dataframe["Nationality"].values.tolist().index(country)
                ioc_code_index = ioc_country_codes["Country"].values.tolist().index(country)
                ioc_code = ioc_country_codes["IOC code"][ioc_code_index]
                dataframe["Nationality"][ioc_dataframe_index] = ioc_code
        return dataframe
        
    @staticmethod
    def insert_event(website_url):
        if website_url[30:43] == "Weightlifting":
            event = "oly"
            return event
        else:
            event = "iwf"
            return event
            
    @staticmethod
    def results_table(website_url):
        year = datatable_cleanup.insert_year(website_url)
        gender = datatable_cleanup.insert_gender(website_url)
        event = datatable_cleanup.insert_event(website_url)
        url_header = WikiParser.get_h1_text(website_url)
        header_name = "Results"
        snatch_cols = ["Snatch 1 (kg)", "Snatch 2 (kg)", "Snatch 3 (kg)"] 
        clean_cols = ["C/J 1 (kg)", "C/J 2 (kg)", "C/J 3 (kg)"]
        df = WikiParser.results_to_dataframe(website_url, header_name)
        ResultsCleanup.column_row_cleanup(df)
        ResultsCleanup.data_cleanup(df)
        ResultsCleanup.lift_rankings(df, snatch_cols, "Max Snatch", "Snatch Rank")
        ResultsCleanup.lift_rankings(df, clean_cols, "Max C/J", "C/J Rank")
        df.insert(0,"Year", year)
        df.insert(1, "Event", event)
        df.insert(2, "Gender", gender)
        file_name = url_header + ".csv"
        df.to_csv(file_name)
        return file_name
        
    @staticmethod
    def concat_csv(file_name):
        file_pattern = ".csv"
        file_rename = file_name + file_pattern
        list_of_files = [file for file in glob("*{}".format(file_pattern))]
        # Combine all files in the list into a dataframe
        dataframe_csv = pd.concat([pd.read_csv(file, engine="python") for file in list_of_files])
        # Export the dataframe to csv
        dataframe_csv.to_csv(file_rename, index=False, encoding='utf-8')
        list_of_files
        return list_of_files


# In[5]:


get_ipython().system('jupyter nbconvert --to script webscraping_functions.ipynb')

