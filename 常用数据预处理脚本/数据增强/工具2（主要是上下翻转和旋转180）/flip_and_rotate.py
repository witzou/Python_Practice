# 转自peterzhang，2019天池纺织品缺陷检测比赛论坛分享 
# https://tianchi.aliyun.com/notebook-ai/detail?spm=5176.12586969.1002.18.43b46448pJMuYK&postId=74575
# 大佬：本次数据尺度固定，又不涉及自然场景，非常适合上下反转，旋转180等操作，这里提供一种不借助第三方增强工具的方法，更高阶可采用albumentations等工具
# 网友提问：得出来vflip和rotate的数据集后怎么和原来的数据集的json叠加呢？
# 大佬回答：mmdet里（自注：就是config文件夹下某个.py配置文件里面）写个list就行了，
# train=dict( type=dataset_type, ann_file=[data_root + 'x1.json', data_root + 'x2.json'], 
# img_prefix=[data_root + 'x1/', data_root + 'x2/' ] pipeline=train_pipeline) 有多少数据集，在list里加就完事了，ann_file和img_prefix对应好就行
# 大佬回答2：180度的增强没问题，我自己也是这样用的，做完数据之后可以用cocoapi可视化一下，确保没问题

import os, json
from PIL import Image, ImageDraw
from tqdm import tqdm
base_dir = '../../../data/guangdong/' # path to your data dir


def vflip(dataset, path, name):
    save_dir = path + 'defect_Images_vflip'
    os.makedirs(save_dir, exist_ok=True)
    for img_info in tqdm(dataset['images']):
        img = Image.open(os.path.join(path, 'defect_Images', img_info['file_name']))
        img = img.transpose(1)
        img.save(os.path.join(save_dir, img_info['file_name']))

    image_id2wh = {i['id']: [i['width'], i['height']] for i in dataset['images']}

    for anno_info in tqdm(dataset['annotations']):
        w, h = image_id2wh[anno_info['image_id']]
        anno_info['bbox'][1] = h - anno_info['bbox'][1] - anno_info['bbox'][3]

        for idx, seg in enumerate(anno_info['segmentation'][0]):
            if idx % 2 == 1:
                anno_info['segmentation'][0][idx] = h - seg

    json.dump(dataset, open(path + '{}_vflip.json'.format(name),'w'))


def rotate180(dataset, path, name):
    save_dir = path + 'defect_Images_rotate180'
    os.makedirs(save_dir, exist_ok=True)
    for img_info in tqdm(dataset['images']):
        img = Image.open(os.path.join(path, 'defect_Images', img_info['file_name']))
        img = img.transpose(3)
        img.save(os.path.join(save_dir, img_info['file_name']))

    image_id2wh = {i['id']: [i['width'], i['height']] for i in dataset['images']}

    for anno_info in dataset['annotations']:
        w,h = image_id2wh[anno_info['image_id']]
        anno_info['bbox'] = [w - anno_info['bbox'][0] - anno_info['bbox'][2], 
                             h - anno_info['bbox'][1] - anno_info['bbox'][3] , 
                             anno_info['bbox'][2], 
                             anno_info['bbox'][3]]
        
        for idx, seg in enumerate(anno_info['segmentation'][0]):
            if idx % 2 == 1:
                anno_info['segmentation'][0][idx-1], anno_info['segmentation'][0][idx] = \
                w- anno_info['segmentation'][0][idx-1], 
                h - anno_info['segmentation'][0][idx]
                
    json.dump(dataset, open(path + '{}_rotate180.json'.format(name), 'w'))

path = '../../../data/guangdong/guangdong1_round1_train1_20190818/'
name = 'train1'
dataset = json.load(open(path + '{}.json'.format(name)))
vflip(dataset, path, name)
rotate180(dataset, path, name)

path = '../../../data/guangdong/guangdong1_round1_train2_20190828/'
name = 'train2'
dataset = json.load(open(path + '{}.json'.format(name)))
vflip(dataset, path, name)
rotate180(dataset, path, name)