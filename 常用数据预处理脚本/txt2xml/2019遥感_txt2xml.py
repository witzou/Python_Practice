import os
import scipy.misc as misc
from xml.dom.minidom import Document
import numpy as np
import copy, cv2


def save_to_xml(save_path, im_height, im_width, objects_axis, label_name, img_name = '000024.jpg'):
    im_depth = 0
    object_num = len(objects_axis)
    doc = Document()

    annotation = doc.createElement('annotation')
    doc.appendChild(annotation)

    folder = doc.createElement('folder')
    folder_name = doc.createTextNode('VOC2007')
    folder.appendChild(folder_name)
    annotation.appendChild(folder)

    filename = doc.createElement('filename')
    #filename_name = doc.createTextNode('000024.jpg')
    filename_name = doc.createTextNode(img_name) #clw modify
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
        difficult.appendChild(doc.createTextNode('0')) # clw note: TODO:后续可以考虑作为参数传进来，但是需要是np.array??仿照box传进来试试
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

    f = open(save_path, 'w')
    f.write(doc.toprettyxml(indent=''))
    f.close()


class_list = ['plane', 'baseball-diamond', 'bridge', 'ground-track-field',
              'small-vehicle', 'large-vehicle', 'ship',
              'tennis-court', 'basketball-court',
              'storage-tank', 'soccer-ball-field',
              'roundabout', 'harbor',
              'swimming-pool', 'helicopter',
              'helipad',  'airport', 'container-crane']


# 将txt中某一行数据组成np.array类型的bbox
def format_label(txt_list):
    format_data = []
    #for i in txt_list[2:]:   # clw note：DOTA原始数据前两行是其他信息，这里需要跳过
    for i in txt_list:
        format_data.append(
            #[int(xy) for xy in i.split(' ')[:8]] + [class_list.index(i.split(' ')[8])]
            [float(xy) for xy in i.split(' ')[:8]] + [class_list.index(i.split(' ')[8])] #clw modify
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
        if i.split(' ')[8] not in class_list:
            print ('warning found a new label :', i.split(' ')[8])
            exit()
    return np.array(format_data)


# main()
print ('class_list', len(class_list))
raw_data = 'H:/deep_learning/competion/2019yaogan/train/train_crop/' #clw note:for windows
raw_images_dir = os.path.join(raw_data, 'images_small-vehicle/') #clw note:for windows
raw_label_dir = os.path.join(raw_data, 'labelTxt_small-vehicle/') #clw note:for windows
#raw_data = '/home/clwclw/dataset/DOTA/train/'   # clw note： for Ubuntu
#raw_images_dir = os.path.join(raw_data, 'images_test/')
#raw_label_dir = os.path.join(raw_data, 'labelTxt_test/')
xml_dir = os.path.join(raw_data, 'Annotations_small-vehicle/')   # clw note：out，保存xml的路径
if not os.path.exists(xml_dir):
    os.makedirs(xml_dir)


images = [i for i in os.listdir(raw_images_dir) if 'png' in i]
labels = [i for i in os.listdir(raw_label_dir) if 'txt' in i]

print ('find image', len(images))
print ('find label', len(labels))

min_length = 1e10
max_length = 1

for idx, img in enumerate(images):
    # img = 'P1524.png'
    print (idx, 'read image', img)
    img_data = misc.imread(os.path.join(raw_images_dir, img))
    # img_data = cv2.imread(os.path.join(raw_images_dir, img))
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
    print('clw:box=', box)




#=======================================================================================
# clw modify : 尝试只将原来的txt转成xml，不做上面的clip_image()数据增强
#              clip_image()的作用是：随机crop图片然后生成crop后对应图片的xml
    print('clw：生成的xml文件路径为：', os.path.join(raw_label_dir, img.replace('png', 'xml')))
    print('clw：image_shape=', img_data.shape[0], 'x' , img_data.shape[1])
    save_to_xml(os.path.join(xml_dir, img.replace('png', 'xml')), img_data.shape[0], img_data.shape[1], box, class_list, img_name=img)  #clw modify
#=======================================================================================












