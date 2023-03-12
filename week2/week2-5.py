"""
作者：Lucifer
日期：2023年03月06日
"""
import jieba
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter


def load_stopwords(path):
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()  # 取出所有行
    return [line.strip() for line in lines]  # 把每行的换行符去掉，追加到新的列表中


stopwords = load_stopwords("stop_words.txt")
fpath = 'C:\Windows\Fonts\STLiti.ttf'
ts1 = []
with open('weibo5_1.txt', 'r', encoding='utf-8') as f1:
    for line in f1:  # 逐行读取
        for word in jieba.cut(line.strip().split('\t')[1]):
            if (word not in stopwords) and (word != " "):
                ts1.append(word)

temp1 = []
tfreq1 = Counter(ts1)

for term in tfreq1:
    temp1.append([term, tfreq1[term]])
freq_lis1 = sorted(temp1, key=lambda x: x[1], reverse=True)
freq1 = [x[0] for x in freq_lis1[:100]]

ts2 = []
with open('weibo5_2.txt', 'r', encoding='utf-8') as f2:
    for line in f2:  # 逐行读取
        for word in jieba.cut(line.strip().split('\t')[1]):
            if (word not in stopwords) and (word != " "):
                ts2.append(word)

temp2 = []
tfreq2 = Counter(ts2)

for term in tfreq2:
    temp2.append([term, tfreq2[term]])
freq_lis2 = sorted(temp2, key=lambda x: x[1], reverse=True)
freq2 = [x[0] for x in freq_lis2[:100]]

vectorizer = TfidfVectorizer()
vectorizer.fit(freq1 + freq2)
tfidf_0 = vectorizer.transform(freq1)
tfidf_1 = vectorizer.transform(freq2)
similarity_matrix = cosine_similarity(tfidf_0, tfidf_1)
print(similarity_matrix)