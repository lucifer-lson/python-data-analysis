"""
作者：Lucifer
日期：2023年05月12日
"""
import os
import librosa
from multiprocessing import Process, Queue
import numpy as np
import time


def calculate_music(q, path):
    while not q.empty():
        mus = q.get()
        # 加载音频
        y, sr = librosa.load(path + '\\' + mus)
        # 求音高
        pitch = librosa.yin(y, fmin=librosa.note_to_hz('C1'), fmax=librosa.note_to_hz('C7'))
        # 求声强
        sdb = librosa.amplitude_to_db(librosa.feature.rms(y=y), ref=0.00002)
        with open(os.path.splitext(mus)[0]+'.txt', 'w') as f:
            np.savetxt(f, pitch, delimiter=',')
            f.write('\n')
            np.savetxt(f, sdb, delimiter=',')
        print(f'{mus} has been loaded and calculated by {os.getpid()}.')


class Myprocess(Process):
    def __init__(self, q, path):
        super().__init__()
        self.queue = q
        self.path = path

    def run(self):
        calculate_music(self.queue, self.path)


if __name__ == "__main__":
    q = Queue()
    path = 'D:\\PycharmProjects\\python_2023\\week11\\music'
    filename = os.listdir(path)
    for file in filename:
        q.put(file)
    p_list = []

    for i in range(2):  # 直接使用Process类创建子进程
        p = Process(target=calculate_music, args=(q, path))
        p_list.append(p)
    for i in range(2, 9):  # 通过继承Process类创建子进程
        p = Myprocess(q, path)
        p_list.append(p)

    start = time.time()
    for p in p_list:
        p.start()
    for p in p_list:
        p.join()
    end = time.time()
    print('All processes end.')
    print(f'time: {end-start}')

