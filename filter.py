import csv
import datetime as dt
'''this file aims to read the input values from the input.csv file,
filter the input values based on the defined rules, 
determine the table type based on the granularity levels defined in the granularity.csv file, 
and convert the created_at time to a dict with hour and minute. 
The output is printed as a list of dicts.
'''
#functionized error checking for the input values
def is_valid_granularity(row):
    try:
        pin = int(row['split'])
    except:
        raise TypeError(f"Invalid value for split: row: {row['type']}, {row['split']}")
    if pin in check_split:
        raise ValueError(f"Split point {row['split']} is assigned to multiple table types: row: {row['type']}, {row['split']}")
    if pin <= 0:
        raise ValueError(f"Split must be a positive integer: row: {row['type']}, {row['split']}")
    return True

#check input values and assign the table type based on the granularity levels
def is_valid_input(row):
    try:
        if int(row['custom_count']) < 0:
            raise ValueError(f"Custom count must be a non-negative integer: row: {row['custom_count']}")
    except:
            raise TypeError(f"Invalid value for custom count: row: {row['custom_count']}, {row['time_cost']}")
    try:
        if int(row['time_cost']) < 0:
            raise ValueError(f"Time cost must be a non-negative integer: row: {row['time_cost']}")
    except:
            raise TypeError(f"Invalid value for time cost: row: {row['custom_count']}, {row['time_cost']}")
    try:
        dt.datetime.strptime(row['created_at'], '%Y-%m-%d %H:%M:%S')
    except:
        raise ValueError(f"Invalid date format for created_at: row: {row['created_at']}")
    return True

#initialize the csv file with the granularity levels
with open('granularity.csv', 'r') as file:
    reader = csv.DictReader(file)
    granularity_levels = []
    #remove duplicate split points and check for invalid values, then sort the granularity levels based on the split points
    check_split = set()
    for row in reader:
        if is_valid_granularity(row):
            granularity_levels.append((row['type'], int(row['split'])))
            check_split.add(int(row['split']))
    granularity_levels.sort(key=lambda x: x[1])
#convert input values to the request dicts
with open('input.csv', 'r') as file:
    reader = csv.DictReader(file)
    output = []
    for row in reader:
        buffer = dict()
        #check input values and assign the table type based on the granularity levels
        if is_valid_input(row):
            buffer['custom_count'] = int(row['custom_count'])
            buffer['time_cost'] = int(row['time_cost'])
            buffer['created_at'] = row['created_at']
        #if the custom count is greater than or equal to the largest split, assign the largest table type
        if int(row['custom_count']) >= granularity_levels[-1][1]:
            buffer['table_type'] = granularity_levels[-1][0]
        else:
            for level in range(len(granularity_levels)-1):
                if int(row['custom_count']) in range(granularity_levels[level][1], granularity_levels[level+1][1]):
                    buffer['table_type'] = granularity_levels[level][0]
                    break
        output.append(buffer)
    output.sort(key=lambda x: x['created_at'])

    #output the request dicts to a csv file with assigned uid, in case some or the requests are missing
    with open('request.csv','w',newline='') as file:
        i = 0
        size = len(str(len(output)))
        fieldnames = ['uid','custom_count', 'created_at', 'time_cost', 'table_type']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in output:
            i+=1
            row['uid'] = 'R' + str(i).zfill(size)
            writer.writerow(row)