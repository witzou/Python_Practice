# 目前常用的图像增广技术有如下几种：
# 镜像变换
# 旋转
# 缩放
# 裁剪
# 平移
# 亮度修改
# 添加噪声
# 剪切
# 变换颜色
# 详见https://zhuanlan.zhihu.com/p/65367068

import cv2
import numpy as np
import skimage
from skimage.util.dtype import convert

img = cv2.imread("../data/2007_000129.jpg")
h = img.shape[0]
w = img.shape[1]

# 初始化一个矩阵，用于存储转化后的图像，
generate_img = np.zeros(img.shape)

# 0.原始图像
#cv2.imshow("Origin", img)
#cv2.waitKey()

# 1.水平镜像
# for i in range(h):
#     for j in range(w):
#         generate_img[i, w - 1 - j] = img[i, j]
#cv2.imshow("Ver", generate_img.astype(np.uint8))
#cv2.waitKey()

# 2.垂直镜像
# for i in range(h):
#     for j in range(w):
#         generate_img[h-1-i, j] = img[i, j]
#cv2.imshow("Ver", generate_img.astype(np.uint8))
#cv2.waitKey()

# 3.图像缩放
# output = cv2.resize(img, (100, 300))
#cv2.imshow("Ver", output.astype(np.uint8))
#cv2.waitKey()

# 4.旋转变换
# 获取一个旋转矩阵，然后调用opencv的warpAffine仿射函数按照旋转矩阵对图像进行旋转变换，
# center = cv2.getRotationMatrix2D((w/2, h/2), 45, 1)
# rotated_img = cv2.warpAffine(img, center, (w, h))
# cv2.imshow("Ver", rotated_img.astype(np.uint8))
# cv2.waitKey()

# 5. 平移变换
# 首先用numpy生成一个平移矩阵，然后用仿射变换函数对图像进行平移变换，
# move = np.float32([[1, 0, 100], [0, 1, 100]])
# move_img = cv2.warpAffine(img, move, (w, h))
# cv2.imshow("Ver", move_img.astype(np.uint8))
# cv2.waitKey()

# 6.亮度变换
# 亮度变换的方法有很多种，这里用一种叠加图像的方式，通过给原图像叠加一副同样大小，
# 不同透明度的全零像素图像来修改图像的亮度，
# alpha = 1.5
# light = cv2.addWeighted(img, alpha, np.zeros(img.shape).astype(np.uint8), 1-alpha, 3)
# cv2.imshow("Ver", light.astype(np.uint8))
# cv2.waitKey()