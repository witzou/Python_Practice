#!/usr/bin/env python
# coding=UTF-8
'''
@Description:
@Author: HuangQinJian
@LastEditors: HuangQinJian
@Date: 2019-04-23 13:43:24
@LastEditTime: 2019-04-30 21:29:26
'''
##### clw note:注意，带label的图片保存在当前路径下的一个名为anno_image_coco的文件夹内，这里取了大概7张图片；


from pycocotools.coco import COCO
import skimage.io as io
import matplotlib.pyplot as plt
import pylab
import cv2
import os
from skimage.io import imsave
import numpy as np
pylab.rcParams['figure.figsize'] = (8.0, 10.0)


img_path = 'C:/Users/Administrator/Desktop/defect_Images/'
annFile = 'C:/Users/Administrator/Desktop/Annotations/gt_result.json'


if not os.path.exists('anno_image_coco/'):
    os.makedirs('anno_image_coco/')




def draw_rectangle(coordinates, image, image_name):
    for coordinate in coordinates:
        left = np.rint(coordinate[0])
        right = np.rint(coordinate[1])
        top = np.rint(coordinate[2])
        bottom = np.rint(coordinate[3])

        # 左上角坐标, 右下角坐标
        cv2.rectangle(image,
                      (int(left), int(right)),
                      (int(top), int(bottom)),
                      (0, 255, 0),
                      2)
    imsave('anno_image_coco/'+image_name, image)




# 初始化标注数据的 COCO api
coco = COCO(annFile)


# display COCO categories and supercategories
cats = coco.loadCats(coco.getCatIds())
nms = [cat['name'] for cat in cats]
# print('COCO categories: \n{}\n'.format(' '.join(nms)))


nms = set([cat['supercategory'] for cat in cats])
# print('COCO supercategories: \n{}'.format(' '.join(nms)))


#img_path = 'data/train/'
img_list = os.listdir(img_path)
# for i in range(len(img_list)):
for i in range(5):
    imgIds = i+1
    img = coco.loadImgs(imgIds)[0]
    image_name = img['file_name']
    # print(img)


    # 加载并显示图片
    # I = io.imread('%s/%s' % (img_path, img['file_name']))
    # plt.axis('off')
    # plt.imshow(I)
    # plt.show()


    # catIds=[] 说明展示所有类别的box，也可以指定类别
    annIds = coco.getAnnIds(imgIds=img['id'], catIds=[], iscrowd=None)
    anns = coco.loadAnns(annIds)
    # print(anns)
    coordinates = []
    img_raw = cv2.imread(os.path.join(img_path, image_name))
    for j in range(len(anns)):
        coordinate = []
        # coordinate.append(anns[j]['bbox'][0])
        # coordinate.append(anns[j]['bbox'][1]+anns[j]['bbox'][3])
        # coordinate.append(anns[j]['bbox'][0]+anns[j]['bbox'][2])
        # coordinate.append(anns[j]['bbox'][1])
        coordinate.append(anns[j]['bbox'][0])
        coordinate.append(anns[j]['bbox'][3])
        coordinate.append(anns[j]['bbox'][2])
        coordinate.append(anns[j]['bbox'][1])
        # print(coordinate)
        coordinates.append(coordinate)
    # print(coordinates)
    draw_rectangle(coordinates, img_raw, image_name)