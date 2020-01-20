# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 23:16:15 2019

@author: user
"""

from selenium import webdriver
import bs4 as bs
import pandas as pd
import datetime

df = pd.DataFrame(columns=['page', 'href'])
chromedriver = '/home/filler/chromedriver'
for i in range(0, 2):
    print('starting page %s in %s' % (str(i), datetime.datetime.now()))
    if i == 0:
        link = 'https://www.fxp.co.il/forumdisplay.php?f=46'
    else:
        link = 'https://www.fxp.co.il/forumdisplay.php?f=46&page=%s' % (str(i + 1))

    browser = webdriver.Chrome(chromedriver)
    browser.get(link)
    html_source = browser.page_source
    browser.quit()
    soup = bs.BeautifulSoup(html_source, "lxml")
    pages = []
    for el in soup.find_all("a", {"class": "title"}):
        full = el.get_text()
        pages.append(el['href'])
    df_temp = pd.DataFrame(columns=['page', 'href'])
    df_temp['href'] = pages
    df_temp['page'] = i
    df = df.append(df_temp, ignore_index=True)
    print('ending page %s in %s' % (str(i), datetime.datetime.now()))
df.to_csv('pages100.csv')
