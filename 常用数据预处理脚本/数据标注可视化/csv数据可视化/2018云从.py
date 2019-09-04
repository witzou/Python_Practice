import cv2
import pandas as pd
from PIL import Image

full_labels = pd.read_csv('head_labels.csv')

print(full_labels.head())

def draw_boxes(image_name):
    selected_value = full_labels[full_labels.filename == image_name]
    img = cv2.imread('images/{}'.format(image_name))
    for index, row in selected_value.iterrows():
        img = cv2.rectangle(img, (row['xmin'], row['ymin']), (row['xmax'], row['ymax']), (0, 255, 0), 3)
    return img

aaa = Image.fromarray(draw_boxes('IMG_123.jpg')) #这里查看不同的图片
aaa.show()

#img = draw_boxes('IMG_1.jpg')
#img.imshow()