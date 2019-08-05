# for maskrcnn benchmark， written by 队友 chenjiahao

import os
import cv2
import json
import numpy as np
img_dic = {}
category_dic = {}
img_folder = '/home/yc/workspace/ZMVISION_workdir/DATASET/xishu/images'
txt_folder = '/home/yc/workspace/ZMVISION_workdir/DATASET/xishu/labelTxt_new'
file_list = os.listdir(img_folder)
id = 1
images = []
categories = []
annotations = []
# input_txt to coco_json
for img_name in file_list:
    img_dic[img_name] = id
    img = cv2.imread(os.path.join(img_folder,img_name))
    images.append({
        "id":id,
        "file_name":img_name,
        "height":img.shape[0],
        "width":img.shape[1]})
    id += 1

txt_list = os.listdir(txt_folder)
id = 1
annid = 1
for txt_name in txt_list:
    f = open(os.path.join(txt_folder,txt_name),'r')
    false_lable = 0
    while false_lable < 2:
        str = f.readline()
        if str == '' or str == '\n':
            false_lable += 1
            continue
        else:
            false_lable = 0
            res = str.split(' ')
            if len(res) < 8 :
                continue
            points = np.array(res[:8]).astype('float').tolist()
            category = res[8]
            if category not in category_dic.keys():
                category_dic[category] = int(id)
                categories.append({
                    "supercategory": "none",
                    "id": id,
                    "name": category})
                id +=1
            x = [points[i] for i in [0,2,4,6]]
            y = [points[i] for i in [1,3,5,7]]
            x_min,x_max = min(x),max(x)
            y_min,y_max = min(y),max(y)
            annotations.append({
                "segmentation":[[points[0],points[1],points[2],points[3],points[4],points[5],points[6],points[7]]],
                "area":(x_max-x_min)*(y_max-y_min),
                "iscrowd":0,
                "image_id":img_dic[txt_name[:-4]+'.png'],
                "bbox":[x_min,y_min,(x_max-x_min),(y_max-y_min)],
                "category_id":category_dic[category],
                "id":int(annid),
                "ignore":0})
            annid +=1
jsonfile = {}
jsonfile['images'] = images
jsonfile['categories'] = categories
jsonfile['annotations'] = annotations
with open("/home/yc/workspace/ZMVISION_workdir/DATASET/xishu/train.json",'w',encoding='utf-8') as f:
    json.dump(jsonfile,f)


