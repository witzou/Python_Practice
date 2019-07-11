# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 11:17:34 2019

@author: Administrator
"""

import numpy as np
import matplotlib.pyplot as plt  
# 李宏毅原代码没有加载相关参数，以上为我自行加载的。
 
x_data = [338, 333, 328, 207, 226, 25, 179, 60, 208, 606]
y_data = [640, 633,619, 393, 428, 27, 193, 66, 226, 1591]
 
x = np.arange(-200, -100, 1) # bias，一共100个数，注意不包括-100
y = np.arange(-5, 5, 0.1)    # weights，一共100个数
Z = np.zeros((len(x), len(y))) # 100*100
X,Y = np.meshgrid(x, y) # 生成所有网格点(x,y)对应的坐标矩阵
for i in range(len(x)):
    for j in range(len(y)):
        b = x[i]
        w = y[j]
        Z[j][i] = 0
        for n in range(len(x_data)):
            Z[j][i] = Z[j][i] + (y_data[n] - b - w*x_data[n])**2
        Z[j][i] = Z[j][i]/len(x_data)
 
# yadata = b + w*xdata
b = -120 # intial b
w = -4 # intial w
lr = 0.000001 # learning rate
iteration = 100000
 
# store initial values for plotting
b_history = [b]
w_history = [w]
 
lr_b = 0
lr_w = 0

# iterations
for i in range(iteration):
 
    b_grad = 0.0
    w_grad = 0.0
    for n in range(len(x_data)):
        b_grad = b_grad - 2.0 * (y_data[n] - b - w*x_data[n]) * 1.0
        w_grad = w_grad - 2.0 * (y_data[n] - b - w*x_data[n]) * x_data[n]
 
    lr_b = lr_b + b_grad ** 2
    lr_w = lr_w + w_grad ** 2
                    
    # update parameters
    b = b - lr * b_grad
    w = w - lr * w_grad
             
    # update parameters：自注，这里使用Adam方法，可以更快收敛到最优点
    #                         可以对比一下上面的update parameters方式
    #b = b - 1/np.sqrt(lr_b) * b_grad
    #w = w - 1/np.sqrt(lr_w) * w_grad
 
    # store parameters for plotting
    b_history.append(b)
    w_history.append(w)
 
# plot the figure
plt.contourf(x, y, Z, 50, alpha=0.5, cmap=plt.get_cmap('jet'))
#contour和contourf都是画三维等高线图的，
#不同点在于contourf会对等高线间的区域进行填充

plt.plot([-188.4], [2.67], 'x', ms=10, marker=6, color='orange')
# marker代表指定点的图标style，也可以写成'o'等
# ms代表指定点图标大小。

plt.plot(b_history, w_history, 'o-', ms=5, lw=1, color='black')
# 绘制每一次w_history和b_history的变化情况
# lw代表线宽

plt.xlim(-200, -100) #x轴的绘制区间，当然也可以不写
plt.ylim(-5, 5) #y轴的绘制区间，当然也可以不写
plt.xlabel(r'$b$', fontsize=16) 
plt.ylabel(r'$w$', fontsize=16)
plt.show()
