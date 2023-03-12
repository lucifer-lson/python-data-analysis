"""
作者：Lucifer
日期：2023年03月02日
"""
import jieba.posseg as pseg
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt


def load_stopwords(path):
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()  # 取出所有行
    return [line.strip() for line in lines]  # 把每行的换行符去掉，追加到新的列表中


stopwords = load_stopwords("stop_words.txt")
ts = []
with open('weibo.txt', 'r', encoding='utf-8') as f:
    for line in f:  # 逐行读取
        for word, flag in pseg.cut(line.strip().split('\t')[1]):
            if (word not in stopwords) and (word != " "):
                ts.append([word, flag])


temp = []
tfreq = Counter(ts[i][1] for i in range(len(ts)))
for term in tfreq:
    temp.append([term, tfreq[term]])
freq_lis = sorted(temp, key=lambda x: x[1], reverse=True)
print(*freq_lis)

tf1 = Counter(ts[i][0] for i in range(len(ts)) if ts[i][1] == 'n')
tf2 = Counter(ts[i][0] for i in range(len(ts)) if ts[i][1] == 'a')

fpath = 'C:\Windows\Fonts\STLiti.ttf'
wd1 = WordCloud(font_path=fpath, max_words=1000, background_color='white', scale=32)
wd1.fit_words(tf1)
wd2 = WordCloud(font_path=fpath, max_words=1000, background_color='white', scale=32)
wd2.fit_words(tf2)
plt.figure(1)
plt.imshow(wd1, interpolation="bilinear")
plt.axis('off')
plt.figure(2)
plt.imshow(wd2, interpolation="bilinear")
plt.axis('off')
plt.show()