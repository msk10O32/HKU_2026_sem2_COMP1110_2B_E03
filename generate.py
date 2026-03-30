# module1 : customer data generater (generate.py)
#function:批量生成模拟用的顾客原始数据，输出为input.csv

import random
import csv

#以下是可以自定义配比的参数
Total_groups = 100 #总顾客组数
Arrival_time_range = (0,100) #顾客到达时间按的范围（单位：分钟，0=模拟开始时间，120=2小时高峰）
Group_size_range = (1,6) #团体人数范围（目前预设的是1-6人）
Dining_duration_range = (20,60) #用餐时间范围（目前预设的是20-60分钟）
Vip_ratio = 0.1 #Vip顾客比例（目前预设的是10%）
Random_seed = 325 #随机种子，固定之后可以复现相同数据，方便进行对比试验

def main():
    random.seed(Random_seed)

    #生成顾客数据
    customer_data = []
    for i in range(Total_groups):
        group_size = random.randint(*Group_size_range)
        arrival_time = random.randint(*Arrival_time_range)
        dining_duration = random.randint(*Dining_duration_range)
        is_vip = random.random() < Vip_ratio #按预设好的比例生成vip

        customer_data.append({
            "group_size": group_size,
            "arrival_time": arrival_time,
            "dining_duration": dining_duration,
            "is_vip": 1 if is_vip else 0
        })

        #按照时间排序，保证顾客按到底按顺序配列
    customer_data.sort(key=lambda x: x["arrival_time"])

        #写入 input.csv 文件
    output_file = "input.csv"
    with open(output_file,"w",newline="",encoding="utf-8") as f:
        #设置表格列名
        writer = csv.DictWriter(f, fieldnames=["group_size", "arrival_time", "dining_duration", "is_vip"])
        writer.writeheader()
        writer.writerows(customer_data)

    print(f"Data Generation is completed.")
    print(f"{Total_groups} groups of data are generated")
    print(f"output file: {output_file}")

if __name__ == "__main__":
    main()
