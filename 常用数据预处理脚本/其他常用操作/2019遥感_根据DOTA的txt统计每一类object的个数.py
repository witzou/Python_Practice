import os

path = 'I:/deep_learning/competion/2019yaogan/train_val/labelTxt_train_val/'
txt_name_list = os.listdir(path)       # 将路径下所有文件存成list


##################### 可以统计一下object的数量
back_ground = 0
roundabout = 0
tennis_court = 0
swimming_pool = 0
storage_tank = 0
soccer_ball_field = 0
small_vehicle = 0
ship = 0
plane = 0
large_vehicle = 0
helicopter = 0
harbor = 0
ground_track_field = 0
bridge = 0
basketball_court = 0
baseball_diamond = 0
helipad = 0
airport = 0
container_crane = 0
#############################

file_count = 0
for txt_name in txt_name_list:
    print(txt_name)
    with open(path + txt_name, 'r') as f1:
        txt_data = f1.readlines()
        for line in txt_data[2:]:  # clw note：从第二行开始读
            result = []
            line_list = line.split(' ')
            if (line_list[8] == 'back_ground'):
                back_ground += 1
            elif (line_list[8] == 'roundabout'):
                roundabout += 1
            elif (line_list[8] == 'tennis-court'):
                tennis_court += 1
            elif (line_list[8] == 'swimming-pool'):
                swimming_pool += 1
            elif (line_list[8] == 'storage-tank'):
                storage_tank += 1
            elif (line_list[8] == 'soccer-ball-field'):
                soccer_ball_field += 1
            elif (line_list[8] == 'small-vehicle'):
                small_vehicle += 1
            elif (line_list[8] == 'ship'):
                ship += 1
            elif (line_list[8] == 'plane'):
                plane += 1
            elif (line_list[8] == 'large-vehicle'):
                large_vehicle += 1
            elif (line_list[8] == 'helicopter'):
                helicopter += 1
            elif (line_list[8] == 'harbor'):
                harbor += 1
            elif (line_list[8] == 'ground-track-field'):
                ground_track_field += 1
            elif (line_list[8] == 'bridge'):
                bridge += 1
            elif (line_list[8] == 'basketball-court'):
                basketball_court += 1
            elif (line_list[8] == 'baseball-diamond'):
                baseball_diamond += 1
            elif (line_list[8] == 'helipad'):
                helipad += 1
            elif (line_list[8] == 'airport'):
                airport += 1
            elif (line_list[8] == 'container-crane'):
                container_crane += 1
    file_count += 1
    print('clw: file_count = ', file_count)

print('clw: back_ground = ',back_ground)
print('clw: roundabout = ',roundabout)
print('clw: tennis_court = ',tennis_court)
print('clw: swimming_pool = ',swimming_pool)
print('clw: storage_tank = ',storage_tank)
print('clw: soccer_ball_field = ',soccer_ball_field)
print('clw: small_vehicle = ',small_vehicle)
print('clw: ship = ',ship)
print('clw: plane = ',plane)
print('clw: large_vehicle = ',large_vehicle)
print('clw: helicopter = ',helicopter)
print('clw: harbor = ',harbor)
print('clw: ground_track_field = ',ground_track_field)
print('clw: bridge = ',bridge)
print('clw: basketball_court = ',basketball_court)
print('clw: baseball_diamond = ',baseball_diamond)
print('clw: helipad = ',helipad)
print('clw: airport = ',airport)
print('clw: container_crane = ',container_crane)

print ("clw: ---------------------success!---------------------")