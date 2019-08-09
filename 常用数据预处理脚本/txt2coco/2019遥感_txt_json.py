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


                # clw note: COCO默认是水平矩形框,但这里是四边形框,而且顺时针或逆时针都不一定,因此考虑使用cv2,先转成矩形框,然后在获取左上角开始的依次四个坐标
                # 而且对于RRPN, 要加入角度信息; 这里直接整合成x_ctr, y_ctr, width,height,angle
                # rect = cv2.minAreaRect(np.array([[float(points[0]), float(points[1])], [float(points[2]), float(points[3])],
                #                                  [float(points[4]), float(points[5])], [float(points[6]), float(points[7])]]))
                rect = cv2.minAreaRect(np.float32([[points[0], points[1]], [points[2], points[3]],
                                                 [points[4], points[5]], [points[6], points[7]]]))
                box = cv2.boxPoints(rect)  # 获取最小外接矩形的4个顶点坐标
                box = np.round(box)  # clw note: 顺时针标注,顺序不一定是右下角, 左下角,左上角,右上角!

                ##################################################
                # clw modify: 保证bbox是左上角作为起点,然后逆时针为顺序
                List = [
                    {"lat": float(box[0][0]), "lng": float(box[0][1])},
                    # clw note:这里lat是纬度的意思,应该是y,不过我当成x处理了...一个道理其实
                    {"lat": float(box[1][0]), "lng": float(box[1][1])},
                    {"lat": float(box[2][0]), "lng": float(box[2][1])},
                    {"lat": float(box[3][0]), "lng": float(box[3][1])}
                ]
                import math

                mlat = sum(x['lat'] for x in List) / len(List)
                mlng = sum(x['lng'] for x in List) / len(List)

                def algo(x):
                    return (math.atan2(x['lat'] - mlat, x['lng'] - mlng) + 2 * math.pi) % (
                            2 * math.pi)  # 以质心为原点，将坐标转化为极坐标，求出角度

                List.sort(key=algo, reverse=True)  # 从大到小排序,注意上面是arctan(x/y),如果是arctan(y/x),则很容易得到
                # 角度从大到小依次为:右下,左下,左上,右上;
                # 而这里是x/y,根据坐标轴改一下,就是左上,左下,右下,右上;
                # 而这里不仅x/y,而且xy坐标轴的正向和数学常用的又是不一样的
                # 只需根据,x负y正是0,x负y负是1,x正y负是2,x正y正是3(最小角度),推算出实际List0~3对应是左下,左上,右上,右下.

                pt1 = (List[1]["lat"], List[1]["lng"])  # 左上角
                pt2 = (List[2]["lat"], List[2]["lng"])  # 右上角,角度最小
                pt3 = (List[3]["lat"], List[3]["lng"])  # 右下角,角度最大
                pt4 = (List[0]["lat"], List[0]["lng"])  # 左下角,角度第二大

                # 右下角x坐标一定比左上或左下大
                assert List[3]["lat"] >= List[1]["lat"] and List[3]["lat"] >= List[0]["lat"]

                # 左上角x坐标一定比右上小(不一定比左下大)
                assert List[1]["lat"] <= List[2]["lat"]

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


