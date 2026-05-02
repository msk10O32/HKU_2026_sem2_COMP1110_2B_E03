#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Restaurant Queue Simulation - Enhanced Metrics Calculator v2 (English Output)
Usage: python compute_metrics_v2.py [result_csv_path] [--granularity GRANULARITY_CSV] [--output OUTPUT_FILE]
"""

import pandas as pd
import argparse
import os
from datetime import datetime
import csv

def parse_arguments():
    parser = argparse.ArgumentParser(description='Calculate restaurant queue simulation metrics (Enhanced)')
    parser.add_argument('csv_file', nargs='?', default='data/result.csv',
                        help='Path to result.csv (default: data/result.csv)')
    parser.add_argument('--granularity', '-g', default='config/granularity.csv',
                        help='Path to granularity.csv for table counts (default: config/granularity.csv)')
    parser.add_argument('--output', '-o', default=None,
                        help='Output report filename (default: metrics_report_enhanced.txt in same directory)')
    parser.add_argument('--log', default='log/simulation_log.txt',
                        help='Path to simulation_log.txt (default: log/simulation_log.txt)')
    return parser.parse_args()

def load_table_config(gran_path):
    """Load table counts for each type from granularity.csv"""
    table_counts = {}
    try:
        with open(gran_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                t_type = row['type'].strip()
                table_counts[t_type] = int(row['table_capacity'])
    except FileNotFoundError:
        print(f"Warning: granularity file not found at {gran_path}. Using default counts {{'A':2,'B':1,'C':1}}")
        table_counts = {'A': 2, 'B': 1, 'C': 1}
    return table_counts

def extract_max_queue_lengths(log_path):
    """Extract maximum observed queue length per table type from log file"""
    max_queues = {}
    try:
        with open(log_path, 'r', encoding='utf-8') as f:
            for line in f:
                if 'type:' not in line or 'waiting customers in queue:' not in line:
                    continue
                # Extract table type
                type_part = line.split('type:')[1].split(',')[0].strip()
                # Extract current queue length
                queue_part = line.split('waiting customers in queue:')[1].strip()
                current_q = int(queue_part.split('/')[0])
                if type_part not in max_queues:
                    max_queues[type_part] = 0
                if current_q > max_queues[type_part]:
                    max_queues[type_part] = current_q
    except FileNotFoundError:
        print(f"Warning: Log file not found at {log_path}. Max queue lengths will be N/A.")
    return max_queues

def main():
    args = parse_arguments()
    csv_path = args.csv_file
    log_path = args.log
    gran_path = args.granularity

    if not os.path.exists(csv_path):
        print(f"Error: File not found - {csv_path}")
        return

    # Load table configuration
    table_counts = load_table_config(gran_path)
    total_tables = sum(table_counts.values())

    # Load simulation results
    df = pd.read_csv(csv_path)
    df['arrival_time'] = pd.to_datetime(df['arrival_time'])
    df['seating_time'] = pd.to_datetime(df['seating_time'])
    df['leaving_time'] = pd.to_datetime(df['leaving_time'])

    served_df = df[df['is_served'] == True].copy()
    unserved_count = len(df) - len(served_df)

    # Calculate wait time (minutes) and occupy time (minutes)
    served_df['wait_minutes'] = (served_df['seating_time'] - served_df['arrival_time']).dt.total_seconds() / 60.0
    served_df['occupy_minutes'] = (served_df['leaving_time'] - served_df['seating_time']).dt.total_seconds() / 60.0

    # Total simulation duration
    first_arrival = df['arrival_time'].min()
    last_leave = df['leaving_time'].max()
    total_sim_minutes = (last_leave - first_arrival).total_seconds() / 60.0
    total_sim_hours = total_sim_minutes / 60.0

    # Overall utilization
    total_occupied = served_df['occupy_minutes'].sum()
    total_available = total_tables * total_sim_minutes
    overall_util = total_occupied / total_available if total_available > 0 else 0.0

    # Extract max queue lengths
    max_queues = extract_max_queue_lengths(log_path)

    # Prepare output lines (English)
    lines = []
    lines.append("=" * 70)
    lines.append("Restaurant Queue Simulation - Enhanced Performance Metrics Report")
    lines.append("=" * 70)
    lines.append(f"Data source: {csv_path}")
    lines.append(f"Table configuration: {gran_path}")
    lines.append(f"Event log: {log_path}")
    lines.append("")

    lines.append("--- Overall Statistics ---")
    lines.append(f"Total customer groups: {len(df)}")
    lines.append(f"Groups successfully served: {len(served_df)}")
    lines.append(f"Groups rejected (lost): {unserved_count}")
    lines.append(f"Service rate: {len(served_df)/len(df)*100:.1f}%")
    lines.append("")

    lines.append("--- Waiting Time (Served Groups Only) ---")
    lines.append(f"Average waiting time: {served_df['wait_minutes'].mean():.2f} minutes")
    lines.append(f"Maximum waiting time: {served_df['wait_minutes'].max():.2f} minutes")
    lines.append(f"Median waiting time: {served_df['wait_minutes'].median():.2f} minutes")
    lines.append("")

    lines.append("--- Waiting Time by Group Size ---")
    for size in sorted(served_df['group_size'].unique()):
        sub = served_df[served_df['group_size'] == size]
        lines.append(f"Group of {size}: served {len(sub)} groups, "
                     f"avg wait {sub['wait_minutes'].mean():.2f} min, "
                     f"max wait {sub['wait_minutes'].max():.2f} min")
    lines.append("")

    lines.append("--- Maximum Queue Length by Table Type ---")
    for t_type in sorted(table_counts.keys()):
        max_q = max_queues.get(t_type, 'N/A')
        lines.append(f"Table type {t_type}: max queue length = {max_q} groups")
    lines.append("")

    lines.append("--- Overall Table Utilization ---")
    lines.append(f"Total simulation duration: {total_sim_minutes:.2f} minutes ({total_sim_hours:.2f} hours)")
    lines.append(f"Total tables: {total_tables} (" + ", ".join([f"{k}:{v}" for k,v in table_counts.items()]) + ")")
    lines.append(f"Total occupied time: {total_occupied:.2f} minutes")
    lines.append(f"Total available time: {total_available:.2f} minutes")
    lines.append(f"Overall table utilization: {overall_util*100:.2f}%")
    lines.append("")

    lines.append("--- Per-Table-Type Detailed Metrics ---")
    for t_type in sorted(table_counts.keys()):
        count = table_counts[t_type]
        sub = served_df[served_df['table_type'] == t_type]
        groups_served = len(sub)
        if groups_served > 0:
            avg_wait = sub['wait_minutes'].mean()
            total_occ = sub['occupy_minutes'].sum()
            avail = count * total_sim_minutes
            util = total_occ / avail if avail > 0 else 0.0
            turnover = groups_served / count / total_sim_hours if total_sim_hours > 0 else 0.0
        else:
            avg_wait = 0
            util = 0.0
            turnover = 0.0

        lines.append(f"Table type {t_type} ({count} table(s)):")
        lines.append(f"  Groups served: {groups_served}")
        lines.append(f"  Average wait: {avg_wait:.2f} minutes")
        lines.append(f"  Table utilization: {util*100:.2f}%")
        lines.append(f"  Table turnover rate: {turnover:.2f} groups/table/hour")
    lines.append("")

    lines.append("--- Summary by Table Type ---")
    for t_type in served_df['table_type'].unique():
        sub = served_df[served_df['table_type'] == t_type]
        lines.append(f"Table type {t_type}: served {len(sub)} groups, avg wait {sub['wait_minutes'].mean():.2f} min")
    lines.append("=" * 70)

    # Output to console
    for line in lines:
        print(line)

    # Write to file
    output_file = args.output
    if output_file is None:
        output_dir = os.path.dirname(csv_path) or '.'
        output_file = os.path.join(output_dir, 'metrics_report_enhanced.txt')
    else:
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f"\nReport saved to: {output_file}")

if __name__ == "__main__":
    main()