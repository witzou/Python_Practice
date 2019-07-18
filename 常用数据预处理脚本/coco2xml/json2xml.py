# 转自：https://github.com/hongge831/R2CNN_FPN_Tensorflow-insulator/blob/master/tools/json2xml.py

import os 
import json
from PIL import Image
from tqdm import tqdm
from xml.etree.ElementTree import ElementTree,Element  
src = r'D:/jyzdata/jyzbig/'
sampleSrc = r'D:/jyzdata/sample.xml'

fileList = os.listdir(src)
jsonFileList = [x for x in fileList if x.endswith('json') ]
#jsonFileList = jsonFileList[:3]
for jsonFile in tqdm(jsonFileList):
    #获取sample文件
    tree=ElementTree()  
    tree.parse(sampleSrc)  
    root=tree.getroot()
    print(jsonFile[:-5])
    with open(src+jsonFile) as f:
        temp = json.loads(f.read())
        imagePath = temp['imagePath']
        img = Image.open(src+imagePath)
        w,h = img.size
        boxNum = len(temp['shapes'])
        size = Element('size')
        width = Element('width')
        height = Element('height')
        depth = Element('depth')
        width.text = str(w)
        height.text = str(h)
        depth.text = '3'
        size.append(width)
        size.append(height)
        size.append(depth)
        fileName = Element('filename')
        fileName.text = imagePath
        root.append(size)
        root.append(fileName)
        for i in range(boxNum):
            element=Element('object') #指点里面是属性，结果展示：<train name="wang">  
            #创建二级目录  
            oneName=Element('name')  
            oneName.text = temp['shapes'][i]['label']#二级目录的值 #结果展示：<id>1</id>  
            onePose = Element('pose')
            onePose.text = 'Unknown'
            oneTruncated = Element('truncated')
            oneTruncated.text = '1'
            oneDifficult = Element('difficult')
            oneDifficult.text = '0'
            oneBndbox = Element('bndbox')
            twoX0 = Element('x0')
            twoY0 = Element('y0')
            twoX1 = Element('x1')
            twoY1 = Element('y1')
            twoX2 = Element('x2')
            twoY2 = Element('y2')
            twoX3 = Element('x3')
            twoY3 = Element('y3')
            twoX0.text = str(temp['shapes'][i]['points'][0][0])
            twoY0.text = str(temp['shapes'][i]['points'][0][1])
            twoX1.text = str(temp['shapes'][i]['points'][1][0])
            twoY1.text = str(temp['shapes'][i]['points'][1][1])
            twoX2.text = str(temp['shapes'][i]['points'][2][0])
            twoY2.text = str(temp['shapes'][i]['points'][2][1])
            twoX3.text = str(temp['shapes'][i]['points'][3][0])
            twoY3.text = str(temp['shapes'][i]['points'][3][1])
            oneBndbox.append(twoX0)
            oneBndbox.append(twoY0)
            oneBndbox.append(twoX1)
            oneBndbox.append(twoY1)
            oneBndbox.append(twoX2)
            oneBndbox.append(twoY2)
            oneBndbox.append(twoX3)
            oneBndbox.append(twoY3)
            element.append(oneName)
            element.append(onePose)
            element.append(oneTruncated)
            element.append(oneDifficult)
            element.append(oneBndbox)
            root.append(element)
#     tree.write('D:/jyzdata/jyzbigxml/'+jsonFile[:-5] + '.xml')
    tree.write(os.path.join('D:/jyzdata/jyzbigxml', jsonFile[:-5]+'.xml'),encoding='utf-8',xml_declaration=True)
#         with open(os.path.join('D:/jyzdata/jyzbigxml/', jsonFile[:-5]+'.xml'), 'w') as fh:
#             dom.writexml(fh)
#             print('写入name/pose OK!')