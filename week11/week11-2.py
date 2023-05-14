"""
作者：Lucifer
日期：2023年05月14日
"""
import os
import librosa
from multiprocessing import Process, Queue
import numpy as np


def calculate_music(q1, q2, path):
    while not q1.empty():
        mus = q1.get()
        # 加载音频
        y, sr = librosa.load(path + '\\' + mus)
        # 求音高
        pitch = librosa.yin(y, fmin=librosa.note_to_hz('C1'), fmax=librosa.note_to_hz('C7'))
        # 求声强
        sdb = librosa.amplitude_to_db(librosa.feature.rms(y=y), ref=0.00002)
        q2.put((mus, pitch, sdb))
        print(f'{mus} has been loaded and calculated by {os.getpid()}.')


def write_to_txt(q):
    with open('result.txt', 'a') as f:
        while True:
            # 从队列中获取结果
            result = q.get()
            if result is None:
                break
            filename, pitch, sdb = result
            # 将结果写入文件
            f.write(filename + '\npitch:\n')
            np.savetxt(f, pitch, delimiter=',')
            f.write('\nsdb:\n')
            np.savetxt(f, sdb, delimiter=',')


if __name__ == "__main__":
    q1 = Queue()  # 存储待处理文件的队列
    q2 = Queue()
    path = 'D:\\PycharmProjects\\python_2023\\week11\\music'
    filename = os.listdir(path)
    for file in filename:
        q1.put(file)
    p1_list = []  # 存储计算子进程
    p2_list = []  # 存储写入子进程
    for i in range(5):
        p = Process(target=calculate_music, args=(q1, q2, path))  # 用于计算的子进程
        p1_list.append(p)
    for j in range(5):
        p = Process(target=write_to_txt, args=(q2, ))  # 用于写入的子进程
        p2_list.append(p)

    for p in p1_list:
        p.start()
    for p in p2_list:
        p.start()
    for p in p1_list:
        p.join()
    q1.put(None)
    for p in p2_list:
        p.join()
    end = time.time()

