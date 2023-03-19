"""
作者：Lucifer
日期：2023年03月17日
"""
import pyLDAvis
import pyLDAvis.sklearn


def visualize(lda, X, vectorizer):
    """
    对lda模型进行可视化
    """
    data = pyLDAvis.sklearn.prepare(lda, X, vectorizer)
    pyLDAvis.show(data)
    return 0
