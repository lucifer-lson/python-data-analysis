"""
作者：Lucifer
日期：2023年03月16日
"""
from sklearn.feature_extraction.text import CountVectorizer


def get_feature(final_text: dict):
    """
    获得文档的词频矩阵（输出并返回）
    """
    docs = []
    for item in final_text.values():
        docs.append(item)
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(docs)
    print(f'词频矩阵:\n{X.toarray()}')
    return X, vectorizer, docs

