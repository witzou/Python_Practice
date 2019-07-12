# -*- coding: utf-8 -*-
"""
Created on Sun Jan 27 21:50:18 2019

@author: clwclw
"""


import zipfile
import os
import numpy as np
import skimage.io as io
import matplotlib.pyplot as plt
import pylab
pylab.rcParams['figure.figsize'] = (8.0, 10.0)
import cv2



def buffer2array(Z, image_name):
    '''
    无需解压，直接获取图片数据
    
    参数
    ===========
    Z:: 图片数据是 ZipFile 对象
    '''
    buffer = Z.read(image_name)
    image = np.frombuffer(buffer, dtype="B")  # 将 buffer 转换为 np.uint8 数组
    img = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return img





# -------------------
try:       # pycocotools 已经加入了全局环境变量中
    from pycocotools.coco import COCO
except ModuleNotFoundError:
    import sys
    # 加载 COCO API 环境
    sys.path.append('D:\API\cocoapi\PythonAPI')
    from pycocotools.coco import COCO

root = 'C:/Users/clwclw/Desktop/coco'  # 你下载的 COCO 数据集所在目录

# 查看 images 下的图片, 格式如['test2014.zip','train2014.zip','val2014.zip]
#print(os.listdir(f'{root}/images'))


Z = zipfile.ZipFile(f'{root}/images/Part_A.zip')
#print(Z.namelist()[7])   # 查看一张图片的文件名  


img = buffer2array(Z, Z.namelist()[7])
print('图片的尺寸：', img.shape)  #输出形如：图片的尺寸： (480, 640, 3)



##### 获取标签信息（利用官方给定教程）
dataType = 'val' #clw note:验证集
annFile = '{}/annotations/clw_{}.json'.format(root, dataType)

# initialize COCO api for instance annotations
coco=COCO(annFile)  
##输出如下
#loading annotations into memory...
#Done (t=0.93s)
#creating index...
#index created!


##### COCO categories and supercategories
cats = coco.loadCats(coco.getCatIds())  #clw note:输出形如{'id': 1, 'supercategory': 'head', 'name': 'head'}
nms = [cat['name'] for cat in cats]
print('COCO categories: \n{}\n'.format(' '.join(nms)))
nms = set([cat['supercategory'] for cat in cats])
print('COCO supercategories: \n{}'.format(' '.join(nms)))

# get all images containing given categories, select one at random
catIds = coco.getCatIds(catNms=['head'])
imgIds = coco.getImgIds(catIds=catIds)
imgIds = coco.getImgIds(imgIds=[1])
img = coco.loadImgs(imgIds[np.random.randint(0, len(imgIds))])[0] #clw note:输出形如{'width': 720, 'id': 1, 'file_name': 'Part_A_IMG_74.jpg', 'height': 479}


###官方给的这个代码需要将图片数据集解压：
# load and display image
# use url to load image
# I = io.imread(img['coco_url'])
#I = io.imread('%s/images/%s/%s' % (dataDir, dataType, img['file_name']))
#plt.axis('off')
#plt.imshow(I)
#plt.show()


#####我们可以使用 zipfile 模块直接读取图片，而无须解压：
##### 载入和展示picture
val_z = zipfile.ZipFile('C:/Users/clwclw/Desktop/coco/images/Part_A.zip') 
img_flatten = np.frombuffer(val_z.read('%s' % (img['file_name'])), 'B')

img_cv = cv2.imdecode(img_flatten,cv2.IMREAD_ANYCOLOR)
#img_mx = mx.image.imdecode(val_z.read('%s' % (img['file_name']))).asnumpy()
# 或者直接使用 I = buffer2array(val_z, val_z.namelist()[8])
plt.axis('off')
#plt.imshow(I)
plt.imshow(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB))
plt.show()



##### 载入和展示annotations
plt.imshow(img_cv)
plt.axis('off')
annIds = coco.getAnnIds(imgIds=img['id'], catIds=catIds, iscrowd=None)
anns = coco.loadAnns(annIds)
coco.showAnns(anns)


print('clw:finish!')







#################################################################################
#  其他功能
#################################################################################


######4.4 载入人体关键点标注
#初始化人体关键点标注（person keypoints annotations）的 COCO api
#annFile = '{}/annotations/person_keypoints_{}.json'.format(dataDir, dataType)
#coco_kps = COCO(annFile)

####show：
#plt.imshow(I)
#plt.axis('off')
#ax = plt.gca()
#annIds = coco_kps.getAnnIds(imgIds=img['id'], catIds=catIds, iscrowd=None)
#anns = coco_kps.loadAnns(annIds)
#coco_kps.showAnns(anns)



#####4.5 载入和展示 caption annotations
#annFile = '{}/annotations/captions_{}.json'.format(dataDir, dataType)
#coco_caps = COCO(annFile)

##show：
#annIds = coco_caps.getAnnIds(imgIds=img['id'])
#anns = coco_caps.loadAnns(annIds)
#coco_caps.showAnns(anns)
#plt.imshow(I)
#plt.axis('off')
#plt.show()

#结果会输出该图片的描述如下：
#A couple of people riding waves on top of boards.
#a couple of people that are surfing in water
#A man and a young child in wet suits surfing in the ocean.
#a man and small child standing on a surf board  and riding some waves
#A young boy on a surfboard being taught to surf.



