
# 检查路径下面是否都是文件
for filename in os.listdir(path):
    if not os.path.isfile(path + '/' + filename):
        print(filename)
        
# 检查路径下面是否都是文件夹    
for filename in os.listdir(path):
    if not os.path.isdir(path + '/' + filename):
        print(filename)