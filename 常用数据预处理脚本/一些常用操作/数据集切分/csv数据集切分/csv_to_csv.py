# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import pandas as pd
np.random.seed(1)

full_labels = pd.read_csv('UCSD_labels.csv')  #clw note：在这里修改需要split的csv路径
print(full_labels.head())

grouped = full_labels.groupby('filename')
a=grouped.apply(lambda x: len(x))
b=a.value_counts()
#print(b)

gb = full_labels.groupby('filename')
grouped_list = [gb.get_group(x) for x in gb.groups]
                
#grouped_list的长度代表了图片的总数；注意区分图片数和csv的记录数。 0.8表示二八开，切分验证集
train_index = np.random.choice(len(grouped_list), size=int(len(grouped_list)*0.8), replace=False)
test_index = np.setdiff1d(list(range(len(grouped_list))), train_index)

train = pd.concat([grouped_list[i] for i in train_index])
test = pd.concat([grouped_list[i] for i in test_index])

train.to_csv('train_labels.csv', index=None)
test.to_csv('test_labels.csv', index=None)

print('clw:finish!')