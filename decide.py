import random

def decide(car_id, car_dict, cross_id, cross_dict, road_dict, P1, P2, balance):
    target_id = car_dict[car_id][1]
    if cross_id == target_id: next_road_id = 0
    else:  
        p = [0, 0, 0, 0]
        first, second = 0, 0
        for i in range(4):
            next_road_id = cross_dict[cross_id][i]
            if next_road_id == -1 or next_road_id == car_dict[car_id][4][0]: continue
            next_dir_i = -1
            if road_dict[next_road_id][3] == cross_id: next_dir_i = 6
            elif road_dict[next_road_id][5] and road_dict[next_road_id][4]==cross_id: next_dir_i = 7
            if next_dir_i == -1: continue
            p[i] += 1
            next_length = road_dict[next_road_id][0]
            next_lane_num = road_dict[next_road_id][2]
            next_lane_i = 1
            while next_lane_i < 1 + next_lane_num:
                if road_dict[next_road_id][next_dir_i][next_lane_i] == [] or car_dict[road_dict[next_road_id][next_dir_i][next_lane_i][-1]][4][3] < next_length - 1: break
                next_lane_i += 1
            if next_lane_i == 1 + next_lane_num: p[i] -= balance
            elif next_road_id == P1[cross_id][target_id]:
                p[i] += 99999
                first = 1
        
        if not first:
            for i in range(4):
                if p[i] < 1: continue
                if cross_dict[cross_id][i] == P2[cross_id][target_id]:
                    p[i] += 99999
                    second = 1
        
        sum_p = 0
        for i in range(4): sum_p += p[i]
        for i in range(4): p[i] /= sum_p
        dice = random.random()
        if 0 <= dice < p[0]: next_i = 0
        elif p[0] <= dice < p[0] + p[1]: next_i = 1
        elif p[0] + p[1] <= dice < p[0] + p[1] + p[2]: next_i = 2
        elif p[0] + p[1] + p[2] <= dice < p[0] + p[1] + p[2] + p[3]: next_i = 3
        next_road_id = cross_dict[cross_id][next_i]
    car_dict[car_id][5] = next_road_id