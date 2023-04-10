"""
作者：Lucifer
日期：2023年04月08日
"""
import os
import PIL
from PIL import Image
import imagehash
from scipy.stats import pearsonr, spearmanr, kendalltau
import traceback
import matplotlib.pyplot as plt
import time
import sys


class ImageQueryError(Exception):
    """
    自定义ImageQuery类里出现的异常基类
    """
    def __init__(self, image):
        self.image = image


class ImageQueryShapeNotMatchError(ImageQueryError):
    """
    pixel_difference类中，尺寸不同的图片无法相减的错误
    """
    def __init__(self, image_name, image2_name):
        self.image = image_name
        self.image2 = image2_name
        self.image_info = Image.open(self.image)
        self.image2_info = Image.open(self.image2)
        self.message = "Error: The dimensions of {} and {} do not match\nimage1:{}\nimage:{}".format(self.image,
                                                                self.image2, self.image_info, self.image2_info)


class ImageQueryNoSimilarImageFoundError(ImageQueryError):
    """
    目标图片与待匹配目录中所有图片都未达到一定相似度的错误
    """
    def __init__(self):
        self.message = "Error: There is no image similar to this one."


class ImageQuery:
    """
    求图片相似度的类
    """
    def __init__(self, path):
        self.path = path
        self.image = self._create_and_image(self.path)

    @staticmethod  # 可以在类外不创建实例的情况下调用的静态方法
    def _create_and_image(image_path):
        """
        加载图片并返回实例
        :param image_path: 图片路径
        :return: 图片实例
        """
        try:
            with Image.open(image_path) as im1:
                image_example = im1.copy()
        except FileNotFoundError:
            print(f"Error:The file or directory: '{image_path}' does not exist.")
            print("===========")
            print(traceback.format_exc())
            sys.exit()
        except PIL.UnidentifiedImageError:
            print("Error:Can't identify the image file.")
            print(traceback.format_exc())
            sys.exit()
        else:
            return image_example

    def pixel_difference(self, other_path):
        """
        像素相减求相似度（要求图片尺寸相同）
        :param other_path: 与self.image进行相似度对比的图片路径
        :return: 相似度
        """
        other_image = ImageQuery._create_and_image(other_path)
        im1_pixel = self.image.load()
        im2_pixel = other_image.load()
        similarity1 = 0
        if self.image.size != other_image.size:
            raise ImageQueryShapeNotMatchError(self.path, other_path)
        else:
            for i in range(self.image.size[0]):
                for j in range(self.image.size[1]):
                    pixel1 = im1_pixel[i, j]
                    pixel2 = im2_pixel[i, j]
                    similarity1 += (abs(pixel1[0] - pixel2[0]) + abs(pixel1[1] - pixel2[1]) + abs(pixel1[2] - pixel2[2]))
            average_similarity = similarity1 / ((self.image.size[0] * self.image.size[1]) * 255 * 3)
            return average_similarity

    def histogram_difference(self, other_path, method):
        """
        利用直方图求相关性，并得到显著值
        :param other_path: self.image进行相似度对比的图片路径
        :param method: 待选择的相关性计算方法:pearsonr, spearmanr, kendalltau
        :return: 相似度，显著值
        """
        other_image = ImageQuery._create_and_image(other_path)
        c_hist1 = self.image.histogram()
        c_hist2 = other_image.histogram()
        if method == 'pearsonr':
            similarity2, p_value = pearsonr(c_hist1, c_hist2)
        elif method == 'spearmanr':
            similarity2, p_value = spearmanr(c_hist1, c_hist2)
        elif method == 'kendalltau':
            similarity2, p_value = kendalltau(c_hist1, c_hist2)
        return similarity2, p_value

    def hash_difference(self, other_path):
        """
        利用hash之差求相似度
        :param other_path: self.image进行相似度对比的图片路径
        :return: 相似度
        """
        other_image = ImageQuery._create_and_image(other_path)
        ahash1 = imagehash.average_hash(self.image)
        ahash2 = imagehash.average_hash(other_image)
        similarity3 = abs(ahash1 - ahash2)
        return similarity3

    @staticmethod
    def load_images(directory):
        """
        从directory中加载多张图片，并返回图片名称与图片实例的对应
        :param directory: 待加载图片存放的目录
        :return: 一个字典，键是图片名称，值时图片实例
        """
        images = {}
        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            if file_path.endswith(('jpg', 'png', 'jpeg')):
                image = ImageQuery._create_and_image(file_path)
                relpath = os.path.relpath(file_path, os.getcwd())
                images[relpath] = image
        return images

    @staticmethod
    def display(row, col, image_size, max_amounts, image_list):
        """
        按照一定排布方式绘制多张图
        :param max_amounts: 绘制图片的最大数量
        :param image_list: 图片实例存放列表
        """
        plt.figure(figsize=image_size)
        for i in range(row * col):
            if i >= max_amounts:
                break
            plt.subplot(row, col, i+1)
            plt.imshow(image_list[i])
            plt.axis('off')
        plt.show()

    def search_image(self, directory, *args):
        """
        将一张图与某目录中所有图片按照某种方式求相似度，并排序，返回并绘制相似度大于某个水平的图片
        :param directory: 待加载图片存放的目录
        :param args: args:不定长参数，若是histogram方法，则还需传入相关性计算方法
        """
        images = ImageQuery.load_images(directory)  # 当前工作目录
        similarity_dict = {}
        qualified_list = []
        if args[0] == 'pixel':
            k = 0.25
            for item in list(images.keys()):
                similarity = self.pixel_difference(item)
                similarity_dict[item] = similarity
            sorted_dict = dict(sorted(similarity_dict.items(), key=lambda x: x[1]))
            qualified_list = [ImageQuery._create_and_image(i) for i in list(sorted_dict.keys()) if sorted_dict[i] <= k]
        elif args[0] == 'histogram':
            k = 0.45
            for item in list(images.keys()):
                similarity, p_value = self.histogram_difference(item, args[1])
                if p_value < 0.05:  # 显著值过小的直接不参与排序（相似度无意义）
                    similarity_dict[item] = similarity
            sorted_dict = dict(sorted(similarity_dict.items(), key=lambda x: x[1], reverse=True))
            qualified_list = [ImageQuery._create_and_image(i) for i in list(sorted_dict.keys()) if sorted_dict[i] >= k]
        elif args[0] == 'hash':
            k = 28
            for item in list(images.keys()):
                similarity = self.hash_difference(item)
                similarity_dict[item] = similarity
            sorted_dict = dict(sorted(similarity_dict.items(), key=lambda x: x[1]))
            qualified_list = [ImageQuery._create_and_image(i) for i in list(sorted_dict.keys()) if sorted_dict[i] <= k]
        if len(qualified_list) == 0:
            raise ImageQueryNoSimilarImageFoundError
        else:
            for i in list(sorted_dict.keys()):
                print(f"{i}: {sorted_dict[i]}")
            ImageQuery.display(3, 3, (250, 250), len(qualified_list), qualified_list)


