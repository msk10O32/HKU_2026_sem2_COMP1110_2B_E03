import simpy
import csv
import datetime as dt
import os
#load request and group data from csv files
def load_request():
    with open(os.path.join("data", "request.csv"), "r") as file:
        reader = csv.DictReader(file)
        request = []
        for row in reader:
            row['group_size'] = int(row['group_size'])
            row['is_vip'] = int(row['is_vip'])
            request.append(row)
        if len(request) == 0:
            raise ValueError("No request data found in request.csv")
    return request
def load_group():
    with open(os.path.join("config", "granularity.csv"), "r") as file:
        reader = csv.DictReader(file)
        group = []
        for row in reader:
            group.append(row)
    return group
#create a restaurant class to simulate the restaurant operation
class Restaurant:
    def __init__(self,env,requests,groups):
        #initialize the restaurant with table groups and queue sizes
        self.queue_sizes = dict()
        self.table_groups = dict()
        for group in groups:
            #create a priority resource for each table group, VIP customers have higher priority
            self.table_groups[group["type"]] = simpy.PriorityResource(env, capacity=int(group["table_capacity"]))
            #manage the queue size for each table group, if the queue capacity is 'inf', set it to infinity, otherwise set it to the specified integer value
            if group["queue_capacity"] == 'inf':
                self.queue_sizes[group["type"]] = float('inf')
            else:
                self.queue_sizes[group["type"]] = int(group["queue_capacity"])
        #other attributes to manage the simulation
        self.env = env
        self.requests = requests
        self.records = []
        self.log = []
        self.standard_time = dt.datetime.strptime(self.requests[0]['arrival_time'], '%Y-%m-%d %H:%M:%S')
        self.end_time = 14400
    def run(self):
        #trigger function for the whole simulation process
        self.env.process(self.process())
        self.env.run()
    def process(self):
        #simulate the arrival of customer requests based on their specified arrival times, and handle each request accordingly
        #set a last variable to keep track of the last arrival time, calculate the time difference to wait for the next request
        last = 0
        #send each request to the handle_request function
        for request in self.requests:
            #record the arrival time of the request, and check the relevant start time for the simulation
            arrival_time = dt.datetime.strptime(request['arrival_time'], '%Y-%m-%d %H:%M:%S')
            start = int((arrival_time-self.standard_time).total_seconds()/60)
            #wait until the event starts, and log the arrival of the request
            yield self.env.timeout(start-last)
            self.log.append(f"Processing request {request['uid']} type: {request['table_type']}, arrived at {start} minutes, waiting customers in queue: {len(self.table_groups[request['table_type']].queue)}/{self.queue_sizes[request['table_type']]}")
            #process arrived request
            self.env.process(self.handle_request(request))
            #update the last variable to the current start time for the next iteration
            last = start
    def handle_request(self,request):
        #if the queue for the requested table type is full, reject the request and log the rejection
        if len(self.table_groups[request['table_type']].queue) >= self.queue_sizes[request['table_type']]:
            self.records.append({
                "uid": request['uid'],
                "group_size": request['group_size'],
                "table_type": request['table_type'],
                "is_vip": request['is_vip'],
                "arrival_time": request['arrival_time'],
                "seating_time": None,
                "leaving_time": None,
                "is_served": False
            })
            self.log.append(f"Request {request['uid']} type: {request['table_type']} is rejected due to full queue at time {self.env.now} minutes, customers limit: {self.queue_sizes[request['table_type']]}")
            return
        #else, request a table resource based on the requested table type, and log the seating time and waiting customers in queue
        with self.table_groups[request['table_type']].request(priority=-request['is_vip']) as req:
            yield req
            seating_time = self.env.now
            self.log.append(f"Request {request['uid']} type: {request['table_type']} is served at time {seating_time} minutes, waiting customers in queue: {len(self.table_groups[request['table_type']].queue)}/{self.queue_sizes[request['table_type']]}")
            yield self.env.timeout(int(request['dining_duration']))
            leaving_time = self.env.now
            self.log.append(f"Request {request['uid']} type: {request['table_type']} is completed at time {leaving_time} minutes")
            self.records.append({
                "uid": request['uid'],
                "group_size": request['group_size'],
                "table_type": request['table_type'],
                "is_vip": request['is_vip'],
                "arrival_time": request['arrival_time'],
                "seating_time": self.standard_time + dt.timedelta(minutes=seating_time),
                "leaving_time": self.standard_time + dt.timedelta(minutes=leaving_time),
                "is_served": True
            })
def main():
    #load request and group data
    requests = load_request()
    groups = load_group()
    #create environment
    env = simpy.Environment()
    #initialize the restaurant with the environment, requests, and groups
    R = Restaurant(env,requests,groups)
    #run the simulation
    R.run()
    #write the results to a csv file and the logs to a text file
    with open(os.path.join('data', 'result.csv'),'w',newline='') as file:
        fieldnames = ['uid','group_size','table_type','is_vip','arrival_time','seating_time','leaving_time','is_served']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for record in R.records:
            writer.writerow(record)
    os.makedirs("log", exist_ok=True)
    with open(os.path.join("log", "simulation_log.txt"), 'w') as file:
        for log in R.log:
            file.write(log+'\n')
if __name__ == "__main__":
    main()