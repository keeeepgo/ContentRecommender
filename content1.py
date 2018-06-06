# -*- coding: utf-8 -*-
"""
Created on Tue May 22 20:16:26 2018

@author: keeee
"""

import pandas as pd
import urllib
from lxml import etree
import html as hm
import time



if __name__ == '__main__':

    #读入文件，并输出前5行
    data = pd.read_json('163news_source_data'+time.strftime("%Y-%m-%d", time.localtime())+'.json', encoding='UTF-8')
    data = data['news']
    data = data[0]+data[1]+data[2]
    
    url_list = []
    title_list = []
    for d in data:
        url_list.append(d['l'])
        title_list.append(d['t'])
    
    with open('163news_article_title_html'+time.strftime("%Y-%m-%d", time.localtime())+'.txt', "wb+") as fo: 
        article_list = []
        for i in range(len(data)):
            url = url_list[i]
            title = title_list[i]
            res = urllib.request.urlopen(url)  
            html = res.read().decode('gbk','ignore').encode('utf-8').decode() 
            html = etree.HTML(html)
            html_data = html.xpath('//*[@id="endText"]')
            if len(html_data) == 0:
                print(url)
            else:
                html_str = etree.tostring(html_data[0])
                html_str = hm.unescape(html_str.decode())
                #去除分隔符
                html_str = html_str.replace("\r","")
                html_str = html_str.replace("\n","")
 
                fo.write(title.encode('UTF-8'))
                fo.write(('\n').encode('UTF-8'))
                fo.write(html_str.encode('UTF-8'))  
                fo.write(('\n').encode('UTF-8'))  

    
