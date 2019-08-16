import os

img_path = '/media/clwclw/data/2018yuncong/Part_B/train_data/'

count = 0
for filename in os.listdir(img_path): #listdir的参数是文件夹的路径4
    print(filename)
    assert filename.endswith(('jpg','png','jpeg','bmp'))  # 如果有不是图片的文件,报错
    tmp_list = filename.split('.')
    os.rename(os.path.join(img_path, filename), os.path.join(img_path, tmp_list[0] + '_Part_B' + tmp_list[1]))
    count += 1
    print('clw: image count = ', count)
