import os

path = 'I:/deep_learning/competion/2019yaogan/train_val/labelTxt_train_val/'
savepath = 'C:/Users/Administrator/Desktop/labelTxt_train_val_EAST/'

txt_name_list = os.listdir(path)       # 将路径下所有文件存成list
txt_count = 0
for txt_name in txt_name_list:
    txt_count += 1
    print('clw: txt_name = ', txt_name)
    with open(path + txt_name, 'r') as f1:
        with open(savepath + txt_name, 'w') as f2:
            result = ""
            txt_data = f1.readlines()
            for line in txt_data[2:]: # clw note：从第二行开始读
                line_data = line.split(' ')
                for i in range(7):
                    result += line_data[i]
                    result += ','
                result += line_data[7]
                result += '\n'
                f2.write(result)

print('clw: end!')
print('clw: txt_count = ', txt_count)