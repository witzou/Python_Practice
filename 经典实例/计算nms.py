# --------------------------------------------------------
# Fast R-CNN
# Copyright (c) 2015 Microsoft
# Licensed under The MIT License [see LICENSE for details]
# Written by Ross Girshick
# --------------------------------------------------------

import numpy as np

def py_cpu_nms(dets, thresh):
    """Pure Python NMS baseline."""
    x1 = dets[:, 0]                     # pred bbox top_x
    y1 = dets[:, 1]                     # pred bbox top_y
    x2 = dets[:, 2]                     # pred bbox bottom_x
    y2 = dets[:, 3]                     # pred bbox bottom_y
    scores = dets[:, 4]              # pred bbox cls score

    areas = (x2 - x1 + 1) * (y2 - y1 + 1)    # pred bbox areas
    order = scores.argsort()[::-1]              # 对pred bbox按score做降序排序，对应step-2

    keep = []    # NMS后，保留的pred bbox
    while order.size > 0:
        i = order[0]          # top-1 score bbox
        keep.append(i)   # top-1 score的话，自然就保留了
        xx1 = np.maximum(x1[i], x1[order[1:]])   # top-1 bbox（score最大）与order中剩余bbox计算NMS
        yy1 = np.maximum(y1[i], y1[order[1:]])
        xx2 = np.minimum(x2[i], x2[order[1:]])
        yy2 = np.minimum(y2[i], y2[order[1:]])

        w = np.maximum(0.0, xx2 - xx1 + 1)
        h = np.maximum(0.0, yy2 - yy1 + 1)
        inter = w * h
        ovr = inter / (areas[i] + areas[order[1:]] - inter)      # 无处不在的IoU计算~~~

        inds = np.where(ovr <= thresh)[0]     # 这个操作可以对代码断点调试理解下，结合step-3，我们希望剔除所有与当前top-1 bbox IoU > thresh的冗余bbox，那么保留下来的bbox，自然就是ovr <= thresh的非冗余bbox，其inds保留下来，作进一步筛选
        order = order[inds + 1]   # 保留有效bbox，就是这轮NMS未被抑制掉的幸运儿，为什么 + 1？因为ind = 0就是这轮NMS的top-1，剩余有效bbox在IoU计算中与top-1做的计算，inds对应回原数组，自然要做 +1 的映射，接下来就是step-4的循环

    return keep    # 最终NMS结果返回

if __name__ == '__main__':
    dets = np.array([[100,120,170,200,0.98],
                     [20,40,80,90,0.99],
                     [20,38,82,88,0.96],
                     [200,380,282,488,0.9],
                     [19,38,75,91, 0.8]])

    py_cpu_nms(dets, 0.5)