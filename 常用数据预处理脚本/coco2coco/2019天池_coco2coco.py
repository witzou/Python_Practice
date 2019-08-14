# for maskrcnn benchmark， written by 队友 chenjiahao

import os
import cv2
import json
import numpy as np
img_dic = {}
category_dic = {}

img_folder = 'C:/Users/Administrator/Desktop/defect_Images/'
file_list = os.listdir(img_folder)
id = 1
images = []
categories = []
annotations = []
# input_txt to coco_json
print('clw:total image number: ', len(file_list))
for img_name in file_list:
    print('clw:image id: ', id)
    img_dic[img_name] = id
    img = cv2.imread(os.path.join(img_folder,img_name))
    images.append({
        "id":id,
        "file_name":img_name,
        "height":img.shape[0],
        "width":img.shape[1]})
    id += 1

id = 1
annid = 1
#####################################################
import json
annFile = 'C:/Users/Administrator/Desktop/Annotations/gt_result.json'
file = open(annFile, "rb")
data_list = json.load(file)
data_list = sorted(data_list,key = lambda e:e['name'],reverse = True)
######################################################3

# 取出data中相应文件名的文件
print('clw:total bbox number: ', len(data_list))
for data in data_list:
    print('clw:bbox id: ', annid)
    x_min = data['bbox'][0]
    y_min = data['bbox'][1]
    x_max = data['bbox'][2]
    y_max = data['bbox'][3]
    category = data['defect_name']
    if category not in category_dic.keys():
        category_dic[category] = int(id)
        categories.append({
            "supercategory": "none",
            "id": id,
            "name": category})
        id += 1
    annotations.append({
        # "segmentation":[[points[0],points[1],points[2],points[3],points[4],points[5],points[6],points[7]]],
        "segmentation": [],
        "area": (x_max - x_min) * (y_max - y_min),
        "iscrowd": 0,
        "image_id": img_dic[data['name']],
        "bbox": [x_min, y_min, (x_max - x_min), (y_max - y_min)],
        "category_id": category_dic[category],
        "id": int(annid),
        "ignore": 0})
    annid += 1

jsonfile = {}
jsonfile['images'] = images
jsonfile['categories'] = categories
jsonfile['annotations'] = annotations
with open("C:/Users/Administrator/Desktop/train.json",'w',encoding='utf-8') as f:
    json.dump(jsonfile,f)

print('clw:category_dic = ', category_dic)
print('clw:end!')