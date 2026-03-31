'''class AnaClock:
    #initialize the clock
    def __init__(self,t):
        t.split(':')
        hour, minute = int(t.split(':')[0]), int(t.split(':')[1])
        if hour < 0 or minute < 0:
            raise ValueError("Hour and minute must be non-negative")
        if hour >= 24 or minute >= 60:
            raise ValueError("Hour must be less than 24 and minute must be less than 60")
        self.clock = (hour*60 + minute) % 1440
        self.time = f'{(self.clock//60):02d}:{(self.clock%60):02d}'
    #add the shift to the clock and update the time
    def add(self,shift):
        self.clock += shift
        self.clock = self.clock % 1440
        self.update()
    #update the time after adding the shift
    def update(self):
        self.time = f'{(self.clock//60):02d}:{(self.clock%60):02d}
T = AnaClock("10:30")
print(T.time)
T.add(70)
print(T.time)'''
import csv
import 
import datetime as dt
time = dt.fromisoformat('2023-06-01 10:00:00')
print(time)
dt.timedelta(hours=1, minutes=10)