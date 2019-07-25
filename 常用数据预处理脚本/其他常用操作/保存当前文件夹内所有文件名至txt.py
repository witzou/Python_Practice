# -*- coding: utf-8 -*-
"""
Created on Thu Dec 27 11:56:27 2018

@author: Administrator
"""
import os

image_path = './annotations'

with open('xmllist.txt', 'a+') as f:
    for filename in os.listdir(image_path):              #listdir的参数是文件夹的路径
        #print(filename)                                  #此时的filename是文件夹中文件的名称
        f.write(filename + '\n')

print('clw:end!')
