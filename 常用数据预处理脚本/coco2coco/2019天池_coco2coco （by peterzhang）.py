# 转自peterzhang，2019天池纺织品缺陷检测比赛论坛分享
# https://tianchi.aliyun.com/notebook-ai/detail?spm=5176.12586969.1002.18.43b46448pJMuYK&postId=74575
# 感觉官方coco数据集的构建不太直观，不太适合新手，我这里提供简约版，coco数据集主要是个dict类型，
# 有'images', 'annotations', 'type', 'categories'几个key, 相应填充即可

import json
from tqdm import tqdm
import cv2, os
from glob import glob
from collections import defaultdict

base_dirs = ['../../../data/guangdong/guangdong1_round1_train1_20190818/', 
            '../../../data/guangdong/guangdong1_round1_train2_20190828/']

mp = {"破洞": 1, "水渍": 2, "油渍": 2, "污渍": 2,  "三丝": 3, "结头": 4, "花板跳": 5, "百脚": 6, "毛粒": 7,
      "粗经": 8, "松经": 9, "断经": 10, "吊经": 11, "粗维": 12, "纬缩": 13, "浆斑": 14, "整经结": 15, "星跳": 16, "跳花": 16,
      "断氨纶": 17, "稀密档": 18, "浪纹档": 18, "色差档": 18, "磨痕": 19, "轧痕": 19, "修痕":19, "烧毛痕": 19, "死皱": 20,
      "云织": 20, "双纬": 20, "双经": 20, "跳纱": 20, "筘路": 20, "纬纱不良": 20
      }


def make_coco_traindataset(images2annos, name='train'):

    idx = 1
    image_id = 20190000000
    images = []
    annotations = []

    for im_name in tqdm(images2annos):

#         im = cv2.imread(base_dir + 'defect_Images/' + im_name)
#         h, w, _ = im.shape
        h, w = 1000, 2446
        image_id += 1
        image = {'file_name': im_name, 'width': w, 'height': h, 'id': image_id}
        images.append(image)

        annos = images2annos[im_name]
        for anno in annos:
            bbox = anno[:-1]
            seg = [bbox[0], bbox[1], bbox[0], bbox[3],
                   bbox[2], bbox[3], bbox[2], bbox[1]]

            bbox = [bbox[0], bbox[1], bbox[2] - bbox[0], bbox[3] - bbox[1]]
            anno_ = {'segmentation': [seg], 'area': bbox[2] * bbox[3], 'iscrowd': 0, 'image_id': image_id,
                   'bbox': bbox, 'category_id': anno[-1], 'id': idx, 'ignore': 0}
            idx += 1
            annotations.append(anno_)

    ann = {}
    ann['type'] = 'instances'
    ann['images'] = images
    ann['annotations'] = annotations
    category = [{'supercategory':'none', 'id': id, 'name': str(id)} for id in range(1, 21)]
    ann['categories'] = category
    json.dump(ann, open(base_dir + '{}.json'.format(name),'w'))

for idx, base_dir in enumerate(base_dir, 1):
    annos = json.load(open(base_dir + 'Annotations/anno_train.json'))
    images2annos = defaultdict(list)
    for anno in annos:
        images2annos[anno['name']].append(anno['bbox'] + [mp[anno['defect_name']]])
    make_coco_traindataset(images2annos, 'train' + str(idx))
