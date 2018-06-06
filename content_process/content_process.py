import pandas as pd
import re
import jieba
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
    df = pd.read_csv("pengpainews.csv", encoding='gb18030')
    print(df.head())
    print('\n')
    '''
    print(df.shape)
    print('\n')
    print(type(df.content))
    print("\n")
    '''

    #去除文本中的标签
    dr = re.compile(r'<[^>]+>', re.S)
    for i in range(0, len(df.content)):
        df.content[i] = dr.sub('', df.content[i])
        print(df.content[i])

    #进行分词
    df["content_cutted"] = df.content.apply(chinese_word_cut)

    # 从文件导入停用词表
    stpwrdpath = "stop_words.txt"
    stpwrd_dic = open(stpwrdpath, 'rb')
    stpwrd_content = stpwrd_dic.read()
    # 将停用词表转换为list
    stpwrdlst = stpwrd_content.splitlines()
    stpwrd_dic.close()

    #将文本向量化
    n_features = 500
    tf_vectorizer = TfidfVectorizer(strip_accents = 'unicode',

                                    max_features=n_features,

                                    stop_words=stpwrdlst,

                                    max_df = 0.5,

                                    min_df = 3)

    tf = tf_vectorizer.fit_transform(df.content_cutted)


    #用LDA进行主题分析
    n_topics = 20
    lda = LatentDirichletAllocation(n_components=n_topics, max_iter=5000,

                                    learning_method='online',

                                    learning_offset=5.,

                                    random_state=0)
    lda.fit(tf)

    n_top_words = 20
    tf_feature_names = tf_vectorizer.get_feature_names()
    print(tf_feature_names)
    print_top_words(lda, tf_feature_names, n_top_words)




    '''
    model = lda.LDA(n_topics=20, n_iter=1500, random_state=1)  # 设置topic的数量是20，定义模型

    model.fit(tf_vectorizer)  # 训练模型

    topic_word = model.topic_word_  # topic到word的模型，（20,4258）的权重矩阵

    n_top_words = 8

    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(df.content_cutted)[np.argsort(topic_dist)][:-(n_top_words + 1):-1]  # 找到topic对应的前8个最重要的单词
        print('Topic {}: {}'.format(i, ' '.join(topic_words)))
        
    '''