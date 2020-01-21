# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 13:38:49 2019

@author: user
"""

from selenium import webdriver
from bs4 import BeautifulSoup
from pandas import DataFrame, read_csv
from datetime import datetime

df_craft = DataFrame(columns=['thread', 'post'])
counter = 0
df_pages = read_csv('pages100.csv')
chromedriver = 'chromedriver.exe'
base_url = 'https://www.fxp.co.il/'
for page in df_pages['href'].values:
    print(counter)
    print('starting page %s in %s' % (page, datetime.now()))
    link = base_url + page
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    browser = webdriver.Chrome(options=options)
    browser.get(link)
    html_source = browser.page_source
    browser.quit()
    soup = BeautifulSoup(html_source, "lxml")
    el = soup.find("h1", {'itemprop': 'headline'})
    if el is None:
        continue
    title = el.get_text()
    df_craft = df_craft.append({'thread': page, 'post': title}, ignore_index=True)
    for el in soup.find_all("blockquote", {"class": "postcontent restore"}):
        full = el.get_text()
        r = el.find_all('div')
        if r is not None:
            for rr in r:
                full = full.replace(rr.get_text(), '')
        if full != '':
            df_craft = df_craft.append({'thread': page, 'post': full}, ignore_index=True)
    last_page = 0
    for el in soup.find_all("span", {"class": "first_last"}):
        if el is not None:
            r = el.find('a')
            if r is not None:
                last_page = r['href']
                start_pos = int(last_page.rfind('page')) + 5
                last_pos = int(last_page[start_pos:].rfind('&'))
                if last_pos == -1:
                    last_page_number = last_page[start_pos:]
                else:
                    last_page_number = last_page[int(start_pos):int(last_pos) + int(start_pos)]
    if last_page != 0:
        last_page_number = int(last_page_number) + 1
        for i in range(2, last_page_number):
            link = base_url + page + '&page=' + str(i)
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            browser = webdriver.Chrome(options=options)
            browser.get(link)
            html_source = browser.page_source
            browser.quit()
            soup = BeautifulSoup(html_source, "lxml")
            for el in soup.find_all("blockquote", {"class": "postcontent restore"}):
                full = el.get_text()
                r = el.find_all('div')
                if r is not None:
                    for rr in r:
                        full = full.replace(rr.get_text(), '')
                if full != '':
                    df_craft = df_craft.append({'thread': page, 'post': full}, ignore_index=True)

    print('ending page %s in %s' % (page, datetime.now()))
    counter = counter + 1
    if counter % 100 == 0:
        df_craft.to_csv('newversion_sc%s.csv' % (str(counter)), encoding='utf-8-sig', index=False)

df_craft.to_csv('newversion_sc%s.csv' % (str(counter)), encoding='utf-8-sig', index=False)
