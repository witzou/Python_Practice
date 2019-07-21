# coding = utf-8
import os
import time
data_path = './labelTxt'
result_path = './labelTxt_preprocessed'

### 找到数据集的所有.txt文件名
def find_all_txts(data_path):
    txts = []
    data_files = os.listdir(data_path)
    for filename in data_files:
        if filename.endswith('.txt'):
            txts.append(filename)
    return txts

### 去掉某一文件夹中所有.txt文件的空行
def clearBlankLine():
    if not os.path.exists(result_path):
        os.makedirs(result_path)

    file_list = find_all_txts(data_path)
    #print(file_list)
    for file_name in file_list:
        with open(data_path + '/' + file_name, 'r') as f_read:
            with open(result_path + '/' + file_name, 'w') as f_write: # 生成没有空行的文件
                for line in f_read.readlines():
                    if len(line) == 0:
                        break
                    if line.count('\n') == len(line):
                        continue
                    f_write.write(line)

if __name__ == '__main__':
    time_start = time.time();
    clearBlankLine()
    time_end = time.time();
    print('clw：time use: ', time_end - time_start)
