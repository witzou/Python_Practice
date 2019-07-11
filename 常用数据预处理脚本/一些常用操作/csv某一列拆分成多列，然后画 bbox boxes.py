# 2019钢筋 written by clw
# 利用pandas将csv文件某一列，如
#  Detection
#  10 20 30 40
#  拆分为
#  xmin  ymin  xmax  ymax
#    10      20     30       40

import os
import pandas as pd
import cv2
from PIL import Image


labels = pd.read_csv('./train_labels_small.csv')
#print(labels.head())


# clw note：提取字段名为' Detection'的列，并按空格或其他相应字符来分割提取
labels['xmin'] = labels[' Detection'].map(lambda x:x.split(' ')[0])
labels['ymin'] = labels[' Detection'].map(lambda x:x.split(' ')[1])
labels['xmax'] = labels[' Detection'].map(lambda x:x.split(' ')[2])
labels['ymax'] = labels[' Detection'].map(lambda x:x.split(' ')[3])
#print(labels.head())


def draw_boxes(image_name):  
    selected_value = labels[labels.ID == image_name]  #根据image_name，找到full_labels也就是上面表格的第一条记录
    img = cv2.imread('./images/{}'.format(image_name))  # clw note: 使用cv2的imread方法来加载图片，注意format函数的用法
                                                      #           这里的images/{}在下面调用的时候，相当于images/raccon1-1.jpg
    for index, row in selected_value.iterrows():
        #print(type(row['xmin']))
        #clw note：经过上面增加了xmin等四个字段后，得到的row['xmin']是str类型的，和raccoon中有区别，因此还需要转成int型
        img = cv2.rectangle(img, (int(row['xmin']), int(row['ymin'])), (int(row['xmax']), int(row['ymax'])), (0, 255, 0), 3)
    return img




img_path = 'C:/Users/Administrator/Desktop/images'
img_list =  os.listdir(img_path)
for img_file in img_list:
    if img_file.endswith(('.jpg','.png')):
        #pil_im = Image.fromarray(draw_boxes(img_file)) #用PIL库的Image模块中的fromarray函数来将数组转化为图片
        #pil_im.show()


        # clw note：如果需要连续显示图片，建议使用下面的方法！！！
        cv2.namedWindow("steer", 0);  #clw note：注意steer应该是窗口名，后面要保持一致！！
        cv2.resizeWindow("steer", 1024, 768); #clw note：如果图片太大显示器看不全，就缩放一下
        cv2.imshow('steer', draw_boxes(img_file))
        cv2.waitKey(0) # clw note：需要使用cv2.waitKey来保持窗口的显示，等待按键后切换图片