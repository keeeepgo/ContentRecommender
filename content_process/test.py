import pandas as pd
import re
import jieba
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from gensim import corpora, models, similarities
from pprint import pprint
import time


def chinese_word_cut(mytext):
    return " ".join(jieba.cut(mytext))


def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)

        print(" ".join([feature_names[i]

                        for i in topic.argsort()[:-n_top_words - 1:-1]]))

    print()


if __name__ == '__main__':

    # 读入文件，并输出前5行
    df = pd.read_csv("pengpainews.csv", encoding='gb18030')
    print(df.head())
    print('\n')
    '''
    print(df.shape)
    print('\n')
    print(type(df.content))
    print("\n")
    '''

    # 去除文本中的标签
    dr = re.compile(r'<[^>]+>', re.S)
    for i in range(0, len(df.content)):
        df.content[i] = dr.sub('', df.content[i])
        print(df.content[i])


    #进行分词
    df["content_cutted"] = df.content.apply(chinese_word_cut)
    print(type(df.content_cutted))


    #将文本向量化
    n_features = 1000
    tf_vectorizer = CountVectorizer(strip_accents = 'unicode',

                                    max_features=n_features,

                                    stop_words='english',

                                    max_df = 0.5,

                                    min_df = 10)

    tf = tf_vectorizer.fit_transform(df.content_cutted)

    texts = df.content
    print ('读入语料数据完成' )
    M = len(texts)
    print ('文本数目：%d个' % M)



    print('6.LDA模型拟合推断 ------')
    # 训练模型
    num_topics = 30
    t_start = time.time()
    lda = models.LdaModel(tf, num_topics=num_topics,
                            alpha=0.01, eta=0.01, minimum_probability=0.001,
                            update_every = 1, chunksize = 100, passes = 1)
    print('LDA模型完成，训练时间为\t%.3f秒' % (time.time() - t_start))

    # 随机打印某10个文档的主题
    num_show_topic = 10  # 每个文档显示前几个主题
    print('7.结果：10个文档的主题分布：--')
    doc_topics = lda.get_document_topics(tf)  # 所有文档的主题分布
    idx = np.arange(M)
    np.random.shuffle(idx)
    idx = idx[:10]
    for i in idx:
        topic = np.array(doc_topics[i])
        topic_distribute = np.array(topic[:, 1])
        # print topic_distribute
        topic_idx = topic_distribute.argsort()[:-num_show_topic-1:-1]
        print( ('第%d个文档的前%d个主题：' % (i, num_show_topic)), topic_idx)
        print (topic_distribute[topic_idx])

    num_show_term = 7   # 每个主题显示几个词
    print( '8.结果：每个主题的词分布：--')
    for topic_id in range(num_topics):
        print ('主题#%d：\t' % topic_id)
        term_distribute_all = lda.get_topic_terms(topicid=topic_id)
        term_distribute = term_distribute_all[:num_show_term]
        term_distribute = np.array(term_distribute)
        term_id = term_distribute[:, 0].astype(np.int)
        print ('词：\t',)

        print ('\n概率：\t', term_distribute[:, 1])

