import os
path = 'C:/Users/Administrator/Desktop/test/'
savepath = 'C:/Users/Administrator/Desktop/test_clw/'
txt_name_list = os.listdir(path) # 将路径下所有文件存成list
for txt_name in txt_name_list:
	print(txt_name)
	with open(path + txt_name, 'r') as f1:
		with open(savepath + txt_name, 'w') as f2:
			# 如果置信度小于某一值，则不写入该行
			for line in f1:
				list = line.split(' ')
				if not float(list[1]) < 0.2:
				f2.write(line)