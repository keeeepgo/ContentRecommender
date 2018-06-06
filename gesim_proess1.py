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
    
    '''
    #分训练集和测试集
    df_check = df[400:];
    df = df[0:400];
    '''

    #进行分词
    df["content_cutted"] = df.content.apply(chinese_word_cut)
    
    # 从文件导入停用词表
    stpwrdpath = "stop_words.txt"
    stpwrd_dic = open(stpwrdpath, 'r')
    stpwrd_content = stpwrd_dic.read()
    # 将停用词表转换为list
    stpwrdlst = stpwrd_content.splitlines()
    stpwrd_dic.close()
    
    for text in df["content_cutted"]:
        cut_text = text.split(' ')
        stop_remove_token = [word for word in cut_text if word not in stpwrdlst]
        # stem_token = [p_stemmer.stem(word) for word in stop_remove_token]
        tokens.append(stop_remove_token)
    # print tokens
    
    '''
    #存为字典
    df_list = list(df["content_cutted"])
    df_uniarray = []
    for i in df_list:
        df_uniarray.append(i.encode())
    dictionary = corpora.Dictionary([df_list])
    dictionary.save('163news_article_dic.dict')
    '''
    
    '''
    # 读取文档的操作
    for line in open('a.txt','r').readlines():
        if '\xef\xbb\xbf' in line:
            line = line.replace('\xef\xbb\xbf', ' ')
        corpus.append(line.strip())
    print(corpus)

    # 去标点符号，去截止词的操作
    en_stop = get_stop_words('en')   # 利用Pypi的stop_words包，需要去掉stop_words

    # # 提取主干的词语的操作
    # p_stemmer = PorterStemmer()

    # 分词的操作
    tokenizer = RegexpTokenizer(r'\w+')
    for text in corpus:
        raw = text.lower()
        token = tokenizer.tokenize(raw)
        stop_remove_token = [word for word in token if word not in en_stop]
        # stem_token = [p_stemmer.stem(word) for word in stop_remove_token]
        tokens.append(stop_remove_token)
    # print tokens
    
    '''

    # 得到文档-单词矩阵 （直接利用统计词频得到特征）
    dictionary = corpora.Dictionary(tokens)   # 得到单词的ID,统计单词出现的次数以及统计信息
    # print dictionary.token2id         # 可以得到单词的id信息  <dict>
    # print type(dictionary)            # 得到的是gensim.corpora.dictionary.Dictionary的class类型

    texts = [dictionary.doc2bow(text) for text in tokens]    # 将dictionary转化为一个词袋，得到文档-单词矩阵

    # # 直接利用词频作为特征来进行处理
    # lda_model = models.ldamodel.LdaModel(texts, num_topics=3, id2word=dictionary,  passes=500)
    # print lda_model.print_topics(num_topics=3,num_words=4)
    # corpus_lda = lda_model[texts]
    # for doc in corpus_lda:
    #     print doc

    # 利用tf-idf来做为特征进行处理
    texts_tf_idf = models.TfidfModel(texts)[texts]     # 文档的tf-idf形式(训练加转换的模式)
    # # for text in texts_tf_idf:            # 逐行打印得到每篇文档的每个单词的TD-IDF的特征值
    # #     print text
    # lda_tf_idf = models.LdaModel(texts_tf_idf, num_topics=3, id2word=dictionary, update_every=0, passes=200)
    # print lda_tf_idf.print_topics(num_topics=3,num_words=4)
    # # doc_topic = [a for a in lda_tf_idf[texts_tf_idf]]
    # # for topic_id in range(3):
    # #     print "topic:{}".format(topic_id+1)
    # #     print lda_tf_idf.show_topic(topic_id)
    # corpus_lda_tfidf = lda_tf_idf[texts_tf_idf]
    # for doc in corpus_lda_tfidf:
    #     print doc


    # 利用LDA做主题分类的情况
    print("**************LDA*************")
    lda = models.ldamodel.LdaModel(corpus=texts, id2word=dictionary, num_topics=100,update_every=0,passes=20)
    lda.save("163news_lda")
    texts_lda = lda[texts_tf_idf]
    print(lda.print_topics(num_topics=100, num_words=10))
    
    '''
    for doc1 in texts_lda:
        print(doc1)
        print('\n')
    '''
    
    
    lovein_topic = []
    rec_df = pd.DataFrame(columns=['id','score'])
    
    #假设前10个是喜欢的文章
    for i in range(0,10):        
        for t in texts_lda[i]:
            if t[1] > 0.5 :
                lovein_topic.append(t[0])
        '''
        print(texts_lda[i])
        print('\n')
        '''
    
    for i in range(0,len(texts_lda)):
        rec_df.loc[i] = [i, 0]
        for tt in texts_lda[i]:
            print(tt)
            if tt[0] in lovein_topic:
                rec_df.loc[i]['score'] += tt[1]
                print(tt[1])
    df['score'] = rec_df['score']
    rec_df = rec_df.sort_index(axis = 0,ascending = True,by = 'score')  

    
    