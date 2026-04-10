# module1 : customer data generater (generate.py)
#function: generate large amount of raw data for simulation and output as input.csv
import random
import csv
from datetime import datetime,timedelta

#The following are parameters that allow for customizable ratios.
Total_groups = 100 #total amount of customer group
created_at_range = (0,100) #Customer arrival time is categorized into ranges (unit: minutes, 0 = simulated start time, 120 = 2-hour peak).
Group_size_range = (1,6) #Group size range (currently preset to 1-6 people)
Dining_duration_range = (20,60) #Meal time range (currently preset to 20-60 minutes)
Vip_ratio = 0.1 #VIP customer ratio (currently set at 10%)
Random_seed = 325 #A random seed, once fixed, allows for the reproduction of identical data, facilitating comparative experiments.
BASE_TIME = datetime(2024,6,1,0,0,0) #Base time: 2024-06-01 00:00:00

def main():
    random.seed(Random_seed)

    # generate customer raw data
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

        # Sort by time to ensure customers are seated in order from bottom to top.
    customer_data.sort(key=lambda x: x["created_at"])

    #input input.csv file
    output_file = "data\\input.csv"
    with open(output_file,"w",newline="",encoding="utf-8") as f:
        # Set table column names
        writer = csv.DictWriter(f, fieldnames=["group_size", "created_at", "dining_duration", "is_vip"])
        writer.writeheader()
        writer.writerows(customer_data)

    print(f"Data Generation is completed.")
    print(f"{Total_groups} groups of data are generated")
    print(f"output file: {output_file}")

if __name__ == "__main__":
    main()