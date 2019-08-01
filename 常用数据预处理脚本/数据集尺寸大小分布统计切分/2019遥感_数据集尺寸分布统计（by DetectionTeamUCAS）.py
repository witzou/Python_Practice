# clw note：参考
# https://github.com/DetectionTeamUCAS/RetinaNet_Tensorflow_Rotation/blob/b03a7eafba21bfbb78dbffe1be53ab914080201e/data/io/DOTA/size_distribution.py
# https://github.com/DetectionTeamUCAS/RetinaNet_Tensorflow_Rotation/blob/b03a7eafba21bfbb78dbffe1be53ab914080201e/libs/box_utils/coordinate_convert.py

import os
import sys
import numpy as np
import cv2

sys.path.append('../../..')
#from libs.box_utils.coordinate_convert import backward_convert


class_list = ['plane', 'baseball-diamond', 'bridge', 'ground-track-field',
              'small-vehicle', 'large-vehicle', 'ship',
              'tennis-court', 'basketball-court',
              'storage-tank', 'soccer-ball-field',
              'roundabout', 'harbor',
              'swimming-pool', 'helicopter']

distribution = {}


#######
# clw note：从上面第2个网址里面搬过来的
def backward_convert(coordinate, with_label=True):
    """
    :param coordinate: format [x1, y1, x2, y2, x3, y3, x4, y4, (label)]
    :param with_label: default True
    :return: format [x_c, y_c, w, h, theta, (label)]
    """

    boxes = []
    if with_label:
        for rect in coordinate:
            box = np.int0(rect[:-1])
            box = box.reshape([4, 2])
            rect1 = cv2.minAreaRect(box)

            x, y, w, h, theta = rect1[0][0], rect1[0][1], rect1[1][0], rect1[1][1], rect1[2]
            boxes.append([x, y, w, h, theta, rect[-1]])

    else:
        for rect in coordinate:
            box = np.int0(rect)
            box = box.reshape([4, 2])
            rect1 = cv2.minAreaRect(box)

            x, y, w, h, theta = rect1[0][0], rect1[0][1], rect1[1][0], rect1[1][1], rect1[2]
            boxes.append([x, y, w, h, theta])

    return np.array(boxes, dtype=np.float32)
	
def format_label(txt_list):
    format_data = []
    for i in txt_list[2:]:
        format_data.append(
            [int(xy) for xy in i.split(' ')[:8]] + [class_list.index(i.split(' ')[8])]
        )
        if i.split(' ')[8] not in class_list:
            print('warning found a new label :', i.split(' ')[8])
            exit()
    return np.array(format_data)
################3###

print('class_list', len(class_list))
raw_data = '/data/DOTA/train/'
raw_images_dir = os.path.join(raw_data, 'images', 'images')
raw_label_dir = os.path.join(raw_data, 'labelTxt')

save_dir = '/data/DOTA/DOTA_TOTAL/train800/'

images = [i for i in os.listdir(raw_images_dir) if 'png' in i]
labels = [i for i in os.listdir(raw_label_dir) if 'txt' in i]

print('find image', len(images))
print('find label', len(labels))

min_length = 1e10
max_length = 1

for idx, img in enumerate(images):
    img_data = cv2.imread(os.path.join(raw_images_dir, img))

    txt_data = open(os.path.join(raw_label_dir, img.replace('png', 'txt')), 'r').readlines()
    box = format_label(txt_data)
    box = backward_convert(box)
    for b in box:
        if class_list[int(b[-1])] not in distribution:
            distribution[class_list[int(b[-1])]] = {'s': 0, 'm': 0, 'l': 0}
        if np.sqrt(b[2] * b[3]) < 32:
            distribution[class_list[int(b[-1])]]['s'] += 1
        elif np.sqrt(b[2] * b[3]) < 96:
            distribution[class_list[int(b[-1])]]['m'] += 1
        else:
            distribution[class_list[int(b[-1])]]['l'] += 1
print(distribution)

