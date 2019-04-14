from decide import decide

def label(road_dict, car_dict, cross_dict, P1, P2, balance):
    waiting_car_num = 0
    for road_id in road_dict:
        for dir_i in range(6, 7 + road_dict[road_id][5]):
            for lane_i in range(1, 1 + road_dict[road_id][2]):
                i, lane_car_num = 0, len(road_dict[road_id][dir_i][lane_i])
                while i < lane_car_num:
                    car_id = road_dict[road_id][dir_i][lane_i][i]
                    s1 = car_dict[car_id][4][3]
                    v1 = min(car_dict[car_id][2], road_dict[road_id][1])
                    if i == 0:
                        if s1 - v1 < 0:
                            if road_id == car_dict[car_id][5]:
                                cross_id = road_dict[road_id][4] if dir_i == 6 else road_dict[road_id][3]
                                decide(car_id, car_dict, cross_id, cross_dict, road_dict, P1, P2, balance)
                            road_dict[road_id][dir_i][0].append([car_id, lane_i, s1])
                            car_dict[car_id][6] = 1
                            waiting_car_num += 1
                        elif s1 - v1 >= 0:
                            car_dict[car_id][4][3] = s1 - v1
                    elif i > 0:
                        car_ahead_id = road_dict[road_id][dir_i][lane_i][i-1]
                        if s1 - v1 <= car_dict[car_ahead_id][4][3]:
                            if car_dict[car_ahead_id][6] == 0:
                                car_dict[car_id][4][3] = car_dict[car_ahead_id][4][3] + 1
                            elif car_dict[car_ahead_id][6]:
                                car_dict[car_id][6] = 1
                                waiting_car_num += 1
                        elif s1 - v1 > car_dict[car_ahead_id][4][3]:
                            car_dict[car_id][4][3] = s1 - v1
                    i += 1
            road_dict[road_id][dir_i][0].sort(key = lambda x : (x[2], x[1]))
    return waiting_car_num