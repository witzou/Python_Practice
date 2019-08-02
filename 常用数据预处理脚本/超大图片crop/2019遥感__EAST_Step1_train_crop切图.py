import os
import scipy.misc as misc
from xml.dom.minidom import Document
import numpy as np
import copy, cv2

from PIL import Image
Image.MAX_IMAGE_PIXELS = None  #clw note：防止一些非常大的图片（~1G）处理不了，超过MAX_IMAGE_PIXELS上限导致报错


class_list = ['plane', 'baseball-diamond', 'bridge', 'ground-track-field',
'small-vehicle', 'large-vehicle', 'ship',
'tennis-court', 'basketball-court',
'storage-tank', 'soccer-ball-field',
'roundabout', 'harbor',
'swimming-pool', 'helicopter',
'helipad',  'airport', 'container-crane' #clw modify
]

cropped_width = 512 # clw modify 20190706
cropped_height = 512
step = 384  # clw note：这里实际上不是overlap，而是图片尺寸-overlap，即步进长度

#raw_data = 'C:/Users/Administrator/Desktop/'
#raw_data = 'E:/deep_learning/competion/2019yaogan/train_val/'
raw_data = 'H:/deep_learning/competion/2019yaogan/train/'  # clw note：主要就是配置好训练集的路径
save_dir = raw_data + 'train_crop/'  # clw note：out

### 原始训练集输入为图片和txt格式的label，输出为crop的images及对应的labelTxt(.txt)和Annotation(.xml)
raw_images_dir = os.path.join(raw_data, 'images')  # clw note：in
raw_label_dir = os.path.join(raw_data, 'labelTxt')  # clw note：in'



if not os.path.exists(save_dir): # clw note：如果没有该文件夹，则建立
    os.makedirs(save_dir)
if not os.path.exists(os.path.join(save_dir + 'images')): # clw note：如果没有该文件夹，则建立
    os.makedirs(os.path.join(save_dir + 'images'))
if not os.path.exists(os.path.join(save_dir + 'Annotations')):  # clw note：如果没有该文件夹，则建立
    os.makedirs(os.path.join(save_dir + 'Annotations'))

### 保存为xml文件 ###
def save_to_xml(save_path, im_height, im_width, objects_axis, label_name, img_name):
    im_depth = 3
    object_num = len(objects_axis)
    doc = Document()

    annotation = doc.createElement('annotation')
    doc.appendChild(annotation)

    folder = doc.createElement('folder')
    folder_name = doc.createTextNode('VOC2007')
    folder.appendChild(folder_name)
    annotation.appendChild(folder)

    filename = doc.createElement('filename')
    filename_name = doc.createTextNode(img_name)
    filename.appendChild(filename_name)
    annotation.appendChild(filename)

    source = doc.createElement('source')
    annotation.appendChild(source)

    database = doc.createElement('database')
    database.appendChild(doc.createTextNode('The VOC2007 Database'))
    source.appendChild(database)

    annotation_s = doc.createElement('annotation')
    annotation_s.appendChild(doc.createTextNode('PASCAL VOC2007'))
    source.appendChild(annotation_s)

    image = doc.createElement('image')
    image.appendChild(doc.createTextNode('flickr'))
    source.appendChild(image)

    flickrid = doc.createElement('flickrid')
    flickrid.appendChild(doc.createTextNode('322409915'))
    source.appendChild(flickrid)

    owner = doc.createElement('owner')
    annotation.appendChild(owner)

    flickrid_o = doc.createElement('flickrid')
    flickrid_o.appendChild(doc.createTextNode('knautia'))
    owner.appendChild(flickrid_o)

    name_o = doc.createElement('name')
    name_o.appendChild(doc.createTextNode('yang'))
    owner.appendChild(name_o)


    size = doc.createElement('size')
    annotation.appendChild(size)
    width = doc.createElement('width')
    width.appendChild(doc.createTextNode(str(im_width)))
    height = doc.createElement('height')
    height.appendChild(doc.createTextNode(str(im_height)))
    depth = doc.createElement('depth')
    depth.appendChild(doc.createTextNode(str(im_depth)))
    size.appendChild(width)
    size.appendChild(height)
    size.appendChild(depth)
    segmented = doc.createElement('segmented')
    segmented.appendChild(doc.createTextNode('0'))
    annotation.appendChild(segmented)
    for i in range(object_num):
        objects = doc.createElement('object')
        annotation.appendChild(objects)
        object_name = doc.createElement('name')
        object_name.appendChild(doc.createTextNode(label_name[int(objects_axis[i][-1])]))
        objects.appendChild(object_name)
        pose = doc.createElement('pose')
        pose.appendChild(doc.createTextNode('Unspecified'))
        objects.appendChild(pose)
        truncated = doc.createElement('truncated')
        truncated.appendChild(doc.createTextNode('1'))
        objects.appendChild(truncated)
        difficult = doc.createElement('difficult')
        difficult.appendChild(doc.createTextNode('0'))
        objects.appendChild(difficult)
        bndbox = doc.createElement('bndbox')
        objects.appendChild(bndbox)
        
        x0 = doc.createElement('x0')
        x0.appendChild(doc.createTextNode(str((objects_axis[i][0]))))
        bndbox.appendChild(x0)
        y0 = doc.createElement('y0')
        y0.appendChild(doc.createTextNode(str((objects_axis[i][1]))))
        bndbox.appendChild(y0)

        x1 = doc.createElement('x1')
        x1.appendChild(doc.createTextNode(str((objects_axis[i][2]))))
        bndbox.appendChild(x1)
        y1 = doc.createElement('y1')
        y1.appendChild(doc.createTextNode(str((objects_axis[i][3]))))
        bndbox.appendChild(y1)
        
        x2 = doc.createElement('x2')
        x2.appendChild(doc.createTextNode(str((objects_axis[i][4]))))
        bndbox.appendChild(x2)
        y2 = doc.createElement('y2')
        y2.appendChild(doc.createTextNode(str((objects_axis[i][5]))))
        bndbox.appendChild(y2)

        x3 = doc.createElement('x3')
        x3.appendChild(doc.createTextNode(str((objects_axis[i][6]))))
        bndbox.appendChild(x3)
        y3 = doc.createElement('y3')
        y3.appendChild(doc.createTextNode(str((objects_axis[i][7]))))
        bndbox.appendChild(y3)
        
    f = open(save_path,'w')
    f.write(doc.toprettyxml(indent = ''))
    f.close() 
