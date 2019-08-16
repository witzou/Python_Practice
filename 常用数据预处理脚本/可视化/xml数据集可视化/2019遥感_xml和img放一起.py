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

# 功能说明：对data_path文件内的xxx.txt和对应的xxx.png或jpg进行可视化（clw note：txt和图片混合放在data_path指向的文件夹内）
data_path = 'C:/Users/Administrator/Desktop/data'

###找到数据集的所有.txt文件名
def find_all_txts(data_path):
    txts = []
    data_files = os.listdir(data_path)
    for filename in data_files:
        if filename.endswith('.txt'):
            txts.append(filename)
    print(txts)
    return txts


###找到数据集的所有图片
def find_all_images(data_path):
    images = []
    data_files = os.listdir(data_path)
    for filename in data_files:
        if filename.endswith('.png','.jpg'):
            images.append(filename)
    print(images)
    return images


###画bbox
def draw_boxes(image_path):
    txt_datas = []
    image_name = image_path.split('/')[-1]
    data_path = image_path.rsplit('/', 1)[0]
    txt_name = image_name.split('.')[0] + '.txt'
    ###########提取某个.txt中的全部有效记录
    i = 0
    with open(data_path + '/' + txt_name, 'r') as f:
        for line in f.readlines():  # str类型
            line = line.rstrip("\n")  # 读文件时去掉换行符
            print(line.strip())
            if not line.strip()=="" and line[0].isnumeric(): #非空行，并且第一个字符是数字
                # 读取
                # print(line)
                txt_datas.append(line)
    # print(txt_datas)
    ###################################

    img = cv2.
