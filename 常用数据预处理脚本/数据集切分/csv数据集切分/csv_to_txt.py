# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import pandas as pd
np.random.seed(1)

full_labels = pd.read_csv('data/raccoon_labels.csv') #clw note:将csv文件读取到一个DataFrame中，shape为(217, 8)
                                                     #         虽然只有200张图片，但由于个别图片有多个raccoon，
                                                     #         因此会有会有217条(>200)的记录； 8代表表格的columns
print(full_labels.head())


grouped = full_labels.groupby('filename')  
a=grouped.apply(lambda x: len(x))  #clw note:a是一个包含200条记录的Series，因为有200张图片
                                   #        该函数的作用在于，统计含有同一'filename'的记录
                                   #        因此如果某张图片含有2只raccoon，则该filename对应的值即为2
b=a.value_counts()   # 统计含有n只raccoon的图片总数，这里1只raccoon有184张，2只有15张，3只1张，之前的1*184+2*15+3=217
print(b)

grouped_list = [grouped.get_group(x) for x in grouped.groups] #clw note:汇总成200个DataFrame，对于只有1只raccon的图
                                                              #         该DataFrame只有1条记录，否则会有多余一条...
                

train_index = np.random.choice(len(grouped_list), size=160, replace=False) #clw note：size=160相当于2:8分测试集
test_index = np.setdiff1d(list(range(200)), train_index) #clw note:在len(grouped_list)中，除了train_index
                                                         #         剩下的都给到中，除了test_index

with open('train.txt', 'w') as f:
    for index in train_index:
        #print('raccoon-' + str(index) + '.jpg')
        f.write('raccoon-' + str(index+1)) #clw note:这里没加.jpg，只是文件名
                                      #加1是因为index范围是0-199而实际xml是1-200
        if not index == train_index[-1]:
            f.write('\n')

        
with open('eval.txt', 'w') as f:  
    for index in test_index:
        #print('raccoon-' + str(index))
        f.write('raccoon-' + str(index+1)) 
        if not index == test_index[-1]:
            f.write('\n')



#train = pd.concat([grouped_list[i] for i in train_index])
#test = pd.concat([grouped_list[i] for i in test_index])