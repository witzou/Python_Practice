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

    img = cv2.imread('./data/{}'.format(image_name)) # clw note: 使用cv2的imread方法来加载图片，注意format函数的用法
                                                      #           这里的images/{}在下面调用的时候，相当于images/raccon1-1.jpg
    for data in txt_datas:
        x1 = float(data.split(' ')[0])
        y1 = float(data.split(' ')[1])
        x2 = float(data.split(' ')[2])
        y2 = float(data.split(' ')[3])
        x3 = float(data.split(' ')[4])
        y3 = float(data.split(' ')[5])
        x4 = float(data.split(' ')[6])
        y4 = float(data.split(' ')[7])
        points = np.array([[x1, y1], [x2, y2], [x3, y3], [x4, y4]], np.float64)
        #points = points.reshape((-1, 1, 2))  #暂时没明白作用
        img = cv2.polylines(img, np.int32([points]), True, (255, 0, 0), 2) # 这里3应该是线条宽度

    return img #如果加在cv2.imread那里，会报错TypeError: Layout of the output array img is incompatible
               # with cv::Mat (step[ndims-1] != elemsize or step[1] != elemsize*nchannels)


###查看某一张图片
# clw note：如果只查看单张图片而且用Image模块，最好把上面函数改成img[:,:,::-1]，否则RGB颜色变成BGR，也就是红色看起来是蓝色。。
def visualize_one_picture(img_path):  #比如img_path='./data/P0005.png'
    pil_im = Image.fromarray(draw_boxes(img_path)) #用PIL库的Image模块中的fromarray函数来将数组转化为图片
    pil_im.show()
    # clw note：也可以尝试一下下面这个方法：
    #img = draw_boxes(img_path)
    #plt.imshow(img)


###连续查看多张图片
def visualize_pictures(data_path):
    img_list =  os.listdir(data_path)
    for img_name in img_list:
        if img_name.endswith(('.jpg','.png')):
            #方法1：调用查看单张图片的方法
            visualize_one_picture(data_path + '/' + img_name)

            #方法2：调用cv2的方法，不用PIL；好处是可以一张一张查看，比如按Esc切到下一张，不像PIL会连续打开多张图；
            # cv2.namedWindow('image', 0);  #clw note：注意steer应该是窗口名，后面要保持一致！！
            # #cv2.resizeWindow('image', 1024, 768); #clw note：如果图片太大显示器看不全，就缩放一下
            # img = draw_boxes(data_path + '/' + img_name)
            # cv2.imshow('image', img)
            # k = cv2.waitKey(0)  # waitkey代表读取键盘的输入，括号里的数字代表等待多长时间，单位ms。 0代表一直等待
            # if k == 27:  # 键盘上Esc键的键值
            #     cv2.destroyAllWindows()
            # cv2.imwrite('./' + img_name, img)  # 对图片进行保存，第一个参数表示保存后的图片名，第二个参数表示需要保存的图片


def main():
    data_path = './data'
    visualize_pictures(data_path)
    #visualize_one_picture(data_path + '/' + 'P0005.png')


main()