import random
from move import move

def start(time, car_ascending, car_dict, cross_dict, road_dict, temp_ans, remaining_car_num, P1, limit):
    due_cars = []
    for car in car_ascending:
        if car[4] > time: break
        due_cars.append(car)
    due_cars.sort(key = lambda x : (x[0]))

    for car in due_cars:
        running_car_num = remaining_car_num - len(car_ascending)
        if running_car_num > limit: break
        car_id = car[0]
        start_id = car[1]
        target_id = car[2]

        next_road_id = P1[start_id][target_id]
        if road_dict[next_road_id][3] == start_id: next_dir_i = 6
        elif road_dict[next_road_id][5] and road_dict[next_road_id][4]==start_id: next_dir_i = 7

        next_length = road_dict[next_road_id][0]
        next_lane_num = road_dict[next_road_id][2]
        next_lane_i = 1
        while next_lane_i < next_lane_num:
            if road_dict[next_road_id][next_dir_i][next_lane_i] == [] or car_dict[road_dict[next_road_id][next_dir_i][next_lane_i][-1]][4][3] < next_length - 1: break
            next_lane_i += 1
        if next_lane_i == next_lane_num and road_dict[next_road_id][next_dir_i][next_lane_i] and car_dict[road_dict[next_road_id][next_dir_i][next_lane_i][-1]][4][3] >= next_length - 2: continue
        
        if running_car_num > 0.9 * limit:
            skip = random.random()
            if skip < 0.02: continue
        
        car_dict[car_id][5] = next_road_id
        temp_ans[car_id].append(time)
        block = move(car_id, car_dict, start_id, road_dict, temp_ans, 1)
        if block:
            temp_ans[car_id].pop(0)
            continue
        car_ascending.remove(car)
        # due_cars.remove(car)