"""
作者：Lucifer
日期：2023年03月16日
"""
import jieba


def load_stopwords(stopwords_path):
    """
    加载停用词表
    """
    with open(stopwords_path, 'r', encoding='utf-8') as f:
        stop_words = f.read()

    def clear_stopwords(sentence):
        """
        清除句中停用词，并将分词后的词语用' '连接为字符串
        """
        nonlocal stop_words
        text = []
        for word in jieba.lcut(sentence):
            if word not in stop_words:
                text.append(word)
        res = ' '.join(text)
        return res
    return clear_stopwords


def preprocess(text_dic: dict, stopwords_path):
    """
    对文本进行预处理（分词、去除停用词、连接为新字符串）
    """
    for item in text_dic.keys():
        temp_str = ''
        for sentence in text_dic[item]:
            temp = load_stopwords(stopwords_path)
            word_str = temp(sentence)
            temp_str = temp_str + ' ' + word_str
        text_dic[item] = temp_str.strip()
    return text_dic


if __name__ == "__main__":
    import sort_text
    from sklearn.feature_extraction.text import CountVectorizer
    text_dic = sort_text.sort('weibo.txt')
    s = preprocess(text_dic, 'stop_words.txt', 'weibo2.txt')

    docs = []
    for item in s.values():
        docs.append(item)

    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(docs)
    print(X.toarray())
    print(vectorizer.get_feature_names_out())
    print(vectorizer)
