## 思路：crop后存在images和Annotations两个文件夹，分别装.png和.xml文件
## 所以第一步先把所有xml转回成txt，然后

import os
import json
import xml.etree.ElementTree as xml_tree
import glob

label_extract = 'small-vehicle'
xml_path = 'H:/deep_learning/competion/2019yaogan/train/train_crop/Annotations/'  # clw note：Step 1的in
txt_path = 'H:/deep_learning/competion/2019yaogan/train/train_crop/labelTxt_' + label_extract + '/'  # clw note：Step 1的out，Step 2的in
img_path = 'H:/deep_learning/competion/2019yaogan/train/train_crop/images/'  # clw note：Setp 2的in
save_path = 'H:/deep_learning/competion/2019yaogan/train/train_crop/images_' + label_extract + '/'  # clw note：Step 2的out
save_path_xml = 'H:/deep_learning/competion/2019yaogan/train/train_crop/Annotations_' + label_extract + '/'

# Step 1:
# xml转txt，主要从DOTA的txt中抽取某一类物体，如'small-vehicle'等，组成新的只针对某一类的数据集
def xml2txt():

    #xml_path = "C:/Users/Administrator/Desktop/Annotations/"


    files = glob.glob(xml_path + '*.xml')


    ##################### 可以统计一下label的数量
    label_count = 0
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
                label_count += 1
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

    print('clw: label_count = ',label_count)
    print ("clw: ---------------------success!---------------------")


# Step 2:
# 提取某一文件夹下txt文件名对应的图片，以及xml（可选）
def extract_img_by_txt_name():
    import os, shutil

    # 找到Step 1生成的所有txt文件，如果img_path中有txt对应名字的图片，就把文件拷贝到save_path下

    if not os.path.exists(save_path):
        os.makedirs(save_path)
    if not os.path.exists(save_path_xml):
        os.makedirs(save_path_xml)

    txt_name_list = os.listdir(txt_path)
    print(txt_path)

    img_count = 0
    xml_count = 0
    i = 0
    for txt_name in txt_name_list:
        # 如果图片存在
        img_name = txt_name.split('.')[0] + '.png'
        #print('clw:img_name = ', img_name)
        if os.path.exists(img_path + img_name):
            # 则拷贝到另外一个文件夹内
            shutil.copy(img_path + img_name, save_path + img_name)
            img_count += 1

        # xml_name = txt_name.split('.')[0] + '.xml'
        # #print('clw:xml_name = ', xml_name)
        # if os.path.exists(xml_path + xml_name):
        #     # 则拷贝到另外一个文件夹内
        #     shutil.copy(xml_path + xml_name, save_path_xml + xml_name)
        #     xml_count += 1

        i += 1
        print('clw：已处理图片数量：', i)

    print('clw: img_count = ', img_count)
    # print('clw: xml_count = ', xml_count)

def main():
    #xml2txt()
    extract_img_by_txt_name()



main()