"""
作者：Lucifer
日期：2023年04月11日
"""
import os
import cv2 as cv
import matplotlib.pyplot as plt
from functools import wraps


class TestDecorator:
    """
    用于测试类装饰器calculation的类
    """
    def __init__(self):
        self._image = None
        self._processed_image = None  # 一个列表，存放处理后的图片

    def open(self, in_path):  # 打开图片
        self._image = cv.imread(in_path)

    def save(self, out_path):  # 保存图片
        for i in range(len(self._processed_image)):
            cv.imwrite(out_path+'\\\\im'+str(i+1)+'.jpg', self._processed_image[i])

    def set_processedlist(self, list):  # 设置存放处理后图片的列表
        self._processed_image = list

    def resize(self):  # 调整图片大小
        height, width = self._image.shape[:2]
        im = self._image[int(0.25*width):int(0.75*width), int(0.25*height):int(0.75*height)]
        cropped_image = cv.cvtColor(im, cv.COLOR_BGR2RGB)
        return cropped_image

    def retate(self):  # 旋转图片
        rows, cols, channel = self._image.shape[:3]
        M = cv.getRotationMatrix2D((cols / 2, rows / 2), -45, 1)
        im = cv.warpAffine(self._image, M, (cols, rows))
        rotated_image = cv.cvtColor(im, cv.COLOR_BGR2RGB)
        return rotated_image

    def edge_extraction(self):  # 提取边缘
        blurred = cv.GaussianBlur(self._image, (11, 11), 0)  # 高斯矩阵的长与宽都是11，标准差为0
        gaussImg = cv.Canny(blurred, 10, 70)
        edged_image = cv.cvtColor(gaussImg, cv.COLOR_BGR2RGB)
        return edged_image


class calculation:
    """
    装饰器，用于打印处理前图片的大小、亮度、饱和度
    """
    def __init__(self):
        print("inside calculation.")

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):  # args = [path]
            image = cv.imread(args[0])
            # 计算图像大小
            height, width, channels = image.shape
            print(f"原始图像大小：{width} x {height}")

            # 将图像转换为HSV颜色空间
            hsv_img = cv.cvtColor(image, cv.COLOR_BGR2HSV)
            hue, saturation, value = cv.split(hsv_img)

            # 计算亮度的平均值
            mean_value = cv.mean(value)[0]
            print(f"原始图像亮度平均值：{mean_value}")

            # 计算饱和度的平均值
            mean_saturation = cv.mean(saturation)[0]
            print(f"原始图像饱和度平均值：{mean_saturation}")

            return func(*args, **kwargs)
        return wrapper


def PathCheck(func):
    """
    装饰器，用于检查func函数中所用路径是否存在，并在不存在的情况下创建该目录
    :param func: 要装饰的函数
    """
    def wrapper(*args, **kwargs):
        out_path = args[1]
        if os.path.exists(out_path):
            return func(*args, **kwargs)
        else:
            print(f"Warn: The directory {out_path} does not exist. It will be created now.")
            os.mkdir(out_path)
            return func(*args, **kwargs)
    return wrapper


if __name__ == "__main__":
    @calculation()
    @PathCheck
    def ImageProcess(image_path, out_path):
        ex = TestDecorator()
        ex.open(image_path)
        im1 = ex.resize()
        im2 = ex.retate()
        im3 = ex.edge_extraction()
        im = [im1, im2, im3]
        ex.set_processedlist(im)
        ex.save(out_path)  # 'D:\\PycharmProjects\\python_2023\\week8\\processed'
        plt.figure()
        for i in range(3):
            plt.subplot(1, 3, i + 1)
            plt.imshow(im[i])
            plt.axis('off')
        plt.show()

    ImageProcess('test.jpg', 'D:\\PycharmProjects\\python_2023\\week8\\processed2')

