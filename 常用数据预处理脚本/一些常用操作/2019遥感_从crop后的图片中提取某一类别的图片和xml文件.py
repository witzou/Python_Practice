## 思路：crop后存在images和Annotations两个文件夹，分别装.png和.xml文件
## 所以第一步先把所有xml转回成txt，然后

import os
import json
import xml.etree.ElementTree as xml_tree
import glob

# Step 1:
# xml转txt，主要从DOTA的txt中抽取某一类物体，如'small-vehicle'等，组成新的只针对某一类的数据集
def xml2txt():
    label_extract = 'helipad'
    #xml_path = "C:/Users/Administrator/Desktop/Annotations/"
    xml_path = "F:/deep_learning/competion/2019yaogan/train_val/train_val_crop/Annotations/"
    txt_path = "F:/deep_learning/competion/2019yaogan/train_val/train_val_crop/labelTxt_" + label_extract + '/'
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
        for obj in root.findall('object'):
            label = str(obj.find('name').text)
            #print('clw: label = ', label)  # clw modify

            if label == label_extract:
                helipad += 1
                with open(os.path.join(txt_path + direct), "a") as f:
                    isdifficult = obj.find('difficult')
                    if isdifficult is not None:
                        difficult = int(isdifficult.text)
                    else:
                        difficult = 0

                    istruncated = obj.find('truncated')
                    if istruncated is not None:
                        truncated = int(istruncated.text)
                    else:
                        truncated = 0
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
                    x0 = float(x0)
                    y0 = float(y0)
                    x1 = float(x1)
                    y1 = float(y1)
                    x2 = float(x2)
                    y2 = float(y2)
                    x3 = float(x3)
                    y3 = float(y3)


                    #str1 = "{},{},{},{},{},{},{},{},{}".format(int_float(box[0][0]), int_float(box[0][1]), int_float(box[1][0]), int_float(box[1][1]), \
                    #                                           int_float(box[2][0]),int_float(box[2][1]), int_float(box[3][0]), int_float(box[3][1]),
                    #                                           label)
                    str1 = "{} {} {} {} {} {} {} {} {} {}".format(x0, y0, x1, y1, x2, y2, x3, y3, label, difficult)
                    f.write (str1 + "\n")

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


# Step 2:
# 提取某一文件夹下txt文件名对应的图片
def extract_img_by_txt_name():
    import os, shutil

    txt_path = 'F:/deep_learning/competion/2019yaogan/train_val/train_val_crop/labelTxt/'
    img_path = 'F:/deep_learning/competion/2019yaogan/train_val/train_val_crop/images/'
    save_path = 'F:/deep_learning/competion/2019yaogan/train_val/train_val_crop/images_extract/'
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    txt_name_list = os.listdir(txt_path)
    print(txt_path)

    img_count = 0
    for txt_name in txt_name_list:
        # 如果图片存在
        img_name = txt_name.split('.')[0] + '.png'
        print('clw:img_name = ', img_name)
        if os.path.exists(img_path + img_name):
            # 则拷贝到另外一个文件夹内
            shutil.copy(img_path + img_name, save_path + img_name)
            img_count += 1

    print('clw: img_count = ', img_count)


def main():
    #xml2txt()
    extract_img_by_txt_name()



main()