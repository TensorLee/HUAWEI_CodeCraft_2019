def move(car_id, car_dict, cross_id, road_dict, temp_ans, start):
    road_id = car_dict[car_id][4][0]
    dir_i = car_dict[car_id][4][1]
    lane_i = car_dict[car_id][4][2]
    s1 = car_dict[car_id][4][3]
    next_road_id = car_dict[car_id][5]
    if next_road_id == 0:
        car_dict[car_id][6] = 0
        road_dict[road_id][dir_i][0].pop(0)
        road_dict[road_id][dir_i][lane_i].pop(0)
        return 1
    else:
        if road_dict[next_road_id][3] == cross_id: next_dir_i = 6
        elif road_dict[next_road_id][5] and road_dict[next_road_id][4] == cross_id: next_dir_i = 7
        v2 = min(car_dict[car_id][2], road_dict[next_road_id][1])
        s2 = max(0, v2 - s1)
        if s2 == 0:
            car_dict[car_id][4][3] = 0
            car_dict[car_id][6] = 0
            road_dict[road_id][dir_i][0].pop(0)
        else:
            next_length = road_dict[next_road_id][0]
            next_lane_num = road_dict[next_road_id][2]
            next_lane_i = 1
            while next_lane_i < 1 + next_lane_num:
                if road_dict[next_road_id][next_dir_i][next_lane_i] == [] or \
                next_length - s2 > car_dict[road_dict[next_road_id][next_dir_i][next_lane_i][-1]][4][3]:
                    car_dict[car_id][4][3] = next_length - s2
                    break
                elif car_dict[road_dict[next_road_id][next_dir_i][next_lane_i][-1]][6]: return 0
                elif car_dict[road_dict[next_road_id][next_dir_i][next_lane_i][-1]][4][3] < next_length - 1:
                    car_dict[car_id][4][3] = \
                    car_dict[road_dict[next_road_id][next_dir_i][next_lane_i][-1]][4][3] + 1
                    break
                next_lane_i += 1
            if next_lane_i == 1 + next_lane_num:
                car_dict[car_id][4][3] = 0
                car_dict[car_id][6] = 0
                if start: return 1
                road_dict[road_id][dir_i][0].pop(0)
            elif next_lane_i < 1 + next_lane_num:
                temp_ans[car_id].append(next_road_id)
                car_dict[car_id][4][0] = next_road_id
                car_dict[car_id][4][1] = next_dir_i
                car_dict[car_id][4][2] = next_lane_i
                car_dict[car_id][6] = 0
                road_dict[next_road_id][next_dir_i][next_lane_i].append(car_id)
                if start == 0:
                    road_dict[road_id][dir_i][0].pop(0)
                    road_dict[road_id][dir_i][lane_i].pop(0)
    return 0