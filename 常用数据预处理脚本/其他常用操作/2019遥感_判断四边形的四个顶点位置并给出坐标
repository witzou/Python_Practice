# by teammate Jiahao Chen
# 功能：给定矩形或接近矩形的四边形的任意的四个顶点，能够判断哪个是其左上角、右上角、右下角、左下角，以及得到相应的坐标

List=[
  { "lat": 2.2, "lng":2 },
  { "lat": -5, "lng": -1 }, 
  { "lat": 1, "lng": -9 },  # 注意这里lat是纬度的意思，也就是y，而lng是经度，表示x；下面有math.atan2(x['lat'] - mlat, x['lng'] - mlng)
  { "lat": -1, "lng": 1 } 
]
import math
mlat = sum(x['lat'] for x in List) / len(List)
mlng = sum(x['lng'] for x in List) / len(List)
def algo(x):
    return (math.atan2(x['lat'] - mlat, x['lng'] - mlng) + 2 * math.pi) % (2*math.pi)#以质心为原点，将坐标转化为极坐标，求出角度

List.sort(key=algo,reverse=True)   # 按最大值排序，如果arctan(y/x)最大，说明角度最大，也就是在右下角，对应坐标(list[0]["lng"], list[0]["lat"])，其他同理。
