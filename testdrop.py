# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 14:50:02 2018

@author: keeee
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 13:28:22 2018

@author: keeee
"""

# -*- coding:utf-8 -*-
import pandas as pd
import re
import jieba
from gensim import corpora, models

def chinese_word_cut(mytext):
    return " ".join(jieba.cut(mytext))


if __name__ == "__main__":

    corpus = []   # 存储文档
    tokens = []   # 存储文档中的单词
    
        #读入文件，并输出前5行
    df = pd.read_table("163news_article_html.txt",header=None,names = ['content'],encoding='utf-8')
    #print(df.head())
    #print('\n')
    '''
    print(df.shape)
    print('\n')
    print(type(df.content))
    print("\n")
    '''

    #去除文本中的标签, 英文数字符号
    dr = re.compile(r'<[^>]+>', re.S)
    r1 = u'[a-zA-Z0-9’!"#$%&\'()*+,-./:;<=>?@：（），。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'
    
    for i in range(0, len(df.content)):
        if '无法播放' in df.content[i]:
            df.drop(i,inplace=True)
            continue          
        df.content[i] = dr.sub('', df.content[i])
        df.content[i] = re.sub(r1, '', df.content[i])
        corpus.append(df.content[i])
        #print(df.content[i])

    #进行分词
    df["content_cutted"] = df.content.apply(chinese_word_cut)
    
