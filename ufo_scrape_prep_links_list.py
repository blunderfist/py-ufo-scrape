# -*- coding: utf-8 -*-
"""
Created on Sat Sep 25 18:18:41 2021

@author: mdt20
"""

#UFO scrape

import requests
from bs4 import BeautifulSoup

def get_links():
    """gather links to scrape"""
    
    lst_of_links = []
    url_for_links = "http://www.nuforc.org/webreports/ndxevent.html"
    fhand = requests.get(url_for_links)
    soup = BeautifulSoup(fhand.content, 'html.parser')    

    for link in soup.findAll('a'):
        urls = link.get('href')
        lst_of_links.append(urls)
    
    #don't return the first value, its not a useful link
    return lst_of_links[1:]        
           
def build_urls_list(lst_of_links):
    """build list of complete urls for scraping"""
    
    url_lst = []
    base = "http://www.nuforc.org/webreports/"
    
    for partial in lst_of_links:
        full_url = base + partial
        url_lst.append(full_url)
    
    with open("ufo_full_urls.txt", "w") as write_file:
        for link in url_lst:
            write_file.write(link + "\n")


def main():
    gather = get_links()
    build_urls_list(gather)
    
main()

