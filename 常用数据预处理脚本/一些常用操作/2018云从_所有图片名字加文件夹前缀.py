#import os
#
#img_path = 'C:/Users/Administrator/Desktop/keras-yolo2/our/train/0/'
#
#for filename in os.listdir(img_path): #listdir的参数是文件夹的路径4
#
#
#    print(filename) #此时的filename是文件夹中文件的名称
#    os.rename(os.path.join(img_path, filename), os.path.join(img_path, '0_' + filename))

import os

img_path = 'C:/Users/Administrator/Desktop/keras-retinanet/Part_B/'

for filename in os.listdir(img_path): #listdir的参数是文件夹的路径4
    print(filename)
    if '.jpg' in filename:
        os.rename(os.path.join(img_path, filename), os.path.join(img_path, img_path.split('/')[-2] + '_' + filename))
    else:
        for imagename in os.listdir(img_path + filename):
            print(imagename) #此时的filename是文件夹中文件的名称
            os.rename(os.path.join(img_path+ filename, imagename), os.path.join(img_path + filename, filename + '_' + imagename))