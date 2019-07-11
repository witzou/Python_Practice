# 来源：https://github.com/aBlueMouse/SomeCode/blob/10845f44faa7487f8c98d1b9e77b9fdd9369c731/baidu%20signboard/convert_to_coco_json.py

#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Author: hbchen
# @Time: 2018-01-29
# @Description: xml转换到coco数据集json格式

import os, sys, json

from xml.etree.ElementTree import ElementTree, Element

XML_PATH = "C:\\Users\\hbchen\\Desktop\\xml_test"
JSON_PATH = "C:\\Users\\hbchen\\Desktop\\record.json"
json_obj = {}
images = []
annotations = []
categories = []
categories_list = []
annotation_id = 1

def read_xml(in_path):
    '''读取并解析xml文件'''
    tree = ElementTree()
    tree.parse(in_path)
    return tree

def if_match(node, kv_map):
    '''判断某个节点是否包含所有传入参数属性
      node: 节点
      kv_map: 属性及属性值组成的map'''
    for key in kv_map:
        if node.get(key) != kv_map.get(key):
            return False
    return True

def get_node_by_keyvalue(nodelist, kv_map):
    '''根据属性及属性值定位符合的节点，返回节点
      nodelist: 节点列表
      kv_map: 匹配属性及属性值map'''
    result_nodes = []
    for node in nodelist:
        if if_match(node, kv_map):
            result_nodes.append(node)
    return result_nodes

def find_nodes(tree, path):
    '''查找某个路径匹配的所有节点
      tree: xml树
      path: 节点路径'''
    return tree.findall(path)

print "-----------------Start------------------"
xml_names = []
for xml in os.listdir(XML_PATH):
    xml_names.append(xml)

for xml in xml_names:
    tree = read_xml(XML_PATH + "\\" + xml)
    object_nodes = get_node_by_keyvalue(find_nodes(tree, "object"), {})
    if len(object_nodes) == 0:
        print xml, "no object"
        continue
    else:
        image = {}
        file_name = os.path.splitext(xml)[0];  # 文件名
        image["file_name"] = file_name + ".jpg"
        width_nodes = get_node_by_keyvalue(find_nodes(tree, "size/width"), {})
        image["width"] = int(width_nodes[0].text)
        height_nodes = get_node_by_keyvalue(find_nodes(tree, "size/height"), {})
        image["height"] = int(height_nodes[0].text)
        image["id"] = int(file_name)
        images.append(image)    #构建images

        name_nodes = get_node_by_keyvalue(find_nodes(tree, "object/name"), {})
        xmin_nodes = get_node_by_keyvalue(find_nodes(tree, "object/bndbox/xmin"), {})
        ymin_nodes = get_node_by_keyvalue(find_nodes(tree, "object/bndbox/ymin"), {})
        xmax_nodes = get_node_by_keyvalue(find_nodes(tree, "object/bndbox/xmax"), {})
        ymax_nodes = get_node_by_keyvalue(find_nodes(tree, "object/bndbox/ymax"), {})
       # print ymax_nodes
        for index, node in enumerate(object_nodes):
            annotation = {}
            segmentation = []
            bbox = []
            seg_coordinate = []     #坐标
            seg_coordinate.append(int(xmin_nodes[index].text))
            seg_coordinate.append(int(ymin_nodes[index].text))
            seg_coordinate.append(int(xmin_nodes[index].text))
            seg_coordinate.append(int(ymax_nodes[index].text))
            seg_coordinate.append(int(xmax_nodes[index].text))
            seg_coordinate.append(int(ymax_nodes[index].text))
            seg_coordinate.append(int(xmax_nodes[index].text))
            seg_coordinate.append(int(ymin_nodes[index].text))
            segmentation.append(seg_coordinate)
            width = int(xmax_nodes[index].text) - int(xmin_nodes[index].text)
            height = int(ymax_nodes[index].text) - int(ymin_nodes[index].text)
            area = width * height
            bbox.append(int(xmin_nodes[index].text))
            bbox.append(int(ymin_nodes[index].text))
            bbox.append(width)
            bbox.append(height)

            annotation["segmentation"] = segmentation
            annotation["area"] = area
            annotation["iscrowd"] = 0
            annotation["image_id"] = int(file_name)
            annotation["bbox"] = bbox
            annotation["category_id"] = int(name_nodes[index].text)
            annotation["id"] = annotation_id
            annotation_id += 1
            annotation["ignore"] = 0
            annotations.append(annotation)

            if int(name_nodes[index].text) in categories_list:
                pass
            else:
                categories_list.append(int(name_nodes[index].text))
                categorie = {}
                categorie["supercategory"] = "none"
                categorie["id"] = int(name_nodes[index].text)
                categorie["name"] = name_nodes[index].text
                categories.append(categorie)

json_obj["images"] = images
json_obj["type"] = "instances"
json_obj["annotations"] = annotations
json_obj["categories"] = categories

f = open(JSON_PATH, "w")
#json.dump(json_obj, f)
json_str = json.dumps(json_obj)
f.write(json_str)
print "------------------End-------------------"