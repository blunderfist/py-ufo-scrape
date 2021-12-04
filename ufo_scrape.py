# -*- coding: utf-8 -*-
"""
Created on Sat Sep 25 18:18:41 2021

@author: mdt20
"""

#UFO scrape

import requests
from bs4 import BeautifulSoup
import pandas as pd

def read_in_links():
    """reads file, sends links to scrape"""
    
    count = 0
    
    with open("ufo_full_urls.txt", 'r') as read_file:
        for url in read_file.readlines():
            url = url.rstrip()
            scrape_and_save(url, count)
            print("Loading {}".format(url))
            count += 1
    
    combine_to_master(count)

def scrape_and_save(url, count):
    """scrape table contents into dataframe, saves csv"""
    
    print("Scraping {}".format(url))

    url_to_scrape = url
    fhand = requests.get(url_to_scrape)
    soup = BeautifulSoup(fhand.content, 'html.parser')    
    table = soup.find('table')


    df_page = pd.DataFrame(columns = ["Date/Time", "City", "State", "Shape", "Duration", "Summary", "Posted"])
    
    for row in table.tbody.find_all('tr'):
        columns = row.find_all('td')

        if columns != []:
            date_time = columns[0].text.strip()
            city = columns[1].text.strip()
            state = columns[2].text.strip()
            shape = columns[3].text.strip()
            duration = columns[4].text.strip()
            summary = columns[5].text.strip()
            posted = columns[6].text.strip()

        print("Appending DataFrame")
        df_page = df_page.append({"Date/Time": date_time, "City": city, "State": state, "Shape": shape, "Duration": duration, "Summary": summary, "Posted": posted}, ignore_index = True)

    print("Writing to file...")
    title = "ufo_data_{}.txt".format(count)    
    df_page.to_csv(title, index = False)
    print("...complete")


def combine_to_master(count):
    """opens csv, appends to master"""
    header = "date_time,city,state,shape,duration,summary,posted\n"
    
    with open("ufo_data_master.txt", 'a', encoding = "utf8") as master:
        master.write(header)
        
        for _ in range(0, count):
            fname = "ufo_data_{}.txt".format(_)
            print("Appending file # {}".format(_))
            with open(fname, 'r', encoding = "utf8") as current_csv:
                lines = current_csv.readlines()
        
                for line in lines[1:]: #skips header
                    master.write(line)
                print("Appended successfully, next file...")

    print("Master file complete")

#read_in_links()

