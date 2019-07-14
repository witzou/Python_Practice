### 参考https://github.com/humeme/json2txt_and_xml2txt/blob/master/json2txt/json2txt.py 具体格式也可以参考一下

import os
import json
import glob
import numpy as np
path = "C:/D-text/Demo/_01_code/_02_python/_01_freTime_test/json2txt/X01json/"
path1="C:/D-text/Demo/_01_code/_02_python/_01_freTime_test/json2txt/x02txt/"
files = glob.glob(path+"*.json")
for file in files:
    name = file.replace("\\","/").split("/")[-1].replace("json","txt")
    with open(os.path.join(path1+name), "w") as f:  #"C:/D-text/Demo/_01_code/_02_python/_01_freTime_test/json2txt/X01json/"
        content = json.load(open(file, "r"))
        label1 = "20181211JB"
        label2 = "172912G2"
        box1 = np.array(content["shapes"][0]["points"])
        box2 = np.array(content["shapes"][1]["points"])
        str1 = "{},{},{},{},{},{},{},{},{}".format(box1[0,0],box1[0,1],box1[1,0],box1[1,1],box1[2,0],box1[2,1],box1[3,0],box1[3,1],label1)
        str2 = "{},{},{},{},{},{},{},{},{}".format(box2[0, 0], box2[0, 1], box2[1, 0], box2[1, 1], box2[2, 0],
                                                   box2[2, 1], box2[3, 0], box2[3, 1], label2)
        f.write(str1 + "\n")
        f.write(str2 + "\n")
    f.close()
print ("success")