####################################################################


### 保存为txt文件 ###
def save_to_txt(save_path, objects_axis, label_name):
    object_num = len(objects_axis)
    with open(save_path, 'w') as f:
        f.write('imagesource:GoogleEarth\n')
        f.write('gsd:None\n')
        for i in range(object_num):
            object_name = label_name[int(objects_axis[i][-1])]
            difficult = '0'
            x0 = str((objects_axis[i][0]))
            y0 = str((objects_axis[i][1]))
            x1 = str((objects_axis[i][2]))
            y1 = str((objects_axis[i][3]))
            x2 = str((objects_axis[i][4]))
            y2 = str((objects_axis[i][5]))
            x3 = str((objects_axis[i][6]))
            y3 = str((objects_axis[i][7]))
            str_line = x0 + ' ' + y0 + ' ' + x1 + ' ' + y1 + ' ' + x2 + ' ' + y2 + ' ' + x3 + ' ' + y3 + ' ' + \
                       object_name + ' ' + difficult + '\n'
            f.write(str_line)
####################################################################


### 格式化标签 ###
def format_label(txt_list):
    format_data = []
    for i in txt_list[2:]:
        format_data.append(
        #[int(xy) for xy in i.split(' ')[:8]] + [class_list.index(i.split(' ')[8])]
        [float(xy) for xy in i.split(' ')[:8]] + [class_list.index(i.split(' ')[8])]  #clw modify
        # {'x0': int(i.split(' ')[0]),
        # 'x1': int(i.split(' ')[2]),
        # 'x2': int(i.split(' ')[4]),
        # 'x3': int(i.split(' ')[6]),
        # 'y1': int(i.split(' ')[1]),
        # 'y2': int(i.split(' ')[3]),
        # 'y3': int(i.split(' ')[5]),
        # 'y4': int(i.split(' ')[7]),
        # 'class': class_list.index(i.split(' ')[8]) if i.split(' ')[8] in class_list else 0, 
        # 'difficulty': int(i.split(' ')[9])}
        )
        if i.split(' ')[8] not in class_list :
            print ('warning found a new label :', i.split(' ')[8])
            exit()
    return np.array(format_data)
#######################################################################


