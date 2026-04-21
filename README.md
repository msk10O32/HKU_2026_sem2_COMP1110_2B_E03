Code Modules
generate.py Module Description

1.Overview

generate.py is the first data module of the Restaurant Queue Simulation project. It automatically generates random customer group data for restaurant queue simulation, including group size, arrival time, dining duration, and VIP status. All data is saved as a standard CSV file for subsequent modules.

2.Core functionality

Generates customizable customer groups based on preset parameters
Creates random but realistic dining behaviour data
Sorts all customers by arrival time (real-world simulation)
Exports clean, structured data to input.csv

3.How to run
Open config/granularity to set fundamental data
including 4 options:
    (1)type
        A string, this attribute means how this type of table is referred to this kind of table,e.g.("A","B","C")
    (2)split_point
        An integer, this attribute means the interval of customer count of this table, up to next smallest number, for example:
            Suppose we have "A" with split point a, and "B" with split point b, a < b. 
            Then, for the customers with group size n∈[a,b), they will be assigned a table type "A", if b is the last split point, then group "B" means n∈[b,inf)
    (3)table_capacity
        An integer, this attribute means the amount of this kind of table that  restaurant have, if a group of customers arrives when all tables are occupied, their request will be passed to queue.
    (4)queue_capacity
        An integer(or a string "inf"), this attribute means how many groups of customers can queue for this kind of table at the same time, if a group of customer arrives when the queue is full, their request will not be served.


Open the terminal
python generate.py

4.Output result

File generated: input.csv
Data columns:
group\_size: number of people in the group
arrival\_time: customer arrival time
dining\_duration: dining time length (minutes)
is\_vip: VIP status (1 = VIP, 0 = normal)



Before using, please run these three commands in terminal/bash

1.python -m venv venv
2.choose one of these two commands according to your operating system
source venv/bin/activate(linux)
venv\\Scripts\\activate (Windows)
3.pip install -r requirements.txt

