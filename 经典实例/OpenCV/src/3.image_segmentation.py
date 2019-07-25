# 功能：图像预处理之图像分割

# 在图像的研究和应用中，很多时候我们关注的仅是图像中的目标或前景(其他部分称为背景)，它们对应图像中特定的、
# 具有独特性质的区域。为了分割目标，需要将这些区域分离提取出来，在此基础上才有可能进一步利用，如进行特征提取、目标识别。
# 因此，图像分割是由图像处理进到图像分析的关键步骤

# 提到图像分割，主要包含两个方面：1、非语义分割 2、语义分割
# 1、非语义分割在图像分割中所占比重更高，目前算法也非常多，研究时间较长，而且算法也比较成熟，此类图像分割目前的算法
# 主要有以下几种：（1）阈值分割：阈值分割是图像分割中应用最多的一类，该算法思想比较简单，给定输入图像一个特定阈值，
# 如果这个阈值可以是灰度值，也可以是梯度值，如果大于这个阈值，则设定为前景像素值，如果小于这个阈值则设定为背景像素值。
# （2）区域分割 （3）聚类 （4）边缘分割：这是图像分割中较为成熟，而且较为常用的一类算法。边缘分割主要利用图像
# 在边缘处灰度级会发生突变来对图像进行分割。常用的方法是利用差分求图像梯度，而在物体边缘处，梯度幅值会较大，
# 所以可以利用梯度阈值进行分割，得到物体的边缘。对于阶跃状边缘，其位置对应一阶导数的极值点，
# 对应二阶导数的过零点(零交叉点)。因此常用微分算子进行边缘检测。常用的一阶微分算子有Roberts算子、Prewitt算子
# 和Sobel算子，二阶微分算子有Laplace算子和Kirsh算子等。由于边缘和噪声都是灰度不连续点，在频域均为高频分量，
# 直接采用微分运算难以克服噪声的影响。因此用微分算子检测边缘前要对图像进行平滑滤波。LoG算子和Canny算子是具有
# 平滑功能的二阶和一阶微分算子，边缘检测效果较好，因此Canny算子也是应用较多的一种边缘分割算法。
# （5）直方图 （6）水平集
# 2、语义分割和非语义分割的共同之处都是要分割出图像中物体的边缘，但是二者也有本质的区别，用通俗的话介绍就是
# 非语义分割只想提取物体的边缘，但是不关注目标的类别。而语义分割不仅要提取到边缘像素级别，还要知道这个目标是什么。
# 因此，非语义分割是一种图像基础处理技术，而语义分割是一种机器视觉技术，难度也更大一些，目前比较成熟且应用广泛的
# 语义分割算法有以下几种：（1）Grab cut （2）Mask R-CNN （3）U-Net （4）FCN （5）SegNet
# 由于篇幅有限，所以在这里就展开介绍语义分割，后期有时间会单独对某几个算法进行详细解析，本文主要介绍非语义分割算法，
# 就以2015年UCLA提出的一种新型、高效的图像分割算法--相位拉伸变换（PST算法）为例

import os
import numpy as np
import mahotas as mh
import matplotlib.pylab as plt
import cv2
import math

# 定义全局变量，
LPF = 0.5
#S = 0.48
#W= 12.14
Phase_strength = 0.48
Warp_strength = 12.14
Threshold_min = -1
Threshold_max = 0.0019
Morph_flag = 1

# 计算公式中的核心参数r，ceita
def cart2pol(x, y):
    theta = np.arctan2(y, x)
    rho = np.hypot(x, y)
    return theta, rho

# 相位拉伸变换的核心部分，
def phase_stretch_transform(img, LPF, S, W, Threshold_min, Threshold_max, flag):
    L = 0.5
    x = np.linspace(-L, L, img.shape[0])
    y = np.linspace(-L, L, img.shape[1])
    X, Y = np.meshgrid(x, y)
    p, q = X.T, y.T
    theta, rho = cart2pol(p, q)

    # 接下来对PST公式从右至左依次实现，
    # 对输入图像进行快速傅里叶变换,
    orig = np.fft.fft2(img)

    # 实现L[p, q]
    expo = np.fft.fftshift(np.exp(-np.power((np.divide(rho, math.sqrt((LPF ** 2) / np.log(2)))), 2)))

    # 对图像进行平滑处理，
    orig_filtered = np.real(np.fft.ifft2((np.multiply(orig, expo))))

    # 实现相位核，
    PST_Kernel_1 = np.multiply(np.dot(rho, W), np.arctan(np.dot(rho, W))) - 0.5 * np.log(1 + np.power(np.dot(rho, W), 2))
    PST_Kernel = PST_Kernel_1 / np.max(PST_Kernel_1) * S

    # 将前面实现的部分与相位核做乘积，
    temp = np.multiply(np.fft.fftshift(np.exp(-1j * PST_Kernel)), np.fft.fft2(orig_filtered))

    # 对图像进行逆快速傅里叶变换，
    orig_filtered_PST = np.fft.ifft2(temp)

    # 进行角运算，得到变换图像的相位，
    PHI_features = np.angle(orig_filtered_PST)

    if flag == 0:
        out = PHI_features
    else:
        # 对图像进行阈值化处理，
        features = np.zeros((PHI_features.shape[0], PHI_features.shape[1]))
        features[PHI_features > Threshold_max] = 1
        features[PHI_features < Threshold_min] = 1
        features[img < (np.amax(img) / 20)] = 0

        # 应用二进制形态学操作来清除转换后的图像,
        out = features
        out = mh.thin(out, 1)
        out = mh.bwperim(out, 4)
        out = mh.thin(out, 1)
        out = mh.erode(out, np.ones((1, 1)))
    return out, PST_Kernel

# 下面完成调用部分的功能，
# 首先读取函数并把图像转化为灰度图，
def main():
    Image_orig = mh.imread("../data/cameraman.tif")
    if Image_orig.ndim == 3:
        Image_orig_grey = mh.colors.rgb2grey(Image_orig)
    else:
        Image_orig_grey = Image_orig

    # 调用前面的函数，对图像进行相位拉伸变换，
    edge, kernel = phase_stretch_transform(Image_orig_grey, LPF, Phase_strength, Warp_strength, Threshold_min, Threshold_max, Morph_flag)

    # 显示图像，
    Overlay = mh.overlay(Image_orig_grey, edge)
    edge = edge.astype(np.uint8)*255
    plt.imshow(edge)
    plt.show()


# 运行
main()