import numpy as np
import cv2

def back_forward_convert(coordinate, with_label=True):
    """
    :param coordinate: format [x1, y1, x2, y2, x3, y3, x4, y4, (label)]
    :param with_label: default True
    :return: format [x_c, y_c, w, h, theta, (label)]
    """

    boxes = []
    if with_label:
        for rect in coordinate: # 比如coordinate是[[10, 10, 20, 10, 20, 20, 10, 20, '3']]
            box = np.int0(rect[:-1]) # 最后一个值是label对应的index，这里坐标换算要把index如'3'去掉；
            box = box.reshape([4, 2])  # reshape成四边形的4个顶点的坐标形式，比如[[10 10]
                                       #                                      [20 10]
                                       #                                      [20 20]
                                       #                                      [10 20]]
            print(box)
            rect1 = cv2.minAreaRect(box)  # 生成最小外接矩形，返回一个Box2D结构rect：
                                          # （最小外接矩形的中心（x，y），（宽度，高度），旋转角度）
                                          # 如用上面的输入，会输出((15.0, 15.0), (10.0, 10.0), -90.0)
                                          # 旋转角度θ是水平轴（x轴）逆时针旋转，与碰到的矩形的第一条边的夹角
            print('clw: rect1 = ', rect1)
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

r_box = back_forward_convert([[10, 10, 20, 10, 20, 20, 10, 20, '3']])
print('clw: r_box = ', r_box)