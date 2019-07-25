# -*- coding: utf-8 -*-
"""
在将多个csv文件拼接到一起的时候，可以用Python通过pandas包的read_csv和to_csv两个方法来完成。

这里不采用pandas.merge()来进行csv的拼接，而只是通过简单的文件的读取和附加方式的写入来完成拼接。
"""

import os
import pandas as pd

inputfile_dir = 'C:/Users/Administrator/Desktop/keras-retinanet/'
inputfile1 = inputfile_dir + 'our_labels.csv'
inputfile2 = inputfile_dir + 'Mall_labels.csv'
inputfile3 = inputfile_dir + 'Part_A_labels.csv'
inputfile4 = inputfile_dir + 'Part_B_labels.csv'
inputfile5 = inputfile_dir + 'UCSD_labels.csv'

outputfile = inputfile_dir + 'clw_merged_labels.csv'


#header=None表示原始文件数据没有列索引，这样的话read_csv会自动加上列索引
csv_file = pd.read_csv(inputfile1, header=None)
#header=0表示不保留列名，index=False表示不保留行索引，mode='a'表示附加方式写入，文件原有内容不会被清除
csv_file.to_csv(outputfile, mode='a', index=False, header=False)
print('clw:inputfile1 finish!')
    
csv_file = pd.read_csv(inputfile2, header=None)
csv_file.to_csv(outputfile, mode='a', index=False, header=False)
print('clw:inputfile2 finish!')

csv_file = pd.read_csv(inputfile3, header=None)
csv_file.to_csv(outputfile, mode='a', index=False, header=False)
print('clw:inputfile3 finish!')

csv_file = pd.read_csv(inputfile4, header=None)
csv_file.to_csv(outputfile, mode='a', index=False, header=False)
print('clw:inputfile4 finish!')

csv_file = pd.read_csv(inputfile5, header=None)
csv_file.to_csv(outputfile, mode='a', index=False, header=False)
print('clw:inputfile5 finish!')

print('clw:end!')