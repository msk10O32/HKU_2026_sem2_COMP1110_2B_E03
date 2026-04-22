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

Code Modules analysis.py Module Description
Core functionality:
This tool is used to analyze the output results of restaurant queuing simulation experiments, calculate key performance indicators (waiting time, rejection rate, table utilization, maximum queue length, etc.), and generate detailed and readable reports.
Output result
File generated: metrics_report_enhanced.txt
