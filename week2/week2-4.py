"""
作者：Lucifer
日期：2023年03月05日
"""
import jieba
from nltk import bigrams
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
f3 = open('weibo3.txt', 'w', encoding='utf-8')

# 过滤停用词
with open('weibo.txt', 'r', encoding='utf-8') as f:
    for line in f:  # 逐行读取
            for word in jieba.cut(line.strip().split('\t')[1]):
                if (word not in stopwords) and (word != " "):
                    f3.write(word)
            f3.write('\n')

with open('weibo3.txt', 'r', encoding='utf-8') as f3:
    text = f3.read()

# 得到bigram的元组
tokens = tuple(jieba.cut(text))
bgs = list(bigrams(tokens))
temp_bgs = []
for i in range(len(bgs)):
    if bgs[i][0] != '\n' and bgs[i][1] != '\n':
        temp_bgs.append('('+bgs[i][0]+','+bgs[i][1]+')')

tfreq = Counter(temp_bgs)
temp = []
for term in tfreq:
    temp.append([term, tfreq[term]])
freq_lis = sorted(temp, key=lambda x: x[1], reverse=True)

f3 = open('result4.txt', 'w', encoding='utf-8')
for item in freq_lis:
    f3.write("%s %d\n" % (item[0], item[1]))

wd = WordCloud(font_path=fpath, max_words=1000, background_color='white', scale=32)
wd.fit_words(tfreq)
plt.imshow(wd, interpolation="bilinear")
plt.axis('off')
plt.show()