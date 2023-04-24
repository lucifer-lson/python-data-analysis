"""
作者：Lucifer
日期：2023年04月22日
"""
from PIL import Image
import numpy as np
import os


class FaceDataset:
    """
    图片数据的加载
    """
    def __init__(self, path):
        self._path = path
        self._imagelist = os.listdir(self._path)
        self._index = 0
        self._arraylist = []

    def load_images(self, image_path):
        """
        打开图片并返回其nparray形式
        :param image_path: 图片路径
        :return: 图片的nparray形式
        """
        image = Image.open(os.path.join(self._path, image_path))
        return np.array(image)

    def image_generator(self):
        """
        生成器函数，不断生成图片的nparray形式
        """
        for image in self._imagelist:
            yield self.load_images(os.path.join(self._path, image))

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self._imagelist):
            image = self._imagelist[self._index]
            self._index += 1
            return self.load_images(os.path.join(self._path, image))
        else:
            raise StopIteration('out of list index.')

    def __len__(self):
        return len(self._imagelist)

    def __getitem__(self, index):
        if index < len(self._imagelist):
            return self.load_images(os.path.join(self._path, self._imagelist[index]))
        else:
            raise IndexError('index out of range.')


if __name__ == "__main__":
    fd = FaceDataset('D:\\PycharmProjects\\python_2023\\week9\\originalPics\\2003\\07\\18\\big')
    # 迭代器方式遍历图片并输出它的shape (高度，宽度，颜色通道)
    print("迭代器:")
    for image in fd:
        print(image.shape)
    # 生成器方式遍历图片并输出它的shape
    print("生成器:")
    for image in fd.image_generator():
        print(image.shape)
    # 利用__getitem__获取第i个图片的ndarray形式，并输出它的shape
    print("让类像列表一样索引:")
    image = fd[6]
    print(image.shape)
    # 获取数据集中图片的数量
    print(f"The amount of pictures:{len(fd)}")

