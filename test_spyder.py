# -*- coding: utf-8 -*-
"""
Created on Tue May 22 17:26:04 2018

@author: keeee
"""

import  urllib.request  
import json
import codecs
import time


url = 'http://news.163.com/special/0001220O/news_json.js'  
res = urllib.request.urlopen(url)  
html = res.read().decode('gbk','ignore').encode('utf-8').decode() 
pos = html.find('data=');
html = html[pos+5:-1];
data = json.loads(html)

with codecs.open('163news_source_data'+time.strftime("%Y-%m-%d", time.localtime())+'.json', 'w', 'utf-8') as f:
    f.write(json.dumps(data)) # 用换行分开