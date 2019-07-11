# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 21:50:25 2019

@author: clwclw
"""

# 【数据预处理】 查看文件夹内所有图片的宽度和高度最大值

# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 15:22:49 2019

@author: clwclw
"""

# 【数据预处理】 查看文件夹内所有图片的宽度和高度最大值

import os
from PIL import Image
from collections import Counter
import numpy as np


# clw note：这里图片用宽*高表示
img_width_list  = []  
img_height_list = []
img_ratio_list = []  # clw note，由于图片都是垂直文字，因此计算 高/宽 的比例
print('打印某文件夹内所有图片的尺寸：')
#img_path = 'C:/Users/clwclw/Desktop/1'
img_path = 'D:/ocr_densenet_origin/data/dataset/train'
img_list =  os.listdir(img_path)
for img_file in img_list:
    if img_file.endswith(('.jpg','.png')):
        img=Image.open(img_path + '/' + img_file)
        #clw note：可以加入一些黑白的处理，比如Image.open(img_path + '/' + img_file).convert('L')
        ratio = img.size[1]/ img.size[0]
        print('%s,  宽：%d,  高：%d, 比例：%f'%(img_file,img.size[0], img.size[1], ratio))
        img_width_list.append(img.size[0])
        img_height_list.append(img.size[1])
        img_ratio_list.append(ratio)
        #img.show()


print("所有图片最大的宽度为%d,对应的图片名为%s" %(max(img_width_list) , img_list[img_width_list.index(max(img_width_list))]  ))
print("所有图片最大的高度为%d,对应的图片名为%s" %(max(img_height_list), img_list[img_height_list.index(max(img_height_list))]  ))
print("所有图片最大的比例为%f,对应的图片名为%s" %(max(img_ratio_list), img_list[img_ratio_list.index(max(img_ratio_list))]  ))


black_list_records = np.sum(list(map(lambda x: x > 8.0, img_ratio_list))) #高宽比大于8:1的图片    #clw note:map()函数Python 2.x 返回列表,Python 3.x 返回迭代器；python3.x如果list(map(...))返回为列表[True, False, True.... ]
white_list_records = len(img_ratio_list) - black_list_records             #高宽比小于或等于8:1的图片

result_width = Counter(img_width_list)     # 统计不同宽度的图片数量
result_height = Counter(img_height_list)   # 统计不同高度的图片数量
result_ratio = Counter(img_ratio_list)   # 统计不同高度的图片数量