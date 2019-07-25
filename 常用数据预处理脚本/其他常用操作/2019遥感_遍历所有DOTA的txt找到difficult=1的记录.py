import os
path = 'C:/Users/Administrator/Desktop/labelTxt/'
txt_name_list = os.listdir(path)       # 将路径下所有文件存成list
for txt_name in txt_name_list:
    with open(path + txt_name, 'r') as f1:
        #print(txt_name)
        # 如果置信度小于某一值，则不写入该行
        for line in f1:
            #print(line)
            line_list = line.strip().split(' ')
            #print(line_list[9])
            if line_list[9] == '1':
                print('clw: difficult = 1, txt_name = ',  txt_name)
            elif line_list[9] == '0':
                print('clw: difficult = 0, txt_name = ',  txt_name)
