#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2019/1/23 17:40
# @Author    : humeme
# @Site      : retoo
# @File      : DOTA_xml2txt.py
# @Software: PyCharm

import os
import json
import xml.etree.ElementTree as xml_tree
import glob

#xml_path = "C:/Users/Administrator/Desktop/Annotations/"
xml_path = "I:/deep_learning/competion/2019yaogan/train_val/train_val_crop/Annotations/"
txt_path = "C:/Users/Administrator/Desktop/labelTxt_train_val_EAST/"
files = glob.glob(xml_path + '*.xml')

##################### 可以统计一下label的数量
back_ground = 0
roundabout = 0
tennis_court = 0
swimming_pool = 0
storage_tank = 0
soccer_ball_field = 0
small_vehicle = 0
ship = 0
plane = 0
large_vehicle = 0
helicopter = 0
harbor = 0
ground_track_field = 0
bridge = 0
basketball_court = 0
baseball_diamond = 0
helipad = 0
airport = 0
container_crane = 0
#############################

file_count = 0
#### 开始转换
for file in files:  # clw note：对文件夹里面的所有xml文件：
    direct = file.replace("\\","/").split("/")[-1].replace("xml","txt")
    with open(os.path.join(txt_path + direct), "w") as f:
        #content = xml.loads(open(file, "r"))
        tree = xml_tree.parse(file)
        root = tree.getroot()

        # clw modify：add filename
        #filename = str(root.find('filename').text)
        #filename = filename.split('.')[0]

        # Image shape.
        size = root.find('size')
        shape = [int(size.find('height').text),
                 int(size.find('width').text),
                 int(size.find('depth').text)]
        # Find annotations.
        difficult = []
        truncated = []
        for obj in root.findall('object'):
            label = str(obj.find('name').text)
            #print('clw: label = ', label)  # clw modify
            if(label == 'back_ground'):
                back_ground += 1
            elif(label == 'roundabout'):
                roundabout += 1
            elif(label == 'tennis-court'):
                tennis_court += 1
            elif(label == 'swimming-pool'):
                swimming_pool += 1
            elif(label == 'storage-tank'):
                storage_tank += 1
            elif(label == 'soccer-ball-field'):
                soccer_ball_field += 1
            elif(label == 'small-vehicle'):
                small_vehicle += 1
            elif(label == 'ship'):
                ship += 1
            elif(label == 'plane'):
                plane += 1
            elif(label == 'large-vehicle'):
                large_vehicle += 1
            elif(label == 'helicopter'):
                helicopter += 1
            elif(label == 'harbor'):
                harbor += 1
            elif(label == 'ground-track-field'):
                ground_track_field += 1
            elif(label == 'bridge'):
                bridge += 1
            elif(label == 'basketball-court'):
                basketball_court += 1
            elif(label == 'baseball-diamond'):
                baseball_diamond += 1
            elif(label == 'helipad'):
                helipad += 1
            elif(label == 'airport'):
                airport += 1
            elif(label == 'container-crane'):
                container_crane += 1


            isdifficult = obj.find('difficult')
            if isdifficult is not None:
                difficult.append(int(isdifficult.text))
            else:
                difficult.append(0)

            istruncated = obj.find('truncated')
            if istruncated is not None:
                truncated.append(int(istruncated.text))
            else:
                truncated.append(0)
            #bbox1 = list(obj.find ('bndbox').find("points_x").text.strip().split(",")[0:4])
            #bbox2 = list(obj.find ('polygen').find("points_y").text.strip().split(",")[0:4])
            #box = list(zip(bbox1, bbox2))

            x0 = str(obj.find('bndbox').find("x0").text)  # clw modify
            y0 = str(obj.find('bndbox').find("y0").text)  # clw modify
            x1 = str(obj.find('bndbox').find("x1").text)  # clw modify
            y1 = str(obj.find('bndbox').find("y1").text)  # clw modify
            x2 = str(obj.find('bndbox').find("x2").text)  # clw modify
            y2 = str(obj.find('bndbox').find("y2").text)  # clw modify
            x3 = str(obj.find('bndbox').find("x3").text)  # clw modify
            y3 = str(obj.find('bndbox').find("y3").text)  # clw modify

            # clw note: convert float to int
            x0 = int(float(x0))
            y0 = int(float(y0))
            x1 = int(float(x1))
            y1 = int(float(y1))
            x2 = int(float(x2))
            y2 = int(float(y2))
            x3 = int(float(x3))
            y3 = int(float(y3))


            #str1 = "{},{},{},{},{},{},{},{},{}".format(int_float(box[0][0]), int_float(box[0][1]), int_float(box[1][0]), int_float(box[1][1]), \
            #                                           int_float(box[2][0]),int_float(box[2][1]), int_float(box[3][0]), int_float(box[3][1]),
            #                                           label)
            str1 = "{},{},{},{},{},{},{},{},{}".format(x0, y0, x1, y1, x2, y2, x3, y3, label)
            f.write (str1 + "\n")
    f.close()

    file_count += 1
    print('clw: file_count = ', file_count)


print('clw: back_ground = ',back_ground)
print('clw: roundabout = ',roundabout)
print('clw: tennis_court = ',tennis_court)
print('clw: swimming_pool = ',swimming_pool)
print('clw: storage_tank = ',storage_tank)
print('clw: soccer_ball_field = ',soccer_ball_field)
print('clw: small_vehicle = ',small_vehicle)
print('clw: ship = ',ship)
print('clw: plane = ',plane)
print('clw: large_vehicle = ',large_vehicle)
print('clw: helicopter = ',helicopter)
print('clw: harbor = ',harbor)
print('clw: ground_track_field = ',ground_track_field)
print('clw: bridge = ',bridge)
print('clw: basketball_court = ',basketball_court)
print('clw: baseball_diamond = ',baseball_diamond)
print('clw: helipad = ',helipad)
print('clw: airport = ',airport)
print('clw: container_crane = ',container_crane)

print ("clw: ---------------------success!---------------------")