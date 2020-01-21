# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 23:16:15 2019

@author: user
"""

from selenium import webdriver
from bs4 import BeautifulSoup
from pandas import DataFrame
from datetime import datetime

df = DataFrame(columns=['page', 'href'])
chromedriver = '/home/filler/chromedriver'
for i in range(0, 2):
    print('starting page %s in %s' % (str(i), datetime.now()))
    if i == 0:
        link = 'https://www.fxp.co.il/forumdisplay.php?f=46'
    else:
        link = 'https://www.fxp.co.il/forumdisplay.php?f=46&page=%s' % (str(i + 1))

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    browser = webdriver.Chrome(options=options)
    browser.get(link)
    html_source = browser.page_source
    # print("html_source:\n",  html_source)
    browser.quit()
    soup = BeautifulSoup(html_source, "lxml")
    pages = []
    for el in soup.find_all("a", {"class": "title"}):
        full = el.get_text()
        pages.append(el['href'])
    df_temp = DataFrame(columns=['page', 'href'])
    df_temp['href'] = pages
    df_temp['page'] = i
    df = df.append(df_temp, ignore_index=True)
    print('ending page %s in %s' % (str(i), datetime.now()))
df.to_csv('pages100.csv')
