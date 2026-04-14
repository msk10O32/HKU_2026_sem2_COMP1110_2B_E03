import simpy
import csv
import datetime as dt
def load_request():
    with open("data\\request.csv","r") as file:
        reader = csv.DictReader(file)
        request = []
        for row in reader:
            request.append(row)
    return request
def load_group():
    with open("data\\granularity.csv","r") as file:
        reader = csv.DictReader(file)
        group = []
        for row in reader:
            group.append(row)
    return group
class Restaurant:
    def __init__(self,env,requests,groups):
        self.queue_sizes = dict()
        self.table_groups = dict()
        for group in groups:
            self.table_groups[group["type"]] = simpy.PriorityResource(env, capacity=int(group["table_capacity"]))
            self.queue_sizes[group["type"]] = float(group["queue_capacity"])
        self.env = env
        self.requests = requests
        self.records = []
        self.standard_time = dt.datetime.strptime(self.requests[0]['arrival_time'], '%Y-%m-%d %H:%M:%S')
        self.end_time = 14400
    def run(self):
        self.env.process(self.process())
        self.env.run(until=self.end_time)
    def process(self):
        last = 0
        for request in self.requests:
            arrival_time = dt.datetime.strptime(request['arrival_time'], '%Y-%m-%d %H:%M:%S')
            start = int((arrival_time-self.standard_time).total_seconds()/60)
            print(f"Processing request {request['uid']}, arrives at {start} minutes")
            yield self.env.timeout(start-last)
            self.env.process(self.handle_request(request))
            last = start
    def handle_request(self,request):
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
            print(f"Request {request['uid']} is rejected due to full queue at time {self.env.now}")
            return
        with self.table_groups[request['table_type']].request(priority=-int(request['is_vip'])) as req:
            yield req
            seating_time = self.env.now
            print(f"Request {request['uid']} type: {request['table_type']} is served at time {seating_time},waiting customers in queue: {len(self.table_groups[request['table_type']].queue)}")
            yield self.env.timeout(int(request['dining_duration']))
            leaving_time = self.env.now
            print(f"Request {request['uid']} type: {request['table_type']} is completed at time {leaving_time}")
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
    requests = load_request()
    groups = load_group()
    env = simpy.Environment()
    R = Restaurant(env,requests,groups)
    R.run()
    with open('data\\result.csv','w',newline='') as file:
        fieldnames = ['uid','group_size','table_type','is_vip','arrival_time','seating_time','leaving_time','is_served']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for record in R.records:
            writer.writerow(record)
if __name__ == "__main__":
    main()