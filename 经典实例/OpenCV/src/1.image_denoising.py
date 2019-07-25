# 功能：图像预处理之图像去噪

# 现实中的图像会受到各种因素的影响而含有一定的噪声，噪声的类别主要有：椒盐噪声、加性噪声、乘性噪声、高斯噪声
# 图像去噪的方法有很多种，其中均值滤波、中值滤波等比较基础且成熟，还有一些基于数学中偏微分方程的去噪方法，
# 此外，还有基于频域的小波去噪方法。均值滤波、中值滤波这些基础的去噪算法以其快速、稳定等特性，在项目中非常受欢迎

# 最后是图像去噪，图像去噪的算法有很多，有基于偏微分热传导方程的，也有基于滤波的，其中基于滤波的以其速度快、算法成熟，
# 在很多工具包中都有实现，所以使用也就较多，常用的滤波去噪算法有几种：中值滤波、均值滤波、高斯滤波
# 滤波的思想和这两年在计算机视觉中用的较多的卷积思想类似，都涉及窗口运算，只是卷积是用一个卷积核
# 和图像中对应位置做卷积运算，而滤波是在窗口内做相应的操作，以均值滤波为例，对图像中每个像素的像素值进行重新计算，
# 假设窗口大小ksize=3，对于均值滤波就是求3*3窗口内所有像素点的平均值，也就是
# (1+2+3+4+5+6+7+8+9)/9 = 4.4
# 同理，对于中值滤波就是把窗口内像素按像素值大小排序求中间值，高斯滤波就是对整幅图像进行加权平均的过程，
# 每一个像素点的值，都由其本身和邻域内的其他像素值经过加权平均后得到，

import cv2
import numpy as np
import skimage
from skimage.util.dtype import convert

# 1.读取图像
img = cv2.imread("../data/2007_001458.jpg")

# 2.添加噪声
### 方法一：用第三方工具添加噪声
img_noise = skimage.util.random_noise(img, mode="gaussian")


### 方法二：用numpy生成噪声
# def add_noise(img):
#     img = np.multiply(img, 1. / 255,
#                         dtype=np.float64)
#     mean, var = 0, 0.01
#     noise = np.random.normal(mean, var ** 0.5,
#                              img.shape)
#     img = convert(img, np.floating)
#     out = img + noise
#     return out
# noise_img = add_noise(img)
# gray_img =  cv2.cvtColor(noise_img, cv2.COLOR_BGR2GRAY)
#########################################################

# 3.图像去噪
### 方法一：用第三方工具去噪
# denoise = cv2.medianBlur(img_noise, ksize=(3,3), sigmaX=0)
# denoise = cv2.fastNlMeansDenoising(img_noise, ksize=(3,3), sigmaX=0)
img_denoise = cv2.GaussianBlur(img_noise, ksize=(3,3), sigmaX=0)

### 方法二：用自己的方法去噪
def compute_pixel_value(img, i, j, ksize, channel):
    h_begin = max(0, i - ksize // 2)
    h_end = min(img.shape[0], i + ksize // 2)
    w_begin = max(0, j - ksize // 2)
    w_end = min(img.shape[1], j + ksize // 2)
    return np.median(img[h_begin:h_end, w_begin:w_end, channel])

def denoise(img, ksize):
    output = np.zeros(img.shape)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            output[i, j, 0] = compute_pixel_value(img, i, j, ksize, 0)
            output[i, j, 1] = compute_pixel_value(img, i, j, ksize, 1)
            output[i, j, 2] = compute_pixel_value(img, i, j, ksize, 2)
    return output

img_denoise = denoise(noise_img, 3)
############################################

cv2.imshow("img_noise", img_noise)
cv2.imshow("img_denoise", img_denoise)
cv2.waitKey()