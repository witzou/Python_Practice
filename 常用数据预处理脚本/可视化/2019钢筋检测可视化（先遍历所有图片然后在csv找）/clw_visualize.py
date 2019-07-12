# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 15:58:25 2019


@author: Administrator
"""


# -*- coding: utf-8 -*-
"""
Spyder Editor


This is a temporary script file.
"""


import pandas as pd
import cv2
import os
from PIL import Image


img_path = './train_dataset_test'
full_labels = pd.read_csv('./train_labels.csv')
print(full_labels.head())


def draw_boxes(image_name):  
    selected_value = full_labels[full_labels.ID == image_name]  #根据image_name，找到full_labels也就是上面表格的第一条记录
    img = cv2.imread(img_path + '/{}'.format(image_name)) # clw note: 使用cv2的imread方法来加载图片，注意format函数的用法
                                                      #           这里的images/{}在下面调用的时候，相当于images/raccon1-1.jpg
    for index, row in selected_value.iterrows():
        row_list = row[' Detection'].split(' ')
        x1 = int(float(row_list[0]))
        y1 = int(float(row_list[1]))
        x2 = int(float(row_list[2]))
        y2 = int(float(row_list[3]))
        if x2 - x1 < 30 or y2 - y1 < 30:
            print('clw: x1 = ', x1)
            print('clw: x2 = ', x2)
            print('clw: y1 = ', y1)
            print('clw: y2 = ', y2)

        #print(x1, y1, x2, y2)
        img = cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
    return img        # 如果加在cv2.imread那里，会报错TypeError: Layout of the output array img is incompatible
                      # with cv::Mat (step[ndims-1] != elemsize or step[1] != elemsize*nchannels)


################  #查看某一张图片  ########################################
# clw note：如果只查看单张图片而且用Image模块，最好把上面函数改成img[:,:,::-1]，
#           否则RGB颜色变成BGR，也就是红色看起来是蓝色。。
#pil_im = Image.fromarray(draw_boxes('img_calligraphy_00002_bg.jpg')) #用PIL库的Image模块中的fromarray函数来将数组转化为图片
#pil_im.show()   
#########################################################################




############### clw note：如果连续查看多张图片，建议使用下面的方法！！ ############

img_list =  os.listdir(img_path)
for img_file in img_list:
    if img_file.endswith(('.jpg','.png')):
        cv2.namedWindow("steer", 0);  #clw note：注意steer应该是窗口名，后面要保持一致！！
        #cv2.resizeWindow("huawei_shufa", 1024, 768); #clw note：如果图片太大显示器看不全，就缩放一下
        cv2.imshow('steer', draw_boxes(img_file))
        cv2.waitKey(0) # clw note：需要使用cv2.waitKey来保持窗口的显示，等待按键后切换图片
################################################################################
