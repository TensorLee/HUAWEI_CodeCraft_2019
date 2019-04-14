import copy
from collections import defaultdict

def construct(car_dict, road_dict, cross_dict):
    total_lane_num = 0
    for road_id in road_dict:
        lane_num = road_dict[road_id][2]
        temp = []
        for _ in range(1 + lane_num): temp.append([])
        road_dict[road_id].append(temp)
        total_lane_num += lane_num
        if road_dict[road_id][5]:
            temp = []
            for _ in range(1 + lane_num): temp.append([])
            road_dict[road_id].append(temp)
            total_lane_num += lane_num

    for car_id in car_dict:
        car_dict[car_id].extend( [[-1, 6, 1, 0], -1, 0] )

    for cross_id in cross_dict:
        temp = copy.deepcopy(cross_dict[cross_id])
        temp.sort()
        cross_dict[cross_id].append(temp)

    D1, P1 = defaultdict(defaultdict), defaultdict(defaultdict)
    for i in cross_dict:
        for j in cross_dict:
            if i == j: D1[i][j] = 0
            else: D1[i][j] = 99999
            P1[i][j] = -1
    for road_id in road_dict:
        start, end = road_dict[road_id][3], road_dict[road_id][4]
        d = road_dict[road_id][0]
        D1[start][end] = d
        P1[start][end] = road_id
        if road_dict[road_id][5]:
            D1[end][start] = d
            P1[end][start] = road_id
    D2, P2 = copy.deepcopy(D1), copy.deepcopy(P1)
    for k in cross_dict:
        for i in cross_dict:
            for j in cross_dict:
                if D1[i][j] > D1[i][k] + D1[k][j]:
                    D1[i][j] = D1[i][k] + D1[k][j]
                    P1[i][j] = P1[i][k]
    for k in cross_dict:
        for i in cross_dict:
            for j in cross_dict:
                if P2[i][k] != P1[i][j] and D2[i][j] > D2[i][k] + D2[k][j]:
                    D2[i][j] = D2[i][k] + D2[k][j]
                    P2[i][j] = P2[i][k]
    return P1, P2, total_lane_num