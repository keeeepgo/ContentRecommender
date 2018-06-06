we# -*- coding: utf-8 -*-

import feedparser  
import csv  

FEED_URL = 'https://feedx.net/rss/thepaper.xml'  
fp = feedparser.parse(FEED_URL)  
  
with open("pengpai_news.csv","w") as csvfile: 
    writer = csv.writer(csvfile)
    for e in fp.entries:  
        print('content:', e.summary_detail.value)
        writer.writerow(e.summary_detail.value)