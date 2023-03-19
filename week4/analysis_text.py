"""
作者：Lucifer
日期：2023年03月17日
"""
from sklearn.decomposition import LatentDirichletAllocation
import pickle


def topic_analysis(X, vectorizer, docs, text_dic: dict):
    """
    构建lda模型，进行主题分析（查看主题词语及主题概率分布）
    """
    k = 4
    # 使用LatentDirichletAllocation构建主题模型
    lda = LatentDirichletAllocation(n_components=k, random_state=1)
    lda.fit(X)

    # 输出每个主题对应的词语
    feature_names = vectorizer.get_feature_names_out()  # 低版本sklearn是get_feature_names
    for i, topic in enumerate(lda.components_, start=1):
        print(f"Topic {i}:")
        top_words = [feature_names[j] for j in topic.argsort()[:-6:-1]]
        print(top_words)

    # 输出每篇文档的主题概率分布
    time = []
    percent = []
    for i in range(len(docs)):
        print(f"Document {i+1} ({str(list(text_dic.keys())[i])}):")
        time.append(str(list(text_dic.keys())[i]))
        print(lda.transform(X[i]))
        percent.append(lda.transform(X[i])[0].tolist()[0])

    # 序列化保存lda模型、词频矩阵、特征表示
    pickle.dump((lda, X, vectorizer), open('./lda_model.pkl', 'wb'))

    return time, percent
