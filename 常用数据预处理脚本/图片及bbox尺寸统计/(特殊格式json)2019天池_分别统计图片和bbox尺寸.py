# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 21:50:25 2019
@author: clwclw
"""

###########################################################################################

#### 1、统计所有图片的宽度、高度的分布情况

import os
from PIL import Image
from collections import Counter

img_path = 'C:/Users/Administrator/Desktop/defect_Images/'

# clw note：这里图片用宽*高表示
img_width_list  = []
img_height_list = []


img_list =  os.listdir(img_path)
for img_file in img_list:
    if img_file.endswith(('.jpg','.png')):
        img=Image.open(img_path + '/' + img_file)
        ratio = img.size[1]/ img.size[0]
        #print('%s,  宽：%d,  高：%d'%(img_file,img.size[0], img.size[1]))
        img_width_list.append(img.size[0])
        img_height_list.append(img.size[1])


print("clw:所有图片最大的宽度为%d,对应的图片名为%s" %(max(img_width_list) , img_list[img_width_list.index(max(img_width_list))]  ))
print("clw:所有图片最大的高度为%d,对应的图片名为%s" %(max(img_height_list), img_list[img_height_list.index(max(img_height_list))]  ))

result_width = Counter(img_width_list)     # 统计不同宽度的图片数量
result_height = Counter(img_height_list)   # 统计不同高度的图片数量

print('clw:图片宽度统计（宽度：个数）：',result_width)
print('clw:图片高度统计（高度：个数）：',result_height)

###########################################################################################



#### 2、统计所有bbox的宽度、高度、宽高比最值和分布情况

import json

annFile = 'C:/Users/Administrator/Desktop/Annotations/gt_result.json'
file = open(annFile, "rb")
data_list = json.load(file)
data_list = sorted(data_list,key = lambda e:e['name'],reverse = True)

bbox_width_list  = []
bbox_height_list = []
bbox_ratio_list = []
bbox_area_list = []

bbox_count = 0

bbox_too_big_count = 0
bbox_too_small_count= 0
bbox_too_high_count= 0
bbox_too_wide_count= 0

too_big_threshold = 96*96
too_small_threshold = 32*32
too_high_threshold = 1/8.
too_wide_threshold = 8/1

for data in data_list:
    bbox_count += 1
    assert data['bbox'][0] <= data['bbox'][2] and data['bbox'][1] <= data['bbox'][3]  # 可以先检查一下是否有错误数据，即对于x1y1x2y2，一定有x1<x2，y1<y2
    bbox_width = float(data['bbox'][2]) - float(data['bbox'][0])
    bbox_height = float(data['bbox'][3]) - float(data['bbox'][1])
    bbox_ratio = bbox_width / bbox_height
    bbox_area = bbox_width * bbox_height

    if (bbox_area < too_small_threshold):
        bbox_too_small_count += 1
    if (bbox_area > too_big_threshold):
        bbox_too_big_count += 1
    if (bbox_ratio < too_high_threshold):
        bbox_too_high_count += 1
    if (bbox_ratio > too_wide_threshold):
        bbox_too_wide_count += 1

    bbox_width_list.append(bbox_width)
    bbox_height_list.append(bbox_height)
    bbox_ratio_list.append(bbox_ratio)
    bbox_area_list.append(bbox_area)

print('clw:bbox数量共计：', bbox_count)

print('clw:bbox宽度：', sorted(bbox_width_list))
print('clw:bbox高度：', sorted(bbox_height_list))
print('clw:bbox宽高比）：',sorted(bbox_ratio_list))
print('clw:bbox面积）：',sorted(bbox_area_list))

print('clw:bbox面积大于 %f 的有 %d 个' % (too_big_threshold, bbox_too_big_count))
print('clw:bbox面积小于 %f 的有 %d 个' % (too_small_threshold, bbox_too_small_count))
print('clw:bbox宽高比小于 %f 的有 %d 个）' % (too_high_threshold, bbox_too_high_count))
print('clw:bbox宽高比大于 %f 的有 %d 个）' % (too_wide_threshold, bbox_too_wide_count))


# result_width = Counter(bbox_width_list)     # 统计不同宽度的图片数量
# result_height = Counter(bbox_height_list)   # 统计不同高度的图片数量
# result_ratio = Counter(bbox_ratio_list)   # 统计不同高度的图片数量
#
# print('clw:bbox宽度统计（宽度：个数）：',result_width)
# print('clw:bbox高度统计（高度：个数）：',result_height)
# print('clw:bbox宽高比统计（宽高比：个数）：',result_ratio)
