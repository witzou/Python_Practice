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

###############################################################################################3
# 斜框 rbox 版本，带角度
###############################################################################################
import os
import cv2
import json
import numpy as np
img_dic = {}
category_dic = {}
img_folder = '/media/clwclw/Elements/deep_learning/competion/2019yaogan/train/train_crop_800_bigger_64/images'
txt_folder = '/media/clwclw/Elements/deep_learning/competion/2019yaogan/train/train_crop_800_bigger_64/labelTxt'

file_list = os.listdir(img_folder)
id = 1
images = []
for img_name in file_list:
    img_dic[img_name] = id
    img = cv2.imread(os.path.join(img_folder,img_name))
    images.append({
        "id":id,
        "file_name":img_name,
        "height":img.shape[0],
        "width":img.shape[1]})
    id += 1
    print('clw: id = ', id)

categories = []
annotations = []
# input_txt to coco_json
txt_list = os.listdir(txt_folder)
id = 1
annid = 1
count_small = 0
for txt_name in txt_list:
    print('clw: txt_name = ', txt_name)
    with open(os.path.join(txt_folder,txt_name), 'r') as f:
        line = f.readlines()
        for str in line:
            if str == '' or str == '\n':
                continue
            else:
                res = str.split(' ')
                if len(res) < 8 :
                    continue
                points = np.array(res[:8]).astype('float').tolist()

                #################################################################################################
                # clw note: COCO默认是水平矩形框,但这里是接近矩形的四边形框,而且顺时针或逆时针都不一定,因此考虑使用cv2,先转成矩形框
                # 从txt读入points[0]到points[7]，表示四个点的坐标
                rect = cv2.minAreaRect(np.float32([[points[0], points[1]], [points[2], points[3]],
                                                 [points[4], points[5]], [points[6], points[7]]]))
                box = cv2.boxPoints(rect)  # 获取最小外接矩形的4个顶点坐标
                box = np.round(box)  # clw note: 顺时针标注，顺序不一定从哪个角点开始，后面求角度的时候会进行判断

                pt1 = (box[0][0], box[0][1]) 
                pt2 = (box[1][0], box[1][1]) 
                pt3 = (box[2][0], box[2][1])  
                pt4 = (box[3][0], box[3][1])

                edge1 = np.sqrt((pt1[0] - pt2[0]) * (pt1[0] - pt2[0]) + (pt1[1] - pt2[1]) * (
                            pt1[1] - pt2[1]))  # clw note: (x1 - x2)^2 + (y1 - y2)^2
                edge2 = np.sqrt((pt2[0] - pt3[0]) * (pt2[0] - pt3[0]) + (pt2[1] - pt3[1]) * (pt2[1] - pt3[1]))

                angle = 0

                if edge1 > edge2:

                    width = edge1
                    height = edge2
                    if pt1[0] - pt2[0] != 0:
                        angle = -np.arctan(float(pt1[1] - pt2[1]) / float(pt1[0] - pt2[0])) / 3.1415926 * 180
                    else:
                        angle = 90.0
                elif edge2 >= edge1:
                    width = edge2
                    height = edge1
                    if pt2[0] - pt3[0] != 0:
                        angle = -np.arctan(float(pt2[1] - pt3[1]) / float(pt2[0] - pt3[0])) / 3.1415926 * 180
                    else:
                        angle = 90.0
                if angle < -45.0:
                    angle = angle + 180

                x_ctr = float(pt1[0] + pt3[0]) / 2  # pt1[0] + np.abs(float(pt1[0] - pt3[0])) / 2
                y_ctr = float(pt1[1] + pt3[1]) / 2  # pt1[1] + np.abs(float(pt1[1] - pt3[1])) / 2
                #################################################################################################
                
                #if height * width < 150:  # clw note: for DOTA
                #    print('clw: 面积小于150, 删掉,count = ', count_small)
                #    count_small = count_small + 1
                #    continue

                category = res[8]
                if category not in category_dic.keys():
                    category_dic[category] = int(id)
                    categories.append({
                        "supercategory": "none",
                        "id": id,
                        "name": category})
                    id +=1

                # clw note:之前版本
                #x = [points[i] for i in [0,2,4,6]]
                #y = [points[i] for i in [1,3,5,7]]
                #x_min,x_max = min(x),max(x)
                #y_min,y_max = min(y),max(y)
                annotations.append({
                    "segmentation":[[points[0],points[1],points[2],points[3],points[4],points[5],points[6],points[7]]],
                    "area":width*height,
                    "iscrowd":0,
                    "image_id":img_dic[txt_name[:-4]+'.png'],
                    #"bbox":[x_min,y_min,(x_max-x_min),(y_max-y_min)],
                    "bbox":[x_ctr, y_ctr, width, height, angle],
                    "category_id":category_dic[category],
                    "id":int(annid),
                    "ignore":0})
                annid +=1



jsonfile = {}
jsonfile['images'] = images
jsonfile['categories'] = categories
jsonfile['annotations'] = annotations
with open("/media/clwclw/Elements/deep_learning/competion/2019yaogan/train/train_crop_800/train.json",'w',encoding='utf-8') as f:
    json.dump(jsonfile,f)


