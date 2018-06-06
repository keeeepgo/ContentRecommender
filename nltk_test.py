# -*- coding: utf-8 -*-
"""
Created on Wed May 23 21:31:11 2018

@author: keeee
"""

# -*- coding: utf-8 -*-  
 
import nltk  
with open('163news_article_html1.txt', "wb+") as fo: 
    nltk.download()
    text = fo.read()  #读取文件  
    tokens = nltk.word_tokenize(text)  #分词  
    tagged = nltk.pos_tag(tokens)  #词性标注  
    entities = nltk.chunk.ne_chunk(tagged)  #命名实体识别  
    a1=str(entities) #将文件转换为字符串  
    file_object = open('out.txt', 'w')    
    file_object.write(a1)   #写入到文件中  
    file_object.close( )  
    print(entities)