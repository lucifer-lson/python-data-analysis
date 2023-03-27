"""
作者：Lucifer
日期：2023年03月23日
"""
import jieba
from sklearn.manifold import TSNE
from gensim.models import Word2Vec
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

Kaiti = FontProperties(fname='C:\Windows\Fonts\simkai.ttf')
import numpy as np


class TextAnalyzer:
    stop_lis = []
    with open('stop_words.txt', 'r', encoding='utf-8') as f:
        for line in f:
            stop_lis.append(line)
    stop_set = set(stop_lis)

    def __init__(self, text_path, model_path, vector_size, window=5):
        self.text_path = text_path
        self.model_path = model_path
        self.vector_size = vector_size
        self.window = window
        self.model = self.train_model()

    def preprocess(self):
        sentences = []
        with open(self.text_path, 'r', encoding='utf-8') as f:
            for line in f:
                sen = [w for w in jieba.cut(line.strip().split('\t')[1]) if w not in TextAnalyzer.stop_set]
                sentences.append(sen)
        return sentences

    def train_model(self):
        self.model = Word2Vec(sentences=self.preprocess(), vector_size=self.vector_size, window=self.window, min_count=1)
        return self.model

    def deduce_synonym(self, word):
        most_similar = self.model.wv.most_similar(word, topn=10)
        least_similar = self.model.wv.most_similar(negative=[word], topn=10)
        return most_similar, least_similar

    def load_model(self, word):
        model = Word2Vec.load(self.model_path)
        similar_premodel = model.wv.most_similar(word, topn=10)
        return similar_premodel

    def print_similarity(self, word):
        most_similar, least_similar = self.deduce_synonym(word)
        similar_premodel = self.load_model(word)
        print(f"训练后模型得到的10个与”{word}“相似的词语:")
        for i in range(10):
            print(most_similar[i][0], end=" ")
        print()
        print(f"预训练模型得到的10个与“{word}”相似的词语:")
        for i in range(10):
            print(similar_premodel[i][0], end=" ")
        print()

    def expand_emodict(self):
        anger_p = 'anger.txt'
        disgust_p = 'disgust.txt'
        fear_p = 'fear.txt'
        joy_p = 'joy.txt'
        sadness_p = 'sadness.txt'
        path_list = [anger_p, disgust_p, fear_p, joy_p, sadness_p]
        word_list = []
        all_word = [i for item in self.preprocess() for i in item]
        for i in range(len(path_list)):
            temp = []
            with open(path_list[i], 'r', encoding='utf-8') as f:
                text = f.read().splitlines()
                for j in text:
                    if j in all_word:
                        positive, negative = self.deduce_synonym(j)
                        temp.append(j)
                        temp.extend(positive[i][0] for i in range(5))
            word_list.append(temp)
        for i in range(len(path_list)):
            with open(path_list[i], 'a', encoding='utf-8') as f:
                for word in word_list[i]:
                    f.write('\n'+word)

    def visualization(self, word):
        positive, negative = self.deduce_synonym(word)
        vectors = np.array([self.model.wv[words] for words, similarity in positive + negative])
        words = [word for word, similarity in positive + negative]
        # 使用t-SNE算法对词向量进行降维
        tsne = TSNE(n_components=2, perplexity=10)
        vectors_tsne = tsne.fit_transform(vectors)

        # 可视化降维后的词向量
        fig, ax = plt.subplots()
        ax.set_title(word, fontproperties=Kaiti)
        ax.scatter(vectors_tsne[:10, 0], vectors_tsne[:10, 1], color='blue')
        ax.scatter(vectors_tsne[10:, 0], vectors_tsne[10:, 1], color='red')
        for i, word in enumerate(words):
            ax.annotate(word, (vectors_tsne[i, 0], vectors_tsne[i, 1]), fontproperties=Kaiti, fontsize=18)
        plt.show()


if __name__ == "__main__":
    print("Enter the word :\n")
    word = input()
    textAnalyzer = TextAnalyzer('weibo.txt', 'weibo_59g_embedding_200.model', vector_size=300)
    textAnalyzer.print_similarity(word)
    textAnalyzer.visualization(word)
    textAnalyzer.expand_emodict()