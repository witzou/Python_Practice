# -*- coding: utf-8 -*-
"""
Created on 2019.9.12 23:20
@author: clwclw
"""

import cv2
import os
from skimage.io import imsave
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from pycocotools.coco import COCO

defect_label2name = {
    1:'破洞', 2:'水渍/油渍/污渍',  3:'三丝', 4:'结头', 5:'花板跳', 6:'百脚', 7:'毛粒',
    8:'粗经', 9:'松经', 10:'断经', 11:'吊经', 12:'粗维', 13:'纬缩', 14:'浆斑', 15:'整经结', 16:'星跳/跳花',
    17:'断氨纶', 18:'稀密档/浪纹档/色差档', 19:'磨痕/轧痕/修痕/烧毛痕', 20:'死皱/云织/双纬/双经/跳纱/筘路/纬纱不良'
}


''' 读取json '''
import json
img_and_anno_root = 'C:/Users/Administrator/Desktop/'
annFile = img_and_anno_root + 'result.json'
file = open(annFile, "r")
data_list = json.load(file)
data_list = sorted(data_list,key = lambda e:e['name'],reverse = True)


''' 获取图片 '''
img_path = img_and_anno_root + 'test/'
img_list = os.listdir(img_path)


''' 是否需要保存可视化的图片 '''
NEED_SAVE = False
img_save_path = img_and_anno_root + 'visualized_image'
if NEED_SAVE:
    if not os.path.exists(img_save_path):
        os.makedirs(img_save_path)


''' 在预测图片上绘制结果（矩形框+label）的方法 '''
def draw_rectangle(boxes, labels, score, image):

    for box, label, score in zip(boxes, labels, scores):
        cv2.rectangle(image, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (0, 255, 0), 2)   # xywh，需要转成左上角坐标, 右下角坐标

        # clw note:主要用于输出中文的label
        cv2img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pilimg = Image.fromarray(cv2img)
        draw = ImageDraw.Draw(pilimg)  # 图片上打印
        #font = ImageFont.truetype('/media/clwclw/data/fonts/simsun.ttf', 20, encoding="utf-8")
        font = ImageFont.truetype('./simsun.ttf', 36, encoding="utf-8")
        #font = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', 36, encoding="utf-8")

        left = float(box[0])
        top = float(box[1])
        right = float(box[2])
        down = float(box[3])

        draw.text(((left + right) / 2.0, (top + down) / 2.0), label, (255, 0, 0), font=font) # clw note：在中心位置输出标签
        draw.text(((left + right) / 2.0 + 30.0, (top + down) / 2.0 + 30.0), str(score), (255, 0, 0), font=font)

        image = cv2.cvtColor(np.array(pilimg), cv2.COLOR_RGB2BGR)

    return image


# 查看所有图片
for i in range(len(img_list)):
# for i in range(5): # clw note：随机查看几张



    image_name = img_list[i]
    img_raw = cv2.imread(os.path.join(img_path, image_name))

    coordinates = []
    labels = []
    scores = []
    for j in range(len(data_list)):
        if data_list[j]['name'] == img_list[i]: # 匹配
            coordinate = []
            coordinate.append(data_list[j]['bbox'][0])
            coordinate.append(data_list[j]['bbox'][1])
            coordinate.append(data_list[j]['bbox'][2])
            coordinate.append(data_list[j]['bbox'][3])
            # print(coordinate)
            coordinates.append(coordinate)

            # 2、找到对应的标签
            label_id = data_list[j]['category']
            label_name = defect_label2name[label_id]
            labels.append(label_name)

            # 3、找到对应的score
            scores.append(data_list[j]['score'])

    image = draw_rectangle(coordinates, labels, scores, img_raw)
    cv2.namedWindow("clwclw",0)
    cv2.resizeWindow("clwclw", 1600, 1200)
    cv2.imshow('clwclw', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    if NEED_SAVE:
        imsave(img_save_path, image)