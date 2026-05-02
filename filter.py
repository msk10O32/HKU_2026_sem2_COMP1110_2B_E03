import csv
import datetime as dt
import os
'''this file aims to read the input values from the input.csv file,
filter the input values based on the defined rules, 
determine the table type based on the granularity levels defined in the granularity.csv file, 
and convert the arrival_time time to a dict with hour and minute. 
The output is printed as a list of dicts.
'''
#functionized error checking for the input values
def is_valid_granularity(row):
    try:
        pin = int(row['split_point'])
    except:
        raise TypeError(f"Invalid value for split_point: row: {row['type']}, {row['split_point']}")
    if pin in check_split:
        raise ValueError(f"Split point {row['split_point']} is assigned to multiple table types: row: {row['type']}, {row['split_point']}")
    if pin <= 0:
        raise ValueError(f"Split must be a positive integer: row: {row['type']}, {row['split_point']}")
    return True

#check input values and assign the table type based on the granularity levels
def is_valid_input(row):
    try:
        if int(row['group_size']) < 0:
            raise ValueError(f"Group size must be a non-negative integer: row: {row}")
    except:
            raise TypeError(f"Invalid value for group size: row: {row}")
    try:
        if int(row['dining_duration']) < 0:
            raise ValueError(f"Dining duration must be a non-negative integer: row: {row}")
    except:
            raise TypeError(f"Invalid value for dining duration: row: {row}")
    try:
        dt.datetime.strptime(row['arrival_time'], '%Y-%m-%d %H:%M:%S')
    except:
        raise ValueError(f"Invalid date format for arrival_time: row: {row['arrival_time']}")
    VIP = {0,1}
    try:
        if int(row['is_vip']) not in VIP:
            raise ValueError(f"Invalid VIP value: row: {row}")
    except:
        raise TypeError(f"Invalid VIP value: row: {row}")
    return True

def main():
    print("Initializing the filter module...")
    #initialize the csv file with the granularity levels
    with open(os.path.join('config', 'granularity.csv'), 'r') as file:
        reader = csv.DictReader(file)
        granularity_levels = []
        #remove duplicate split_point points and check for invalid values, then sort the granularity levels based on the split_point points
        global check_split
        check_split = set()
        for row in reader:
            if is_valid_granularity(row):
                granularity_levels.append((row['type'], int(row['split_point'])))
                check_split.add(int(row['split_point']))
        granularity_levels.sort(key=lambda x: x[1])
    #convert input values to the request dicts
    with open(os.path.join('data', 'input.csv'), 'r') as file:
        reader = csv.DictReader(file)
        output = []
        for row in reader:
            buffer = dict()
            #check input values and assign the table type based on the granularity levels
            if is_valid_input(row):
                buffer['group_size'] = int(row['group_size'])
                buffer['dining_duration'] = int(row['dining_duration'])
                buffer['arrival_time'] = row['arrival_time']
                buffer['is_vip'] = int(row['is_vip'])
            #if the custom count is greater than or equal to the largest split_point, assign the largest table type
            if int(row['group_size']) >= granularity_levels[-1][1]:
                buffer['table_type'] = granularity_levels[-1][0]
            elif int(row['group_size']) < granularity_levels[0][1]:
                buffer['table_type'] = granularity_levels[0][0]
            else:
                for level in range(len(granularity_levels)-1):
                    if int(row['group_size']) in range(granularity_levels[level][1], granularity_levels[level+1][1]):
                        buffer['table_type'] = granularity_levels[level][0]
                        break
            output.append(buffer)
        output.sort(key=lambda x: x['arrival_time'])

        #output the request dicts to a csv file with assigned uid, in case some or the requests are missing
        with open(os.path.join('data', 'request.csv'),'w',newline='') as file:
            i = 0
            size = len(str(len(output)))
            fieldnames = ['uid','group_size', 'arrival_time', 'dining_duration', 'table_type', 'is_vip']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for row in output:
                i+=1
                row['uid'] = 'R' + str(i).zfill(size)
                writer.writerow(row)
    print(f"Filtering is completed.\n{len(output)} groups of data are filtered and assigned with table types.")
if __name__ == "__main__":
    main()