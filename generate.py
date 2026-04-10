# module1 : customer data generater (generate.py)
#function: generate large amount of raw data for simulation and output as input.csv

import random
import csv
from datetime import datetime,timedelta

<<<<<<< HEAD
#以下是可以自定义配比的参数
Total_groups = 100 #总顾客组数
created_at_range = (0,100) #顾客到达时间按的范围（单位：分钟，0=模拟开始时间，120=2小时高峰）
Group_size_range = (1,6) #团体人数范围（目前预设的是1-6人）
Dining_duration_range = (20,60) #用餐时间范围（目前预设的是20-60分钟）
Vip_ratio = 0.1 #Vip顾客比例（目前预设的是10%）
Random_seed = 325 #随机种子，固定之后可以复现相同数据，方便进行对比试验
BASE_TIME = datetime(2024,6,1,0,0,0) #基础时间 2024-06-01 00.00.00
=======
#The following are parameters that allow for customizable ratios.
Total_groups = 100 #total amount of customer group
Arrival_time_range = (0,100) #Customer arrival time is categorized into ranges (unit: minutes, 0 = simulated start time, 120 = 2-hour peak).
Group_size_range = (1,6) #Group size range (currently preset to 1-6 people)
Dining_duration_range = (20,60) #Meal time range (currently preset to 20-60 minutes)
Vip_ratio = 0.1 #VIP customer ratio (currently set at 10%)
Random_seed = 325 #A random seed, once fixed, allows for the reproduction of identical data, facilitating comparative experiments.
BASE_TIME = datetime(2024,6,1,0,0,0) #Base time: 2024-06-01 00:00:00
>>>>>>> cd402706b3777e1e2c3868d6e8793bfa78059f3e

def main():
    random.seed(Random_seed)

    #generate customer raw data
    customer_data = []
    for i in range(Total_groups):
        group_size = random.randint(*Group_size_range)
        arrival_min = random.randint(*created_at_range)
        dining_duration = random.randint(*Dining_duration_range)
        is_vip = random.random() < Vip_ratio #Generate VIP according to the preset ratio

        created_at = (BASE_TIME + timedelta(minutes=arrival_min)).strftime("%Y-%m-%d %H:%M:%S")

        customer_data.append({
            "group_size": group_size,
            "created_at": created_at,
            "dining_duration": dining_duration,
            "is_vip": 1 if is_vip else 0
        })

<<<<<<< HEAD
        #按照时间排序，保证顾客按到底按顺序配列
    customer_data.sort(key=lambda x: x["created_at"])

        #写入 input.csv 文件
    output_file = "data\\input.csv"
    with open(output_file,"w",newline="",encoding="utf-8") as f:
        #设置表格列名
        writer = csv.DictWriter(f, fieldnames=["group_size", "created_at", "dining_duration", "is_vip"])
=======
        #Sort by time to ensure customers are seated in order from bottom to top.
    customer_data.sort(key=lambda x: x["arrival_time"])

        #input input.csv file
    output_file = "input.csv"
    with open(output_file,"w",newline="",encoding="utf-8") as f:
        #Set table column names
        writer = csv.DictWriter(f, fieldnames=["group_size", "arrival_time", "dining_duration", "is_vip"])
>>>>>>> cd402706b3777e1e2c3868d6e8793bfa78059f3e
        writer.writeheader()
        writer.writerows(customer_data)

    print(f"Data Generation is completed.")
    print(f"{Total_groups} groups of data are generated")
    print(f"output file: {output_file}")

if __name__ == "__main__":
    main()