### 裁剪图片 ###
def clip_image(file_idx, image, boxes_all, width, height):
    # print ('image shape', image.shape)
    if len(boxes_all) > 0:
        shape = image.shape         #比如有一张1235*1143的图，下面start_h的范围是(0,1143-800+256)，每次步进256；也就是说会取到0,256和512
                                    #但是下面还有一步判断start_w + width > shape[1]，在取512的时候会大于，因此用start_w_new = shape[1] - width来修正
                                    #修正后512变成了343；所以在h=0的时候会crop3个图：分别在w取0,256和343的位置；
                                    #同理，h也会在每个w位置crop3个图，因此一共会crop3*3=9张图片，用于之后的训练；

        #for start_h in range(0, shape[0] - cropped_height + 256, 256):  # clw note:这里配置h或w方向每次移动多少距离再crop，这里是256个像素，
        #for start_w in range(0, shape[1] - cropped_width + 256, 256): #比如开始从左上角(0,0)开始crop个800*800的图，之后移动到(256, 0)再crop800*800的图
        # clw note：上面的写法还是有问题，无法把小于800*800的图留下来！
		# 暂时还是先用下面这种，即使有些地方会重复抠图，总数量还是一样的，会覆盖
        #for start_h in range(0, shape[0], 256):
            #for start_w in range(0, shape[1], 256):
        for start_h in range(0, shape[0], step):
            for start_w in range(0, shape[1], step):
                #boxes = copy.deepcopy(boxes_all)
                boxes = copy.deepcopy(boxes_all)  #如果比如最后剩100，不足256，那么就少移动156，然后也把它作为一个800*800的图给crop出来。之后转到下一行的最左侧重新crop
                box = np.zeros_like(boxes_all)
                start_h_new = start_h
                start_w_new = start_w
                if start_h + height > shape[0]:
                  start_h_new = shape[0] - height
                if start_w + width > shape[1]:
                  start_w_new = shape[1] - width
                top_left_row = max(start_h_new, 0)
                top_left_col = max(start_w_new, 0)
                bottom_right_row = min(start_h + height, shape[0])
                bottom_right_col = min(start_w + width, shape[1])

                subImage = image[top_left_row:bottom_right_row, top_left_col: bottom_right_col]

                box[:, 0] = boxes[:, 0] - top_left_col  # clw note：对box位置进行修正
                box[:, 2] = boxes[:, 2] - top_left_col
                box[:, 4] = boxes[:, 4] - top_left_col
                box[:, 6] = boxes[:, 6] - top_left_col

                box[:, 1] = boxes[:, 1] - top_left_row
                box[:, 3] = boxes[:, 3] - top_left_row
                box[:, 5] = boxes[:, 5] - top_left_row
                box[:, 7] = boxes[:, 7] - top_left_row
                box[:, 8] = boxes[:, 8]
                center_y = 0.25*(box[:, 1] + box[:, 3] + box[:, 5] + box[:, 7])
                center_x = 0.25*(box[:, 0] + box[:, 2] + box[:, 4] + box[:, 6])
                # print('center_y', center_y)
                # print('center_x', center_x)
                # print ('boxes', boxes)
                # print ('boxes_all', boxes_all)
                # print ('top_left_col', top_left_col, 'top_left_row', top_left_row)

                cond1 = np.intersect1d(np.where(center_y[:] >=0 )[0], np.where(center_x[:] >=0 )[0])
                cond2 = np.intersect1d(np.where(center_y[:] <= (bottom_right_row - top_left_row))[0],
                                        np.where(center_x[:] <= (bottom_right_col - top_left_col))[0])
                idx = np.intersect1d(cond1, cond2)  # clw note：找到crop的图片内含有的box，不能超出crop的图片范围。。
                # idx = np.where(center_y[:]>=0 and center_x[:]>=0 and center_y[:] <= (bottom_right_row - top_left_row) and center_x[:] <= (bottom_right_col - top_left_col))[0]
                # save_path, im_width, im_height, objects_axis, label_name
                if len(idx) > 0:
                    xml = os.path.join(save_dir, 'Annotations', "%s_%05d_%05d.xml" % (file_idx, top_left_row, top_left_col)) #clw note:有些遥感图片是20000*20000的，4位表示不了，故写成了%05d。。
                    txt = os.path.join(save_dir, 'labelTxt', "%s_%05d_%05d.txt" % (file_idx, top_left_row, top_left_col))
                    img = os.path.join(save_dir, 'images', "%s_%05d_%05d.png" % (file_idx, top_left_row, top_left_col))
                    img_name = img.split('\\')[-1]
                    #print('clw: cropped_img_name = ', img_name)
                    save_to_xml(xml, subImage.shape[0], subImage.shape[1], box[idx, :], class_list, img_name)
                    # save_to_txt(txt, box[idx, :], class_list)  # clw modify: 可选
                    cv2.imwrite(img, subImage)
########################################################3



### 主函数 ###
images = [i for i in os.listdir(raw_images_dir) if 'png' in i]
labels = [i for i in os.listdir(raw_label_dir) if 'txt' in i]

print ('find image', len(images))
print ('find label', len(labels))

min_length = 1e10
max_length = 1

print ('class_list', len(class_list))

for idx, img in enumerate(images):
# img = 'P1524.png'
    print (idx, 'read image', img)
    # img_data = misc.imread(os.path.join(raw_images_dir, img))
    img_data = cv2.imread(os.path.join(raw_images_dir, img))
    # if len(img_data.shape) == 2:
        # img_data = img_data[:, :, np.newaxis]
        # print ('find gray image')

    txt_data = open(os.path.join(raw_label_dir, img.replace('png', 'txt')), 'r').readlines()
    # print (idx, len(format_label(txt_data)), img_data.shape)
    # if max(img_data.shape[:2]) > max_length:
        # max_length = max(img_data.shape[:2])
    # if min(img_data.shape[:2]) < min_length:
        # min_length = min(img_data.shape[:2])
    # if idx % 50 ==0:
        # print (idx, len(format_label(txt_data)), img_data.shape)
        # print (idx, 'min_length', min_length, 'max_length', max_length)
    box = format_label(txt_data)
    clip_image(img.strip('.png'), img_data, box, cropped_width, cropped_height)
    
    
    
    

#     rm train/images/*   &&   rm train/labeltxt/*

    
    
    








