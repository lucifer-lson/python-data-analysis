"""
作者：Lucifer
日期：2023年04月01日
"""
from PIL import Image
from PIL import ImageFilter
import os
import matplotlib.pyplot as plt


class ImageProcessor:
    """
    处理图片的基类
    """

    def __init__(self, path, **kwargs):
        self.image = Image.open(path)
        self.value_list = kwargs  # 包含'box'(裁剪参数)、'resize'(重新调整大小的参数)

    def process(self):
        raise NotImplementedError("Error: fun not implemented!")


class Grayscale(ImageProcessor):
    """
    图片的灰度化处理
    """
    def __init__(self, path):
        ImageProcessor.__init__(self, path)

    def process(self):
        gray_image = self.image.convert('L')
        return gray_image


class Crop_to_half(ImageProcessor):
    """
    图片的裁剪处理
    """
    def __init__(self, path, **kwargs):
        ImageProcessor.__init__(self, path, **kwargs)

    def process(self):
        region = self.image.crop(self.value_list['box'])
        resize_image = region.resize(self.value_list['resize'])
        return resize_image


class Blur(ImageProcessor):
    """
    图片的模糊处理
    """
    def __init__(self, path):
        ImageProcessor.__init__(self, path)

    def process(self):
        blur_image = self.image.filter(ImageFilter.BLUR)
        return blur_image


class Edge_extraction(ImageProcessor):
    """
    图片的边缘提取
    """
    def __init__(self, path):
        ImageProcessor.__init__(self, path)

    def process(self):
        temp = self.image.convert('L')
        extract_image = temp.filter(ImageFilter.FIND_EDGES)
        return extract_image


class ImageShop:
    """
    对某一目录中某种格式的图片进行统一操作，并存储
    """

    def __init__(self, image_format, image_directory):
        self.image_format = image_format
        self.image_directory = image_directory
        self.image_list = []
        self.processed_image = None

    def load_images(self):
        directory = os.listdir(self.image_directory)
        for item in directory:
            if item.endswith(self.image_format):
                self.image_list.append(Image.open(os.path.join(self.image_directory, item)))

    def __batch_ps(self, Processor, **kwargs):
        for index, image in enumerate(self.image_list):
            self.image_list[index] = image.filter(Processor(**kwargs))

    def batch_ps(self, *values):
        for value in values:
            self.__batch_ps(value[0], **(value[1]))

    def save(self, out_path):
        self.processed_image = self.processed_image.convert('RGB')
        self.processed_image.save(out_path, 'JPEG')  # 调用时需要自己设置self.processed_image为image_list中的哪张

    def display(self, row, col, image_size, max_amounts):
        plt.figure(figsize=image_size)
        for i in range(row * col):
            if i >= max_amounts:
                break
            plt.subplot(row, col, i+1)
            plt.imshow(self.image_list[i])
            plt.axis('off')
        plt.show()


class TestImageShop:
    """
    用于测试ImageShop的类
    """

    def __init__(self, image_format, image_directory, processor, save_path):
        self.image_format = image_format
        self.image_directory = image_directory  # 'C:\\Users加百列MH\\Desktop\\图\\test'
        self.processor = processor  # ImageFilter.BLUR
        self.save_path = save_path  # 'D:\\PycharmProjects\\python_2023\\week6\\processed_images'
        self.image_sample = ImageShop(self.image_format, self.image_directory)

    def Totest(self):
        # 加载操作
        self.image_sample.load_images()
        # 统一处理, 并将处理后的图片存进self.image_sample.image_list里
        self.image_sample.batch_ps((self.processor, {'radius': 2}))
        # 将image_list里的图片全部存进当前目录里
        for i in range(len(self.image_sample.image_list)):
            self.image_sample.processed_image = self.image_sample.image_list[i]
            self.image_sample.save(self.save_path + '\\' + '{}.'.format(i) + self.image_format)
        # 呈现
        self.image_sample.display(2, 3, (1500, 1000), 6)


if __name__ == "__main__":
    image = 'lx.jpg'
    ex1 = Grayscale(image)
    im1 = ex1.process()
    ex2 = Crop_to_half(image, **{'box': (0, 0, 500, 500), 'resize': (876, 904)})
    im2 = ex2.process()
    ex3 = Blur(image)
    im3 = ex3.process()
    ex4 = Edge_extraction(image)
    im4 = ex4.process()

    plt.figure()

    plt.subplot(2, 2, 1)
    plt.imshow(im1)
    plt.axis('off')
    plt.subplot(2, 2, 2)
    plt.imshow(im2)
    plt.axis('off')
    plt.subplot(2, 2, 3)
    plt.imshow(im3)
    plt.axis('off')
    plt.subplot(2, 2, 4)
    plt.imshow(im4)
    plt.axis('off')

    plt.show()

    test_imageshop = TestImageShop('jpg', 'C:\\Users\\加百列MH\\Desktop\\图\\test', ImageFilter.GaussianBlur,
                                   'D:\\PycharmProjects\\python_2023\\week6\\processed_images')
    test_imageshop.Totest()
