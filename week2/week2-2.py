"""
作者：Lucifer
日期：2023年03月02日
"""
import jieba
import jieba.posseg as pseg
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt


def load_stopwords(path):
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()  # 取出所有行
    return [line.strip() for line in lines]  # 把每行的换行符去掉，追加到新的列表中


stopwords = load_stopwords("stop_words.txt")
fpath = 'C:\Windows\Fonts\STLiti.ttf'
ts = []
with open('weibo.txt', 'r', encoding='utf-8') as f:
    for line in f:  # 逐行读取
        for word in jieba.cut(line.strip().split('\t')[1]):
            if (word not in stopwords) and (word != " "):
                ts.append(word)

temp = []
tfreq = Counter(ts)
for term in tfreq:
    temp.append([term, tfreq[term]])
freq_lis = sorted(temp, key=lambda x: x[1], reverse=True)

f3 = open('result2.txt', 'w', encoding='utf-8')
for item in freq_lis:
    f3.write("%s %d\n" % (item[0], item[1]))

f3.close()
wd = WordCloud(font_path=fpath, max_words=1000, background_color='white', scale=32)
wd.fit_words(tfreq)
plt.imshow(wd, interpolation="bilinear")
plt.axis('off')
plt.show()