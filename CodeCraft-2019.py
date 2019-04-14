import logging
import sys
import copy
from collections import defaultdict
from read import read
from construct import construct
from label import label
from schedule import schedule
from start import start
logging.basicConfig(level=logging.DEBUG,
                    filename='../logs/CodeCraft-2019.log',
                    format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filemode='a')
def main():
    if len(sys.argv) != 5:
        logging.info('please input args: car_path, road_path, cross_path, answerPath')
        exit(1)
    car_path = sys.argv[1]
    road_path = sys.argv[2]
    cross_path = sys.argv[3]
    answer_path = sys.argv[4]
    logging.info("car_path is %s" % (car_path))
    logging.info("road_path is %s" % (road_path))
    logging.info("cross_path is %s" % (cross_path))
    logging.info("answer_path is %s" % (answer_path))
    # to read input file
    car_dict, road_dict, cross_dict, car_ascending, cross_ascending = read(car_path, road_path, cross_path)
    P1, P2, total_lane_num = construct(car_dict, road_dict, cross_dict)
    # process
    ans, total_car_num, road_num = defaultdict(list), len(car_ascending), len(road_dict)
    best_balance, best_limit = 0, 0
    min_time, dead_lock = 99999, 0
    for balance in [0.5, ]:
        limit = 2000
        for _ in range(1):
            car_dict_copy = copy.deepcopy(car_dict)
            road_dict_copy = copy.deepcopy(road_dict)
            car_ascending_copy = copy.deepcopy(car_ascending)
            time, arrival_num, temp_ans = 0, 0, defaultdict(list)
            while arrival_num < total_car_num:
                waiting_car_num = label(road_dict_copy, car_dict_copy, cross_dict, P1, P2, balance)
                dead_lock, schedule_arrival_num = \
                schedule(cross_ascending, cross_dict, road_dict_copy, car_dict_copy, temp_ans, waiting_car_num, P1, P2, balance)
                arrival_num += schedule_arrival_num
                if dead_lock:
                    print("dead_lock at time:", time)
                    break
                remaining_car_num = total_car_num - arrival_num
                start(time, car_ascending_copy, car_dict_copy, cross_dict, road_dict_copy, temp_ans, remaining_car_num, P1, limit)
                time += 1
                if time > min_time: break
            print("balance:", balance, "limit:", limit, "time:", time, "arrival_num:", arrival_num)
            if not dead_lock and time < min_time:
                best_limit = limit
                best_balance = balance
                min_time = time
                ans = copy.deepcopy(temp_ans)
            if dead_lock: limit -= 500
            else: limit += 800
    print("best_balance:",best_balance, "best_limit:",best_limit, "total_car_num:",total_car_num, "road_num:",road_num, "total_lane_num:",total_lane_num, "min_time:",min_time)
    # to write output file
    with open(answer_path, 'w') as ans_file:
        for car_id in ans:
            ans_file.write("(" + str(car_id) + ',' + ','.join(list(map(str, ans[car_id]))) + ")\n")
    
if __name__ == "__main__":
    main()