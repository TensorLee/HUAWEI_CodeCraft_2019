import copy
from decide import decide
from move import move

def schedule(cross_ascending, cross_dict, road_dict, car_dict, temp_ans, waiting_car_num, P1, P2, balance):
    schedule_arrival_num = 0
    while waiting_car_num > 0:
        last_waiting_car_num = copy.deepcopy(waiting_car_num)
        for cross_id in cross_ascending:
            for road_id in cross_dict[cross_id][4]:
                if road_id == -1: continue
                dir_i = -1
                if road_dict[road_id][4] == cross_id: dir_i = 6
                elif road_dict[road_id][5] and road_dict[road_id][3] == cross_id: dir_i = 7
                if dir_i == -1 or road_dict[road_id][dir_i][0] == []: continue
                cur_i, left_yes, right_yes = 0, 1, 1
                while cross_dict[cross_id][cur_i] != road_id: cur_i += 1
                left_road_id = cross_dict[cross_id][(cur_i+1)%4]
                front_road_id = cross_dict[cross_id][(cur_i+2)%4]
                right_road_id = cross_dict[cross_id][(cur_i+3)%4]
                if left_road_id != -1:
                    left_dir_i = -1
                    if road_dict[left_road_id][4] == cross_id: left_dir_i = 6
                    elif road_dict[left_road_id][5] and road_dict[left_road_id][3] == cross_id:
                        left_dir_i = 7
                    if left_dir_i != -1 and road_dict[left_road_id][left_dir_i][0] != []:
                        if car_dict[road_dict[left_road_id][left_dir_i][0][0][0]][5] == right_road_id or \
                           car_dict[road_dict[left_road_id][left_dir_i][0][0][0]][5] == 0: right_yes = 0
                if front_road_id != -1:
                    front_dir_i = -1
                    if road_dict[front_road_id][4] == cross_id: front_dir_i = 6
                    elif road_dict[front_road_id][5] and road_dict[front_road_id][3] == cross_id:
                        front_dir_i = 7
                    if front_dir_i != -1 and road_dict[front_road_id][front_dir_i][0] != []:
                        if car_dict[road_dict[front_road_id][front_dir_i][0][0][0]][5] == right_road_id: right_yes = 0
                if right_road_id != -1:
                    right_dir_i = -1
                    if road_dict[right_road_id][4] == cross_id: right_dir_i = 6
                    elif road_dict[right_road_id][5] and road_dict[right_road_id][3] == cross_id:
                        right_dir_i = 7
                    if right_dir_i != -1 and road_dict[right_road_id][right_dir_i][0] != []:
                        if car_dict[road_dict[right_road_id][right_dir_i][0][0][0]][5] == left_road_id or \
                           car_dict[road_dict[right_road_id][right_dir_i][0][0][0]][5] == 0: left_yes = 0
                while True:
                    car_id = road_dict[road_id][dir_i][0][0][0]
                    lane_i = car_dict[car_id][4][2]
                    if car_dict[car_id][5] == left_road_id and left_yes == 0: break
                    if car_dict[car_id][5] == right_road_id and right_yes == 0: break
                    move_arrival_num = move(car_id, car_dict, cross_id, road_dict, temp_ans, 0)
                    if car_dict[car_id][6]: break
                    waiting_car_num -= 1
                    schedule_arrival_num += move_arrival_num
                    i, lane_car_num = 0, len(road_dict[road_id][dir_i][lane_i])
                    while i < lane_car_num:
                        after_car_id = road_dict[road_id][dir_i][lane_i][i]
                        if after_car_id == car_id:
                            i += 1
                            continue
                        if car_dict[after_car_id][6] == 0: break
                        s1 = car_dict[after_car_id][4][3]
                        v1 = min(car_dict[after_car_id][2], road_dict[road_id][1])
                        if i == 0:
                            if s1 - v1 < 0:
                                decide(after_car_id, car_dict, cross_id, cross_dict, road_dict, P1, P2, balance)
                                road_dict[road_id][dir_i][0].append([after_car_id, lane_i, s1])
                                road_dict[road_id][dir_i][0].sort(key = lambda x : (x[2], x[1]))
                                break
                            else:
                                car_dict[after_car_id][4][3] = s1 - v1
                                car_dict[after_car_id][6] = 0
                                waiting_car_num -= 1
                        elif i > 0:
                            car_ahead_id = road_dict[road_id][dir_i][lane_i][i-1]
                            if s1 - v1 <= car_dict[car_ahead_id][4][3]:
                                car_dict[after_car_id][4][3] = car_dict[car_ahead_id][4][3] + 1
                            elif s1 - v1 > car_dict[car_ahead_id][4][3]:
                                car_dict[after_car_id][4][3] = s1 - v1
                            car_dict[after_car_id][6] = 0
                            waiting_car_num -= 1
                        i += 1
                    if road_dict[road_id][dir_i][0] == []: break
        if last_waiting_car_num == waiting_car_num:
            return 1, schedule_arrival_num
    return 0, schedule_arrival_num