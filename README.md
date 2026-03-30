# HKU_COMP1110_2B_E03
A workspace for group project of COMP1110 2B E03 group

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
Open the terminal
python generate.py
4.Output result
File generated: input.csv
Data columns:
group_size: number of people in the group
arrival_time: customer arrival time (minutes)
dining_duration: dining time length (minutes)
is_vip: VIP status (1 = VIP, 0 = normal)
