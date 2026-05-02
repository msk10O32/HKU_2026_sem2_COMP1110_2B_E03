# module1 : customer data generater (generate.py)
#function: generate large amount of raw data for simulation and output as input.csv

import random
import csv
from datetime import datetime,timedelta
import os

#the variable that can define by yourself
Total_groups = 100 #no of groups of customer
created_at_range = (0,60) #customer arrival time(unit min)
Group_size_range = (1,6) #number of people inside each group e.g 1-6 people per group
Dining_duration_range = (20,60) #time used for dining
Vip_ratio = 0.1 #vip ratio
Random_seed = 325
BASE_TIME = datetime(2024,6,1,0,0,0) #base time 2024-06-01 00.00.00

def main():
    random.seed(Random_seed)

    #generate customer raw data
    customer_data = []
    for i in range(Total_groups):
        group_size = random.choices([1,2,3,4,5,6], weights=[10,35,25,15,10,5])[0] #Generate group size according to the preset ratio
        arrival_min = random.randint(*created_at_range)
        dining_duration = random.randint(*Dining_duration_range)
        is_vip = random.random() < Vip_ratio #Generate VIP according to the preset ratio

        arrival_time = (BASE_TIME + timedelta(minutes=arrival_min)).strftime("%Y-%m-%d %H:%M:%S")

        customer_data.append({
            "group_size": group_size,
            "arrival_time": arrival_time,
            "dining_duration": dining_duration,
            "is_vip": 1 if is_vip else 0
        })

        #arrange in terms of time
    customer_data.sort(key=lambda x: x["arrival_time"])

        #write in to the input.csv
    os.makedirs('data', exist_ok=True)
    output_file = os.path.join("data", "input.csv")
    with open(output_file,"w",newline="",encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["group_size", "arrival_time", "dining_duration", "is_vip"])
        writer.writeheader()
        writer.writerows(customer_data)

    print(f"Data Generation is completed.")
    print(f"{Total_groups} groups of data are generated")
    print(f"output file: {output_file}")

if __name__ == "__main__":
    main()
