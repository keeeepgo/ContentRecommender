# -*- coding: utf-8 -*-
import pandas as pd
import re
import jieba
from gensim import corpora, models, similarities
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import numpy as np

def chinese_word_cut(mytext):
    return " ".join(jieba.cut(mytext))

def print_top_words(model, feature_names, n_top_words):

    for topic_idx, topic in enumerate(model.components_):

        print("Topic #%d:" % topic_idx)

        print(" ".join([feature_names[i]

                        for i in topic.argsort()[:-n_top_words - 1:-1]]))

    print()

if __name__ == '__main__':

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
        df.content[i] = dr.sub('', df.content[i])
        df.content[i] = re.sub(r1, '', df.content[i])
        #print(df.content[i])

    #进行分词
    df["content_cutted"] = df.content.apply(chinese_word_cut)
    
    '''
    #存为字典
    df_list = list(df["content_cutted"])
    df_uniarray = []
    for i in df_list:
        df_uniarray.append(i.encode())
    dictionary = corpora.Dictionary([df_list])
    dictionary.save('163news_article_dic.dict')
    '''
    
    df_pra = df["content_cutted"][0:400];
    df_check = df["content_cutted"][400:];
    
    
    # 从文件导入停用词表
    stpwrdpath = "stop_words.txt"
    stpwrd_dic = open(stpwrdpath, 'r')
    stpwrd_content = stpwrd_dic.read()
    # 将停用词表转换为list
    stpwrdlst = stpwrd_content.splitlines()
    stpwrd_dic.close()

    #将文本向量化
    n_features = 700
    tf_vectorizer = TfidfVectorizer(strip_accents = 'unicode',

                                    max_features=n_features,

                                    stop_words=stpwrdlst,

                                    max_df = 0.5,

                                    min_df = 0)

    tf = tf_vectorizer.fit_transform(df_pra)
    tf_feature_names = tf_vectorizer.get_feature_names()
    #print(tf_feature_names)
    
    tf_check = tf_vectorizer.fit_transform(df_check)

    #用LDA进行主题分析
    
    #corpus = [dictionary.doc2bow(text) for text in texts]
    #model = models.LdaModel(tf, id2word=dictionary, num_topics=100)

    



    
    #用LDA进行主题分析
    n_topics = 10
    lda = LatentDirichletAllocation(n_components=n_topics, max_iter=5000,

                                    learning_method='online',

                                    learning_offset=50.,

                                    random_state=0)
    lda.fit(tf)

    n_top_words = 20
    tf_feature_names = tf_vectorizer.get_feature_names()
    #print(tf_feature_names)
    print_top_words(lda, tf_feature_names, n_top_words)
        
    ans = lda.transform(tf_check)
    print(ans)
