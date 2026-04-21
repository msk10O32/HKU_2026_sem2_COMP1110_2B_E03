Code Modules analysis.py Module Description

Core functionality:
This tool is used to analyze the output results of restaurant queuing simulation experiments, calculate key performance indicators (waiting time, rejection rate, table utilization, maximum queue length, etc.), and generate detailed and readable reports.

Output result
File generated: metrics_report_enhanced.txt

Sample Output:
======================================================================
Restaurant Queue Simulation - Enhanced Performance Metrics Report
======================================================================
Data source: data/result.csv
...
--- Overall Statistics ---
Total customer groups: 150
Groups successfully served: 142
Groups rejected (lost): 8
Service rate: 94.7%

--- Waiting Time (Served Groups Only) ---
Average waiting time: 12.34 minutes
Maximum waiting time: 45.67 minutes
Median waiting time: 9.87 minutes

--- Per-Table-Type Detailed Metrics ---
Table type A (2 table(s)):
  Groups served: 80
  Average wait: 10.20 minutes
  Table utilization: 78.50%
  Table turnover rate: 3.20 groups/table/hour
...
