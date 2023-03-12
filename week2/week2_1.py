"""
作者：Lucifer
日期：2023年02月28日
"""
import jieba
import jieba.posseg as pseg
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt


def deal_noise(txt):  # 初步清除一段文本的噪音
    for ch in '[ ]，。！？+-@~#$&（）；：《》“”-_*!"%(),./:;<=>?[\\]^‘{|}～、':
        txt = txt.replace(ch, ' ')  # 将文本中的特殊字符替换为空格
    return txt


f2 = open('new_weibo.txt', 'w', encoding='utf-8')
with open('weibo.txt', 'r+', encoding='utf-8') as f1:
    for line in f1:  # 逐行读取
        new_line = deal_noise(line)
        f2.write(new_line)

f2.close()
fpath = 'C:\Windows\Fonts\simfang.ttf'
ts = []
with open('new_weibo.txt', 'r', encoding='utf-8') as f:
    for line in f:  # 逐行读取
        for word in jieba.cut(line.strip().split('\t')[1]):
            if word != ' ':
                ts.append(word)

temp = []
tfreq = Counter(ts)
for term in tfreq:
    temp.append([term, tfreq[term]])
freq_lis = sorted(temp, key=lambda x: x[1], reverse=True)

f3 = open('result1.txt', 'w', encoding='utf-8')
for item in freq_lis:
    f3.write("%s %d\n" % (item[0], item[1]))

f3.close()
# wd = WordCloud(font_path=fpath, max_words=1000)
# wd.fit_words(tfreq)
# plt.imshow(wd, interpolation="bilinear")
# plt.axis('off')
# plt.show()

