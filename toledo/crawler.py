from urllib.request import urlopen, Request
from lxml import html
import pandas as pd
from datetime import datetime
import re

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}


def thread_ids(pages, verbose=True):
    print('Fetching pages...')
    count = 0
    thread_ids = []
    for i in pages:
        request = Request(url='https://www.fxp.co.il/forumdisplay.php?f=46&page=%s' % i,
                          headers=headers)
        tree = html.fromstring(urlopen(request).read().decode('utf-8'))

        # slice [7:] to eliminate prefix
        thread_ids += [int(x[7:]) for x
                       in tree.xpath('//ol[@id=\'threads\']/li/@id')]

        count += 1
        if verbose and (count % 10 == 0):
            print('Fetched %s pages' % (count))
            print(datetime.now().time())
    print(pd.Series(thread_ids).value_counts().head(20))
    return thread_ids


def thread_content(thread_ids, file, verbose=True):
    print('Fetching threads...')
    count = 0
    df = pd.DataFrame(columns=['thread', 'post'])
    for i in thread_ids:
        request = Request(
            url='https://www.fxp.co.il/showthread.php?t=%s' %
            (i),
            headers=headers)
        tree = html.fromstring(urlopen(request).read().decode('utf-8'))
        messages = tree.xpath('//div[@id=\'postlist\']//blockquote\
            [@class=\'postcontent restore\']')
        for m in messages:
            message_text = ' '.join(m.xpath('./text()'))
            df = df.append({'thread': i, 'post': message_text},
                           ignore_index=True)
        last_page = tree.xpath('//span[@class=\'first_last\']/a/@href')
        if len(last_page) > 0:
            last_page = last_page[0]
            last_page = int(re.search('page=([0-9]+)', last_page).group(1))
            for j in range(2, last_page + 1):
                request = Request(
                    url='https://www.fxp.co.il/showthread.php?t=%s&page=%s' %
                    (i, j),
                    headers=headers)
                tree = html.fromstring(urlopen(request).read().decode('utf-8'))
                messages = tree.xpath('//div[@id=\'postlist\']//\
                    blockquote[@class=\'postcontent restore\']')
                for m in messages:
                    message_text = ' '.join(m.xpath('./text()'))
                    df = df.append({'thread': i, 'post': message_text},
                                   ignore_index=True)
        count += 1
        if verbose and (count % 100 == 0):
            print('Fetched %s threads' % (count))
            print(datetime.now().time())
        if (count % 1000 == 0):
            df.to_csv(file, encoding='utf-8')


thread_content(thread_ids(range(1, 240)), '1to240.csv')
