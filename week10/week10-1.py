"""
作者：Lucifer
日期：2023年04月27日
"""
import abc
import jieba
import librosa.display
import numpy as np
from matplotlib import pyplot as plt
from collections import Counter
from wordcloud import WordCloud
from PIL import Image


class Plotter(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def plot(self, data, *args, **kwargs):
        pass


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class PointPlotter(Plotter):
    """
    实现数据点型数据的绘制（散点图），data=[(x1,y1), (x2,y2),...]
    """
    def plot(self, data, *args, **kwargs):
        x_list = [p.x for p in data]
        y_list = [p.y for p in data]
        plt.scatter(x_list, y_list)
        plt.show()


class ArrayPlotter(Plotter):
    """
    实现多维数组型数据的绘制,data = [[x1,x2,...], [y1,y2,...], [z1,z2,...]]
    """
    def plot(self, data, *args, **kwargs):
        if len(data) == 2:
            plt.scatter(data[0], data[1])
            plt.show()
        elif len(data) == 3:
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.scatter(data[0], data[1], data[2])
            plt.show()


class TextPlotter(Plotter):
    """
    实现文本型数据的绘制(词云图),data='*.txt'
    """
    def __init__(self):
        self.stop_words = 'stop_words.txt'

    @staticmethod
    def load_txt(path):  # 加载文件
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
        return text

    def get_clear_text(self, text):  # 对文本进行停用词清除
        ts = []
        for word in jieba.lcut(text):
            if (word not in TextPlotter.load_txt(self.stop_words)) and (word != ' '):
                ts.append(word)
        return ts

    def plot(self, data, *args, **kwargs):
        fpath = 'C:\Windows\Fonts\STLiti.ttf'
        text = TextPlotter.load_txt(data)
        ts = self.get_clear_text(text)
        tfreq = Counter(ts)
        wd = WordCloud(font_path=fpath, max_words=1000, background_color='white', scale=32)
        wd.fit_words(tfreq)
        plt.imshow(wd, interpolation="bilinear")
        plt.axis('off')
        plt.show()


class ImagePlotter(Plotter):
    """
    实现图片型数据的绘制,data=[图片1路径, 图片2路径,...]
    """
    def __init__(self, layout):  # layout = (row, col)
        self.layout = layout
        self.images = []

    def add_to_images(self, image):
        if isinstance(image, str):
            image = Image.open(image)
        self.images.append(image)

    def plot(self, data, *args, **kwargs):
        for item in data:
            self.add_to_images(item)
        plt.figure()
        row, col = self.layout[0], self.layout[1]
        for i in range(row * col):
            plt.subplot(row, col, i + 1)
            plt.imshow(self.images[i])
            plt.axis('off')
        plt.show()


class MusicPlotter(Plotter):
    """
    实现音频录入并绘制时间点对应的幅度图及能谱图，data='*.mp3'
    """
    def plot(self, data, *args, **kwargs):
        y, sr = librosa.load(data)
        print(f'sampling rate:{sr}')
        print(f'sound time series shape:{y.shape}')

        plt.figure()
        plt.plot(y[:5000])
        plt.show()
        # 能谱图
        fig, ax = plt.subplots(nrows=2, ncols=1, sharex=True)
        D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
        img = librosa.display.specshow(D, y_axis='linear', x_axis='time', sr=sr, ax=ax[0])
        ax[0].set(title='Linear-frequency power spectrogram')
        ax[0].label_outer()

        hop_length = 1024
        D2 = librosa.amplitude_to_db(np.abs(librosa.stft(y, hop_length=hop_length)), ref=np.max)
        librosa.display.specshow(D2, y_axis='log', sr=sr, hop_length=hop_length, x_axis='time', ax=ax[1])
        ax[1].set(title='Log-frequency power spectrogram')
        ax[1].label_outer()
        fig.colorbar(img, ax=ax, format="%+2.f dB")
        plt.show()


if __name__ == "__main__":

    # 测试PointPlotter
    p1, p2, p3, p4, p5, p6 = Point(1,2), Point(3,9), Point(2,4), Point(1,7), Point(9,4), Point(3,3)
    p_list = [p1, p2, p3, p4, p5, p6]
    test1 = PointPlotter()
    test1.plot(p_list)
    
    # 测试ArrayPlotter
    array1 = [[1, 3, 8, 5, 2], [4, 5, 2, 7, 9]]
    array2 = [[1, 3, 8, 5, 2], [4, 5, 2, 7, 9], [3, 1, 5, 2, 1]]
    test2 = ArrayPlotter()
    test2.plot(array1)
    test2.plot(array2)

    # 测试TextPlotter
    test3 = TextPlotter()
    test3.plot('passage.txt')

    # 测试ImagePlotter
    test4 = ImagePlotter((2, 3))
    test4.plot(['0001.jpg', '0002.jpg', '0003.jpg', '0004.jpg', '0005.jpg', '0006.jpg'])

    # 测试MusicPlotter
    test5 = MusicPlotter()
    test5.plot('Surprising Thanks.mp3')

