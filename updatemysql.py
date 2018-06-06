# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 21:40:46 2018

@author: keeee
"""
import pymysql
import pandas as pd 

# 打开数据库连接
db = pymysql.connect("localhost","root","0147QWE","irecommender",charset="utf8")
 
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
 
df = pd.read_table("163news_article_title_html2018-06-02.txt",header=None,names = ['content'],encoding='utf-8')
istitle = True
title_list = []
content_list = []

for indexs in df.index: 
    if istitle:
        istitle = False
        title_list.append(df.loc[indexs]['content'])
    else:
        istitle = True
        content_list.append(df.loc[indexs]['content'])

for i in range(0,len(title_list)):
    
    # SQL 插入语句
    sql = "INSERT INTO news( \
           newsTitle, newsContent) \
           VALUES ('%s', '%s')" % \
           (pymysql.escape_string(title_list[i]),pymysql.escape_string(content_list[i]) )
    
 
    cursor.execute('SET NAMES utf8;')
    cursor.execute('SET CHARACTER SET utf8;')
    cursor.execute('SET character_set_connection=utf8;')
    
    try:
       # 执行sql语句
       cursor.execute(sql)
       # 提交到数据库执行
       db.commit()
    except Exception as err:
       print(err)
       print(i)
       # 如果发生错误则回滚
       db.rollback()
 
# 关闭数据库连接
db.close()