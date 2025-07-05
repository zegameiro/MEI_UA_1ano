#!/usr/bin/env python3
# filepath: /home/d479/Uni/MEI/1ANO/2SEMESTRE/CLE/2425-tp02-group11/mpi/word-count/mpi_benchmark.py

import os
import subprocess
import time
import matplotlib.pyplot as plt
import argparse
import numpy as np
import csv
from datetime import datetime

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def prepare_input_files(base_input_file, max_multiplier=16):
    """Create a series of input files with doubling size"""
    results = {}
    current_multiplier = 1
    current_file = base_input_file
    base_name = os.path.basename(base_input_file)
    
    # Save original file as 1x
    input_dir = "input_files"
    create_directory(input_dir)
    first_file = f"{input_dir}/{base_name}.1x"
    with open(base_input_file, 'r') as src, open(first_file, 'w') as dst:
        dst.write(src.read())
    
    results[1] = first_file
    current_file = first_file
    
    while current_multiplier < max_multiplier:
        next_multiplier = current_multiplier * 2
        new_file = f"{input_dir}/{base_name}.{next_multiplier}x"
        
        with open(current_file, 'r') as src, open(new_file, 'w') as dst:
            for _ in range(2):  # Double the content
                src.seek(0)
                dst.write(src.read())
        
        results[next_multiplier] = new_file
        current_file = new_file
        current_multiplier = next_multiplier
        print(f"Created {next_multiplier}x input file: {new_file}")
    
    return results

