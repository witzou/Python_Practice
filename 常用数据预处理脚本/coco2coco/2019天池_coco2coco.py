# for maskrcnn benchmark， written by 队友 chenjiahao and 本人
# 总共要改三个地方: 1 图片路径 2 json文件路径 3 保存json的路径
import os
import cv2
import json
import numpy as np
img_dic = {}
category_dic = {}

img_and_anno_root = '/mfs/home/fangyong/data/guangdong/train/'
#img_folder = 'C:/Users/Administrator/Desktop/defect_Images/'
img_folder = img_and_anno_root + 'defect_Images/'
file_list = os.listdir(img_folder)
id = 1
images = []
categories = []
annotations = []

#####################################################
NEED_ORDER = True  # clw note:如果需要保持一定的顺序,比如官方给了1代表person,2代表plane,最好用下面的方式;
                   # 反之如果没有顺序要求,或者只有一类物体如head,那么可以让 NEED_ORDER = False
                   # 中文转Unicode地址:http://tool.chinaz.com/tools/unicode.aspx
if NEED_ORDER:
    my_categories = ['\u7834\u6d1e', '\u6c34\u6e0d', '\u6cb9\u6e0d', '\u6c61\u6e0d',
                  '\u4e09\u4e1d', '\u7ed3\u5934', '\u82b1\u677f\u8df3', '\u767e\u811a', '\u6bdb\u7c92',
                  '\u7c97\u7ecf', '\u677e\u7ecf', '\u65ad\u7ecf', '\u540a\u7ecf', '\u7c97\u7ef4',
                  '\u7eac\u7f29', '\u6d46\u6591', '\u6574\u7ecf\u7ed3', '\u661f\u8df3', '\u8df3\u82b1',
                  '\u65ad\u6c28\u7eb6', '\u7a00\u5bc6\u6863', '\u6d6a\u7eb9\u6863', '\u8272\u5dee\u6863', '\u78e8\u75d5',
                  '\u8f67\u75d5', '\u4fee\u75d5', '\u70e7\u6bdb\u75d5', '\u6b7b\u76b1', '\u4e91\u7ec7',
                  '\u53cc\u7eac', '\u53cc\u7ecf', '\u8df3\u7eb1', '\u7b58\u8def', '\u7eac\u7eb1\u4e0d\u826f']
    for i in range(len(my_categories)):
        category_dic[my_categories[i]] = i + 1
        categories.append({
            "supercategory": "none",
            "id": i + 1,
            "name": my_categories[i]})
        i += 1
#####################################################

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
#annFile = 'C:/Users/Administrator/Desktop/Annotations/gt_result.json'
annFile = img_and_anno_root + 'Annotations/anno_train.json'
file = open(annFile, "rb")
data_list = json.load(file)
data_list = sorted(data_list,key = lambda e:e['name'],reverse = True)
######################################################

# 取出data中相应文件名的文件
print('clw:total bbox number: ', len(data_list))
for data in data_list:
    print('clw:bbox id: ', annid)
    x_min = data['bbox'][0]
    y_min = data['bbox'][1]
    x_max = data['bbox'][2]
    y_max = data['bbox'][3]
    category = data['defect_name']
    #################################################
    if not NEED_ORDER:
        if category not in category_dic.keys():
            category_dic[category] = int(id)
            categories.append({
                "supercategory": "none",
                "id": id,
                "name": category})
            id += 1
    ################################################
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
with open(img_and_anno_root + "Annotations/train.json",'w',encoding='utf-8') as f:
    json.dump(jsonfile,f)

print('clw:category_dic = ', category_dic)
print('clw:end!')
