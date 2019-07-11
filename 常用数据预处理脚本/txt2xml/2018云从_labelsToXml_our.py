from xml.etree import ElementTree
from xml.dom import minidom
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import csv
import xml.etree.cElementTree as ET
import os
from PIL import Image  #clw modify

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent='  ') #或者'\t'也行

def writeToXml(imageName, imageSize, imagePath, allCellInfo, outputFile):
	""" Makes xml-labels for one image

		Args:
		imageName: Filename of image
		imageSize: [width, height]
		imagePath: Path to image
		allCellInfo: [[name1, xmin1, ymin1, xmax1, ymax1], ..., [nameN, xminN, yminN, xmaxN, ymaxN]]
		outputFile:  xml output-file
	"""

	root = Element('annotation')
	root.set('verified', 'no')

	folder = SubElement(root, 'folder')
	folder.text = 'WBC'   #clw note：这里可以根据情况进行修改，不过貌似用不到
	filename = SubElement(root, 'filename')
	filename.text = imageName
	path = SubElement(root, 'path')
	path.text = imagePath
	source = SubElement(root, 'source')
	database = SubElement(source, 'database')
	database.text = 'Unknown'
	size = SubElement(root, 'size')
	width = SubElement(size, 'width')
	width.text = str(imageSize[0])
	height = SubElement(size, 'height')
	height.text = str(imageSize[1])
	depth = SubElement(size, 'depth')
	depth.text = '3'
	segmented = SubElement(root, 'segmented')
	segmented.text = "0"

	for cell in allCellInfo:
         for i in range(len(cell)//5): #clw modify 20181226:可能一幅图里有n个box，因此稍作修改
             #name_str, xmin_str, ymin_str, xmax_str, ymax_str = cell

             #clw modify 20181226:云从的数据是(x,y,w,h)，考虑转换为xmin,ymin,xmax,ymax
             objectTag = SubElement(root, 'object')
             name = SubElement(objectTag, 'name')
             name.text = cell[i*5]
             pose = SubElement(objectTag, 'pose')
             pose.text = 'Unspecified'
             truncated = SubElement(objectTag, 'truncated')
             truncated.text = '0'
             difficult = SubElement(objectTag, 'difficult')
             difficult.text = '0'
             bndbox = SubElement(objectTag, 'bndbox')
             xmin = SubElement(bndbox, 'xmin')
             xmin.text = cell[i*5+1]
             ymin = SubElement(bndbox, 'ymin')
             ymin.text = cell[i*5+2]
             xmax = SubElement(bndbox, 'xmax')
             xmax.text = str(int(cell[i*5+1]) + int(cell[i*5+3]))
             ymax = SubElement(bndbox, 'ymax')
             ymax.text = str(int(cell[i*5+2]) + int(cell[i*5+4]))

#	    name_str, xmin_str, ymin_str, xmax_str, ymax_str = cell
#	    objectTag = SubElement(root, 'object')
#	    name = SubElement(objectTag, 'name')
#	    name.text = name_str
#	    pose = SubElement(objectTag, 'pose')
#	    pose.text = 'Unspecified'
#	    truncated = SubElement(objectTag, 'truncated')
#	    truncated.text = '0'
#	    difficult = SubElement(objectTag, 'difficult')
#	    difficult.text = '0'
#	    bndbox = SubElement(objectTag, 'bndbox')
#	    xmin = SubElement(bndbox, 'xmin')
#	    xmin.text = xmin_str
#	    ymin = SubElement(bndbox, 'ymin')
#	    ymin.text = ymin_str
#	    xmax = SubElement(bndbox, 'xmax')
#	    xmax.text = xmax_str
#	    ymax = SubElement(bndbox, 'ymax')
#	    ymax.text = ymax_str


	pretty_str = prettify(root) #clw note:执行美化方法，输出str类型的值
	#print(pretty_str)  

	#tree = ET.ElementTree(root)          
	#tree.write(outputFile)
	open(outputFile, 'w').write(pretty_str) #clw note:直接输出prettify后的str到xml文件

def getOldLabels(oldLabelFile):
	# Get old labels
	allOldLabels = []
	allImageNumbers = []
	imageNum = 0
	with open(oldLabelFile, 'r') as oldLabels:
		for line in oldLabels:
			cells = []
			thisLine = line.replace(" ", "").split(',');
			if thisLine[1].isdigit():
			  index = int(line.split(',')[1])
			  for i in range(2,len(thisLine)):
			    cells.append(thisLine[i].strip('\n').replace('"', '')) # Remove end of line and " before appening to cells
			  # Skip images with more than one cell
			  if(len(cells)==1 and cells!=['\r']):
			  	allOldLabels.append(cells)
			  	allImageNumbers.append(imageNum)
			  imageNum += 1
	return allOldLabels, allImageNumbers

def getBoundingBoxes(csvFile):
	# Get bounding boxes [xmin, ymin, xmax, ymax] for all images
	bndboxList = []
	with open(csvFile, 'r') as bFile:
		for line in bFile:
			thisLine = line.strip('\n').replace(" ", "").replace('"', '').split(',');
			bndboxList.append(thisLine)
	return bndboxList


#def main():
#
#	allOldLabels, allImageNumbers = getOldLabels('labels.csv')
#	bndboxList = getBoundingBoxes('cellbounds.csv')
#
#	# Create new labels
#	nImages = len(bndboxList)
#	for i in range(nImages):
#		imageName = 'BloodImage_'+format(allImageNumbers[i], '05') # Do we have to add '.jpg'?
#		imageSize = ['640', '480']
#		imagePath = 'dataset/JPEGImages/'+imageName+'.jpg'
#		outputFile = 'dataset/wbcAnnotations/'+imageName+'.xml'
#
#		# TODO: Make a for-loop here if we want to handle images with several cells
#		classLabel = [allOldLabels[i][0].replace('\r', "")]
#		bndboxLabel = bndboxList[i]
#		allCellInfo = [classLabel + bndboxLabel]
#		#print(allCellInfo)
#		writeToXml(imageName, imageSize, imagePath, allCellInfo, outputFile)



input_path = 'our_train.txt'    #clw note:这里可以修改成其他的txt文件
with open(input_path,'r') as f:   
    lines = f.readlines()
    for line in lines:
        allCellInfo = []
        bndboxList =  []
        image_annotation_list = line.split(' ')
        #clw note：image_annotation_list[0]就是文件名，如train/19/4440.jpg
        imageName =  image_annotation_list[0].split('/')[-2] + '_' + image_annotation_list[0].split('/')[-1] #clw note：这里是带.jpg的，相当于19_4440.jpg
        imagePath = imageName
        
        #clw note：相当于C:/Users/Administrator/Desktop/keras-yolo2/our/train/19_4440.jpg
        img = Image.open('C:/Users/Administrator/Desktop/keras-yolo2/our/train/' + imageName)  
        imageSize = img.size 
        image_obj_number = int(image_annotation_list[1])
        for i in range(image_obj_number):
            bndboxList.append('head')
            bndboxList.append(image_annotation_list[3+5*i])
            bndboxList.append(image_annotation_list[3+5*i+1])
            bndboxList.append(image_annotation_list[3+5*i+2])
            bndboxList.append(image_annotation_list[3+5*i+3])
        allCellInfo.append(bndboxList)
        save_path = 'annotation_'+ input_path.split('.')[0]
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        outputFile = save_path + '/' + imageName.split('.')[0] +'.xml'
        writeToXml(imageName, imageSize, imagePath, allCellInfo, outputFile)
        print('D:/Deep-Learning/dataset/yuncong/yuncong_data/'+imageName, "written to", outputFile)
   
#    imageName = 'clw'
#    imageSize = ['640','480']
#    imagePath = imageName+'.jpg'
#    allCellInfo = [['head', '1', '2', '3', '4']]
#    outputFile = imageName+'.xml'
#    writeToXml(imageName, imageSize, imagePath, allCellInfo, outputFile)
#    print(imageName, "written to", outputFile)









print('           ##########################################    ')
print('           #                finish！                #    ')
print('           ##########################################    ')


print("                            _ooOoo_               ")
print("                           o8888888o               ")
print("                           88  .  88              ")
print("                           (| -_- |)                   ")
print("                            O\\ = /O                    ")
print("                        ____/`---'\\____               ")
print("                      .   ' \\| |// `.             ")
print("                       / \\||| : |||// \\          ")
print("                     / _||||| -:- |||||- \\          ")
print("                       | | \\\\\\ - /// | |            ")
print("                     | \\_| ''\\---/'' | |           ")
print("                      \\ .-\\__ `-` ___/-. /           ")
print("                   ___`. .' /--.--\\ `. . __            ")
print("                ."" '< `.___\\_<|>_/___.' >'"".         ")
print("               | | : `- \\`.;`\\ _ /`;.`/ - ` : | |     ")
print("                 \\ \\ `-. \\_ __\\ /__ _/ .-` / /     ")
print("         ======`-.____`-.___\\_____/___.-`____.-'======  ")
print("                            `=---='  ")