def run_benchmark(executable, input_file, processes, csv_writer=None):
    """Run benchmark with specified executable and input file using MPI"""
    start_time = time.time()
    cmd = ["mpiexec", "-n", str(processes), executable, input_file]
    
    print(f"Running: {' '.join(cmd)}")
    try:
        # Run the command and capture output but also show it
        process = subprocess.run(
            cmd, 
            check=True,
            text=True,
            capture_output=True  # Capture stdout and stderr
        )
        
        # Display the output
        if process.stdout:
            print("--- Program Output ---")
            print(process.stdout)
            print("--------------------")
            
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Processes: {processes}, Time: {elapsed_time:.4f} seconds")
        
        if csv_writer:
            csv_writer.writerow([processes, elapsed_time])
            
        return elapsed_time
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        if e.stdout:
            print(f"STDOUT: {e.stdout}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        return None

def run_benchmarks(opt_executable, unopt_executable, input_files, process_counts, output_dir):
    """Run benchmarks for both optimized and unoptimized versions"""
    create_directory(f"{output_dir}/csv")
    
    results = {}
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create CSV files for results
    opt_csv_path = f"{output_dir}/csv/optimized_results_{timestamp}.csv"
    unopt_csv_path = f"{output_dir}/csv/unoptimized_results_{timestamp}.csv"
    comparative_csv_path = f"{output_dir}/csv/comparative_results_{timestamp}.csv"
    
    with open(opt_csv_path, 'w', newline='') as opt_file, \
         open(unopt_csv_path, 'w', newline='') as unopt_file, \
         open(comparative_csv_path, 'w', newline='') as comp_file:
        
        opt_writer = csv.writer(opt_file)
        unopt_writer = csv.writer(unopt_file)
        comp_writer = csv.writer(comp_file)
        
        # Write headers
        opt_writer.writerow(["multiplier", "processes", "time"])
        unopt_writer.writerow(["multiplier", "processes", "time"])
        comp_writer.writerow(["multiplier", "processes", "opt_time", "unopt_time", "speedup"])
        
        for multiplier, input_file in input_files.items():
            results[multiplier] = {"opt": {}, "unopt": {}}
            
            for processes in process_counts:
                print(f"\n=== Running benchmark with {processes} processes on {multiplier}x input file ===")
                
                # Run optimized version
                print(f"Running optimized (-O3) version...")
                opt_time = run_benchmark(opt_executable, input_file, processes)
                
                # Run unoptimized version
                print(f"Running unoptimized (-O0) version...")
                unopt_time = run_benchmark(unopt_executable, input_file, processes)
                
                if opt_time and unopt_time:
                    speedup = unopt_time / opt_time
                    print(f"Speedup (unopt/opt): {speedup:.2f}x")
                    
                    # Store results
                    results[multiplier]["opt"][processes] = opt_time
                    results[multiplier]["unopt"][processes] = unopt_time
                    
                    # Write to CSV files
                    opt_writer.writerow([multiplier, processes, opt_time])
                    unopt_writer.writerow([multiplier, processes, unopt_time])
                    comp_writer.writerow([multiplier, processes, opt_time, unopt_time, speedup])
    
    print(f"\nResults saved to:\n{opt_csv_path}\n{unopt_csv_path}\n{comparative_csv_path}")
    return results, comparative_csv_path

def read_comparative_csv(csv_path):
    """Read comparative CSV file into a structured format"""
    data = []
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            multiplier, processes, opt_time, unopt_time, speedup = row
            data.append({
                'multiplier': int(multiplier),
                'processes': int(processes),
                'opt_time': float(opt_time),
                'unopt_time': float(unopt_time),
                'speedup': float(speedup)
            })
    return data

def plot_all_graphs(csv_path, output_dir):
    """Generate plots focusing on execution time vs processes and speedup"""
    # Create separate directories for optimized and unoptimized graphs
    create_directory(f"{output_dir}/images")
    create_directory(f"{output_dir}/images/optimized")
    create_directory(f"{output_dir}/images/unoptimized")
    create_directory(f"{output_dir}/images/comparison")
    
    data = read_comparative_csv(csv_path)
    
    # Group data
    by_multiplier = {}
    
    for entry in data:
        mult = entry['multiplier']
        
        if mult not in by_multiplier:
            by_multiplier[mult] = []
            
        by_multiplier[mult].append(entry)
    
    # Sort keys
    multipliers = sorted(by_multiplier.keys())
    
    # 1. Optimized: Execution time vs processes for each multiplier (separate graphs)
    for mult in multipliers:
        plt.figure(figsize=(10, 6))
        entries = by_multiplier[mult]
        entries.sort(key=lambda x: x['processes'])
        
        processes = [e['processes'] for e in entries]
        opt_times = [e['opt_time'] for e in entries]
        
        plt.plot(processes, opt_times, 'b-o', linewidth=2, markersize=8)
        
        # Add data labels
        for i, v in enumerate(opt_times):
            plt.text(processes[i], v + (max(opt_times) * 0.03), f'{v:.2f}s', 
                    ha='center', va='bottom', fontweight='bold')
        
        plt.title(f'Optimized: Execution Time vs Processes (Input Size x{mult})', fontsize=14)
        plt.xlabel('Number of Processes', fontsize=12)
        plt.ylabel('Execution Time (seconds)', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(f"{output_dir}/images/optimized/time_vs_proc_x{mult}.png")
        plt.close()
    
    # 2. Unoptimized: Execution time vs processes for each multiplier (separate graphs)
    for mult in multipliers:
        plt.figure(figsize=(10, 6))
        entries = by_multiplier[mult]
        entries.sort(key=lambda x: x['processes'])
        
        processes = [e['processes'] for e in entries]
        unopt_times = [e['unopt_time'] for e in entries]
        
        plt.plot(processes, unopt_times, 'r-o', linewidth=2, markersize=8)
        
        # Add data labels
        for i, v in enumerate(unopt_times):
            plt.text(processes[i], v + (max(unopt_times) * 0.03), f'{v:.2f}s', 
                    ha='center', va='bottom', fontweight='bold')
        
        plt.title(f'Unoptimized: Execution Time vs Processes (Input Size x{mult})', fontsize=14)
        plt.xlabel('Number of Processes', fontsize=12)
        plt.ylabel('Execution Time (seconds)', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(f"{output_dir}/images/unoptimized/time_vs_proc_x{mult}.png")
        plt.close()
    
    # 3. Optimized: Combined execution time vs processes for all multipliers
    plt.figure(figsize=(12, 7))
    for mult in multipliers:
        entries = by_multiplier[mult]
        entries.sort(key=lambda x: x['processes'])
        
        processes = [e['processes'] for e in entries]
        opt_times = [e['opt_time'] for e in entries]
        
        plt.plot(processes, opt_times, marker='o', linewidth=2, label=f'Input Size x{mult}')
    
    plt.title('Optimized: Execution Time vs Number of Processes (All Input Sizes)', fontsize=14)
    plt.xlabel('Number of Processes', fontsize=12)
    plt.ylabel('Execution Time (seconds)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend(title='Input Size')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/images/optimized/time_vs_proc_combined.png")
    plt.close()
    
    # 4. Unoptimized: Combined execution time vs processes for all multipliers
    plt.figure(figsize=(12, 7))
    for mult in multipliers:
        entries = by_multiplier[mult]
        entries.sort(key=lambda x: x['processes'])
        
        processes = [e['processes'] for e in entries]
        unopt_times = [e['unopt_time'] for e in entries]
        
        plt.plot(processes, unopt_times, marker='o', linewidth=2, label=f'Input Size x{mult}')
    
    plt.title('Unoptimized: Execution Time vs Number of Processes (All Input Sizes)', fontsize=14)
    plt.xlabel('Number of Processes', fontsize=12)
    plt.ylabel('Execution Time (seconds)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend(title='Input Size')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/images/unoptimized/time_vs_proc_combined.png")
    plt.close()
    
    # 5. Speedup vs number of processes for all sizes - Optimized vs Unoptimized (comparison)
    plt.figure(figsize=(12, 7))
    
    # Get baseline times (1 process) for each multiplier for both versions
    baselines_opt = {}
    baselines_unopt = {}
    
    for mult in multipliers:
        entries = by_multiplier[mult]
        entries.sort(key=lambda x: x['processes'])
        
        # Find the entry with smallest process count for baseline
        base_entry = entries[0]
        baselines_opt[mult] = base_entry['opt_time']
        baselines_unopt[mult] = base_entry['unopt_time']
    
    # Calculate and plot speedups
    for mult in multipliers:
        entries = by_multiplier[mult]
        entries.sort(key=lambda x: x['processes'])
        
        processes = [e['processes'] for e in entries]
        
        # Calculate speedup relative to 1 process (or minimum process count)
        speedups_opt = [baselines_opt[mult] / e['opt_time'] for e in entries]
        speedups_unopt = [baselines_unopt[mult] / e['unopt_time'] for e in entries]
        
        plt.plot(processes, speedups_opt, marker='o', linestyle='-', linewidth=2, 
                 label=f'Optimized x{mult}')
        plt.plot(processes, speedups_unopt, marker='x', linestyle='--', linewidth=2, 
                 label=f'Unoptimized x{mult}')
    
    # Add ideal speedup line (if baseline is 1 process)
    if any(entries[0]['processes'] == 1 for entries in by_multiplier.values()):
        max_procs = max(e['processes'] for e in data)
        plt.plot([1, max_procs], [1, max_procs], 'k--', alpha=0.3, label='Ideal Speedup')
    
    plt.title('Parallel Speedup vs Number of Processes', fontsize=14)
    plt.xlabel('Number of Processes', fontsize=12)
    plt.ylabel('Speedup (T₁/Tₚ)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend(title='Version & Size', fontsize=10)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/images/comparison/parallel_speedup_comparison.png")
    plt.close()
    
    # Also save individual parallel speedup graphs for optimized and unoptimized
    
    # 5a. Optimized only parallel speedup
    plt.figure(figsize=(12, 7))
    for mult in multipliers:
        entries = by_multiplier[mult]
        entries.sort(key=lambda x: x['processes'])
        
        processes = [e['processes'] for e in entries]
        speedups_opt = [baselines_opt[mult] / e['opt_time'] for e in entries]
        
        plt.plot(processes, speedups_opt, marker='o', linestyle='-', linewidth=2, 
                 label=f'Input Size x{mult}')
    
    # Add ideal speedup line
    if any(entries[0]['processes'] == 1 for entries in by_multiplier.values()):
        max_procs = max(e['processes'] for e in data)
        plt.plot([1, max_procs], [1, max_procs], 'k--', alpha=0.3, label='Ideal Speedup')
    
    plt.title('Optimized: Parallel Speedup vs Number of Processes', fontsize=14)
    plt.xlabel('Number of Processes', fontsize=12)
    plt.ylabel('Speedup (T₁/Tₚ)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend(title='Input Size', fontsize=10)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/images/optimized/parallel_speedup.png")
    plt.close()
    
    # 5b. Unoptimized only parallel speedup
    plt.figure(figsize=(12, 7))
    for mult in multipliers:
        entries = by_multiplier[mult]
        entries.sort(key=lambda x: x['processes'])
        
        processes = [e['processes'] for e in entries]
        speedups_unopt = [baselines_unopt[mult] / e['unopt_time'] for e in entries]
        
        plt.plot(processes, speedups_unopt, marker='x', linestyle='-', linewidth=2, 
                 label=f'Input Size x{mult}')
    
    # Add ideal speedup line
    if any(entries[0]['processes'] == 1 for entries in by_multiplier.values()):
        max_procs = max(e['processes'] for e in data)
        plt.plot([1, max_procs], [1, max_procs], 'k--', alpha=0.3, label='Ideal Speedup')
    
    plt.title('Unoptimized: Parallel Speedup vs Number of Processes', fontsize=14)
    plt.xlabel('Number of Processes', fontsize=12)
    plt.ylabel('Speedup (T₁/Tₚ)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend(title='Input Size', fontsize=10)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/images/unoptimized/parallel_speedup.png")
    plt.close()
    
    # 6. Optimization Speedup Comparison (optimized vs unoptimized)
    plt.figure(figsize=(12, 7))
    for mult in multipliers:
        entries = by_multiplier[mult]
        entries.sort(key=lambda x: x['processes'])
        
        processes = [e['processes'] for e in entries]
        speedups = [e['speedup'] for e in entries]
        
        plt.plot(processes, speedups, marker='o', linewidth=2, label=f'Input Size x{mult}')
    
    plt.title('Optimization Speedup vs Number of Processes', fontsize=14)
    plt.xlabel('Number of Processes', fontsize=12)
    plt.ylabel('Speedup (Unoptimized/Optimized)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend(title='Input Size')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/images/comparison/optimization_speedup_vs_proc.png")
    plt.close()

    print(f"Performance comparison plots saved to {output_dir}/images/ with separate directories for optimized and unoptimized results")

def main():
    parser = argparse.ArgumentParser(description="Run performance benchmarks on MPI word-count program")
    parser.add_argument("--opt-executable", type=str, default="./test_build/optimized/cle-mpi", 
                        help="Path to the optimized executable")
    parser.add_argument("--unopt-executable", type=str, default="./test_build/unoptimized/cle-mpi", 
                        help="Path to the unoptimized executable")
    parser.add_argument("--input-file", type=str, default="./books_test.txt", 
                        help="Path to the base input file")
    parser.add_argument("--output-dir", type=str, default="./results", 
                        help="Output directory for results")
    parser.add_argument("--processes", type=str, default="1,2,4,6,8", 
                        help="Comma-separated list of process counts")
    parser.add_argument("--max-multiplier", type=int, default=64, 
                        help="Maximum file size multiplier")
    
    args = parser.parse_args()  
    
    # Parse process counts
    process_counts = [int(p) for p in args.processes.split(',')]
    
    # Create output directory
    create_directory(args.output_dir)
    
    # Prepare input files with increasing sizes
    print("Preparing input files...")
    input_files = prepare_input_files(args.input_file, args.max_multiplier)
    
    # Run benchmarks
    print(f"\nRunning benchmarks with process counts: {process_counts}")
    results, csv_path = run_benchmarks(
        args.opt_executable,
        args.unopt_executable,
        input_files,
        process_counts,
        args.output_dir
    )
    
    # Create plots
    print("\nGenerating plots...")
    plot_all_graphs(csv_path, args.output_dir)
    
    print("\nBenchmark completed successfully!")

if __name__ == "__main__":
    main()
