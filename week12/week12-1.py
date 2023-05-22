"""
作者：Lucifer
日期：2023年05月21日
"""
from threading import Thread,currentThread
import requests
from lxml import etree
from tqdm import tqdm
import re
import queue
import librosa
import time


class GetWeblink(Thread):
    """
    抽取页面链接
    1. https://www.51voa.com/VOA_Standard_3.html 从这类页面上抽取一个一个的链接
    """
    def __init__(self, name, q):
        super().__init__()
        self._name = name
        self._queue = q

    def run(self):
        links = []
        for i in tqdm(range(3, 4)):
            url = f'https://www.51voa.com/VOA_Standard_{i}.html'  # 翻页
            response = requests.get(url)
            html = etree.HTML(response.text)
            for j in range(0, 50):
                links = links + html.xpath('//*[@id="righter"]/div[3]/ul/li[%s]/a/@href' % str(j))
        # print(len(links), links[:10])
        for link in tqdm(links):
            self._queue.put(link)


class GetMp3link(Thread):
    """
    分析并得到mp3的链接
    2. https://www.51voa.com/VOA_Standard_English/u-s-supports-diversity-of-energy-sources-in-europe-79541.html 从这类页面上，抽取mp3的那个链接。
    """
    def __init__(self, name, get_q, put_q):
        super().__init__()
        self._name = name
        self._web_queue = get_q
        self._mp3_queue = put_q

    def run(self):
        time.sleep(2)
        # counter1 = 0
        while True:
            if self._web_queue.empty():
                print("all tasks in weblink_q had been done.")
                break
            # print(f"thread {currentThread().name} {counter1} is working...\n")
            # counter1 += 1
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/78.0.3904.97 Safari/537.36 '
            }
            mlist = []
            link = self._web_queue.get()
            url = 'https://www.51voa.com' + link
            # print(url)
            response = requests.get(url, headers=headers)
            mlist = mlist + list(set(re.findall(r'https://.+?\.mp3', response.text)))
            # print(len(mlist), mlist[:10])
            for m in mlist:
                self._mp3_queue.put(m)


class SaveMp3(Thread):
    """
    保存mp3文件至路径
    """
    def __init__(self, name, get_q, put_q):
        super().__init__()
        self._name = name
        self._mp3_queue = get_q
        self._sry_queue = put_q

    def run(self):
        time.sleep(3)
        # counter2 = 0
        while True:
            if self._mp3_queue.empty():
                print("all tasks in mp3link_q had been done.")
                break
            # print(f"thread {currentThread().name} {counter2} is working...\n")
            # counter2 += 1
            # 下载mp3文件
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/78.0.3904.97 Safari/537.36 '
            }
            murl = self._mp3_queue.get()
            # print(murl)
            mp3_stream = requests.get(murl, headers=headers).content
            fname = murl[murl.rfind('/') + 1:]
            # print(fname)
            with open(fname, 'wb') as f:
                f.write(mp3_stream)
            y, sr = librosa.load(fname, sr=None)
            self._sry_queue.put((y, sr, fname))


class Calculate_speechrate(Thread):
    """
    计算语速并输出
    """
    def __init__(self, name, get_q):
        super().__init__()
        self._name = name
        self._sry_queue = get_q

    def run(self):
        time.sleep(20)
        # counter3 = 0
        while True:
            if self._sry_queue.empty():
                print("all tasks in sry_q had been done.")
                break
            # print(f"thread {currentThread().name} {counter3} is working...\n")
            # counter3 += 1
            y, sr, fname = self._sry_queue.get()
            onsets = librosa.onset.onset_detect(y=y, sr=sr, units="time", hop_length=128, backtrack=False)
            number_of_words = len(onsets)
            duration = len(y) / sr
            words_per_second = number_of_words / duration
            print(f'words-per-second of {fname}: {words_per_second}')


if __name__ == "__main__":
    # 创建队列
    weblink_q = queue.Queue()
    mp3link_q = queue.Queue()
    sry_q = queue.Queue()
    # 创建线程
    get_web_link = GetWeblink('get_web_link', weblink_q)
    get_mp3_link = GetMp3link('get_mp3_link', weblink_q, mp3link_q)
    save_mp3 = SaveMp3('save_mp3', mp3link_q, sry_q)
    cal_mp3 = Calculate_speechrate('cal_mp3', sry_q)
    thread_list = [get_web_link, get_mp3_link, save_mp3, cal_mp3]
    for thread in thread_list:
        thread.start()
    for thread in thread_list:
        thread.join()





