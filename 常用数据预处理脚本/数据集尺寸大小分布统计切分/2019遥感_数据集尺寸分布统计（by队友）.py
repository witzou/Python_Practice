# ! /usr/bin/env python
# -*- coding:utf-8 -*-

# @author: Edison Jia-hao-Chen
# time: 2019-7-31
# email: JiahaoChen@whu.edu.cn

# Dataset: 遥感稀疏表征比赛数据集
# 分成两类：大目标、小目标


import os
# from competition.utils.FileReader import read_files
# import numpy as np
# import cv2


def read_files(file_path: object = '', file_type: object = '.json') -> object:
    file_list = os.listdir(file_path)
    file_list.sort()
    file_list = [file for file in file_list if file.endswith(file_type)]
    return file_list


categories = ('airport', 'baseball-diamond', 'basketball-court', 'bridge', 'container-crane', 'ground-track-field',
              'harbor', 'helicopter', 'helipad', 'large-vehicle', 'plane', 'roundabout', 'ship', 'small-vehicle',
              'soccer-ball-field', 'storage-tank', 'swimming-pool', 'tennis-court')
categories_id = [0] * len(categories)


class DivideDotaDataset(object):
    def __init__(self, gt_label='./', outdir='./', thres=32*32):
        # input:
        #   gt_label: gt label path
        #   outdir: output dir path
        #        small objects: [outdir]/smallObj/
        #        large objects: [outdir]/largeObj/
        #   thres: area threshold (small or large)
        #          (default: 32*32)

        self.gt_path = gt_label
        self.outdir = outdir
        self.thres = thres
        self.label_type = {'s': 'smallObj', 'l': 'largeObj'}

        self._main()

    def _load_txt(self, label_name='P0000.txt'):
        boxes_list = []
        bbox_p1_p2 = []
        bbox_small = []
        bbox_large = []
        x_idx = (0, 2, 4, 6)
        y_idx = (1, 3, 5, 7)
        with open(self.gt_path + label_name, 'r') as f:
            idx = 0
            for line in f:
                if line is '\n':
                    continue
                if idx > 1:
                    line = line.split()
                    # print(line)
                    line[: -2] = [int(float(line[i])) for i in range(len(line) - 2)]
                    line[-1] = int(line[-1])
                    x_arr = [line[i] for i in x_idx]
                    y_arr = [line[i] for i in y_idx]
                    # if line[-2] == 'plane':
                    #     raise Exception(idx)
                    bbox_p1_p2.append([min(x_arr), min(y_arr), max(x_arr), max(y_arr), categories.index(line[-2])])
                    boxes_list.append(line)

                    area = (max(x_arr) - min(x_arr)) * (max(y_arr) - min(y_arr))
                    if area > self.thres:
                        bbox_large.append(line)
                    else:
                        bbox_small.append(line)
                idx += 1
        return boxes_list, bbox_p1_p2, bbox_large, bbox_small

    def _create_newlabel(self, bbox, lb_type='s', label_name='P0000.txt'):
        file_dir = os.path.join(self.outdir, self.label_type[lb_type])
        if not os.path.isdir(file_dir):
            os.mkdir(file_dir)
        with open(file_dir + '/' + label_name, 'a') as f:
            print(self.label_type[lb_type], bbox)
            for line in bbox:
                print(line)
                str1 = ' '.join('%s' % item for item in line)
                str1 += '\n'
                f.write(str1)

    def _main(self):
        label_list = read_files(self.gt_path, '.txt')
        for label in label_list:
            _1, _2, bbox_large, bbox_small = self._load_txt(label)
            self._create_newlabel(bbox_large, 'l', label)
            self._create_newlabel(bbox_small, 's', label)


if __name__ == '__main__':
    d = DivideDotaDataset()


