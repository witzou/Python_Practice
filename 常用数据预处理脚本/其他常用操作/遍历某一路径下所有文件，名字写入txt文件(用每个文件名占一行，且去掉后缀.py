import os
path = 'C:/Users/Administrator/Desktop/1'
savepath = 'C:/Users/Administrator/Desktop/'
image_name = os.listdir(path)       # 将路径下所有文件存成list
f = open(savepath + 'file_list.txt', 'w')  #
for temp in image_name:
    if temp.endswith('.txt'):
        f.write(temp.replace('.txt','\n')) # 去掉.xxx后缀，并用换行符代替
f.close()