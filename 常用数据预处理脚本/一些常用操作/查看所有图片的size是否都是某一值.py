# 查看所有图片的size是否都是某一值

# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 15:58:25 2019
@author: Administrator
"""
import numpy as np
import pandas as pd
import cv2
import os
from PIL import Image
import matplotlib.pyplot as plt



###找到数据集的所有图片（暂时没用到）
def find_all_images(data_path):
    images = []
    data_files = os.listdir(data_path)
    #print(data_files)
    for filename in data_files:
        print(filename)
        if filename.endswith('.png'):
            img = cv2.imread(data_path + filename)
            #print(img.shape)
            assert(img.shape == (800,800,3))

    return images


def main():
    #data_path = 'C:/Users/Administrator/Desktop/train_crop/'  #clw note：注意：对于cv2.imread如果图像不在当前目录中，则必须提供图像的绝对路径！！！！！
    data_path = 'F:/deep_learning/competion/2019yaogan/train/train_crop/images/'
    find_all_images(data_path)
    #img = cv2.imread(img_all_path)

main()