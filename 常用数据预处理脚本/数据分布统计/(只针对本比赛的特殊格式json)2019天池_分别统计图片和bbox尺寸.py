# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 21:50:25 2019
@author: clwclw
"""

img_and_anno_root = '/mfs/home/fangyong/data/guangdong/train/'
#img_and_anno_root ='K:/deep_learning/dataset/2019tianchi/train/'
###########################################################################################

#### 1、统计所有图片的宽度、高度的分布情况

# import os
# from PIL import Image
# from collections import Counter
# img_path = img_and_anno_root + 'defect_Images/'
#
# # clw note：这里图片用宽*高表示
# img_width_list  = []
# img_height_list = []
# img_list =  os.listdir(img_path)
# for img_file in img_list:
#     if img_file.endswith(('.jpg','.png')):
#         img=Image.open(img_path + '/' + img_file)
#         ratio = img.size[1]/ img.size[0]
#         print('%s,  宽：%d,  高：%d'%(img_file,img.size[0], img.size[1]))
#         img_width_list.append(img.size[0])
#         img_height_list.append(img.size[1])
#
# print("clw:所有图片最大的宽度为%d,对应的图片名为%s" %(max(img_width_list) , img_list[img_width_list.index(max(img_width_list))]  ))
# print("clw:所有图片最大的高度为%d,对应的图片名为%s" %(max(img_height_list), img_list[img_height_list.index(max(img_height_list))]  ))
#
# result_width = Counter(img_width_list)     # 统计不同宽度的图片数量
# result_height = Counter(img_height_list)   # 统计不同高度的图片数量
#
# print('clw:图片宽度统计（宽度：个数）：',result_width)
# print('clw:图片高度统计（高度：个数）：',result_height)

###########################################################################################



#### 2、统计所有bbox的宽度、高度、宽高比最值和分布情况
import json

annFile = img_and_anno_root + 'Annotations/anno_train.json'
file = open(annFile, "rb")
data_list = json.load(file)
data_list = sorted(data_list,key = lambda e:e['name'],reverse = True)

bbox_width_list  = []
bbox_height_list = []
bbox_ratio_list = []
bbox_area_list = []

bbox_too_high_count= 0
bbox_too_wide_count= 0

bbox_count_all = 0
bbox_big_count = 0
bbox_small_count= 0
bbox_too_big_count = 0
bbox_too_small_count= 0
bbox_normal_count= 0
big_threshold = 96*96
too_big_threshold = 384*384
small_threshold = 32*32
too_small_threshold = 16*16

bbox_ratio0_count = 0
bbox_ratio1_count = 0
bbox_ratio2_count = 0
bbox_ratio3_count = 0
bbox_ratio4_count = 0
bbox_ratio5_count = 0
bbox_ratio6_count = 0
bbox_ratio7_count = 0
bbox_ratio8_count = 0
bbox_ratio9_count = 0
bbox_ratio10_count = 0

file_names = []
defect_names = []
for data in data_list:
    file_names.append(data['name'])
    defect_names.append(data['defect_name'])
    bbox_count_all += 1
    assert data['bbox'][0] <= data['bbox'][2] and data['bbox'][1] <= data['bbox'][3]  # 可以先检查一下是否有错误数据，即对于x1y1x2y2，一定有x1<x2，y1<y2
    bbox_width = float(data['bbox'][2]) - float(data['bbox'][0])
    bbox_height = float(data['bbox'][3]) - float(data['bbox'][1])
    bbox_ratio = bbox_width / bbox_height
    if bbox_ratio > 1:
        bbox_ratio = 1.0 / bbox_ratio
    bbox_area = bbox_width * bbox_height

    # 统计bbox大小分布
    if bbox_area <= too_small_threshold:
        bbox_too_small_count += 1
    elif bbox_area > too_small_threshold and bbox_area <= small_threshold:
        bbox_small_count += 1
    elif bbox_area > small_threshold and bbox_area <= big_threshold:
        bbox_normal_count += 1
    elif bbox_area > big_threshold and bbox_area <= too_big_threshold:
        bbox_big_count += 1
    elif bbox_area > too_big_threshold:
        bbox_too_big_count += 1

    # 统计bbox ratio分布  （前开后闭）
    if bbox_ratio <= 0.05:
        bbox_ratio0_count += 1
    if bbox_ratio > 0.05 and bbox_ratio <= 0.1:
        bbox_ratio1_count += 1
    elif bbox_ratio > 0.1 and bbox_ratio <= 0.2:
        bbox_ratio2_count += 1
    elif bbox_ratio > 0.2 and bbox_ratio <= 0.3:
        bbox_ratio3_count += 1
    elif bbox_ratio > 0.3 and bbox_ratio <= 0.4:
        bbox_ratio4_count += 1
    elif bbox_ratio > 0.4 and bbox_ratio <= 0.5:
        bbox_ratio5_count += 1
    elif bbox_ratio > 0.5 and bbox_ratio <= 0.6:
        bbox_ratio6_count += 1
    elif bbox_ratio > 0.6 and bbox_ratio <= 0.7:
        bbox_ratio7_count += 1
    elif bbox_ratio > 0.7 and bbox_ratio <= 0.8:
        bbox_ratio8_count += 1
    elif bbox_ratio > 0.8 and bbox_ratio <= 0.9:
        bbox_ratio9_count += 1
    elif bbox_ratio > 0.9 and bbox_ratio <= 1.0:
        bbox_ratio10_count += 1

    bbox_width_list.append(bbox_width)
    bbox_height_list.append(bbox_height)
    bbox_ratio_list.append(bbox_ratio)
    bbox_area_list.append(bbox_area)

# print('clw:bbox数量共计：', bbox_count_all)
# print('clw:bbox宽度：', sorted(bbox_width_list))
# print('clw:bbox高度：', sorted(bbox_height_list))
# print('clw:bbox宽高比）：',sorted(bbox_ratio_list))
# print('clw:bbox面积）：',sorted(bbox_area_list))
#
# print('clw:bbox面积大于 %f 的有 %d 个' % (too_big_threshold, bbox_too_big_count))
# print('clw:bbox面积小于 %f 的有 %d 个' % (too_small_threshold, bbox_too_small_count))
# print('clw:bbox宽高比小于 %f 的有 %d 个）' % (too_high_threshold, bbox_too_high_count))
# print('clw:bbox宽高比大于 %f 的有 %d 个）' % (too_wide_threshold, bbox_too_wide_count))
#
#
# # result_width = Counter(bbox_width_list)     # 统计不同宽度的图片数量
# # result_height = Counter(bbox_height_list)   # 统计不同高度的图片数量
# # result_ratio = Counter(bbox_ratio_list)   # 统计不同高度的图片数量
# #
# # print('clw:bbox宽度统计（宽度：个数）：',result_width)
# # print('clw:bbox高度统计（高度：个数）：',result_height)
# # print('clw:bbox宽高比统计（宽高比：个数）：',result_ratio)


#########################
### 作图
########################
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
#plt.style.use('ggplot') #使用'ggplot'风格美化显示的图表
# font = {'family':'SimHei'} #设置使用的字体（需要显示中文的时候使用）
# plt.rc('font',**font) #设置显示中文，与字体配合使用
import matplotlib as mpl #新增包
#from matplotlib.ticker import MultipleLocator, FormatStrFormatter #新增函数
mpl.rcParams['font.size'] = 12 #设置字体大小
plt.rcParams['font.family'] = 'SimSun'  # 设置全局的字体
custom_font = mpl.font_manager.FontProperties(fname='/home/user/clwclw/simsun.ttf') #导入字体文件
#custom_font = mpl.font_manager.FontProperties(fname='C:/Windows/Fonts/msyh.ttc') #导入字体文件

# （1）一幅图的gt数量的统计直方图
bbox_counts = Counter(file_names)
################################ 可以打印出拥有gt最多的图片的名字
#top_three = bbox_counts.most_common(3)
#print(top_three)
#########################################
bbox_count_list = [i[1] for i in bbox_counts.most_common()]  # 形如[37, 25, 24, 24, ...., 1, 1, 1, 1, 1]
bbox_count_max = max(bbox_count_list)

#plt.hist(bbox_count_list, bins=bbox_count_max, normed=False, log=True, color='cornflowerblue')  # clw note：bins指定总共有几条条状图； normed是否归一化；log取对数
# 可以用以下功能代替plt.hist()，就可以手动添加一些想要的功能，比如在bar上面把数字打出来
num_list = []
for i in range(bbox_count_max+1):
    num_list.append(bbox_count_list.count(i))
bbb = plt.bar(range(bbox_count_max+1), num_list, color='cornflowerblue', tick_label=range(bbox_count_max+1), log=True)  # x：bar的横坐标
for x, y in enumerate(num_list):
    if y == 0:  # 直方图如果高度为0，就不用在上面加个数字0了，否则很难看
        plt.text(x, y + 0.7, y, ha='center', va='bottom', fontsize=10)
    elif y <= 3:
        plt.text(x, y + 0.1, y, ha='center', va='bottom', fontsize=10)  # font='/home/user/clwclw/simsun.ttf'
    else:
        plt.text(x, y+1, y, ha='center', va='bottom', fontsize=10)  # font='/home/user/clwclw/simsun.ttf'   # 前三个参数：x,y:表示坐标值上的值，string:表示说明文字

plt.title('含有一定数量object的图片个数统计', fontsize=24, fontproperties=custom_font)
plt.xlabel('object个数', fontsize=14, fontproperties=custom_font)
plt.ylabel('图片数量', fontsize=14, fontproperties=custom_font)


# （2）34类缺陷，每一类缺陷个数的直方图
defect_counts = Counter(defect_names)
num_list = []
name_list = ['\u7834\u6d1e', '\u6c34\u6e0d', '\u6cb9\u6e0d', '\u6c61\u6e0d',
                 '\u4e09\u4e1d', '\u7ed3\u5934', '\u82b1\u677f\u8df3', '\u767e\u811a', '\u6bdb\u7c92',
                 '\u7c97\u7ecf', '\u677e\u7ecf', '\u65ad\u7ecf', '\u540a\u7ecf', '\u7c97\u7ef4',
                 '\u7eac\u7f29', '\u6d46\u6591', '\u6574\u7ecf\u7ed3', '\u661f\u8df3', '\u8df3\u82b1',
                 '\u65ad\u6c28\u7eb6', '\u7a00\u5bc6\u6863', '\u6d6a\u7eb9\u6863', '\u8272\u5dee\u6863', '\u78e8\u75d5',
                 '\u8f67\u75d5', '\u4fee\u75d5', '\u70e7\u6bdb\u75d5', '\u6b7b\u76b1', '\u4e91\u7ec7',
                 '\u53cc\u7eac', '\u53cc\u7ecf', '\u8df3\u7eb1', '\u7b58\u8def', '\u7eac\u7eb1\u4e0d\u826f']
final_list = [' \u7834\n \u6d1e', '\u6c34\n\u6e0d', '\u6cb9\n\u6e0d', '\u6c61\n\u6e0d',   # clw note：很奇怪，如果第一个元素没有空格，或者不去掉回车，那么后面元素都会在左右两侧有一段缺失，可以看下效果
            '\u4e09\n\u4e1d', '\u7ed3\n\u5934', '\u82b1\n\u677f\n\u8df3', '\u767e\n\u811a', '\u6bdb\n\u7c92',
            '\u7c97\n\u7ecf', '\u677e\n\u7ecf', '\u65ad\n\u7ecf', '\u540a\n\u7ecf', '\u7c97\n\u7ef4',
            '\u7eac\n\u7f29', '\u6d46\n\u6591', '\u6574\n\u7ecf\n\u7ed3', '\u661f\n\u8df3', '\u8df3\n\u82b1',
            '\u65ad\n\u6c28\n\u7eb6', '\u7a00\n\u5bc6\n\u6863', '\u6d6a\n\u7eb9\n\u6863', '\u8272\n\u5dee\n\u6863', '\u78e8\n\u75d5',
            '\u8f67\n\u75d5', '\u4fee\n\u75d5', '\u70e7\n\u6bdb\n\u75d5', '\u6b7b\n\u76b1', '\u4e91\n\u7ec7',
            '\u53cc\n\u7eac', '\u53cc\n\u7ecf', '\u8df3\n\u7eb1', '\u7b58\n\u8def', '\u7eac\n\u7eb1\n\u4e0d\n\u826f']
for name in name_list:
    num_list.append(defect_counts[name])

fig, ax = plt.subplots()
bbb = ax.bar(range(len(name_list)), num_list, color='cornflowerblue', tick_label=final_list)  # x：bar的横坐标
#bbb = ax.barh(range(len(name_list)), num_list, color='cornflowerblue', tick_label=name_list)  # clw note：如果改成水平，后面ax.text内坐标也需要调整
for x, y in enumerate(num_list):
    ax.text(x, y+1, y, ha='center', va='bottom', fontsize=10)  # font='/home/user/clwclw/simsun.ttf'   # 前三个参数：x,y:表示坐标值上的值，string:表示说明文字

plt.title('每一类缺陷个数统计', fontsize=24, fontproperties=custom_font)
plt.xlabel('类别', fontsize=14, fontproperties=custom_font)
plt.ylabel('bounding box数量', fontsize=14, fontproperties=custom_font)

# （3）bbox大小统计
name_list = ['<=16x16', '16x16~32x32', '32x32~96x96', '96x96~384x384', '>384x384'] # 前开后闭
num_list = [bbox_too_small_count, bbox_small_count, bbox_normal_count, bbox_big_count, bbox_too_big_count]
fig, ax = plt.subplots()
bbb = ax.bar(range(len(name_list)), num_list, color='cornflowerblue', tick_label=name_list, width=0.5)  # x：bar的横坐标
for x, y in enumerate(num_list):
    ax.text(x, y+1, y, ha='center', va='bottom', fontsize=10)
plt.title('bounding box尺寸大小统计', fontsize=24, fontproperties=custom_font)
plt.xlabel('面积范围', fontsize=14, fontproperties=custom_font)
plt.ylabel('bounding box个数', fontsize=14, fontproperties=custom_font)

# （4）bbox长宽比统计
name_list = ['<0.05', '0.05~0.1', '0.1~0.2', '0.2~0.3', '0.3~0.4', '0.4~0.5', '0.5~0.6', '0.6~0.7', '0.7~0.8', '0.8~0.9', '0.9~1.0'] # 前开后闭
num_list = [bbox_ratio0_count, bbox_ratio1_count, bbox_ratio2_count, bbox_ratio3_count, bbox_ratio4_count, bbox_ratio5_count,
            bbox_ratio6_count, bbox_ratio7_count, bbox_ratio8_count, bbox_ratio9_count, bbox_ratio10_count]
fig, ax = plt.subplots()
bbb = ax.bar(range(len(name_list)), num_list, color='cornflowerblue', tick_label=name_list, width=0.5)  # x：bar的横坐标
for x, y in enumerate(num_list):
    ax.text(x, y+1, y, ha='center', va='bottom', fontsize=10)
plt.title('bounding box宽高比统计', fontsize=24, fontproperties=custom_font)
plt.xlabel('宽高比范围', fontsize=14, fontproperties=custom_font)
plt.ylabel('bounding box个数', fontsize=14, fontproperties=custom_font)






plt.show()


