"""
作者：Lucifer
日期：2023年03月17日
"""
import pickle
import matplotlib.pyplot as plt
from sklearn.decomposition import LatentDirichletAllocation
import sort_text, preprocess_text, feature_text, analysis_text, visualization_lda


if __name__ == "__main__":
    text_dic = sort_text.sort('weibo.txt')
    s = preprocess_text.preprocess(text_dic, 'stop_words.txt')
    # 输出词频矩阵
    X, vectorizer, docs = feature_text.get_feature(s)
    # 输出主题词语、主题概率分布
    time, percent = analysis_text.topic_analysis(X, vectorizer, docs, s)
    # 计算困惑度绘制elbow图确定主题数量
    plt.figure(1)
    perplexity_scores = []
    k_range = range(1, 11)  # 假设k的范围是1到10
    for k in k_range:
        lda = LatentDirichletAllocation(n_components=k)
        lda.fit(X)
        perplexity_scores.append(lda.perplexity(X))
    plt.plot(k_range, perplexity_scores, '-o')
    plt.xlabel('Number of topics')
    plt.ylabel('Perplexity')
    plt.show()

    # 观察某话题随时间的变化趋势(以topic1为例)
    plt.figure(2)
    plt.plot(time[:25], percent[:25], '-')
    plt.xlabel('Time')
    plt.ylabel('Percent of topic1 in docs')
    plt.show()

    with open('lda_model.pkl', 'rb') as f:
        lda = pickle.load(f)[0]
    # 可视化lda模型
    visualization_lda.visualize(lda, X, vectorizer)