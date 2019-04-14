from collections import defaultdict

def read(car_path, road_path, cross_path):
    car_dict, road_dict, cross_dict = defaultdict(list), defaultdict(list), defaultdict(list)
    with open(car_path, 'r') as car_file: 
        car_ascending = []
        for line in car_file.readlines():
            if line.strip()[0] == '#': continue
            temp = line.replace(' ', '').replace('\n', '').replace('(', '').replace(')', '').split(',')
            if not temp: continue
            temp = list(map(int, temp))
            car_dict[temp[0]] = temp[1: ]
            car_ascending.append(temp)
    with open(road_path, 'r') as road_file:
        for line in road_file.readlines():
            if line.strip()[0] == '#': continue
            temp = line.replace(' ', '').replace('\n', '').replace('(', '').replace(')', '').split(',')
            if not temp: continue
            temp = list(map(int, temp))
            road_dict[temp[0]] = temp[1: ]
    with open(cross_path, 'r') as cross_file:
        cross_ascending = []
        for line in cross_file.readlines():
            if line.strip()[0] == '#': continue
            temp = line.replace(' ', '').replace('\n', '').replace('(', '').replace(')', '').split(',')
            if not temp: continue
            temp = list(map(int, temp))
            cross_dict[temp[0]] = temp[1: ]
            cross_ascending.append(temp[0])
    
    car_ascending.sort(key = lambda x : (x[4]))
    cross_ascending.sort()
    return car_dict, road_dict, cross_dict, car_ascending, cross_ascending