if __name__ == "__main__":
    # 像素直接相减求相似度
    start_time1 = time.time()
    try:
        x1 = ImageQuery('example.jpg')
        similarity1 = x1.pixel_difference('0001.jpg')
    except ImageQueryShapeNotMatchError as ism:
        print(ism.message)
        print(traceback.format_exc())
        sys.exit()
    else:
        print(f"similarity1: {similarity1:.2f}%")
    end_time1 = time.time()
    print(f"pixel方法消耗时间: {end_time1-start_time1}")
    # 利用直方图求相关性
    start_time2 = time.time()
    x2 = ImageQuery('example.jpg')
    similarity2, p_value = x2.histogram_difference('0001.jpg', 'kendalltau')
    print(f"similarity2: {similarity2}, 显著值: {p_value}")
    end_time2 = time.time()
    print(f"histogram方法消耗时间: {end_time2 - start_time2}")
    # 利用hash之差求相似度
    start_time3 = time.time()
    x3 = ImageQuery('example.jpg')
    similarity3 = x3.hash_difference('0001.jpg')
    print(f"similarity3: {similarity3}")
    end_time3 = time.time()
    print(f"hash方法消耗时间: {end_time3 - start_time3}")
    # 批量加载图片，并输出名称与对应实例
    image_dict = ImageQuery.load_images('.')  # 加载当前目录里的图片
    for i in list(image_dict.keys()):
        print(f"{i}: {image_dict[i]}")
    # 相似度排序并可视化
    x4 = ImageQuery('example.jpg')
    try:
        # x4.search_image('D:\\PycharmProjects\\python_2023\\week7', 'histogram', 'pearsonr')
        # x4.search_image('D:\\PycharmProjects\\python_2023\\week7', 'pixel')
        x4.search_image('D:\\PycharmProjects\\python_2023\\week7', 'hash')
    except ImageQueryNoSimilarImageFoundError as ins:
        print(ins.message)



